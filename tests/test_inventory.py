import inventory
from inventory import add_record, search, update_record, delete_record


# 1. Тест на успешное добавление
def test_add_record_success():
    records = []
    success, message = add_record(records, "Ноутбук", "INV-0001", "каб. 305", "рабочее", "Иванов И.И.")

    assert success is True
    assert message == "Запись 'Ноутбук' добавлена."
    assert len(records) == 1
    assert records[0] == {
        "id": "INV-0001",
        "name": "Ноутбук",
        "cabinet": "каб. 305",
        "condition": "рабочее",
        "responsible": "Иванов И.И."}


# 2. Тест на пустые поля (пустое название или пустой номер)
def test_add_record_empty_fields():
    records = []

    # Проверяем пустое название и название из одних пробелов
    res_empty_name = add_record(records, "", "INV-0001", "каб. 305", "рабочее", "Иванов И.И.")
    res_spaces_name = add_record(records, "   ", "INV-0001", "каб. 305", "рабочее", "Иванов И.И.")
    # Проверяем пустой инвентарный номер
    res_empty_number = add_record(records, "Монитор", "", "каб. 305", "рабочее", "Иванов И.И.")
    res_spaces_number = add_record(records, "Монитор", "    ", "каб. 305", "рабочее", "Иванов И.И.")
    #Проверяем пустоту заполнения кабинета
    res_empty_cabinet = add_record(records, "Монитор", "INV-0002", "", "рабочее", "Иванов И.И.")
    res_spaces_cabinet = add_record(records, "Монитор", "INV-0002", "   ", "рабочее", "Иванов И.И.")
    #Проверка пустого состояния
    res_empty_condition = add_record(records, "Монитор", "INV-0002", "каб. 305", "", "Иванов И.И.")
    res_spaces_condition = add_record(records, "Монитор", "INV-0002", "каб. 305", "   ", "Иванов И.И.")
    #Проверка заполнения ответственного
    res_empty_responsible = add_record(records, "Монитор", "INV-0002", "каб. 305", "рабочее", "")
    res_spaces_responsible = add_record(records, "Монитор", "INV-0002", "каб. 305", "рабочее", "   ")

    assert res_empty_name[0] is False
    assert res_spaces_name[0] is False
    assert res_empty_number[0] is False
    assert res_spaces_number[0] is False
    assert res_empty_cabinet[0] is False
    assert res_spaces_cabinet[0] is False
    assert res_empty_condition[0] is False
    assert res_spaces_condition[0] is False
    assert res_empty_responsible[0] is False
    assert res_spaces_responsible[0] is False
    assert len(records) == 0


# 3. Тест на повторяющийся инвентарный номер
def test_add_record_duplicate_number():
    records = [{
        "id": "INV-0001",
        "name": "Ноутбук",
        "cabinet": "каб. 305",
        "condition": "рабочее",
        "responsible": "Иванов И.И.",
    }]

    success, message = add_record(records, "Принтер", "INV-0001", "каб. 101", "рабочее", "Петров П.П.")

    assert success is False
    assert message == "Запись с номером INV-0001 уже существует."
    assert len(records) == 1

# 4. Тест поиска существующего номера
def test_search_existing_number(monkeypatch, capsys):
    # Подменяем данные, которые возвращает select_js()
    test_data = [
        {"id": "INV-0001", "name": "Ноутбук", "cabinet": "каб. 305", "condition": "рабочее", "responsible": "Иванов И.И.",},
        {"id": "INV-0002", "name": "Монитор","cabinet": "каб. 101", "condition": "рабочее", "responsible": "Петров П.П.",}
    ]
    monkeypatch.setattr(inventory, "select_js", lambda: test_data)

    # Вызываем поиск существующего номера
    search("INV-0002")

    # Перехватываем то, что функция вывела через print()
    captured = capsys.readouterr()

    assert "id : INV-0002" in captured.out
    assert "name : Монитор" in captured.out
    assert "cabinet : каб. 101" in captured.out
    assert "condition : рабочее" in captured.out
    assert "responsible : Петров П.П." in captured.out

# 5. Тест поиска отсутствующего номера
def test_search_missing_number(monkeypatch, capsys):
    test_data = [
        {"id": "INV-0001", "name": "Ноутбук", "cabinet": "каб. 305", "condition": "рабочее", "responsible": "Иванов И.И.",}
    ]
    monkeypatch.setattr(inventory, "select_js", lambda: test_data)

    # Вызываем поиск номера, которого нет
    search("INV-9999")

    captured = capsys.readouterr()

    assert "Такого инвентарный номера нет" in captured.out

# 6. Тест успешного изменения записи (все поля)
def test_update_record_success():
    records = [{
        "id": "INV-0001", "name": "Ноутбук",
        "cabinet": "каб. 305", "condition": "рабочее", "responsible": "Иванов И.И.",
    }]

    success, message = update_record(
        records, "INV-0001", "Принтер", "каб. 101", "неисправно", "Петров П.П."
    )

    assert success is True
    assert message == "Запись INV-0001 обновлена."
    assert records[0] == {
        "id": "INV-0001",
        "name": "Принтер",
        "cabinet": "каб. 101",
        "condition": "неисправно",
        "responsible": "Петров П.П.",
    }

