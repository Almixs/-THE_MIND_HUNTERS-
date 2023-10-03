# Встановлюємо базовий імедж
FROM python:3.9

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли Python в контейнер
COPY assistant /app/assistant
COPY setup.py /app/setup.py

# Копіюємо файли даних в контейнер
COPY AddressBook.bin /app/AddressBook.bin
COPY NoteBook.bin /app/NoteBook.bin

# Встановлюємо необхідні залежності для вашого проекту (якщо це потрібно)
RUN pip install -r /app/assistant/requirements.txt
# Запускаємо ваш додаток
CMD ["python", "assistant/__main__.py"]

