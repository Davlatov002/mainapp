from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


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
    path('profile-history/<str:pk>/', views.get_tr_us, name='profile-history'),
    path('get-maxbalanspr/', views.get_max_usdt_profile, name='get-maxbalanspr'),
    path('get-identified-id/<str:pk>/', views.get_identified_id, name='get-identified-id'),
    path('creat-identified/<str:pk>/', views.upload_image, name='creat-identified'),
    path("get-moneyout-id/<str:pk>/", views.get_moneyout_id, name='get-moneyout-id'),
    path("moneyout/<str:pk>/", views.moneyout, name='moneyout'),
    path("recovery-password/<str:email>/", views.send_otp, name='recovery-password'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
