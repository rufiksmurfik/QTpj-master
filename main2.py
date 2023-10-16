import sys
import sqlite3
import random
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout

# Функция для расчета премии на основе времени работы
def count_premia(time_worked_on_week):
    if time_worked_on_week > 40:
        return 800 * (time_worked_on_week - 40)
    if time_worked_on_week < 25:
        return 'уволен'

# Функция для расчета премии и обновления данных в базе
def count_formula(id, exit_time):
    con = sqlite3.connect("maindb.db")
    cur = con.cursor()

    cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo = list(
        cur.execute(f"SELECT * from worktime where id={id}").fetchall()[0][1:])

    time_worked_on_week += exit_time - cum_time
    worked_days += 1

    if worked_days == 5:
        print("конец недели")
        premia = count_premia(time_worked_on_week)
        if premia == "уволен":
            print("сотрудник увольняется!")
        else:
            premia_nakapalo += premia
            time_worked_on_week = 0
            worked_weeks += 1

            if worked_weeks == 4:
                print("выдайте премию и зарплату!")
                worked_weeks = 0

        worked_days = 0

    # Обновляем данные в базе
    cur.execute(f"UPDATE worktime SET cum_time = {exit_time}, time_worked_on_week = {time_worked_on_week}, "
                f"worked_days = {worked_days}, worked_weeks = {worked_weeks}, premia_nakapalo = {premia_nakapalo} "
                f"WHERE id = {id}")
    con.commit()

class MainWindow(QMainWindow):
    def except_hook(cls, exception, traceback):
        sys.excepthook(cls, exception, traceback)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Учет рабочего времени')
        self.setWindowIcon(QIcon('icon.png'))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.add_employee_button = QPushButton('Добавить сотрудника')
        self.add_employee_button.clicked.connect(self.openAddEmployeeWindow)

        self.work_time_button = QPushButton('Ввод времени работы')
        self.work_time_button.clicked.connect(self.openWorkTimeWindow)

        layout.addWidget(self.add_employee_button)
        layout.addWidget(self.work_time_button)

        central_widget.setLayout(layout)

    def openAddEmployeeWindow(self):
        self.add_employee_window = AddEmployeeWindow()
        self.add_employee_window.show()

    def openWorkTimeWindow(self):
        work_time_window.show()

class AddEmployeeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('Добавить сотрудника')

        layout = QVBoxLayout()

        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()

        self.surname_label = QLabel("Фамилия:")
        self.surname_input = QLineEdit()

        self.age_label = QLabel("Возраст:")
        self.age_input = QLineEdit()

        self.phone_label = QLabel("Номер телефона:")
        self.phone_input = QLineEdit()

        self.gender_label = QLabel("Пол:")
        self.gender_input = QLineEdit()

        self.salary_label = QLabel("Зарплата:")
        self.salary_input = QLineEdit()

        self.add_button = QPushButton("Добавить сотрудника")
        self.result_label = QLabel()

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.add_button)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_input)
        layout.addWidget(self.salary_label)
        layout.addWidget(self.salary_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.result_label)
        self.add_button.clicked.connect(self.add_employee)
        self.setLayout(layout)

    def add_employee(self):
        super().__init__()
        name = self.name_input.text()
        surname = self.surname_input.text()
        age = self.age_input.text()
        phone_number = self.phone_input.text()
        gender = self.gender_input.text()
        salary = self.salary_input.text()

        if not name or not surname or not age or not phone_number or not gender or not salary:
            self.result_label.setText("Заполните все поля.")
            self.result_label.setStyleSheet("color: red;")
            return

        if not age.isdigit() or not salary.isdigit():
            self.result_label.setText("Возраст и зарплата должны быть числами.")
            self.result_label.setStyleSheet("color: red;")
            return

        try:
            con = sqlite3.connect("maindb.db")
            cur = con.cursor()
            id = random.randint(100000, 999999)
            cur.execute("INSERT INTO main_sotrud (id, name, surname, age, phone_number, gender, salary) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)", (id, name, surname, age, phone_number, gender, salary))
            con.commit()
            self.result_label.setText("Сотрудник успешно добавлен в базу данных.")
            self.result_label.setStyleSheet("color: green;")

        except sqlite3.Error as e:
            self.result_label.setText(f"Ошибка базы данных: {e}")
            self.result_label.setStyleSheet("color: red;")
        finally:
            con.close()

class WorkTimeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Ввод времени работы')

        layout = QVBoxLayout()

        self.id_label = QLabel("ID сотрудника:")
        self.id_input = QLineEdit()

        self.time_label = QLabel("Время ухода (в формате HH:MM):")
        self.time_input = QLineEdit()

        self.calculate_button = QPushButton("Добавить в базу")
        self.result_label = QLabel()

        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)

        self.calculate_button.clicked.connect(self.calculate_premia)

        self.setLayout(layout)

    def calculate_premia(self):
        super().__init__()
        id = self.id_input.text()
        time = self.time_input.text()

        if not id.isdigit() or int(id) < 100000 or int(id) > 999999:
            self.result_label.setText("Некорректный ID сотрудника.")
            return

        def calculate_premia(self):
            id = self.id_input.text()
            time = self.time_input.text()

            if not id.isdigit() or int(id) < 100000 or int(id) > 999999:
                self.result_label.setText("Некорректный ID сотрудника.")
                return

            try:
                time_parts = time.split(":")
                exit_time = int(time_parts[0]) + int(time_parts[1]) / 60
            except ValueError:
                self.result_label.setText("Некорректное время.")
                return

            con = sqlite3.connect("maindb.db")
            cur = con.cursor()
            cur.execute(f"SELECT * from worktime where id={id}")
            result = cur.fetchall()

            if not result:
                self.result_label.setText("Сотрудник с указанным ID не найден.")
            else:
                cum_time, time_worked_on_week, worked_days, worked_weeks, premia_nakapalo = result[0][1:]
        try:
            time_parts = time.split(":")
            exit_time = int(time_parts[0]) + int(time_parts[1]) / 60
        except ValueError:
            self.result_label.setText("Некорректное время.")
            return

        count_formula(int(id), exit_time)
        self.result_label.setText("Расчет премии выполнен.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    except_hook = ''
    sys.excepthook = except_hook
    work_time_window = WorkTimeWindow()
    sys.exit(app.exec_())