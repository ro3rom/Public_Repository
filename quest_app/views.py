# 必要なDjangoモジュールをインポート
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from . import views

# 自分のアプリケーションのモデルやフォームをインポート
from .models import Point, Reward, Quest, Habit, HabitQuest, Profile  # Profile は一度にインポート
from .forms import HabitForm, CustomUserCreationForm, UserEditForm, QuestForm, RewardForm, UserProfileForm, CustomUserChangeForm
from quest_app.forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


# ウェルカムページのビュー
def welcome(request):
    return render(request, 'shukanka_quest/welcome.html')

def index(request):
    if request.user.is_authenticated:
        return redirect('home')  # ログインしている場合はホーム画面にリダイレクト
    return redirect('welcome')  # ログインしていない場合はウェルカムページにリダイレクト

# アカウント削除
@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "アカウントを削除しました。")
        return redirect('welcome')  # リダイレクト先を指定
    else:
        messages.error(request, "無効なリクエストです。")
        return redirect('user_edit')  # 編集ページに戻る

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # ログインしている場合はホーム画面にリダイレクト

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # ホーム画面にリダイレクト
        else:
            messages.error(request, '無効なユーザー名またはパスワードです。')  # エラーメッセージ
    else:
        form = AuthenticationForm()

    return render(request, 'quest_app/login.html', {'form': form})

from django.http import HttpResponseNotAllowed

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('quest_app:home')  # ログアウト後にホームにリダイレクト
    return HttpResponseNotAllowed(['POST'])  # GETリクエストの場合は405エラーを返す


# ホーム画面ビュー
@login_required
def home(request):
    # クエストを全て取得
    quests = Quest.objects.all()

    # ユーザーがログインしている場合にメッセージを表示
    if request.user.is_authenticated:
        messages.success(request, f'ようこそ、{request.user.username} さん！')

    # テンプレートをレンダリング
    return render(request, 'quest_app/home.html', {'quests': quests})

