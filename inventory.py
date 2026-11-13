from storage import select_js, save_js

def select():
    data = select_js()
    for products in data:
        for keys , values in products.items():
            print(f"{keys} : {values}")

def search(id):
    data = select_js()
    try:
        obiect_js = next((d for d in data if d.get("id") == id), None)
        for keys, values in obiect_js.items():
            print(f"{keys} : {values}")
    except AttributeError:
        print("Такого инвентарный номера нет")




def generate_inventory_number(records):
    max_num = 0
    for rec in records:
        inv = str(rec.get("id", ""))
        if inv.startswith("INV-"):
            try:
                max_num = max(max_num, int(inv.split("-")[1]))
            except (ValueError, IndexError):
                continue
    return f"INV-{max_num + 1:04d}"

def is_number_unique(records, id):
    
    return all(
        str(rec.get("id", "")) != str(id)
        for rec in records
    )


def add_record(records, name, id, cabinet, condition, responsible):
    if not name or not name.strip():
        return False, "Строка не может остаться пустой."
    if not id or not id.strip():
        return False, "Строка не может остаться пустой."
    if not cabinet or not cabinet.strip():
        return False, "Строка не может остаться пустой."
    if not condition or not condition.strip():
        return False, "Строка не может остаться пустой."
    if not responsible or not responsible.strip():
        return False, "Строка не может остаться пустой."
    if not is_number_unique(records, id):
        return False, f"Запись с номером {id} уже существует."

    records.append({
        "id": id.strip(),
        "name": name.strip(),
        "cabinet": cabinet.strip(),
        "condition": condition.strip(),
        "responsible": responsible.strip(),
    })
    return True, f"Запись '{name}' добавлена."

def add():

    records = select_js()

    name = input("Введите название объекта: ")

    suggested = generate_inventory_number(records)
    print(f"Предлагаемый инвентарный номер: {suggested}")
    id = input(f"Введите номер: ").strip() or suggested

    cabinet = input("Введите кабинет: ")
    condition = input("Введите состояние: ")
    responsible = input("Введите ответственное лицо: ")


    success, message = add_record(records, name, id, cabinet, condition, responsible)
    print(message)
    if success:
        save_js(records)

#Изменение данных
def update_record(records, id, name=None, cabinet=None, condition=None, responsible=None):
    for rec in records:
        if str(rec.get("id")) == str(id):
            #Благодаря этой записи при пустом поле прошлые данные останутся не тронутыми, то есть и пробелы и
            # пустое поле ни на что не повлияют и поле не останется пустым
            if name and name.strip():
                rec["name"] = name.strip()
            if cabinet and cabinet.strip():
                rec["cabinet"] = cabinet.strip()
            if condition and condition.strip():
                rec["condition"] = condition.strip()
            if responsible and responsible.strip():
                rec["responsible"] = responsible.strip()
            return True, f"Запись {id} обновлена."
    return False, f"Запись с номером {id} не найдена."

#Тут мы просто вводим номер записи которую будем изменять
def update():
    records = select_js()

    id = input("Введите номер записи для изменения: ").strip()
    #Показывает текущие значения записи, но скорее просто ищет её, а уже ниже показывает
    current = next((r for r in records if str(r.get("id")) == str(id)), None)
    if current is None:
        print(f"Запись с номером {id} не найдена.")
        return

    print("Оставьте поле пустым, чтобы не менять.")
    #Ага, тут показывает
    name = input(f"Название [{current.get('name', '')}]: ")
    cabinet = input(f"Кабинет [{current.get('cabinet', '')}]: ")
    condition = input(f"Состояние [{current.get('condition', '')}]: ")
    responsible = input(f"Ответственное лицо [{current.get('responsible', '')}]: ")

    success, message = update_record(records, id, name, cabinet, condition, responsible)
    print(message)
    if success:
        save_js(records)


#Удаление данных
def delete_record(records, id):
    for i, rec in enumerate(records):
        if str(rec.get("id")) == str(id):
            del records[i]
            return True, f"Запись {id} удалена."
    return False, f"Запись с номером {id} не найдена."

def delete():
    records = select_js()

    id = input("Введите номер записи для удаления: ").strip()

    current = next((r for r in records if str(r.get("id")) == str(id)), None)
    if current is None:
        print(f"Запись с номером {id} не найдена.")
        return

    # Показываем, что именно будет удалено
    print("Будет удалена запись:")
    for key, value in current.items():
        print(f"  {key} : {value}")

    # Подтверждение
    confirm = input(f"Удалить запись {id}? (y/n): ").strip().lower()
    if confirm not in ("y", "yes", "д", "да"):
        print("Удаление отменено.")
        return

    success, message = delete_record(records, id)
    print(message)
    if success:
        save_js(records)
