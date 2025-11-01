from contacts import AddressBook, Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except KeyError as e:
            return f"Error: {e}"
        except IndexError:
            return "Give me correct number of arguments please."
        except TypeError as e:
            return f"Error: {e}"

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Incorrect number of arguments. Expected at least 2: name and phone.")
    
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
def change_contact(args, book: AddressBook):
    if len(args) != 3:
        raise ValueError(f"Incorrect number of arguments: {len(args)}. Expected 3: name, old phone, new phone.")

    name, old_phone, new_phone = args
    record = book.find(name)
    
    if record is None:
        raise KeyError(f"Contact with name '{name}' does not exist.")
    
    record.edit_phone(old_phone, new_phone)
    return "Contact changed."

@input_error
def phone_contact(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError(f"Incorrect number of arguments: {len(args)}. Expected 1: name.")

    name = args[0]
    record = book.find(name)
    
    if record is None:
        raise KeyError(f"Contact with name '{name}' does not exist.")
    
    if not record.phones:
        return f"Contact '{name}' has no phone numbers."
    
    return f"{name}: {'; '.join(p.value for p in record.phones)}"

@input_error
def all_contacts(args, book: AddressBook):
    if not book.data:
        return "No contacts."
    
    result = []
    for record in book.data.values():
        result.append(str(record))
    
    return "\n".join(result)

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError(f"Incorrect number of arguments: {len(args)}. Expected 2: name and birthday (DD.MM.YYYY).")
    
    name, birthday = args
    record = book.find(name)
    
    if record is None:
        raise KeyError(f"Contact with name '{name}' does not exist.")
    
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError(f"Incorrect number of arguments: {len(args)}. Expected 1: name.")
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        raise KeyError(f"Contact with name '{name}' does not exist.")
    
    if record.birthday is None:
        return f"Contact '{name}' has no birthday set."
    
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    
    if not upcoming:
        return "No upcoming birthdays in the next week."
    
    result = []
    for item in upcoming:
        result.append(f"{item['name']}: {item['date']}")
    
    return "\n".join(result)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
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
            print(change_contact(args, book))

        elif command == "phone":
            print(phone_contact(args, book))

        elif command == "all":
            print(all_contacts(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()