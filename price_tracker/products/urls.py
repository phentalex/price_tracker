from django.urls import path

from .views import ProductCheckView, ProductDeleteView, ProductHistoryDetailView, ProductListView

urlpatterns = [
    path('<int:pk>/history/', ProductHistoryDetailView.as_view(), name='product_history'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<int:pk>/check/', ProductCheckView.as_view(), name='product_check'),
    path('', ProductListView.as_view(), name='product_list'),
]
