from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required   
from django.contrib import messages
from django.contrib.auth.models import User
from match.models import Match


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'User Does Not Exist')
            return render(request, 'login.html')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard') # Log user in if credentials are correct and redirect to dashboard
        else:
            messages.error(request, 'Invalid Username or Password') #Deny Login if credentials are incorrect

    return render(request, 'login.html')

def register_new_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        #Informs users passwords do not match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
        
        
        #Informs users username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        
        #Create new user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'User registered successfully')
        return redirect('login')  # redirect to login page after successful registration
    
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

#Login to the system
@login_required
def dashboard(request):
    open_matches = Match.objects.filter(
        user = request.user,
        voting_open = True
        ).order_by('-created_at')
        
    
    return render(request, 'dashboard.html', {'open_matches': open_matches})




