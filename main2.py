import sqlite3
import uuid
import random


def count_premia(time_worked_on_week):
    if time_worked_on_week > 40:
        return 800 * (time_worked_on_week - 40)

    if time_worked_on_week < 25:
        return 'уволен'
def count_formula(id):
    cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo = list(
        cur.execute(f"SELECT * from worktime where id={id}").fetchall()[0][1:])
    exit_time = time_to_float(input("введите время ухода"))
    time_worked_on_week += exit_time - cum_time
    worked_days += 1
    if worked_days == 5:
        print("канец нидили")
        prem = count_premia(time_worked_on_week)
        if prem == "уволен":
            print("сотрудник увольняется! увольте вручную")
        else:
            premia_nakapalo += prem
            time_worked_on_week = 0

            worked_weeks += 1
            if worked_weeks == 4:
                print("выдайте премию и зарплату!")
                worked_weeks = 0
        worked_days = 0
    return ", ".join(list(map(str, [cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo])))


import sqlite3

def add_employee(id, name, surname, age, phone_number,gender, salary):
    try:
        con = sqlite3.connect("maindb.db")
        cur = con.cursor()
        cur.execute("INSERT INTO main_sotrud (id, name, surname, age, phone_number, gender, salary) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, name, surname, age, phone_number, gender, salary))
        con.commit()
        print("Сотрудник успешно добавлен в базу данных.")
        print(f"ID добавленного сотрудника: {id}")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        con.close()


def time_to_float(time):
    time = time.split(":")
    return int(time[0]) + int(time[1]) / 60



con = sqlite3.connect("maindb.db")
cur = con.cursor()
for i in cur.execute("SELECT id, name, surname, salary from main_sotrud"):
    for j in i:
        print(j, end=" ")
    print()
while True:
    deyst = int(input("1 - сотрудник пришел, 2 - сотрудник ушел, 3 - добавить рабочего \n"))
    if deyst == 1:
        id = input("введите id сотрудника: ")
        if id.isdigit() == False:
            raise Exception("ID cant be text")
        if int(id) > 999999 or int(id) < 100000:
            raise Exception("ID не может быть больше 999999 и меньше 100000")

        try:
            needed_values = ", ".join(list(map(str, list(cur.execute(f"SELECT time_worked_on_week, worked_days, worked_weeks, premia_nakapalo from worktime where id={id}").fetchall()[0]))))
        except IndexError:
            needed_values = "0, 0, 0, 0"
        cur.execute(f"INSERT OR REPLACE into worktime (id, cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo) VALUES ({id}, {str(time_to_float(input('введите время')))}, {needed_values})")
        con.commit()
    if deyst == 2:
        id = input("введите id: ")
        if id.isdigit() == False:
            raise ValueError("ID cant be text")
        if int(id) > 999999 or int(id) < 100000:
            raise Exception("ID не может быть больше 999999 и меньше 100000")
        cur.execute(f"INSERT OR REPLACE into worktime (id, cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo) VALUES ({id}, {count_formula(id)})")
        con.commit()

    if deyst == 3:
        id = random.randint(100000, 999999)
        name = input("Имя: ")
        surname = input("Фамилия: ")
        age = input("Сколько лет: ")
        phone_number = input("Номер телефона: ")
        gender = input("Пол: Мужской, Женский \n")
        salary = input("Зарплата: ")
        if salary.isdigit() == False:
            raise Exception('Введите число')
        add_employee(id, name, surname, age, phone_number,gender, salary)

