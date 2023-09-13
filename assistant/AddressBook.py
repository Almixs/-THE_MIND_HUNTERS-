from collections import UserDict
from datetime import datetime, timedelta
import re
import pickle
import os

filepath = os.path.expanduser("~\Documents")


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    @Field.value.setter
    def value(self, value):
        if re.search(r"[а-яa-zА-ЯA-Z']{2,}[\w-]+", value):
            self._value = value.title()
        else:
            raise ValueError('Wrong name. Please enter correct name')


class Address(Field):
    @Field.value.setter
    def value(self, new_value: str):

        if re.search(r',', new_value) and re.search(r'\b[a-zA-Z]+\,[a-zA-Z]+ [0-9]+\b', new_value):
            self._value = new_value

        else:
            raise ValueError('Wrong address.')


class Phone(Field):
    @Field.value.setter
    def value(self, new_value: str):
        if re.search(r'\+?\b[\d]{3} [\d]{2} [\d]{3}-[\d]{2}-[\d]{2}\b', new_value):
            self._value = new_value
        else:
            raise ValueError('Wrong format of phone.')


class Email(Field):
    @Field.value.setter
    def value(self, new_value: str):
        if re.search(r'\b([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+\b', new_value):
            self._value = new_value
        else:
            raise ValueError(f'Email: {new_value} wrong format.\n')


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value: str):
        try:
            birthday_data = datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            raise ValueError('Wrong format.')

        if birthday_data <= datetime.now():
            self._value = birthday_data.date()
        else:
            # 'Date of birthday in the future
            raise ValueError


class Record:
    def __init__(self):
        self.name = None
        self.phones = []
        self.birthday = None
        self.emails = []
        self.address = None

    def add_name(self, name: str):
        if name:
            self.name = Name(name)
            print(f"{self.name.value} was successfully added")
            return True
        else:
            print("No name was given.")
            return False

    def add_address(self, address: str):
        if address:
            try:
                self.address = Address(address)
                print(f"{self.address.value} was successfully added")
                return True
            except ValueError:
                print("Wrong format of adress. Example: \"City,street number\"")
                return False
        else:
            # print(f'No address was given.')
            return f'No address was given.'

    def add_phone(self, phone: str):
        try:
            phone = Phone(phone)
        except ValueError:
            print(f'{phone} - Wrong format of phone. Please enter correct phone number. Example: +xxx xx xxx-xx-xx')
            return False

        for phone_sub in self.phones:
            if phone.value == phone_sub.value:
                print(f"{phone.value} already exists.")
                return False

        print(f'{phone.value} successfully added')
        self.phones.append(phone)
        return True

    def add_email(self, email: str):
        if email:
            try:
                email = Email(email)
            except ValueError:
                print(f"Wrong format of \'{email}\'. Example: \"xxxx@xxxx.xxxx or xxxx.xxxx@xxxx.xxxx\"")
                return False

        for email_sub in self.emails:
            if email.value == email_sub.value:
                print(f'\'{email.value}\' already exists.')
                return False

        print(f'{email.value} successfully added')
        self.emails.append(email)
        return True

    def add_birthday(self, birthday: str):
        if not self.birthday:
            try:
                self.birthday = Birthday(birthday)
                print(f"{self.birthday.value} was successfully added")
                return True
            except ValueError:
                print(f"Wrong format of {birthday} (Example: yyyy-mm-dd) or Date of birthday in the future")
                return False

        else:
            print("No birthday was given.")
            return False

    def change_name(self, new_name: str):
        if new_name:
            self.name = Name(new_name)
            print(f"{self.name.value} was successfully changed")
            return True
        else:
            print("No name was given.")
            return False

    def change_address(self, new_address: str):
        if new_address:
            try:
                self.address = Address(new_address)
                print(f"{self.address.value} was successfully changed")
                return True
            except ValueError:
                print("Wrong format of adress. Example: \"City,street number\"")
                return False

        else:
            print(f'No address was given.')
            return False

    def change_birthday(self, new_birthday: str):
        if self.birthday:
            try:
                self.birthday = Birthday(new_birthday)
                print(f"{self.birthday.value} was successfully changed")
                return True
            except ValueError:
                print(f"Wrong format of {new_birthday}. Example: yyyy-mm-dd.")
                return False

    def change_phone(self, old_phone: str, new_phone: str):
        flag_1 = False
        for index, phone in enumerate(self.phones, start=0):
            if old_phone == phone.value:
                flag_1 = True
                flag_2 = False
                for phone_sub in self.phones:
                    if new_phone == phone_sub.value:
                        print(f"There is already exists phone {new_phone}")
                        return False
                    flag_2 = True
                if flag_2 == True:
                    index_of_old_phone = index
                    try:
                        self.phones[index_of_old_phone] = Phone(new_phone)
                        print(f'{phone.value} successfully changed to {new_phone}')
                        return True
                    except ValueError:
                        print(
                            f'{new_phone} - Wrong format of phone. Please enter correct phone number. Example: +xxx xx xxx-xx-xx')
                        return False

        if flag_1 == False:
            print("There is no phone that you wrote to change.")
            return False

    def change_email(self, old_email: str, new_email: str):
        flag_1 = False
        for index, email in enumerate(self.emails, start=0):
            if old_email == email.value:
                flag_1 = True
                flag_2 = False
                for email_sub in self.emails:
                    if new_email == email_sub.value:
                        print(f"There is already exists email {new_email}")
                        return False
                    flag_2 = True
                if flag_2 == True:
                    index_of_old_email = index
                    try:
                        self.emails[index_of_old_email] = Email(new_email)
                        print(f'{email.value} successfully changed to {new_email}')
                        return True
                    except ValueError:
                        print(f"Wrong format of \'{new_email}\'. Example: \"xxxx@xxxx.xxxx or xxxx.xxxx@xxxx.xxxx\"")
                        return False

        if flag_1 == False:
            print("There is no email that you wrote to change.")
            return False

    def remove_address(self):
        if self.address:
            print(f'Address {self.address.value} was deleted')
            self.address._value = ""
            return True
        return False

    def remove_birthday(self):
        if self.birthday:
            print(f'Birthday {self.birthday.value} was deleted')
            self.birthday._value = ""
            return True
        return False

    def remove_phone(self, phone_to_remove: str):
        for phone in self.phones:
            if phone.value == phone_to_remove:
                self.phones.remove(phone)
                print(f'Phone {phone.value} was deleted')
                return True
        print(f'There is no such phone')
        return False

    def remove_email(self, email_to_remove: str):
        for email in self.emails:
            if email.value == email_to_remove:
                self.emails.remove(email)
                print(f'Email {email_to_remove} was deleted')
                return True

        print(f'There is no such email')
        return False


