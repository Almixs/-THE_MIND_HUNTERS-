from collections import UserDict
import os
import pickle
from prettytable import PrettyTable

# код визначає клас під назвою Field який інкапсулює значення,
# і надає методи для отримання та встановлення цього значення. 
# Клас також забезпечує рядкове представлення значення.
class Field:

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Title(Field):
    pass


class Note(Field):
    pass


class Tag(Field):
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value

# код визначає клас, який представляє запис із заголовком, приміткою та тегом. 
# Метод __str__ дозволяє легко друкувати об’єкт запису.
class Record:

    def __init__(self, title, note, tag):
        self.title = title
        self.note = note
        self.tag = [tag]

    def __str__(self) -> str:

        return f'Title: {self.title}, Note: {self.note}, Tag: {self.tag}'

#Цей код визначає клас NoteBook, який успадковує клас UserDict.
class NoteBook(UserDict):
    #Метод add_record приймає параметр запису та додає його до атрибута data об’єкта NoteBook
    def add_record(self, record):
            self.data[record.title.value] = record
    # Метод remove_record приймає параметр title і видаляє запис із цим заголовком зі словника даних, якщо він існує.
    def remove_record(self, title):

        if title in self.data:
            del self.data[title]
    # Метод add_tag_to_record приймає параметр title і new_tag та додає new_tag до атрибута тегу запису
    def add_tag_to_record(self, title, new_tag):
        if title in self.data:
            record = self.data[title]
            if isinstance(new_tag, Tag):
                record.tag.append(new_tag)
            else:
                raise ValueError("new_tag должен быть объектом класса Tag")
        else:
            raise KeyError(f"Запись с ключом '{title}' не найдена в записной книжке")


file_name = 'NoteBook.bin'
file_path = os.path.expanduser("~\Documents")


def write_file(self, file_name=rf"{file_path}\NoteBook.bin"):
    with open(file_name, "wb") as file:
        pickle.dump(self, file)


def read_file(file_name=rf"{file_path}\NoteBook.bin"):
    try:
        with open(file_name, "rb") as file:
            data = pickle.load(file)
            return data
    except (EOFError, FileNotFoundError):
        data = NoteBook()
        return data


def add_note(notebook):
    input_title = input("Введіть назву нотатка: ")
    while input_title == "":
        input_title = input(
            "Нотаток повинен бути з назвою, ведіть будь ласка назву: ")

    input_note = input("Введіть текст нотатка: ")
    while input_note == "":
        input_note = input(
            "Нотаток не має бути пустим, ведіть будь ласка текст: ")

    input_tag = input("Введіть тег(ключове слово) до нотатка: ")
    while input_tag == "":
        input_tag = input("Введіть хочаб один тег: ")

    input_record = Record(Title(input_title), Note(input_note), Tag(input_tag))
    notebook.add_record(input_record)
    write_file(notebook)
    return f'Нотаток успішно створено'


def edit_note(notebook):
    titles_list = list(map(str, (notebook.keys())))
    print(f"Виберіть назву нотатка, текст якого треба змінити:\n{titles_list}")
    input_title = input()
    if input_title in titles_list:
        print("Введіть новий текст нотатка: ")
        input_note = input()
        for title, value in notebook.items():
            if str(title) == input_title:
                value.note = input_note
                write_file(notebook)
                return f"Текст нотатка успішно змінений"
    else:
        return f"Нотатка з назвою'{input_title}' не знайдено"
    
def add_tag(notebook):
    titles_list = list(map(str, (notebook.keys())))
    print(f"Виберіть назву нотатка, в який треба додати тег:\n{titles_list}")
    input_title = input()

    if input_title in titles_list:
        print('Введіть новий тег: ')
        new_tag = Tag(input())
        notebook.add_tag_to_record(input_title, new_tag)
        write_file(notebook)
        return f"Тег'{new_tag}' був додан"
    
def delete_tag_from_note(notebook):
    titles_list = list(map(str, (notebook.keys())))
    print(f"Виберіть назву нотатка, з якого треба видалити тег:\n{titles_list}")
    input_title = input()
    if input_title in notebook:
        note = notebook[input_title]
        if note.tag:
            print("Введіть тег, який потрібно видалити:")
            input_tag = input()
            for tag in note.tag:
                if tag.value == input_tag:
                    note.tag.remove(tag)
                    write_file(notebook)
                    return f"Тег '{input_tag}' видалено з нотатка '{input_title}'"
            return f"Тег '{input_tag}' не знайдено в нотатку '{input_title}'"
        else:
            return f"Нотаток '{input_title}' не має тегів"
    else:
        return f"Нотаток з назвою '{input_title}' не знайдено"
    

