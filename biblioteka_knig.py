"""
Библиотека книг, возможен поиск в каталоге по автору, названию, году;
добавление и удаление книги или автора в библиотеку
"""

import json

katalog_dict = {}  # словарь книг
frasa = str()  # переменная для ввода


def dobavlenie_udalenie(kniga, operation="add"):
    """
    Добавление/удаление книги в библитотеку
    :param kniga: str
    :param operation: str
    :return: None
    """

    global katalog_dict
    # вытаскивание автора, названия и года
    kniga = kniga.split(", ")
    if len(kniga) == 2:
        nazvanie = kniga[0]
        avtor = kniga[1]
        god = "neizv"
    else:
        nazvanie = kniga[0]
        avtor = kniga[1]
        god = kniga[2]

    with open("knigi.json", "r") as file:
        katalog_dict = json.load(file)

    if avtor in katalog_dict and god in katalog_dict[avtor]:
        # добавление названия
        if operation == "add":
            if nazvanie not in katalog_dict[avtor][god]:
                katalog_dict[avtor][god].append(nazvanie)
                print("Книга добавлена!")
            else:
                print("Книга с таким названием уже есть в списке.")

        # удаление названия
        elif operation == "del":
            if nazvanie in katalog_dict[avtor][god]:
                index = -1
                for i in range(len(katalog_dict[avtor][god])):
                    if nazvanie == katalog_dict[avtor][god][i]:
                        index = i
                if index > -1:
                    del katalog_dict[avtor][god][index]
                print("Книга удалена!")
                if len(katalog_dict[avtor][god]) == 0:
                    del katalog_dict[avtor][god]
            else:
                print("Удалять нечего! Такой книги в списке не было.")

    elif avtor in katalog_dict and god not in katalog_dict:
        # добавление года и названия
        if operation == "add":
            katalog_dict[avtor][god] = [nazvanie]
            print("Книга добавлена!")

        # удаление года
        if operation == "del":
            print("Удалять нечего! Такой книги в списке не было.")

    # добавление нового автора вместе с названием
    else:
        katalog_dict[avtor] = {god: [nazvanie]}
        print("Новый автор и книга добавлены!")

    # запись в файл
    with open("knigi.json", "w") as file:
        json.dump(katalog_dict, file)
    return None


def poisk_knigi(kniga):
    """
    Функция поиска книг в библиотеке, поддерживает возможность поиска по автору, году, названию
    :param kniga: str
    :return: None
    """
    global katalog_dict
    with open("knigi.json", "r") as file:
        katalog_dict = json.load(file)

    # вытаскивание автора, названия и года
    kniga = kniga.split(", ")

    # проверка нахождения книги в библиотеке
    if len(kniga) == 3:
        nazvanie = kniga[0]
        avtor = kniga[1]
        god = kniga[2]
        if avtor in katalog_dict and god in katalog_dict[avtor]:
            if nazvanie in katalog_dict[avtor][god]:
                print("Есть такая книга")
            else:
                print("Данного произведения этого автора в библиотеке нет")
        elif god not in katalog_dict[avtor]:
            print("В этом году данного произведения не было")
        else:
            print("Нет такого автора в библиотеке")

    elif len(kniga) == 1:
        # вывод всех произведений писателя
        if "." in kniga[0]:
            avtor = kniga[0]
            if avtor in katalog_dict:
                for god in katalog_dict[avtor]:
                    print(god)
                    for i in range(len(katalog_dict[avtor][god])):
                        print(f"{i+1}. {katalog_dict[avtor][god][i]}")
            else:
                print("Такого автора нет")

        # поиск всех произведений по году
        elif kniga[0].isdigit():
            god = kniga[0]
            for avtor in katalog_dict:
                if god in katalog_dict[avtor]:
                    print(f"{avtor} в {god} написал:")
                    for i in katalog_dict[avtor][god]:
                        print(i)
                    print()
                else:
                    print("В таком году произведений нет ни у одного автора.")

        # поиск автора и года по названию произведения
        else:
            nazvanie = kniga[0]
            avtor = None
            god = None
            for pisatel, chislo in katalog_dict.items():
                for chislo, story in katalog_dict[pisatel].items():
                    if nazvanie in katalog_dict[pisatel][chislo]:
                        avtor = pisatel
                        god = chislo
                        break
            if avtor and god is not None:
                print(f"{nazvanie}, {avtor}, {god}")
            else:
                print("Видимо, нет такого произведения в нашей библиотеке.")

    elif len(kniga) == 2:
        avtor = kniga[0]
        god = kniga[1]
        if avtor in katalog_dict and god in katalog_dict[avtor]:
            for i in katalog_dict[avtor][god]:
                print(i)
        else:
            print("В этом году автор ничего не написал.")

    else:
        print("Нет такой книги в библиотеке")

    return None


def console_vvod():
    """
    Ввод с консоли названия книг, авторов, операций
    :return: str
    """
    global frasa
    frasa = input("Ввод: ")
    return frasa


def zapusk():
    """
    Выбор и запуск программ
    :return: None
    """

    global frasa
    while True:
        print("---------")
        print("Что будем делать?\nИскать книгу: find\nДобавить или удалить: act\nВыход: ext")
        console_vvod()
        if frasa == "find":
            print("Введите название, автора и/или год:")
            console_vvod()
            poisk_knigi(frasa)
        elif frasa == "act":
            print("Введите название книги:")
            act_kn = console_vvod()
            print("Что нужно сделать, добавить (add) или удалить (del)?")
            console_vvod()
            dobavlenie_udalenie(act_kn, frasa)
        elif frasa == "ext":
            return None
        else:
            print("Введено не верно")


if __name__ == "__main__":
    # kn_a_g = "Ostrie britvi, Moem U.S., 1944"
    # op = "del"
    # dobavlenie_udalenie(kn_a_g)
    # console_vvod()
    # poisk_knigi(kn_a_g)
    zapusk()

