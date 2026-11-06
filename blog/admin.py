from django.contrib import admin
from .models import Category, Post, Comment


# Кастомизация админки для Статей (Post)
class PostAdmin(admin.ModelAdmin):
    # Колонки в общем списке
    list_display = ('title', 'category', 'author', 'created_at')
    # 4. Поле поиска по заголовку и тексту
    search_fields = ('title', 'content')
    # 5. Фильтрация справа (по рубрикам, авторам и дате)
    list_filter = ('category', 'author', 'created_at')
    # Навигация по датам
    date_hierarchy = 'created_at'
    # 3. Поле только для чтения
    readonly_fields = ('created_at',)


# Кастомизация админки для Комментариев (Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'post', 'created_at', 'is_published')
    # Быстрое редактирование прямо в списке
    list_editable = ('is_published',)
    search_fields = ('subject', 'text')
    list_filter = ('is_published', 'created_at')
    # 2. Скрываем поле created_at при редактировании
    exclude = ('created_at',)

    # Действие админа: опубликовать выбранные комменты разом
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    make_published.short_description = "Опубликовать выбранные комментарии"


# 1. Регистрируем все модели с их кастомными классами
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)