import json
filename = 'data/inventory.json'

def select_js():
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []



# # Шаг 1: Безопасно читаем текущие данные из файла
# try:
#     with open(filename, 'r', encoding='utf-8') as f:
#         templates = json.load(f)
# except (FileNotFoundError, json.JSONDecodeError):
#     templates = []
#
# print(templates)
# # Шаг 2: Добавляем или обновляем данные в словаре Python
# templates.append({"id": 1, "name": "Объект"})
#
# # Шаг 3: Записываем обновленный словарь обратно в тот же файл
# with open(filename, 'w', encoding='utf-8') as f:
#     json.dump(templates, f, indent=4, ensure_ascii=False)
#
#
# print(templates)