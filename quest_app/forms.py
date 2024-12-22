from django import forms
from .models import Habit, Quest, Reward
from django.contrib.auth.models import User
from .models.profile import Profile  # 'UserProfile' を 'Profile' に変更
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# 習慣フォーム
class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description']

# ユーザー登録用フォーム
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="メールアドレス", required=True, help_text="有効なメールアドレスを入力してください。")
    username = forms.CharField(
        label="ユーザー名",
        max_length=150,
        required=True,
        help_text="必須項目。150文字以内で、アルファベット、数字、@、.、+、-、_のみ使用できます。"
    )
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        help_text="8文字以上で、個人情報と類似しないパスワードを使用してください。"
    )
    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput,
        help_text="再入力したパスワードと一致する必要があります。"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# ユーザー情報編集用フォーム
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


# クエストフォーム
class QuestForm(forms.ModelForm):
    class Meta:
        model = Quest
        fields = ['title', 'description', 'points']
        labels = {
            'title': 'クエスト名',
            'description': '詳細',
            'points': 'ポイント数',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'クエスト名を入力してください'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '詳細を入力してください'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ポイント数を入力してください'}),
        }

# 報酬登録フォーム
class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['name', 'description', 'points_required']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Optional: Enter description here'}),
            'points_required': forms.NumberInput(attrs={'placeholder': 'Required points'})  # ここでポイントにプレースホルダーを追加
        }

        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # 'UserProfile' を 'Profile' に変更
        fields = ['points']

# ユーザー変更用フォーム
class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
