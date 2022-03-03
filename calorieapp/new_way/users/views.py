from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect, Http404, reverse
from users.forms import ContactForm, LoginForm, UserForm, RegisterForm, UserImageForm, ProfileImageForm
from django.contrib.auth import authenticate, login, logout
from users.email import email, send_register_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def userlist(request):
    return render(request, 'users/userlist.html')



# Create your views here.
def register(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            send_register_mail(user)

            return redirect('/')
      
    return render(request, 'users/register.html', {
        'form': form,
    })


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'GET':
        form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            raise Http404('Username or password not provided!')
        user = authenticate(request, email=email, password=password)

        if user is None:
            return render(request, 'users/login.html', {'msg':'Email or password is incorrect', 'form':form})
        else:
            login(request, user)

            return redirect('/')

    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/')


def upload_view(request):
    if request.method == 'GET':
        form = UserImageForm()
    else:
        form = UserImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return render(request, 'users/file_uploaded.html')

    return render(request, 'users/upload.html', {
        'form': form
    })


@login_required(login_url="/users/login")
def profile_view(request):

    if request.method == 'GET':
        profile_form = UserForm(initial={
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'username':request.user.username,
            'email':request.user.email
        })
        form = ProfileImageForm()     
    else:
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:profile'))

    return render(request, 'users/profile.html', {
        'form': form,
        'profile_form':profile_form
    })

def profile_update(request):
    profile_form = UserForm()
    if request.method == 'GET':
        form = ProfileImageForm()
    else:
        profile_update_form = UserForm(request.POST, instance=request.user)
        if profile_update_form.is_valid():
            profile_update_form.save()          
            return redirect(reverse('users:profile'))

    return render(request, 'users/profile.html', {
        'form': form,
        'profile_form':profile_form
    })


#Contact us

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'from@calorieapp.com', ['martinaslaura123@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("calories:home")

    form = ContactForm()
    return render(request, "users/contact.html", {'form': form})