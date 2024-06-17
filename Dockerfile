# Используем официальный образ Python в качестве базового образа
FROM python:3.12

# Устанавливаем переменную окружения для отключения буферизации stdout и stderr
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . /app/

# Устанавливаем переменные окружения для базы данных
ENV SECRET_KEY=django-insecure-kkk3_m878*vn6ei9+kghh-r0!ri)4u$#u=01bu@n2w^pbh)=x0
ENV DATABASE_NAME=restreservationdb
ENV DATABASE_USER=adminka
ENV DATABASE_PASSWORD=password
ENV DATABASE_HOST=db
ENV DATABASE_PORT=5432
ENV RECAPTCHA_PUBLIC_KEY=6LfJRvUpAAAAAICpI_ut0cX3d9-UFsr-sow7Njep
ENV RECAPTCHA_PRIVATE_KEY=6LfJRvUpAAAAAD0a0lkxFrlO73ZU1xnK5JXn5KhY
ENV EMAIL_HOST_USER=forSendEmails@yandex.ru
ENV EMAIL_HOST_PASSWORD=nstgqcoupputlcvd

# Запускаем команды для выполнения миграций и запуска сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
