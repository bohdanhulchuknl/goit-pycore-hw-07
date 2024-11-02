from datetime import datetime, timedelta
from typing import List, Optional

class Field:
    pass

class Name(Field):
    def __init__(self, value: str):
        self.value = value

class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        self.value = value

class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone: str) -> None:
        """
        Додає телефонний номер до запису.

        :param phone: Телефонний номер у вигляді рядка з 10 цифр.
        """
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday: str) -> None:
        """
        Додає день народження до запису.

        :param birthday: День народження у форматі DD.MM.YYYY.
        """
        self.birthday = Birthday(birthday)

    def show_birthday(self) -> str:
        """
        Повертає день народження у форматі DD.MM.YYYY або повідомлення, якщо день народження не встановлено.

        :return: День народження або повідомлення "No birthday set."
        """
        if self.birthday:
            return self.birthday.value.strftime("%d.%m.%Y")
        return "No birthday set."

class AddressBook:
    def __init__(self):
        self.records: dict[str, Record] = {}

    def add_record(self, record: Record) -> None:
        """
        Додає запис до адресної книги.

        :param record: Об'єкт класу Record.
        """
        self.records[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """
        Знаходить запис за ім'ям.

        :param name: Ім'я контакту.
        :return: Об'єкт класу Record або None, якщо запис не знайдено.
        """
        return self.records.get(name)

    def get_upcoming_birthdays(self) -> List[str]:
        """
        Повертає список імен контактів, у яких день народження протягом наступного тижня.

        :return: Список імен контактів.
        """
        today = datetime.today()
        upcoming_birthdays = []
        for record in self.records.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if 0 <= (birthday_this_year - today).days < 7:
                    upcoming_birthdays.append(record.name.value)
        return upcoming_birthdays

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    name, = args
    record = book.find(name)
    if record:
        return record.show_birthday()
    return "Contact not found."

@input_error
def birthdays(args: List[str], book: AddressBook) -> List[str]:
    return book.get_upcoming_birthdays()

def parse_input(user_input: str) -> List[str]:
    return user_input.split()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Available commands:")
    print("-> add [ім'я] [телефон]: Додати або новий контакт з іменем та телефонним номером, або телефонний номер к ко��такту який вже існує.")
    print("-> change [ім'я] [старий телефон] [новий телефон]: Змінити телефонний номер для вказаного контакту.")
    print("-> phone [ім'я]: Показати телефонні номери для вказаного контакту.")
    print("-> all: Показати всі контакти в адресній книзі.")
    print("-> add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту.")
    print("-> show-birthday [ім'я]: Показати дату народження для вказаного контакту.")
    print("-> birthdays: Показати дні народження, які відбудуться протягом наступного тижня.")
    print("-> hello: Отримати вітання від бота.")
    print("-> close або exit: Закрити програму.")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

@input_error
def change_phone(args: List[str], book: AddressBook) -> str:
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        for phone in record.phones:
            if phone.value == old_phone:
                record.phones.remove(phone)
                record.add_phone(new_phone)
                return "Phone number updated."
        return "Old phone number not found."
    return "Contact not found."

@input_error
def show_phones(args: List[str], book: AddressBook) -> str:
    name, = args
    record = book.find(name)
    if record:
        return ", ".join(phone.value for phone in record.phones)
    return "Contact not found."

@input_error
def show_all_contacts(book: AddressBook) -> str:
    contacts = []
    for record in book.records.values():
        phones = ", ".join(phone.value for phone in record.phones)
        contacts.append(f"{record.name.value}: {phones}")
    return "\n".join(contacts)

if __name__ == "__main__":
    main()