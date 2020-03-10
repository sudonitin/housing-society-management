
from django.contrib import admin
from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.landing, name = 'landing'),
    path('home/', user_views.home, name = 'home'),
    path('createbill/', user_views.createBill, name = 'createBill'),
    path('sendbill/', user_views.sendBill, name = 'sendBill'),
    path('forum/', user_views.forumDisplay, name = 'forum'),
    path('upvote/', user_views.upVote, name = 'upvote'),
    path('newtopic/', user_views.newTopic, name = 'newtopic'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name = 'users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'users/password_reset.html'), name = 'password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name = 'password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name = 'password_reset_complete'),
]
