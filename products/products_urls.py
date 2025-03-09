from django.urls import path
from products import views

urlpatterns = [
    path('', views.ProductViewList.as_view(), name='product-list'),
    path('<int:id>/', views.ViewSpecificProduct.as_view(), name='product-list'),

]
