ИНСТРУКЦИЯ ПО ЗАПУСКУ МАГАЗИНА

1. Установите Python (если нет): https://www.python.org/
2. Откройте эту папку в терминале (командной строке).

3. Создайте виртуальное окружение:
   python -m venv venv

4. Активируйте его:
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

5. Установите библиотеки:
   pip install -r requirements.txt

6. Запустите сайт:
   python manage.py runserver

7. Откройте в браузере: http://127.0.0.1:8000/
   Админка: http://127.0.0.1:8000/admin/
   Логин админа: admin
   Пароль админа: admin