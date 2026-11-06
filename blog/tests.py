from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Category, Post, Comment

class BlogTests(TestCase):
    def setUp(self):
        # Создаем тестовые данные в виртуальной тестовой базе
        self.user = User.objects.create_user(username='tester', password='password123')
        self.category = Category.objects.create(name='Тест-рубрика')
        self.post = Post.objects.create(
            title='Тестовый пост',
            content='Текст тестового поста',
            author=self.user,
            category=self.category
        )
        self.client = Client()

    # 1. Тест создания модели Post и строкового метода __str__
    def test_post_creation(self):
        self.assertEqual(str(self.post), 'Тестовый пост')
        self.assertEqual(self.post.category.name, 'Тест-рубрика')

    # 2. Тест ответа главной страницы (код 200 OK)
    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый пост')

    # 3. Тест добавления комментария через форму (POST запрос)
    def test_add_comment(self):
        response = self.client.post('/', {
            'post': self.post.id,
            'subject': 'Тестовая тема',
            'text': 'Тестовый текст комментария'
        })
        # Должен произойти редирект на главную (код 302)
        self.assertEqual(response.status_code, 302)
        # Проверяем, что коммент реально создался в базе
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().subject, 'Тестовая тема')