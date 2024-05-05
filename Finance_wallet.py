import datetime
from typing import List, Optional, Union

filename = 'wallet.txt'


class Report:
    def __init__(self, date: str, category: str, amount: float, description: str):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def __str__(self):
        return f"Дата: {self.date}\nКатегория: {self.category}\nСумма: {self.amount}\nОписание: {self.description}"


class FinanceWallet:
    """
     Класс FinanceWallet представляет личный финансовый кошелек.

     Attributes:
         filename (str): Имя файла для хранения записей.
         records (List[Report]): Список записей о финансовых операциях.

     Methods:
         read_records_from_file(): Чтение записей из файла и возврат списка объектов Report.
         show_balance(): Отображение текущего баланса, суммы доходов и расходов.
         add_record(record: Report): Добавление новой записи и сохранение ее в файл.
         edit_record(index: int, new_record: Report): Редактирование существующей записи по индексу и сохранение изменений в файл.
         display_records(): Отображение списка всех записей с их индексами.
         search_records(category: Optional[str] = None, date: Optional[datetime.datetime] = None, amount: Optional[float] = None) -> List[Report]: Поиск записей по категории, дате и/или сумме.
     """

    def __init__(self, filename: str):
        self.filename = filename
        self.records = self.read_records_from_file()

    def read_records_from_file(self) -> Union[List[Report], None]:
        """
        Чтение записей из файла и возврат списка объектов Report.

        Returns:
            List[Report] or None: Список объектов Report, представляющих записи, если чтение прошло успешно,
                                  или None в случае ошибки.
        """
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                records = []
                i = 0
                while i < len(lines):
                    date_str = lines[i].strip().split(": ")[1]
                    category = lines[i + 1].strip().split(": ")[1]
                    amount = float(lines[i + 2].strip().split(": ")[1])
                    description = lines[i + 3].strip().split(": ")[1]
                    records.append(Report(date_str, category, amount, description))
                    i += 5  # Пропускаем пустую строку между записями
                return records
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден.")
            return None
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    def show_balance(self) -> None:
        """
        Отображение текущего баланса, суммы доходов и расходов.
        """
        total_income = sum(record.amount for record in self.records if record.category == "Доход")
        total_expense = sum(record.amount for record in self.records if record.category == "Расход")
        balance = total_income - total_expense
        print(f"Текущий баланс: {balance}")
        print(f"Сумма доходов: {total_income}")
        print(f"Сумма расходов: {total_expense}")

    def display_records(self) -> None:
        """Отображение списка всех записей с их индексами."""
        print("Список доходов/расходов:")
        for i, record in enumerate(self.records):
            print(f"{i + 1}. {record}")
            print()

    def add_record(self, record: Report) -> None:
        """
        Добавление новой записи и сохранение ее в файл.

        Parameters:
            record (Report): Новая запись для добавления.
        """
        try:
            with open(self.filename, 'a') as file:
                file.write(f"Дата: {record.date}\n")
                file.write(f"Категория: {record.category}\n")
                file.write(f"Сумма: {record.amount}\n")
                file.write(f"Описание: {record.description}\n\n")
            self.records.append(record)
        except Exception as e:
            print(f"Ошибка при добавлении записи в файл: {e}")

    def edit_record(self, index: int, new_record: Report) -> None:
        """
        Редактирование существующей записи по индексу и сохранение изменений в файл.

        Parameters:
            index (int): Индекс записи для редактирования.
            new_record (Report): Новая запись для замены существующей.
        """
        try:
            self.records[index] = new_record
            with open(self.filename, 'w') as file:
                for i, record in enumerate(self.records):
                    file.write(f"Дата: {record.date}\n")
                    file.write(f"Категория: {record.category}\n")
                    file.write(f"Сумма: {record.amount}\n")
                    file.write(f"Описание: {record.description}\n")
                    if i != len(self.records) - 1:
                        file.write("\n")
        except IndexError:
            print(f"Запись с индексом {index} не найдена.")
        except Exception as e:
            print(f"Ошибка при редактировании записи: {e}")

    def search_records(self,
                       category: Optional[str] = None,
                       date: Optional[datetime.datetime] = None,
                       amount: Optional[float] = None
                       ) -> List[Report]:
        """
        Поиск записей по категории, дате и/или сумме.

        Параметры:
            category (str): Категория записи.
            date (datetime.datetime): Дата записи.
            amount (float): Сумма записи.

        Возвращает:
            List[Report]: Список записей, удовлетворяющих условиям поиска.
        """
        result: List[Report] = []
        for record in self.records:
            record_date = datetime.datetime.strptime(record.date, '%Y-%m-%d')
            if (not category or record.category == category) and \
                    (not date or record_date == date) and \
                    (not amount or record.amount == amount):
                result.append(record)
            elif category and record.category != category:
                continue
        return result


if __name__ == "__main__":
    # Создание экземпляра класса FinanceWallet
    wallet = FinanceWallet('wallet.txt')

    # Пример использования методов
    wallet.show_balance()  # Отображение текущего баланса
    wallet.display_records()  # Отображение списка всех записей

