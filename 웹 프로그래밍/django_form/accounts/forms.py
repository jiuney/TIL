from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()    # 현재 활성화 된 user model을 리턴한다.
        fields = ('first_name', 'last_name')