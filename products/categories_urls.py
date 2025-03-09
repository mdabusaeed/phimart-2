from django.urls import path
from products import views

urlpatterns = [
    path('', views.ViewCategory.as_view(), name='category-list'),
    path('<int:id>/', views.ViewSpecificCategory.as_view(), name='view_specifiq_category')
]
