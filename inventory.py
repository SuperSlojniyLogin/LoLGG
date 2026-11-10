from storage import select_js, save_js

def select():
    list_js = select_js()
    for products in list_js:
        for keys , values in products.items():
            print(f"{keys} : {values}")



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


def add_record(records, name, id):
    
    if not name or not name.strip():
        return False, 
    if not id or not id.strip():
        return False, 
    if not is_number_unique(records, id):
        return False, f"Запись с номером {id} уже существует."
        

    records.append({

        "id": id.strip(),
        "name": name.strip(),
    })
    return True, f"Запись '{name}' добавлена."

def add():

    records = select_js()

    name = input("Введите название объекта: ")
    suggested = generate_inventory_number(records)
    print(f"Предлагаемый инвентарный номер: {suggested}")

    id = input(f"Введите номер: ").strip() or suggested

    success, message = add_record(records, name, id)
    print(message)
    if success:
        save_js(records)
