import pymongo
from pymongo import MongoClient

# -----------------------------------Cоединение с базой данных-----------------------------------#
cluster = MongoClient("localhost", 27017)

db = cluster["volonters"]

collection = db["users"]
collection2 = db["reviews"]

# -------------------------Работа с запросами к БД по выбору пользователя-------------------------#

flag_cycle = 0

while flag_cycle != 1:
    print("Выберите запрос, который хотите выполнить:\n")
    print("1.Вывести одного выбранного пользователя и его отзыв")
    print("2.Вывести N пользователей или отзывов")
    print("3.Добавить нового пользователя.")
    print("4.Изменить отзыв.")
    print("5.Удалить пользователя")
    choice_querry = input("\n\nВаш выбор: ")

    if choice_querry == "1":
        name = input("\n\nВведите ФИО пользователя: ")
        user = collection.find_one({
            "full_name": name
        })
        user1 = collection2.find_one({
            "visitors": name
        })
        print("Результат запроса:\n", user, "\n", user1)

    elif choice_querry == "2":
        print("1) Вывести пользователей")
        print("2) Вывести новости")
        choice_vivod = input("\n\nВаш выбор: ")

        if choice_vivod == "1":
            N = int(input("\n\nВведите кол-во пользователей: "))
            users = collection.find().limit(N)
            for user in users:
                print(user)

        if choice_vivod == "2":
            K = int(input("\n\nВведите кол-во новостей: "))
            reviews = collection2.find({"rating": {"$gt": 0}}).limit(K)
            for review in reviews:
                print(review)

    # добавление
    elif choice_querry == "3":
        FIO = input("\n\nВведите ФИО пользователя: ")
        email = input("\nВведите эл. почту: ")
        phone_number = input("\nВведите номер телефона: ")
        password = input("\nВведите пароль: ")
        print("\nВыберите роль пользователя:")
        print("1) администратор")
        print("2) волонтер")
        print("3) посетитель")
        choice_role = input("Ваш выбор: ")
        if choice_role == "1":
            role = "администратор"
        if choice_role == "2":
            role = "волонтер"
        if choice_role == "3":
            role = "посетитель"

        collection.insert_one({
            "full_name": FIO,
            "email": email,
            "phone_number": phone_number,
            "password": password,
            "roles": {"title": role}
        })

    # редактирование
    elif choice_querry == "4":
        id = input("\n\nВведите ФИО пользователя, чей отзыв хотите заменить: ")
        rev = collection2.find_one({  # Ввывод отзыва
            "visitors": id
        })
        print("Отзыв, который хотите изменить: ", rev)
        rating = int(input("Введите рейтинг: "))
        info = input("Введите отзыв: ")

        collection2.update_one(
            {"visitors": id},
            {
                "$set": {
                    "rating": rating,
                    "info": info}
            }
        )

     # удаление
    elif choice_querry == "5":
        FIO = input("\n\nВведите ФИО пользователя: ")
        collection.delete_many({
            "full_name": FIO
        })

    else:
        print("Вы ввели что-то другое...\n")

    answer = input(
        "\n\nХотите продолжить работу с запросами(1 - да, 2 - нет)? ")
    if answer == "1":
        flag_cycle = 0

    elif answer != "1":
        print("Вы ответили нет.\n")
        flag_cycle = 1
