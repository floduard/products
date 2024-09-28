from django.shortcuts import HttpResponse, render,redirect
from django.views import View
from.models import Product, Customer
from django.db.models import Count
from .forms import CustomerRegistrationForm, CustomerProfileForm, MessageForm,PasswordChangeForm
from django.contrib import messages
from django.views.generic.edit import FormView
from django.core.mail import send_mail
import logging
from django.contrib.auth.views import PasswordResetView,PasswordChangeView,PasswordChangeDoneView
from django.core.mail import BadHeaderError
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from urllib.parse import urlparse, urlunparse
from django.urls import reverse
from django.contrib.auth.views import LogoutView
from django.conf import settings

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_not_required, login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string




logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'app/home.html')
    

def about(request):
    return render(request, 'app/about.html')


def contact(request):
    return render(request, 'app/contact.html')\



class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html',locals())

class CategoryTitle(View):
    def get(self, request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html',locals())

class ProductDetails(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/product_details.html',locals())


class CustomerRegistrationView(View):

    def get(self, request):
        form= CustomerRegistrationForm()
        return render(request, 'app/customer_registration.html',locals())

    def post(self, request):
        form= CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email') 
            form.save()

            html_message = render_to_string('app/email_template.html', {'user': user})
            send_mail(
                subject='Registration Successful',
                message='Your registration was successful!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,  # Include the HTML content
                fail_silently=False,
            )
            messages.success(request, 'Congratulations! Registration successful.')
            return redirect(reverse('login'))    
        else:
            messages.warning(request, 'Invalid form submission.')
        return render(request, 'app/customer_registration.html',locals())


class ProfileView(View): 
    def get(self, request):
        form= CustomerProfileForm()
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            mobile=form.cleaned_data['mobile']
            locality=form.cleaned_data['locality']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, mobile=mobile, locality=locality,state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'conglulations! Profile saved successfully.')
            return redirect('address')
        else:
            messages.warning(request, 'Invalid Input data')
        return render(request, 'app/profile.html', locals())


def address(request):
    # Filter the Customer objects for the logged-in user
    add = Customer.objects.filter(user=request.user)
    
    # Pass the 'add' data to the 'address' template
    return render(request, 'app/address.html', {'add': add})



class updateAddress(View):
    def get(self, request,pk):
        add = Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())

    def post(self, request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.mobile=form.cleaned_data['mobile']
            add.locality=form.cleaned_data['locality']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'conglulations! Profile saved successfully.')
        else:
            messages.warning(request, 'Invalid Input data')
        return redirect('address')

        

class MessageView(FormView):
    template_name = 'app/message.html'
    form_class = MessageForm
    success_url = '/'  

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        try:
            send_mail(
                f'New message from {name}',
                message,
                email,  # From email
                ['flodouard2000@gmail.com'],  # Replace with your email
                fail_silently=False,
            )
        except BadHeaderError:
            messages.error(self.request, 'Invalid header found.')
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            messages.error(self.request, 'There was an error sending your message.')
            return self.form_invalid(form)

        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)





class CustomPasswordResetView(PasswordResetView):
    template_name = 'app/registration/password_reset_form.html'
    email_template_name = 'app/registration/password_reset_email.html'
    subject_template_name = 'app/registration/password_reset_subject.txt'
    success_url = '/password_reset/done/'

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'app/registration/password_change.html'  # Create this template
    success_url = reverse_lazy('password_change_done')  # Create this URL


class ChangePasswordDoneView(PasswordChangeDoneView):
    template_name = 'app/registration/password_change_done.html' 


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context


@method_decorator(login_not_required, name="dispatch")
class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "registration/password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "registration/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


@method_decorator(login_not_required, name="dispatch")
class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_reset_done.html"
    title = _("Password reset sent")


@method_decorator(login_not_required, name="dispatch")
class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = "set-password"
    success_url = reverse_lazy("password_reset_complete")
    template_name = "registration/password_reset_confirm.html"
    title = _("Enter new password")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    "form": None,
                    "title": _("Password reset unsuccessful"),
                    "validlink": False,
                }
            )
        return context


@method_decorator(login_not_required, name="dispatch")
class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_reset_complete.html"
    title = _("Password reset complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "registration/password_change_form.html"
    title = _("Password change")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_change_done.html"
    title = _("Password change successful")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
