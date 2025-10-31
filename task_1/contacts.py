from collections import UserDict
from datetime import datetime
from datetime import timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        
        name = name.strip()
        if not name:
            raise ValueError("name must not be empty")
        
        super().__init__(name)
    
    def __eq__(self, other):
        return isinstance(other, Name) and self.value == other.value
    
    def __repr__(self):
        return f"Name('{self.value})"

class Phone(Field):
    def __init__(self, phone):
        if not isinstance(phone, str):
            raise TypeError("phone must be a str")
        
        phone = phone.strip()
        if not all(c.isdigit() for c in phone):
            raise ValueError("phone must contain only digits")
        
        if len(phone) != 10:
            raise ValueError("phone must contain 10 digits")
        
        super().__init__(phone)
    
    def __eq__(self, other):
        return isinstance(other, Phone) and self.value == other.value
    
    def __repr__(self):
        return f"Phone('{self.value})"
    
class Birthday(Field):
    def __init__(self, value):
        if isinstance(value, datetime):
            self.value = value
            return
        
        if not isinstance(value, str):
            raise TypeError("date must be a string or datetime")

        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone = Phone(phone)
        if phone in self.phones:
            raise ValueError("phone must be unique")
        
        self.phones.append(phone)

    def remove_phone(self, phone):
        phone = Phone(phone)
        if phone not in self.phones:
            raise ValueError("phone does not exist")
        
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        old_phone = Phone(old_phone)
        if old_phone not in self.phones:
            raise ValueError("old phone does not exist")
        
        new_phone = Phone(new_phone)
        if new_phone in self.phones:
            raise ValueError("new phone must be unique")
        
        self.phones[self.phones.index(old_phone)] = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        
        return None
    
    def add_birthday(self, birthday):
        if self.birthday:
            raise ValueError("birthday already exists")
        
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("record must be a Record")
        
        if record.name.value in self.data:
            raise ValueError("record name must be unique")
        
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name not in self.data:
            raise ValueError("record does not exist")
        
        del self.data[name]

    def get_upcoming_birthdays(self):
        birthdays = []
        
        for key, value in self.data.items():
            if not value.birthday:
                continue

            today = datetime.today().date()
            next_birthday = value.birthday.value.replace(year=today.year).date()

            if next_birthday < today:
                next_birthday = next_birthday.replace(year=next_birthday.year+1)

            if (next_birthday-today).days <= 7:
                if next_birthday.weekday() == 5:
                    next_birthday += timedelta(days=2)
                elif  next_birthday.weekday() == 6:
                    next_birthday += timedelta(days=1)
                
                birthdays.append({"name": key, "date": next_birthday.strftime('%d.%m.%Y')})

        return birthdays

def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("06.11.2006")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("19.01.2006")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    print(book.get_upcoming_birthdays())

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()