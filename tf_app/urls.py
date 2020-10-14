from django.urls import path
from . import views

urlpatterns = [
    path('',views.index_view,name='home'),
    path('project',views.project_view,name='project'),
    path('source_code',views.source_code_view,name='source_code'),
    path('blog',views.blog_view,name='blog'),
    path('member',views.member_view,name='member'),
    path('about',views.about_view,name='about'),
    path('login',views.login_view,name='login'),
    path('register',views.register_view,name='register'),
    path('forgot-password',views.forgot_view,name='forgot_password'),
    path('activate/<slug:token>',views.activate_view,name='activate'),
    path('reset/<slug:token>',views.reset_password_view,name='reset'),
]