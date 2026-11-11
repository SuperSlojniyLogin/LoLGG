import inventory
from inventory import add_record, search


# 1. Тест на успешное добавление
def test_add_record_success():
    records = []
    success, message = add_record(records, "Ноутбук", "INV-0001")

    assert success is True
    assert message == "Запись 'Ноутбук' добавлена."
    assert len(records) == 1
    assert records[0] == { "id": "INV-0001", "name": "Ноутбук"}


# 2. Тест на пустые поля (пустое название или пустой номер)
def test_add_record_empty_fields():
    records = []

    # Проверяем пустое название и название из одних пробелов
    res_empty_name = add_record(records, "", "INV-0001")
    res_spaces_name = add_record(records, "   ", "INV-0001")
    # Проверяем пустой инвентарный номер
    res_empty_number = add_record(records, "Монитор", "")

    assert res_empty_name[0] is False
    assert res_spaces_name[0] is False
    assert res_empty_number[0] is False
    assert len(records) == 0


# 3. Тест на повторяющийся инвентарный номер
def test_add_record_duplicate_number():
    records = [{ "id": "INV-0001", "name": "Ноутбук"}]

    success, message = add_record(records, "Принтер", "INV-0001")

    assert success is False
    assert message == "Запись с номером INV-0001 уже существует."
    assert len(records) == 1

# 4. Тест поиска существующего номера
def test_search_existing_number(monkeypatch, capsys):
    # Подменяем данные, которые возвращает select_js()
    test_data = [
        {"id": "INV-0001", "name": "Ноутбук"},
        {"id": "INV-0002", "name": "Монитор"}
    ]
    monkeypatch.setattr(inventory, "select_js", lambda: test_data)

    # Вызываем поиск существующего номера
    search("INV-0002")

    # Перехватываем то, что функция вывела через print()
    captured = capsys.readouterr()

    assert "id : INV-0002" in captured.out
    assert "name : Монитор" in captured.out


# 5. Тест поиска отсутствующего номера
def test_search_missing_number(monkeypatch, capsys):
    test_data = [
        {"id": "INV-0001", "name": "Ноутбук"}
    ]
    monkeypatch.setattr(inventory, "select_js", lambda: test_data)

    # Вызываем поиск номера, которого нет
    search("INV-9999")

    captured = capsys.readouterr()

    assert "Такого инвентарный номера нет" in captured.out

