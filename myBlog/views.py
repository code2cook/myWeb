from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserProfileForm, LoginForm


# Create your views here.



def home(request):
    return render(request, 'home.html')


def resume(request):
    return render(request, 'resume.html')

def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.user.is_active = True
            profile.save()
           
            return redirect('login')  # Redirect to a success page or another view
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('profile')  # Redirect to the home page or any other desired page
            else:
                form.add_error(None, "Invalid credentials. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')
