from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, PasswordChangeForm, PasswordResetForm, MessageForm
from .views import *


urlpatterns = [

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("category-title/<val>",views.CategoryTitle.as_view(),name="category-title"),
    path("product-detail/<int:pk>",views.ProductDetails.as_view(),name="product-detail"), 
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('address/',views.address, name='address'),
    path('message/', MessageView.as_view(), name='message'),
    path('updateAddress/<int:pk>',views.updateAddress.as_view(), name='updateAddress'),
    
    # password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('change-password/', ChangePasswordView.as_view(), name='password_change'),
    path('change-password/done/', ChangePasswordDoneView.as_view(), name='password_change_done'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Other URL patterns...

    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
        name='password_reset_complete'),

    # Other password reset views, if not already added:
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), 
        name='password_reset'),
        
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
        name='password_reset_confirm'),

  #login authentication
    path("registration/",views.CustomerRegistrationView.as_view(),name="customerregistration"),
     path('logout/', CustomLogoutView.as_view(), name='logout'),   
    path("accounts/login/",auth_views.LoginView.as_view(template_name="app/login.html", authentication_form = LoginForm), name="login"),
    # path("password-reset/",auth_views.PasswordResetView.as_view(template_name="app/password_reset.html", email_template_name="app/password_reset.html", 
    # form_class=PasswordChangeForm),name="password-reset"),
    path("passwordchange/",auth_views.PasswordChangeView.as_view(template_name="app/passwordchange.html", form_class=PasswordChangeForm),name="changepassword"),
    path("passwordchangedone/",auth_views.PasswordChangeDoneView.as_view(template_name="app/passwordchangedone.html"),name="passwordchangedone"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