def search_note_by_text(notebook):
    print('Введіть фрагмент текста який будемо шукати: ')
    search_text = input()
    found_records = []

    table = PrettyTable()
    table.field_names = ["Title", "Note", "Tags"]

    for record in notebook.values():
        if search_text in str(record.title) or search_text in str(record.note):
            found_records.append(record)
    
    if found_records:
        for record in found_records:
            print(f'Текст {search_text}, був знайден в наступних нотатках:')
            table.add_row([record.title.value, record.note.value, ", ".join(tag.value for tag in record.tag)])
        return str(table)
    else:
        return f'Нажаль нічого не знайдено'
    
def search_note_by_tag(notebook):
    print('Введіть тег за яким будемо шукати: ')
    search_tag = input()
    found_records = []
    table = PrettyTable()
    table.field_names = ["Title", "Note", "Tags"]
    for record in notebook.values():
            if search_tag in str(record.tag):
                found_records.append(record)
    if found_records:
        print(f'Тег {search_tag}, був знайден в наступних нотатках:') 
        for record in found_records:
            table.add_row([record.title.value, record.note.value, ", ".join(tag.value for tag in record.tag)])
            return str(table)
        
    else:
        return f'Нажаль нічого не знайдено'
    


def sort_note_by_tag(notebook):
    sorted_records = list(notebook.values())
    sorted_records.sort(key=lambda note: [tag.value for tag in note.tag])

    if not sorted_records:
        return 'Немає жодних записів'

    table = PrettyTable()
    table.field_names = ["Title", "Note", "Tags"]

    for record in sorted_records:
        table.add_row([record.title.value, record.note.value, ", ".join(tag.value for tag in record.tag)])

    return str(table)

def show_all_note(notebook):

    if not notebook:
        return 'Немає жодного запису'
    
    table = PrettyTable()
    table.field_names = ["Title", "Note", "Tags"]

    for record in notebook.values():
        table.add_row([record.title.value, record.note.value, ", ".join(tag.value for tag in record.tag)])

    return str(table)


def delete_note(notebook):
    titles_list = list(map(str, (notebook.keys())))
    print(f"Виберіть назву нотатка, який треба видалити:\n{titles_list}")
    input_title = input()
    if input_title in titles_list:
        notebook.remove_record(input_title)
        write_file(notebook)
        return f"Нотаток з назвою'{input_title}' був видален"
    else:
        return f"Нотаток з назвою'{input_title}' нажаль не знайдено"


def exit(notebook):
    write_file(notebook)
    return 'До побачення'


def unknown_command(*args):
    return 'Я не знаю такої команди, спробуйте ще раз!'


def help(*args):
    return r"""
    Вас вітає розумний записник!
    +---------------------------------------------------------+
    |               Список доступних команд:                  |
    +---------------------------------------------------------+
    |"help" Список доступних команд                           |
    +---------------------------------------------------------+
    |"add note" Створює новий нотаток (назва, текст, тег)     |
    +---------------------------------------------------------+
    |"add tag" Додає новий тег до нотатка                     |
    +---------------------------------------------------------+                  
    |"delete tag" Видаляє вказаний тег з нотатка              |
    +---------------------------------------------------------+
    |"edit note" Замінює текст нотатка                        |
    +---------------------------------------------------------+
    |"show all note" Виводить в консоль всі записи            |
    +---------------------------------------------------------+
    |"search by text" Шукає нотатки за текстом                |
    +---------------------------------------------------------+
    |"search by tag" Шукає нотатки за тегом                   |
    +---------------------------------------------------------+
    |"sort by tag" Сортує нотатки за тегом                    |
    +---------------------------------------------------------+
    |"delete note" Видаляє нотаток за назвою                  |
    +---------------------------------------------------------+
    |"exit" Вихід з застосунка                                |
    +---------------------------------------------------------+
    """


COMMANDS = {
    help: ['help'],
    add_note: ['add note'],
    add_tag: ['add tag'],
    delete_tag_from_note: ['delete tag'],
    edit_note: ['edit note'],
    show_all_note: ['show all note'],
    search_note_by_text: ['search by text'],
    search_note_by_tag: ['search by tag'],
    sort_note_by_tag: ['sort by tag'],
    delete_note: ['delete note'],
    exit: ['exit']
}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def main():
    notebook = read_file()
    print(help())
    while True:
        user_command = input("Введіть команду: ")
        if user_command == "exit":
            return f"Вихід"
        command, data = command_parser(user_command)
        print(command(notebook))

        if command is exit:
            break


if __name__ == "__main__":
    main()
