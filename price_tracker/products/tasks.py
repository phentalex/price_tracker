from decimal import Decimal

from camoufox.sync_api import Camoufox
from celery import shared_task
from django.core.cache import cache

from .models import Product, PriceHistory
from .utils import send_tg_alert


def _parse_with_browser(url, price_selector, name_selector):
    try:
        with Camoufox(headless='virtual', os='windows') as browser:
            page = browser.new_page()
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(5000)
            page.wait_for_selector(price_selector, timeout=20000)

            name = None
            name_el = page.locator(name_selector).first
            if name_el.count():
                name = name_el.inner_text().strip()

            price_el = page.locator(price_selector).first
            price_text = price_el.inner_text()
            price_clean = ''.join(c for c in price_text if c.isdigit() or c in '.,')
            price_clean = price_clean.replace(',', '.')
            return name, Decimal(price_clean)
    except Exception as e:
        print(f'[PARSER ERROR] {type(e).__name__}: {e}', flush=True)
        return None, None


def _parse_wildberries(url):
    return _parse_with_browser(
        url,
        price_selector='.mo-typography_color_danger, .mo-typography_color_accent',
        name_selector='[class*="productTitle"]',
    )


def _parse_ozon(url):
    return _parse_with_browser(
        url,
        price_selector='.tsHeadline600Large',
        name_selector='.pdp_j4b',
    )


@shared_task
def check_price(product_id):
    product = Product.objects.get(id=product_id)
    url = product.url

    if 'wildberries.ru' in url:
        name, price = _parse_wildberries(url)
    elif 'ozon.ru' in url:
        name, price = _parse_ozon(url)
    else:
        return

    if price is None:
        return

    update_fields = ['current_price']
    product.current_price = price

    if not product.name and name:
        product.name = name
        update_fields.append('name')

    product.save(update_fields=update_fields)

    PriceHistory.objects.create(product=product, price=price)
    cache.set(f'price_{product_id}', price, timeout=3600)

    if price <= product.target_price:
        alert_key = f'alert_sent_{product_id}'
        if not cache.get(alert_key):
            profile = getattr(product.user, 'profile', None)
            tg_chat_id = profile.tg_chat_id if profile else None
            if tg_chat_id:
                send_tg_alert(
                    tg_chat_id,
                    f'Цена на «{product.name} | {product.url}» снизилась до {price} ₽.'
                )
                cache.set(alert_key, True, timeout=86400)


@shared_task
def check_price_all():
    product_ids = Product.objects.values_list('id', flat=True)
    for product_id in product_ids:
        check_price.delay(product_id)
