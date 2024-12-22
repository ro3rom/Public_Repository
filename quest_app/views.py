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


# 自分のアプリケーションのモデルやフォームをインポート
from .models import Point, Reward, Quest, Habit, HabitQuest, Profile  # Profile は一度にインポート
from .forms import HabitForm, CustomUserCreationForm, UserEditForm, QuestForm, RewardForm, UserProfileForm, CustomUserChangeForm
from quest_app.forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


# ウェルカムページのビュー
def welcome(request):
    return render(request, 'welcome.html')


def index(request):
    if request.user.is_authenticated:
        return redirect('home')  # ログインしている場合はホーム画面にリダイレクト
    return redirect('welcome')  # ログインしていない場合はウェルカムページにリダイレクト


# ログインビュー: ユーザーがログインするための処理
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
            messages.error(request, '無効なユーザー名またはパスワードです。')
    else:
        form = AuthenticationForm()

    return render(request, 'quest_app/login.html', {'form': form})


from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponseNotAllowed

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('quest_app:home')  # ログアウト後にホームにリダイレクト
    return HttpResponseNotAllowed(['POST'])  # GETリクエストの場合は405エラーを返す


# ホーム画面ビュー
@login_required 
def home(request):
    quests = Quest.objects.all()  # クエストを全て取得
    return render(request, 'quest_app/home.html', {'quests': quests})

# 新規登録ページのビュー
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ユーザーを保存
            login(request, user)  # ログイン
            return redirect('home')  # 登録後にホームにリダイレクト
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


# ユーザー編集とパスワードの変更ビュー
@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        
        # バリデーション: パスワードフォームが無効でも、パスワード変更しないことに対応
        if user_form.is_valid():
            user_form.save()

            # パスワードが変更された場合のみ保存
            if password_form.is_valid():
                password_form.save()

            return redirect('quest_app:home')  # 編集後のリダイレクト先
        else:
            # バリデーションエラー時にフォームとエラーメッセージを表示
            return render(request, 'quest_app/edit_user.html', {'user_form': user_form, 'password_form': password_form, 'errors': 'フォームが無効です。再確認してください。'})

    else:
        user_form = UserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    
    return render(request, 'quest_app/edit_user.html', {'user_form': user_form, 'password_form': password_form})

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
@login_required
def edit_reward(request, reward_id):
    reward = get_object_or_404(Reward, pk=reward_id)
    if request.method == 'POST':
        # フォームからのデータを処理する
        form = RewardForm(request.POST, instance=reward)
        if form.is_valid():
            form.save()
            return redirect('quest_app:reward_list')
    else:
        # GETリクエスト時にフォームを準備する
        form = RewardForm(instance=reward)
    return render(request, 'quest_app/edit_reward.html', {'form': form})

# 報酬削除
@login_required
def reward_delete(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id)
    reward.delete()  # 報酬を削除
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

