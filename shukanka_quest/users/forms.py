from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ユーザー登録用フォーム
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Emailフィールドを追加

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # 登録時に表示するフィールド

