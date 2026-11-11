from inventory import add_record


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