# 7. Тест частичного изменения (пустые поля не меняются)
def test_update_record_partial():
    records = [{
        "id": "INV-0001", "name": "Ноутбук",
        "cabinet": "каб. 305", "condition": "рабочее", "responsible": "Иванов И.И.",
    }]

    # Меняем только кабинет, остальное — пустые строки
    success, message = update_record(records, "INV-0001", "", "каб. 101", "", "")

    assert success is True
    assert records[0]["name"] == "Ноутбук"
    assert records[0]["cabinet"] == "каб. 101"
    assert records[0]["condition"] == "рабочее"
    assert records[0]["responsible"] == "Иванов И.И."

# 8. Тест частичного изменения (пробелы не меняют поле)
def test_update_record_spaces():
    records = [{
        "id": "INV-0001", "name": "Ноутбук",
        "cabinet": "каб. 305", "condition": "рабочее", "responsible": "Иванов И.И.",
    }]

    success, message = update_record(records, "INV-0001", "   ", "   ", "   ", "   ")

    assert success is True
    assert records[0]["name"] == "Ноутбук"
    assert records[0]["cabinet"] == "каб. 305"
    assert records[0]["condition"] == "рабочее"
    assert records[0]["responsible"] == "Иванов И.И."

# 9. Тест изменения несуществующей записи
def test_update_record_not_found():
    records = []

    success, message = update_record(records, "INV-9999", "X", "Y", "Z", "W")

    assert success is False
    assert message == "Запись с номером INV-9999 не найдена."
    assert len(records) == 0

# 10. Тест успешного удаления
def test_delete_record_success():
    records = [{
        "id": "INV-0001", "name": "Ноутбук",
        "cabinet": "каб. 305", "condition": "рабочее", "responsible": "Иванов И.И.",
    }]

    success, message = delete_record(records, "INV-0001")

    assert success is True
    assert message == "Запись INV-0001 удалена."
    assert len(records) == 0

# 11. Тест удаления несуществующей записи
def test_delete_record_not_found():
    records = []

    success, message = delete_record(records, "INV-9999")

    assert success is False
    assert message == "Запись с номером INV-9999 не найдена."
    assert len(records) == 0


# 12. Тест: удаление не трогает другие записи
def test_delete_record_keeps_others():
    records = [
        {"id": "INV-0001", "name": "Ноутбук", "cabinet": "каб. 305", "condition": "рабочее", "responsible": "Иванов И.И."},
        {"id": "INV-0002", "name": "Монитор", "cabinet": "каб. 101", "condition": "рабочее", "responsible": "Петров П.П."},
    ]

    success, message = delete_record(records, "INV-0001")

    assert success is True
    assert len(records) == 1
    assert records[0]["id"] == "INV-0002"

# Тест 13. Отмена удаления
def test_delete_cancel(monkeypatch, capsys):
    import inventory

    test_data = [
        {"id": "INV-0001", "name": "Ноутбук", "cabinet": "каб. 305",
         "condition": "рабочее", "responsible": "Иванов И.И."}
    ]
    monkeypatch.setattr(inventory, "select_js", lambda: test_data)

    inputs = iter(["INV-0001", "n"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    saved = []
    monkeypatch.setattr(inventory, "save_js", lambda data: saved.append(data))

    inventory.delete()

    out = capsys.readouterr().out
    assert "Удаление отменено" in out
    assert len(test_data) == 1            
    assert len(saved) == 0     

# Тест 14. Подтверждение удаления
def test_delete_confirm(monkeypatch, capsys):
    import inventory

    test_data = [
        {"id": "INV-0001", "name": "Ноутбук", "cabinet": "каб. 305",
         "condition": "рабочее", "responsible": "Иванов И.И."}
    ]
    monkeypatch.setattr(inventory, "select_js", lambda: test_data)
    inputs = iter(["INV-0001", "y"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    saved = []
    monkeypatch.setattr(inventory, "save_js", lambda data: saved.append(data))

    inventory.delete()

    out = capsys.readouterr().out
    assert "Запись INV-0001 удалена." in out
    assert len(test_data) == 0           
    assert len(saved) == 1                 
   

 # Тест 15. Повторный поиск            
def test_search_repeat(monkeypatch, capsys):
    import inventory

    test_data = [
        {"id": "INV-0001", "name": "Ноутбук", "cabinet": "каб. 305",
         "condition": "рабочее", "responsible": "Иванов И.И."}
    ]
    monkeypatch.setattr(inventory, "select_js", lambda: test_data)

    # Первый поиск существующего
    inventory.search("INV-0001")
    out1 = capsys.readouterr().out
    assert "id : INV-0001" in out1

    # Повторный поиск того же  должен работать так же
    inventory.search("INV-0001")
    out2 = capsys.readouterr().out
    assert "id : INV-0001" in out2

    # Поиск отсутствующего после существующего  не «залипает»
    inventory.search("INV-9999")
    out3 = capsys.readouterr().out
    assert "номера нет" in out3

    # И снова существующего  состояние не сломалось
    inventory.search("INV-0001")
    out4 = capsys.readouterr().out
    assert "id : INV-0001" in out4    
