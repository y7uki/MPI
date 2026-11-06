from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Post
from .forms import CommentForm

# Словарь переводов для сайта (Лаба 19)
TRANSLATIONS = {
    'ru': {
        'site_title': 'Блог на Django',
        'home': 'Главная',
        'admin_panel': 'Панель управления',
        'welcome': 'Привет',
        'logout': 'Выйти',
        'login': 'Войти',
        'register': 'Регистрация',
        'leave_comment': 'Оставить комментарий',
        'submit_comment': 'Опубликовать комментарий',
        'posts_title': 'Публикации',
        'category': 'Рубрика',
        'author': 'Автор',
        'comments': 'Комментарии',
        'no_comments': 'Комментариев пока нет.',
        'no_posts': 'Статей пока нет.',
    },
    'en': {
        'site_title': 'Django Blog',
        'home': 'Home',
        'admin_panel': 'Admin Panel',
        'welcome': 'Hello',
        'logout': 'Log out',
        'login': 'Log in',
        'register': 'Register',
        'leave_comment': 'Leave a comment',
        'submit_comment': 'Submit comment',
        'posts_title': 'Publications',
        'category': 'Category',
        'author': 'Author',
        'comments': 'Comments',
        'no_comments': 'No comments yet.',
        'no_posts': 'No articles yet.',
    }
}

def post_list(request):
    # Получаем язык из куки (по умолчанию 'ru')
    lang = request.COOKIES.get('django_language', 'ru')
    if lang not in TRANSLATIONS:
        lang = 'ru'
    t = TRANSLATIONS[lang]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            cache.clear()
            send_mail(
                subject=f'Новый комментарий: {comment.subject}',
                message=f'К статье "{comment.post.title}" оставлен комментарий:\n\n{comment.text}',
                from_email='noreply@myblog.com',
                recipient_list=['admin@myblog.com'],
                fail_silently=False,
            )
            messages.success(request, 'Комментарий успешно добавлен!' if lang == 'ru' else 'Comment added successfully!')
            return redirect('/')
    else:
        form = CommentForm()

    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts, 'form': form, 't': t, 'current_lang': lang})

def switch_lang(request, lang):
    cache.clear()
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('django_language', lang)
    return response

def register(request):
    lang = request.COOKIES.get('django_language', 'ru')
    t = TRANSLATIONS.get(lang, TRANSLATIONS['ru'])
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            cache.clear()
            messages.success(request, f'Добро пожаловать, {user.username}!' if lang == 'ru' else f'Welcome, {user.username}!')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form, 't': t})

def user_login(request):
    lang = request.COOKIES.get('django_language', 'ru')
    t = TRANSLATIONS.get(lang, TRANSLATIONS['ru'])
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            cache.clear()
            messages.success(request, f'Вы вошли как {user.username}!' if lang == 'ru' else f'Logged in as {user.username}!')
            return redirect('/')
        else:
            messages.error(request, 'Неверный логин или пароль.' if lang == 'ru' else 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form, 't': t})

def user_logout(request):
    lang = request.COOKIES.get('django_language', 'ru')
    logout(request)
    cache.clear()
    messages.info(request, 'Вы успешно вышли из системы.' if lang == 'ru' else 'You have been logged out.')
    return redirect('/')