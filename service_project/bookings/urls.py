from django.urls import path
from . import views
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('signup')),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    
    path('ajax/load-models/', views.load_models, name='ajax_load_models'),
    
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('update-booking/<int:booking_id>/', views.update_booking, name='update_booking'),
    
    path('edit-modal/<int:booking_id>/', views.edit_booking_modal, name='edit_booking_modal'),
    
]
