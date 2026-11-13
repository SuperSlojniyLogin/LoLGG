import json
import os

filename = 'data/inventory.json'
if not os.path.isfile(filename):
    print("Файл не найден, при первом сохранении создастся новый.")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([], f)


def select_js():
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_js(data):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except (OSError, TypeError) as e:
        print(f"Ошибка при сохранении файла: {e}")