# 新規登録ページのビュー
def register_view(request):
    """新規登録用のビュー"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ユーザーを保存
            login(request, user)  # 自動ログイン
            messages.success(request, '登録が完了しました！')  # 成功メッセージ
            return redirect('home')  # 登録後にホーム画面にリダイレクト
        else:
            # フォームが無効な場合、エラーメッセージを追加
            messages.error(request, '入力内容に誤りがあります。再度お試しください。')
    else:
        form = CustomUserCreationForm()

    return render(request, 'quest_app/register.html', {'form': form})

# 習慣一覧ビュー
@login_required  # ログイン必須のビューにデコレータを追加
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)  # ユーザーに関連する習慣を取得
    return render(request, 'habit_list.html', {'habits': habits})


# 習慣追加ビュー
@login_required  # ログイン必須のビューにデコレータを追加
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user  # ユーザーを習慣に紐づけ
            habit.save()
            return redirect('habit_list')  # 習慣一覧ページにリダイレクト
    else:
        form = HabitForm()

    return render(request, 'add_habit.html', {'form': form})

# クエスト追加ビュー
def add_quest(request):
    if request.method == 'POST':
        form = QuestForm(request.POST)
        if form.is_valid():
            form.save()  # クエストを保存
            messages.success(request, 'クエストが追加されました。')
            return redirect('quest_list')  # クエスト一覧ページにリダイレクト
    else:
        form = QuestForm()

    return render(request, 'quest_app/add_quest.html', {'form': form})

# クエスト編集ビュー
def edit_quest(request, quest_id):
    quest = get_object_or_404(Quest, id=quest_id)  # クエストを取得
    if request.method == 'POST':
        form = QuestForm(request.POST, instance=quest)
        if form.is_valid():
            form.save()  # クエストを更新
            messages.success(request, 'クエストが編集されました。')
            return redirect('quest_list')  # 編集後に一覧に戻る
    else:
        form = QuestForm(instance=quest)  # 既存のデータをフォームに表示
    
    return render(request, 'quest_app/edit_quest.html', {'form': form})

# クエスト削除ビュー
def delete_quest(request, quest_id):
    quest = get_object_or_404(Quest, id=quest_id)
    quest.delete()
    messages.success(request, 'クエストが削除されました。')
    return redirect('quest_list')  # quest_listにリダイレクト

# クエスト一覧ビュー
def quest_list(request):
    quests = Quest.objects.all()  # クエスト一覧を取得

    if request.method == 'POST':
        form = QuestForm(request.POST)
        if form.is_valid():
            form.save()  # 新しいクエストを追加
            messages.success(request, 'クエストが追加されました。')
    else:
        form = QuestForm()  # 新規追加フォームを表示
    
    return render(request, 'quest_app/quest_list.html', {'form': form, 'quests': quests})

@login_required
def exchange_points(request):
    # ユーザーにプロファイルがない場合は作成
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    # ユーザーのプロファイルを取得
    user_profile = request.user.profile
    user_points = user_profile.points

    # すべての報酬を取得
    rewards = Reward.objects.all()

    if request.method == 'POST':
        # ユーザーが交換したい報酬を選択
        reward_id = request.POST.get('reward')
        try:
            reward = Reward.objects.get(id=reward_id)
        except Reward.DoesNotExist:
            messages.error(request, "選択した報酬が存在しません。")
            return redirect('quest_app:exchange_points')

        # 報酬に必要なポイントを確認
        if user_points >= reward.points_required:  
            # ポイントを引き、報酬を付与
            user_profile.points -= reward.points_required  
            user_profile.save()

            # 報酬をユーザーに追加
            user_profile.rewards.add(reward)

            messages.success(request, f"報酬「{reward.name}」を交換しました。")
        else:
            messages.error(request, "ポイントが不足しています。")

    # GETリクエスト時はポイントと報酬を表示
    return render(request, 'quest_app/exchange_points.html', {
        'user_points': user_points,
        'rewards': rewards
    })

def complete_quest(request, quest_id):
    # クエストを取得（存在しない場合は404エラー）
    quest = get_object_or_404(Quest, id=quest_id)

    # クエストがまだ完了していない場合のみ完了処理を行う
    if not quest.is_completed():
        quest.completed_at = timezone.now()  # 完了日時を現在日時に設定
        quest.save()

        # ユーザーにポイントを加算
        user = request.user
        if hasattr(user, 'profile'):  # ユーザーにプロフィールがある場合
            user.profile.points += quest.points  # ユーザーのプロフィールにあるpointsフィールドに加算
            user.profile.save()  # ポイントを保存

            # 完了したことをユーザーに知らせるメッセージ
            messages.success(request, f'クエスト『{quest.title}』を完了しました！')

    # クエスト一覧ページにリダイレクト
    return redirect('quest_list')


@login_required
def initialize_points(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # UserProfileからProfileに変更
    profile.points = 0  # ポイントを初期化
    profile.save()
    return render(request, 'initialize_points.html', {'profile': profile})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'form': form})

# 必要なフォームをインポート
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        # ユーザー名を更新する処理
        if 'update_username' in request.POST and user_form.is_valid():
            new_username = user_form.cleaned_data['username']
            request.user.username = new_username
            request.user.save()
            request.session['username'] = request.user.username  # セッションを更新
            print(f"ユーザー名が更新されました: {new_username}")  # デバッグ用の出力

        # メールアドレスを更新する処理
        if 'update_email' in request.POST and user_form.is_valid():
            request.user.email = user_form.cleaned_data['email']
            request.user.save()

        # パスワードを更新する処理
        if 'update_password' in request.POST and password_form.is_valid():
            password_form.save()

        # 更新後のリダイレクト
        if 'update_username' in request.POST or 'update_email' in request.POST or 'update_password' in request.POST:
            return render(request, 'quest_app/home.html', {
    'user': request.user,  # 更新されたユーザー情報を渡す
})
    else:
        user_form = UserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'quest_app/edit_user.html', {
        'user_form': user_form,
        'password_form': password_form
    })

# 報酬追加
@login_required
def add_reward(request):
    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quest_app:reward_list')  # 報酬一覧にリダイレクト
    else:
        form = RewardForm()
    return render(request, 'quest_app/add_reward.html', {'form': form})

# 報酬編集
def edit_reward(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id)
    if request.method == 'POST':
        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            form.save()
            # 編集後に成功メッセージを設定
            messages.success(request, "報酬が編集されました！")
            return redirect('quest_app:reward_list')
    else:
        form = RewardForm(instance=reward)
    return render(request, 'quest_app/edit_reward.html', {'form': form, 'reward': reward})

# 報酬削除
@login_required
def reward_delete(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id)
    reward.delete()  # 報酬を削除

    # 削除成功メッセージを設定
    messages.success(request, "報酬が削除されました！")

    return redirect('quest_app:reward_list')  # 報酬管理ページにリダイレクト


# カスタム変更フォーム例
@login_required
def custom_edit_user(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'quest_app/edit_user.html', {'form': form})

# 報酬一覧を表示する画面
def reward_list(request):
    rewards = Reward.objects.all()  # 全ての報酬を取得
    return render(request, 'quest_app/reward_list.html', {'rewards': rewards})

