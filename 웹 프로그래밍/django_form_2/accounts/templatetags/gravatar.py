import hashlib
from django import template

register = template.Library()

@register.filter # 아래의 함수를 필터로 추가한다.
def makemd5(email):
    return hashlib.md5(email.strip().lower().encode("utf-8")).hexdigest()