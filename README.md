Clip Joy - видио хостинг


Для запуска создайте окружение и загрузите в него все из myvlog/requirements.txt

Имеет 3 основных приложения:
1. myvlog - приложение с настройкими
2. vlog - Основное пиложение сайти
3. users - Приложение отвечающее за авторизацию регистрацию и тд (может востановить пароль через почту)


 Для запуска пропишите 
 
```
 git clone https://github.com/Alex1555ggff/Clip_Joy.git
 cd ./myvlog
 pip install -r requirements.txt
 python generate_token.py
 python manage.py makemigrations
 python manage.py migrate
 python manage.py createsuperuser
```
