from django.contrib import admin
from django.urls import include, path

from accounts.views import CustomLoginView, register, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('products.urls')),
]
