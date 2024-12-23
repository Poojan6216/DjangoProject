from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import UserDetails


def hello_world(request):
    return HttpResponse("Hello, world!")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if UserDetails.objects.filter(email=email).exists():
            return HttpResponse("Email already exists. Please try again.")

        user = UserDetails(username=username, email=email, password=password)
        user.save()
        return redirect('login') 
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserDetails.objects.get(email=email)
            if user.password == password:
                return HttpResponse("Login Successful!")
            else:
                return HttpResponse("Invalid password. Please try again.")
        except UserDetails.DoesNotExist:
            return HttpResponse("Email not registered.")
    return render(request, 'login.html')

def get_all_users(request):
    if request.method == "GET":
        users = UserDetails.objects.all()
        users_list = [{"username": user.username, "email": user.email} for user in users]
        return JsonResponse({"users": users_list}, safe=False)


def get_user_by_email(request, email):
    if request.method == "GET":
        user = get_object_or_404(UserDetails, email=email)
        user_data = {"username": user.username, "email": user.email}
        return JsonResponse(user_data)


def update_user(request, email):
    if request.method == "POST":
        user = get_object_or_404(UserDetails, email=email)
        username = request.POST.get("username", user.username)
        password = request.POST.get("password", user.password)
        user.username = username
        user.password = password
        user.save()
        return JsonResponse({"message": "User updated successfully!"})


def delete_user(request, email):
    if request.method == "DELETE":
        user = get_object_or_404(UserDetails, email=email)
        user.delete()
        return JsonResponse({"message": "User deleted successfully!"})

# Create your views here.
