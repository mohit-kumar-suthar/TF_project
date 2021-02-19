from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name='login'),
    path('register',views.register_view,name='register'),
    path('forgot-password',views.forgot_view,name='forgot_password'),
    path('activate/<slug:token>',views.activate_view,name='activate'),
    path('reset/<slug:token>',views.reset_password_view,name='reset'),
]