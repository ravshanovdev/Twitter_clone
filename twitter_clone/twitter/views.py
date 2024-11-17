from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, 'meep has been posted.!')
                return redirect('home')

        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'meeps': meeps, 'form': form})
    else:
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'meeps': meeps})


def profile_list(request):
    if request.user.is_authenticated:
        profiless = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profile': profiless})
    else:
        messages.success(request, 'You must login or signup')
        return redirect('home')


def profile(request, pk):

    if request.user.is_authenticated:
        profiles = Profile.objects.get(user_id=pk)
        meep = Meep.objects.filter(user_id=pk).order_by('-created_at')

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profiles)

            elif action == "follow":
                current_user_profile.follows.add(profiles)
            current_user_profile.save()

        return render(request, 'profile.html', {'profile': profiles, 'meeps': meep})
    else:
        messages.success(request, 'You must login or signup')
        return redirect('login')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in! Get Meeping.! ')
            return redirect('home')
        else:
            messages.success(request, 'there was an error. please try again ! ')
            return redirect('login')

    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'you have been log out ')
    return redirect('login')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'you have been successfully signup bro )')
            return redirect('home')

    return render(request, 'register.html', {'form': form})


def update_user(request):

    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, 'your profile has been updated')
            return redirect('home')

        return render(request, 'update_user.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, 'you must logged view this page bro ')
        return redirect('login')


def meep_like(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'you must logged view this page bro ')
        return redirect('login')


def meep_show(request, pk):
    meep = get_object_or_404(Meep, id=pk)
    if meep:
        return render(request, 'show_meep.html', {'meep': meep})
    else:
        messages.success(request, 'this meep does not exist... ')
        return redirect('home')


def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()

        messages.success(request, f"you successfully unfollow {profile.user.username}")
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.success(request, 'you must logged view this page bro...! ')
        return redirect('home')


def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()

        messages.success(request, f"you successfully follow {profile.user.username}")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'you must logged view this page bro...! ')
        return redirect('home')


def followers(request, pk):

    if request.user.is_authenticated:
        if request.user.id == pk:
            profiless = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {'profile': profiless})
        else:
            profiless = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {'profile': profiless})

    else:
        messages.success(request, 'You must login or signup')
        return redirect('home')


def follows(request, pk):

    if request.user.is_authenticated:
        if request.user.id == pk:
            profiless = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {'profile': profiless})
        else:
            profiless = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {'profile': profiless})

    else:
        messages.success(request, 'You must login or signup')
        return redirect('home')


def delete_meep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if request.user.id == meep.user.id:
            meep.delete()
            messages.success(request, "this meep has been deleted !")
            return redirect(request.META.get('HTTP_REFERER'))
        elif request.user.id != meep.user.id:
            messages.success(request, "this meep not yours !")
            return redirect('home')

    else:
        messages.success(request, 'You must login or signup')
        return redirect(request.META.get('HTTP_REFERER'))


def update_meep(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meep, id=pk)
        if request.user.id == meep.user.id:
            form = MeepForm(request.POST or None, instance=meep)
            if request.method == "POST":
                if form.is_valid():
                    meep = form.save(commit=False)
                    meep.user = request.user
                    meep.save()
                    messages.success(request, 'your meep has been updated !')
                    return redirect('home')
            else:
                return render(request, 'update_meep.html', {'form': form, 'meep': meep})
        elif request.user.id != meep.user.id:
            messages.success(request, "this meep not yours !")
            return redirect('home')

    else:
        messages.success(request, 'You must login or signup')
        return redirect(request.META.get('HTTP_REFERER'))


def search(request):
    if request.method == "POST":
        searchs = request.POST['search']
        searched = Meep.objects.filter(body__icontains=searchs)

        return render(request, 'search.html', {'searchs': searchs, 'searched': searched})
    else:
        return render(request, 'search.html', {})


def search_user(request):
    if request.method == "POST":
        searchs = request.POST['search']
        searched = User.objects.filter(username__contains=searchs)

        return render(request, 'search_user.html', {'searchs': searchs, 'searched': searched})
    else:
        return render(request, 'search_user.html', {})
