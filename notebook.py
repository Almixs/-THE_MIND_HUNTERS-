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
    pass


class Record:

    def __init__(self, title: str, note, tag):
        self.title = title
        self.tag = [tag]
        self.note = [{"note": str(note), "tag": self.tag}]

    def __str__(self) -> str:

        all_notes = [x['note'] for x in self.note]
        return f'Title: {self.title}, Note: {all_notes}, Tag: {self.tag}'


class NoteBook(UserDict):

    def add_record(self, record: list):
        self.data[record.title] = record

    def delete_record(self, record):
        del self.data[record.title]

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

    title = Title(input_title)
    input_record = Record(str(title), Note(input_note), Tag(input_tag))
    notebook.add_record(input_record)
    write_file(notebook)
    return f'Нотаток усппішно створено'


def edit_note(notebook):
    titles_list = list(notebook.keys())
    print(f"Виберіть назву нотатка, текст якого треба змінити:\n{titles_list}")
    input_title = input()
    if input_title in titles_list:
        print("Введіть новий текст нотатка: ")
        input_note = input()
        for title, value in notebook.items():
            if title == input_title:
                value.note[0]['note'] = input_note
                write_file(notebook)
                return f"Текст нотатка успішно змінений"
    else:
        return f"Нотатка з назвою'{input_title}' не знайдено"


def show_all_note(notebook):
    if not notebook:
        return 'Немає жодного запису'
    record_list = notebook.iterator()
    to_show = ''
    for record in record_list:
        to_show += f'{record}'
    return to_show


def delete_note(notebook):
    titles_list = list(notebook.keys())
    print(f"Виберіть назву нотатка, який треба видалити:\n{titles_list}")
    input_title = input()
    if input_title in titles_list:
        notebook.delete_record(notebook[input_title])
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
    "delete note" Видаляє нотаток за назвою
    "exit" Вихід з застосунка
    """


COMMANDS = {
    help: ['help'],
    add_note: ['add note'],
    edit_note: ['edit note'],
    show_all_note: ['show all note'],
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
