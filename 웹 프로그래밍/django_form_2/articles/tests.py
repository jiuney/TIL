from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from .models import Article

class SettingsTest(TestCase):
    def test_01_settings(self):
        self.assertEqual(settings.USE_I18N, True)
        self.assertEqual(settings.USE_TZ, True)
        self.assertEqual(settings.LANGUAGE_CODE, 'ko-kr')
        self.assertEqual(settings.TIME_ZONE, 'Asia/Seoul')

class ArticleModelTest(TestCase):
    def test_01_model(self):
        user = User.objects.create(username="test user")
        article = Article.objects.create(title="test title", content="test content", user=user)
        self.assertEqual(str(article), f'{article.title}')
