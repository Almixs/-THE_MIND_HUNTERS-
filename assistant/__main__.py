from time import sleep
from itertools import zip_longest
import AddressBook as ab
import sort_folder as sf
import notebook as nb

address_book = ab.AddressBook.read_adress_book_from_file()

MAIN_MENU = {"title": "Main menu", '1': 'Address book', '2': 'Note book', '3': 'Sort folder', '4': 'Exit'}

ADDRESS_BOOK_MENU = {'title': "Address book menu", 'show all': 'Show all contacts in Book', 'add': 'Add contact to Book',
                     'find': 'Find person in Book', "show bd": "Show persons with birthday", 'edit': 'Edit personal info',
                     'del': 'Delete personal info', 'remove': 'Remove person from Book', 'return': 'Return to main menu'}


class MainMenu:
    def __init__(self, table: dict):
        self._table = table.copy()

    def print_table(self):

        wide = 30
        print("_"*(wide+2))
        print(f'|{self._table["title"]:^{wide}}|')
        print("-" * (wide + 2))
        del self._table['title']
        for key, value in self._table.items():
            print(f"|{key:^5}|    {value:20}|")
        print("-" * (wide + 2))


class MenuBook:
    def __init__(self, table: dict):
        self._table = table.copy()

    def print_table(self):
        wide = 44
        print("_" * (wide + 2))
        print(f'|{self._table["title"]:^{wide}}|')
        print("-" * (wide + 2))
        del self._table['title']
        print(f'|{"Command":^15}|{"Description":^28}|')
        print("-" * (wide + 2))
        for (key, value) in self._table.items():
            print(f"|{key:^15}|{value:^28}|")

        print("-" * (wide + 2))


def print_list_contacts(contacts: ab.Record):
    wide = 120
    print("_" * (wide + 2))
    print(f"|{'List of contact':^{wide}}|")
    print("-" * (wide + 2))
    print(f"|{'#':^5}|{'Name':^20}|{'Phones':^20}|{'email':^30}|{'Birthday':^20}|{'Address':^20}|")
    for i, val in enumerate(contacts.values(), 1):
        phones = [phone.value for phone in val.phones]
        emails = [email.value for email in val.emails]
        print("-" * (wide + 2))
        if len(phones) == 0:
            phones.append("")
        if len(emails) == 0:
            emails.append("")
        print(
            f'|{i:^5}|{val.name.value:^20}|{phones[0]:^20}|{emails[0]:^30}|{str(val.birthday.value):^20}|{val.address.value:^20}|')

        if max(len(phones), len(emails)) > 1:
            zipped = zip_longest(phones[1:], emails[1:], fillvalue="")
            for phone, email in zipped:
                print(
                    f'|{"":^5}|{"":^20}|{phone:^20}|{email:^30}|{"":^20}|{"":^20}|')
        else:
            pass
    print("-" * (wide + 2))


