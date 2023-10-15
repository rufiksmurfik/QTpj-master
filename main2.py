import sys
import sqlite3

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit

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
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
        self.work_time_window = WorkTimeWindow()
        self.work_time_window.show()

class AddEmployeeWindow(QWidget):
    def __init__(self):
        super().__init()
        self.initUI()
    def initUI(self):
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('Добавить сотрудника')


class WorkTimeWindow(QWidget):
    def __init__(self):
        super().__init()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Ввод времени работы')

        layout = QVBoxLayout()

        self.id_label = QLabel("ID сотрудника:")
        self.id_input = QLineEdit()

        self.time_label = QLabel("Время ухода (в формате HH:MM):")
        self.time_input = QLineEdit()

        self.calculate_button = QPushButton("Рассчитать премию")
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

        count_formula(int(id), exit_time)
        self.result_label.setText("Расчет премии выполнен.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
