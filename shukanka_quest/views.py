from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from quest_app.models import Habit
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

# habit_list ビュー
@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)  # ログイン中のユーザーの習慣のみ取得
    return render(request, 'habit_list.html', {'habits': habits})

# ユーザー登録ビュー
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            return render(request, 'registration/register.html', {'error': 'パスワードが一致しません'})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, 'registration/register.html', {'error': 'ユーザー名またはメールアドレスがすでに登録されています'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

        return redirect('home')

    return render(request, 'registration/register.html')

# ホームページビュー
@login_required
def home(request):
    return render(request, 'home.html')


# ログインビュー
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '無効なユーザー名またはパスワードです。'})

    return render(request, 'login.html')

# 習慣追加ビュー
@login_required
def add_habit(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Habit.objects.create(user=request.user, name=name, description=description)
        return redirect('habit_list')

    return render(request, 'add_habit.html')

# トップページビュー
def index(request):
    return render(request, 'index.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # ログインページにリダイレクトする場合
    return redirect('home')  # GETメソッドでアクセスした場合にはホームページに戻す
