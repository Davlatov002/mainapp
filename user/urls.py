from django.urls import path
from . import views


urlpatterns = [

    path('signup/', views.signup, name='signup'),
    path('get-profile/', views.get_profile, name='get-profile'),
    path('login/', views.login, name='login'),
    path('get-profile-id/<str:pk>/', views.get_profile_id, name='get-profile-id'),
    path('get-profile-username/<str:username>/', views.get_profile_username, name='get-profile-username'),
    path('update-profile/<str:pk>/', views.update_profile, name='update-profile'),
    path('update-email-password/<str:pk>/', views.update_email_password, name='update-email-password'),
    path('delete-profile/<str:pk>/', views.delete_profile, name='delete-profile'),
    path('activate-referral-link/<str:pk>/', views.activate_referral_link, name='activate-referral-link'),
    path('ad-reward/<str:pk>/', views.ad_reward, name='ad-reward'),
    path('confirmation-otp/', views.confirmation_otp, name='confirmation-otp'),
    path('update-password/<str:email>/', views.update_password, name='update-password'),
    path('archive-account/<str:pk>/', views.archive_account, name='archive-account'),
    path('send-otp/', views.send_otp, name='send-otp'),
    path('verify-email/<str:pk>/', views.verify_email, name='verify-email'),
    path('balance-history/<str:pk>/', views.balance_history, name='balance-history'),
    path('get-TR/', views.get_tr, name='get-TR'),

]