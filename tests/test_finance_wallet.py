import datetime
import pytest
import os

from Finance_wallet import FinanceWallet, Report

@pytest.fixture
def wallet():
    filename = "test_wallet.txt"
    # Создаем пустой файл для тестов
    with open(filename, 'w'):
        pass
    return FinanceWallet(filename)

def test_add_record(wallet):
    initial_length = len(wallet.records)
    record = Report("2024-05-01", "Доход", 500.0, "Зарплата")
    wallet.add_record(record)
    assert len(wallet.records) == initial_length + 1

def test_edit_record(wallet):
    record = Report("2024-05-02", "Расход", 100.0, "Покупка продуктов")
    wallet.add_record(record)
    modified_record = Report("2024-05-02", "Расход", 150.0, "Покупка продуктов")
    wallet.edit_record(0, modified_record)
    assert wallet.records[0].amount == 150.0

def test_search_records(wallet):
    record1 = Report("2024-05-01", "Доход", 500.0, "Зарплата")
    record2 = Report("2024-05-02", "Расход", 100.0, "Покупка продуктов")
    wallet.add_record(record1)
    wallet.add_record(record2)

    # Поиск по категории "Доход"
    result = wallet.search_records(category="Доход")
    assert len(result) == 1
    assert result[0].category == "Доход"

    # Поиск по сумме
    result = wallet.search_records(amount=100.0)
    assert len(result) == 1
    assert result[0].amount == 100.0

    # Поиск по дате
    result = wallet.search_records(date=datetime.datetime(2024, 5, 1))
    assert len(result) == 1
    assert result[0].date == "2024-05-01"

# Удаление тестового файла после выполнения тестов
def teardown_module(module):
    filename = "test_wallet.txt"
    if os.path.exists(filename):
        os.remove(filename)
