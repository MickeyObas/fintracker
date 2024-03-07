from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from .tokens import account_activation_token
from .models import User



def register(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Email Address Confirmation"
            message = render_to_string("accounts/account_activation.html", {
                'user': user,
                "domain": current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data['email']
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse("An activiation link has been sent to your email address")
        else:
            print(form.errors)

    else:
        form = CustomUserCreationForm()


    context = {
        "form": form
    }

    return render(request, "accounts/register.html", context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials.")
            print("Login Failure")

    return render(request, "accounts/login.html")


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        print(e)
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse("<h1>Activation link is invalid.</h1>")