class AddressBook(UserDict):
    # filepath = os.path.expanduser("~\Documents")

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record
        self.save_adress_book_to_file()

    def save_adress_book_to_file(self, filename=f"{filepath}\AddressBook.bin"):
        with open(filename, "wb") as fh:
            pickle.dump(self.data, fh)

    @classmethod
    def read_adress_book_from_file(cls, filename=f"{filepath}\AddressBook.bin"):
        try:
            with open(filename, "rb") as fh:
                load_dict = pickle.load(fh)
                return cls(load_dict)
        except FileNotFoundError:
            return cls()

    def show_list_birthday(self, number):

        dict_with_name_and_birthday = {}

        c_d = datetime.now()

        days = timedelta(days=number)
        for person in self.data:
            try:
                birthday_data_str = self.data[person].birthday.value.strftime("%Y-%m-%d")  # type: str
                user_date_of_birth = datetime.strptime(birthday_data_str, '%Y-%m-%d').date()  # type: datetime
                main_date = c_d.date() + days
                if main_date.day == user_date_of_birth.day and main_date.month == user_date_of_birth.month:
                    dict_with_name_and_birthday[person] = birthday_data_str
            except AttributeError:
                pass

        return dict_with_name_and_birthday

    def find_person(self, name: str):
        if name == "":
            print("You typed empty.")
            return False

        dict = {}
        for person in self.data:
            if name in person:
                dict[person] = self.data[person]
        if len(dict) == 0:
            # print("There is no such contact that you are looking for.")
            return False
        # print(dict)
        return dict

    def remove_record(self, name: str):
        del self.data[name]
