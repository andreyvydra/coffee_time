import sqlite3
import sys

from PyQt5 import uic
from ui_main import Ui_MainWindow
from ui_addEditCoffeeForm import Ui_Dialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog


class TableWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('data/coffee.db')
        self.cur = self.con.cursor()
        self.load_data()
        self.dialog = AddDialog()
        self.dialog.accepted.connect(self.add_item)
        self.pushButton.clicked.connect(self.run_dialog)

    def run_dialog(self):
        self.dialog.exec()

    def add_item(self):
        res = self.dialog.get_info()

        self.cur.execute('INSERT INTO coffee(name, roast,' +
                         'is_ground, desc,' +
                         f"price, volume) VALUES('{res[0]}', " +
                         f"{res[1]}, '{res[2]}', '{res[3]}', {res[4]}," +
                         f'{res[5]})').fetchall()
        self.con.commit()

        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        for j, elem in enumerate(res):
            print(self.tableWidget.rowCount())
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, j, QTableWidgetItem(str(elem)))

    def load_data(self):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['Название сорта',
                                                    'Степень обжарки',
                                                    'Молотый/в зернах',
                                                    'Описание вкуса',
                                                    'Цена', 'Объем упаковки'])
        self.tableWidget.setRowCount(0)
        data = self.cur.execute('SELECT * From coffee').fetchall()
        for i, item in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(item[1:]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


class AddDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def get_info(self):
        name = self.lineEdit.text()
        roast = self.doubleSpinBox.value()
        is_ground = self.comboBox.currentText()
        desc = self.plainTextEdit.toPlainText()
        price = self.doubleSpinBox_2.value()
        volume = self.doubleSpinBox_3.value()
        return name, str(roast), is_ground, desc, str(price), str(volume)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tw = TableWindow()
    tw.show()
    sys.exit(app.exec())
