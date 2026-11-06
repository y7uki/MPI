from django.db import models
from django.contrib.auth.models import User

# Рубрики (14)
class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)

    def __str__(self):
        return self.name

# Статьи (14)
class Post(models.Model):
    title = models.CharField('Заголовок статьи', max_length=200)
    content = models.TextField('Текст статьи')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.title

# Комментарии с возможностью снять с публикации (Лаба 16)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='К какой статье')
    subject = models.CharField('Тема комментария', max_length=100)  # Валидация: максимум 100 символов
    text = models.TextField('Текст комментария', max_length=500)      # Валидация: максимум 500 символов
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_published = models.BooleanField('Опубликован', default=True)   # Снять с публикации (галочка)

    def __str__(self):
        return f"{self.subject} ({'Опубликован' if self.is_published else 'Снят'})"