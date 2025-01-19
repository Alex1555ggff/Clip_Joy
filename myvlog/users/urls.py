from django.urls import path, reverse_lazy
from . import views

from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordChangeDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView, 
                                       LogoutView,)


app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),

    path('password-reset/',
         PasswordResetView.as_view(
               template_name="form_post.html",
               email_template_name="users/password_reset_email.html",
               success_url=reverse_lazy("users:password_reset_done"),
               extra_context={'title_btn': 'Отправить'},
               title="Сброс пароля"),
               name='password_reset'),

    path('password-reset/done/',
         PasswordResetDoneView.as_view(
               template_name="users/password_reset_done.html",
               title="Письмо отправлено"),
               name='password_reset_done'),

     path("password-reset/<uidb64>/<token>",
          PasswordResetConfirmView.as_view(
               template_name="form_post.html",
               success_url=reverse_lazy("users:password_reset_complete"),
               extra_context={'title_btn': 'Сменить пароль'},
               title="Придумайте новый пароль"),
               name="password_reset_confirm"),

     path("password-reset/complete/",
          PasswordResetCompleteView.as_view(
               template_name="users/password_reset_complete.html",
               title="Придумайте новый пароль"),
               name="password_reset_complete"),

     


]

