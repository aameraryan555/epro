from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .forms import SignUpForm
from .tokens import account_activation_token
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


def home(request):
    return render(request, 'portal/home.html', {'user': request.user})


@login_required
def profile(request):
    return render(request, 'portal/profile.html', {'candidate': request.user.candidate})


@login_required
def update_profile(request):
    candidate = request.user.candidate
    if request.method == "POST":
        form = UpdateProfileForm(data=request.POST, files=request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Suucessfully Updated')
            return redirect('profile')
        else:
            form = UpdateProfileForm(candidate=candidate)
            return render(request, 'portal/update_profile.html', {'form': form, 'form_invalid': "form is invalid !"})
    else:
        form = UpdateProfileForm(candidate=candidate)
        return render(request, 'portal/update_profile.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'portal/dashboard.html', {'candidate': request.user.candidate})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            uid = urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8')
            token = account_activation_token.make_token(user)
            domain = current_site.domain
            activation_link = '{0}/activate/{1}/{2}'.format(domain, uid, token)
            email_message = "\t Activate your account for {0} \n" \
                            "{1}".format(domain, activation_link)
            send_mail(from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email], subject=subject, message=email_message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'portal/register.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'portal/email_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.candidate.email_confirmed = True
        user.candidate.email = user.email
        user.save()
        login(request, user)
        messages.success(request, 'Succfully confirmed your email address')
        return redirect('profile')
    else:
        return render(request, 'portal/email_activation_invalid.html')
