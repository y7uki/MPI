# Задания 21–23: деплой Django-проекта (aidar) + Supervisor

## 21. Хостинг, Nginx, uWSGI
1. Зарегистрируйтесь на хостинге с Python (PythonAnywhere — бесплатный, https://www.pythonanywhere.com)
   или возьмите любой VPS (Ubuntu) из списка в задании.
2. Загрузите проект (git clone или scp) в `/home/USER/aidar`.
3. Окружение:
   ```bash
   cd ~/aidar && python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
4. Замените `USER` и `example.com` в файлах `deploy/*` на свои значения.
5. Nginx + uWSGI (на VPS):
   ```bash
   sudo apt install nginx
   sudo cp deploy/nginx.conf /etc/nginx/sites-available/aidar
   sudo ln -s /etc/nginx/sites-available/aidar /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl restart nginx
   venv/bin/uwsgi --ini deploy/uwsgi.ini   # проверка вручную
   ```
   На PythonAnywhere Nginx/uWSGI настраивать не нужно: вкладка Web → Add new web app →
   Manual configuration → указать путь к проекту, virtualenv и WSGI-файл (`aidar.wsgi`),
   Static files: URL `/static/` → `/home/USER/aidar/staticfiles`.

## 22–23. Supervisor
```bash
sudo apt install supervisor
sudo cp deploy/supervisor.conf /etc/supervisor/conf.d/aidar.conf
mkdir -p ~/aidar/logs
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status aidar
```
Управление: `sudo supervisorctl restart aidar | stop aidar | start aidar | tail aidar`.
Проверка автоперезапуска: `pkill -f uwsgi` — supervisor поднимет процесс заново.
