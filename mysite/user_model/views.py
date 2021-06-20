from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def register(request):

    registered = False

    if request.method == 'POST':

        userform = UserForm(data=request.POST)
        userprofileinfo = UserProfileInfoForm(data=request.POST)

        if userprofileinfo.is_valid() and userform.is_valid():
            user = userform.save()
            #it go setting and then hashing password
            user.set_password(user.password)
            #
            user.save()

            profile = userprofileinfo.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic'] 
            profile.save()

            registered = True
        else:
            print(userform.errors, userprofileinfo.errors)
    else:
        userform = UserForm()
        userprofileinfo = UserProfileInfoForm()
    return render(request, 'user_model/register.html', {'user_form': userform, 'profile_form': userprofileinfo, 'registere': registered})

def index(request):
    return render(request, 'user_model/index.html')


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print('Someone tried to login and failed!')
            return HttpResponse("Invalid Login details !")

    else:
        return render(request, 'user_model/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def check_user_login(request):
    return HttpResponse("You are logged in")