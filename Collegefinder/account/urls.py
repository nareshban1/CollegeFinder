from django.urls import path
from django.conf.urls import url
from . import views as account_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', account_views.signup, name='register'),
    path('login/', account_views.login, name='login'),
    path('logout/', account_views.logout, name='logout'),
    path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

]