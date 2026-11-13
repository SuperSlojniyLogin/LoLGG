from storage import select_js, save_js

def select():
    data = select_js()
    if not data:
        print("Список записей пуст.")
        return
    for products in data:
        for keys , values in products.items():
            print(f"{keys} : {values}")

def search():
    print("Ищите по \n1.кабинету\nили\n2.Инвентарному номеру")
    choice = input("1 или 2: ").strip()
    if choice == "1":
        kab = input("Какой кабинет: ")
        search_kab(kab)
    elif choice == "2":
        id = input("Какой инвентарный номер: ")
        search_id(id)
    else:
        print("Введите число 1 или 2")


def search_kab(kab):
    data = select_js()
    kab = str(kab).strip()
    try:
        if not (1 <= int(kab) <= 499):
            print("нет такого кабинета")
            return
    except (AttributeError, ValueError):
        print("Кабинет должен содержать только цифры.")
        return

    found_items = [d for d in data if d.get("cabinet") == kab]

    if not found_items:
        print("В этом кабинете ничего нет")
        return

    for item in found_items:
        for keys, values in item.items():
            print(f"{keys} : {values}")

def search_id(id):
    data = select_js()
    try:
        id = int(id.removeprefix("INV-"))
    except (AttributeError, ValueError):
        print("Номер это не буквы")
        return
    try:
        object_js = next((d for d in data if int(d.get("id").removeprefix("INV-")) == id), None)
        for keys, values in object_js.items():
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
        rec.get("id", "") != id
        for rec in records
    )

cond = {
        "1": "исправно",
        "2": "требует ремонта",
        "3": "списано",
    }

def add_record(records, name, id, cabinet, condition, responsible):

    if not name or not name.strip():
        return False, "Строка не может остаться пустой."
    if not id or not id.strip():
        return False, "Строка не может остаться пустой."
    if not cabinet or not cabinet.strip():
        return False, "Строка не может остаться пустой."
    try:
        if not (1 <= int(cabinet) <= 499):
            return False, "нет такого кабинета"
    except (AttributeError, ValueError):
        return False, "Кабинет должен содержать только цифры."
    if not condition or not condition.strip():
        return False, "Строка не может остаться пустой."
    condition = condition.strip().lower()
    if condition not in cond.keys() and condition not in cond.values():
        return False, "Нет такого состояния"
    else:
        if condition in cond.keys():
            condition = cond[condition]

    if not responsible or not responsible.strip():
        return False, "Строка не может остаться пустой."

    try:
        id = f"INV-{int(id.strip().removeprefix('INV-')):04d}"
    except (AttributeError, ValueError):
        return False, "Номер должен содержать только цифры."
    if not is_number_unique(records, id):
        return False, f"Запись с номером {id} уже существует."

    records.append({
        "id": id,
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
    print("Варианты состояния 1.Исправно - 2.Требует ремонта - 3.Списано")
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
                try:
                    if not (1 <= int(cabinet) <= 499):
                        return False, "Номер кабинета должен быть от 1 до 499."
                except ValueError:
                    return False, "Кабинет должен содержать только цифры."
                rec["cabinet"] = cabinet.strip()
            if condition and condition.strip():
                condition = condition.strip().lower()
                if condition not in cond.keys() and condition not in cond.values():
                    return False, "Нет такого состояния"
                else:
                    if condition in cond.keys():
                        rec["condition"] = cond[condition]
                    else:
                        rec["condition"] = condition

            if responsible and responsible.strip():
                rec["responsible"] = responsible.strip()
            return True, f"Запись {id} обновлена."
    return False, f"Запись с номером {id} не найдена."

#Тут мы просто вводим номер записи которую будем изменять
def update():
    records = select_js()

    id = input("Введите номер записи для изменения: ").strip()
    try:
        id = f"INV-{int(id.strip().removeprefix('INV-')):04d}"
    except ValueError:
        print("Номер должен содержать только цифры.")
        return
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
    try:
        id = f"INV-{int(id.removeprefix('INV-')):04d}"
    except ValueError:
        print("Номер должен содержать только цифры.")
        return
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
