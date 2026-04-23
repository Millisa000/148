import requests
import time
import json

# ---НАСТРОЙКИ---
TOKEN = ""
FOLDER_NAME = "Python-148"
CAT_TEXT = "I_MADE_IT"

# Ссылка на картинку
SOURCE_URL = f"https://cataas.com/cat/cute/says/{CAT_TEXT}"

# Формируем путь:
DISK_PATH = f"/Python-148/cat_from_air.jpg"

# URL API
UPLOAD_URL = "https://cloud-api.yandex.net/v1/disk/resources/upload"

# ---ЗАПРОС---

headers = {
    "Authorization": f"OAuth {TOKEN.strip()}"
}

params = {
    "path": DISK_PATH,
    "url": SOURCE_URL
}

print(f"Отправляю команду Яндексу. Файл должен появиться как: {DISK_PATH}")

response = requests.post(UPLOAD_URL, headers=headers, params=params)

who_am_i = requests.get("https://cloud-api.yandex.net/v1/disk", headers=headers).json()
print("Я зашел как пользователь:", who_am_i.get('user', {}).get('display_name'))
if response.status_code == 202:
    print(" Яндекс принял задачу!")
    operation_link = response.json().get("href")
    print(f"Проверь статус операции здесь (открой в браузере): {operation_link}")
else:
    print(f" Ошибка запроса: {response.status_code}")
    print(f"Ответ: {response.text}")


# ---ПРОВЕРКА СТАТУСА---

print("Ждем 5 секунды, пока Яндекс качает...")
time.sleep(5) # Даем время на скачивание

status_check = requests.get(operation_link, headers=headers).json()

print(f"Реальный статус загрузки: {status_check.get('status')}")

if status_check.get('status') == 'failed':
    print(f"Причина неудачи: {status_check.get('message')}")
elif status_check.get('status') == 'success':
    file_meta = requests.get("https://yandex.net/resources",
                             headers=headers, params={"path": DISK_PATH}).json()
    result_data = {
        "image": SOURCE_URL,
        "size": file_meta.get("size"),
        "folder": FOLDER_NAME,
        "filename": "cat_from_air.jpg"
    }
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=4)
    print(" ВСЁ! Картинка точно на месте. Обнови страницу Диска.")