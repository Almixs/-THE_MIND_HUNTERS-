from collections import UserDict
import os
import pickle


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


class Record:

    def __init__(self, title, note, tag):
        self.title = title
        self.note = note
        self.tag = [tag]

    def __str__(self) -> str:

        return f'Title: {self.title}, Note: {self.note}, Tag: {self.tag}'


class NoteBook(UserDict):

    def add_record(self, record):
            self.data[record.title.value] = record

    def remove_record(self, title):

        if title in self.data:
            del self.data[title]

    def add_tag_to_record(self, title, new_tag):
        if title in self.data:
            record = self.data[title]
            if isinstance(new_tag, Tag):
                record.tag.append(new_tag)
            else:
                raise ValueError("new_tag должен быть объектом класса Tag")
        else:
            raise KeyError(f"Запись с ключом '{title}' не найдена в записной книжке")


    def iterator(self):
        record_list = ''
        for record in self.data.values():
            record_list += str(record) + '\n'
        return record_list


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
    
def search_note_by_text(notebook):
    print('Введіть фрагмент текста який будемо шукати: ')
    search_text = input()
    found_records = []
    for record in notebook.values():
            if search_text in str(record.title) or search_text in str(record.note):
                found_records.append(str(record))
    if found_records: 
        return f'Текст {search_text}, був знайден в наступних нотатках {[*found_records]}'
    else:
        return f'Нажаль нічого не знайдено'
    
def search_note_by_tag(notebook):
    print('Введіть тег за яким будемо шукати: ')
    search_tag = input()
    found_records = []
    for record in notebook.values():
            if search_tag in str(record.tag):
                found_records.append(str(record))
    if found_records: 
        return f'Тег {search_tag}, був знайден в наступних нотатках {[*found_records]}'
    else:
        return f'Нажаль нічого не знайдено'
    
def sort_note_by_tag(notebook):
        
        sort_record = list(notebook.values())
        sort_record.sort(key=lambda note: note.tag)
        print ('Ось що вийшло: ')
        
        return '\n'.join(map(str,  sort_record))

def show_all_note(notebook):
    if not notebook:
        return 'Немає жодного запису'
    record_list = notebook.iterator()
    to_show = ''
    for record in record_list:
        to_show += f'{record}'
    return to_show


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
    return """
    Список доступних команд:

    "help" Список доступних команд
    "add note" Створює новий нотаток (назва, текст, тег)
    "edit note" Замінює текст нотатка
    "show all note" Виводить в консоль всі записи
    "search by text" Шукає нотатки за текстом
    "search by tag" Шукає нотатки за тегом
    "sort by tag" Сортує нотатки за тегом
    "delete note" Видаляє нотаток за назвою
    "exit" Вихід з застосунка
    """


COMMANDS = {
    help: ['help'],
    add_note: ['add note'],
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
    print(notebook)
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
