from storage import select_js, save_js

def select():
    list_js = select_js()
    for products in list_js:
        for keys , values in products.items():
            print(f"{keys} : {values}")

def generate_inventory_number(records):
    max_num = 0
    for rec in records:
        inv = str(rec.get("inventory_number", ""))
        if inv.startswith("INV-"):
            try:
                max_num = max(max_num, int(inv.split("-")[1]))
            except (ValueError, IndexError):
                continue
    return f"INV-{max_num + 1:04d}"

def is_number_unique(records, inventory_number):
    
    return all(
        str(rec.get("inventory_number", "")) != str(inventory_number)
        for rec in records
    )


def add_record(records, name, inventory_number):
    
    if not name or not name.strip():
        return False, 
    if not inventory_number or not inventory_number.strip():
        return False, 
    if not is_number_unique(records, inventory_number):
        return False, f"Запись с номером {inventory_number} уже существует."
    records.append({
        "name": name.strip(),
        "inventory_number": inventory_number.strip(),
    })
    
    return True, f"Запись '{name}' добавлена."

def add():

    records = select_js()

    name = input("Введите название объекта: ")
    suggested = generate_inventory_number(records)
    print(f"Предлагаемый инвентарный номер: {suggested}")

    inventory_number = input(f"Введите номер (Enter — {suggested}): ").strip() or suggested

    success, message = add_record(records, name, inventory_number)
    print(message)
    
    if success:
        save_js(records)