def run_address_book():
    address_menu = MenuBook(ADDRESS_BOOK_MENU)
    address_menu.print_table()

    while True:
        # address_menu = MenuBook(ADDRESS_BOOK_MENU)
        # address_menu.print_table()
        input_command = input("Input command of < Address Book >: ")
        if input_command not in ADDRESS_BOOK_MENU:
            print("You input incorrect command!")
            continue
        elif input_command == "edit":

            while True:
                name_edit = input("Input name to edit: ")
                if name_edit == "exit":
                    address_menu = MenuBook(ADDRESS_BOOK_MENU)
                    address_menu.print_table()
                    break
                elif name_edit not in address_book:
                    print("Input name not in Address Book. Try again or input 'exit' to return to Address book menu")
                else:
                    while True:
                        field_edit = input("Input field you want to edit (phone, email, birthday, address): ")
                        if field_edit not in ('phone', 'email', 'birthday', 'address'):
                            print("Incorrect field")

                        else:
                            break
                    if field_edit == 'phone':
                        old_phone = input("Input old phone: ")
                        new_phone = input("Input new phone: ")
                        address_book[name_edit].change_phone(old_phone, new_phone)

                    elif field_edit == 'email':
                        old_email = input("Input old email: ")
                        new_email = input("Input new email: ")
                        address_book[name_edit].change_email(old_email, new_email)

                    elif field_edit == 'birthday':
                        new_birthday = input("Input birthday: ")
                        address_book[name_edit].change_birthday(new_birthday)

                    elif field_edit == 'address':
                        new_address = input("Input address: ")
                        address_book[name_edit].change_address(new_address)
                    address_book.save_adress_book_to_file()
                    break
        elif input_command == "return":
            # run_main_menu()
            # возвращ. в головне меню
            return
        elif input_command == 'show all':
            print_list_contacts(address_book)
        elif input_command == 'add':
            new_rec = ab.Record()
            is_added = new_rec.add_name(input("Input name: "))
            while not is_added:
                print("Try again")
                is_added = new_rec.add_name(input("Input name: "))

            is_added = new_rec.add_address(input("Input address: "))
            while not is_added:
                print("Try again")
                is_added = new_rec.add_address(input("Input address: "))

            is_added = new_rec.add_phone(input("Input phone number: "))
            while not is_added:
                print("Try again")
                is_added = new_rec.add_phone(input("Input phone number: "))

            while True:
                answer = input("Would you like add another phone number (yes/no)?: ")
                if answer == "yes":
                    is_added = new_rec.add_phone(input("Input phone number: "))
                    while not is_added:
                        print("Try again")
                        is_added = new_rec.add_phone(input("Input phone number: "))
                    continue
                elif answer == "no":
                    break
                else:
                    print('Incorrect answer. Must be (yes/no).')
                    continue
            is_added = new_rec.add_email(input("Input email: "))
            while not is_added:
                print("Try again")
                is_added = new_rec.add_email(input("Input email: "))

            while True:
                answer = input("Would you like add another email (yes/no)?: ")
                if answer == "yes":
                    is_added = new_rec.add_email(input("Input email: "))
                    while not is_added:
                        print("Try again")
                        is_added = new_rec.add_email(input("Input email: "))
                    continue
                elif answer == "no":
                    break
                else:
                    print('Incorrect answer. Must be (yes/no).')
                    continue

            is_added = new_rec.add_birthday(input("Input birthday(Y-M-D): "))
            while not is_added:
                print("Try again")
                is_added = new_rec.add_birthday(input("Input birthday(Y-M-D): "))

            address_book.add_record(new_rec)
            print("Contact successfully added")
        elif input_command == 'find':
            name = input("Input name to search person: ")
            result = address_book.find_person(name)
            if result:
                print_list_contacts(result)
            else:
                print("There is no such contact that you are looking for.")
        elif input_command == 'show bd':
            num_days = int(input("Input number of days: "))
            result = address_book.show_list_birthday(num_days)
            if result:
                wide = 49
                print("-"*wide)
                print(f"|{'#':^5}|{'Name':^20}|{'Birthday':^20}|")
                print("-"*wide)
                for i, person in enumerate(result, 1):
                    print(f"|{i:^5}|{person:^20}|{result[person]:^20}|")
                    print("-" * wide)
            else:
                print("<< No results >>")
        elif input_command == "del":
            while True:
                name_edit = input("Input name to del info or exit: ")
                if name_edit == "exit":
                    address_menu = MenuBook(ADDRESS_BOOK_MENU)
                    address_menu.print_table()
                    break
                if name_edit not in address_book:
                    print("Input name not in Address Book. Try again or input 'exit' to return to Address book menu")
                else:
                    while True:
                        field_del = input("Input field you want to delete (phone, email, birthday, address): ")
                        if field_del not in ('phone', 'email', 'birthday', 'address'):
                            print("<Incorrect field!!!>")
                            continue
                        else:
                            break
                    if field_del == 'phone':
                        phone_del = input("Input phone you want to delete: ")
                        address_book[name_edit].remove_phone(phone_del)
                    elif field_del == 'email':
                        email_del = input("Input email you want to delete: ")
                        address_book[name_edit].remove_email(email_del)
                    elif field_del == 'birthday':
                        address_book[name_edit].remove_birthday()
                    elif field_del == 'address':
                        address_book[name_edit].remove_address()
                    address_book.save_adress_book_to_file()
                    break

        elif input_command == "remove":
            while True:
                name_remove = input("Input name to remove from Book: ")
                if name_remove == "exit":
                    address_menu = MenuBook(ADDRESS_BOOK_MENU)
                    address_menu.print_table()
                    break
                if name_remove not in address_book:
                    print("Input name not in Address Book. Try again or input 'exit' to return to Address book menu")
                else:

                    while True:
                        confirmation = input("Are you sure?(yes/no): ")
                        if confirmation == "yes":
                            address_book.remove_record(name_remove)
                            address_book.save_adress_book_to_file()
                            print(f"<< {name_remove} was removed from Book >>")
                            break
                        elif confirmation == "no":
                            break
                        else:
                            print("Input 'yes' or 'no'")
                            continue
                    break

def run_note_book():
    nb.main()
    sleep(1)


def run_sort_folder():
    folder = input("Input folder to sort: ")
    result = sf.sort_folder(folder)
    if result:
        print("<< Sorting completed >>")
    else:
        print("<< Folder does not exist >>")
    sleep(1)


def run_main_menu():
    while True:
        main_menu = MainMenu(MAIN_MENU)
        main_menu.print_table()
        num_input = input("Enter number 1-4: ")
        input_command = MAIN_MENU.get(num_input)
        if input_command == 'Address book':
            run_address_book()
        elif input_command == 'Note book':
            run_note_book()
        elif input_command == 'Sort folder':
            run_sort_folder()
        elif input_command == 'Exit':
            print("<< Good Buy! >>")
            exit()
        else:
            print(f"<< Incorrect number! Must be 1 - 4 >>")
            sleep(0.7)


if __name__ == "__main__":
    run_main_menu()
