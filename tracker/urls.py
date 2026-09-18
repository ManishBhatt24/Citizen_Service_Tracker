from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('complaints/', views.complaints, name='complaints'),
    path('complaints/<int:complaint_id>/status/', views.update_status, name='update_status'),
    path('api/category-data/', views.category_data, name='category_data'),
]
