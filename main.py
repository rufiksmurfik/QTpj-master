from PyQt5 import Qt, QtWidgets, uic
import sys





class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('untitled.ui', self) # Load the .ui file
        self.show() # Show the GUI


app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application

# import sqlite3
#
# con = sqlite3.connect('maindb.db')
# cursor = con.cursor()
# for i in cursor.execute("SELECT * FROM test").fetchall():
#     for j in i:
#         print(j, end=" ")
#     print()
# t = input("введите id сотрудника, которого хотите уволить")
# cursor.execute(f"DELETE FROM test WHERE id={t}")
# con.commit()
