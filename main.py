import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class TableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_data()

    def load_data(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название сорта',
                                                    'Степень обжарки',
                                                    'Молотый/в зернах',
                                                    'Описание вкуса',
                                                    'Цена', 'Объем упаковки'])
        self.tableWidget.setRowCount(0)
        con = sqlite3.connect('coffee.db')
        cur = con.cursor()
        data = cur.execute('SELECT * From coffee').fetchall()
        for i, item in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(item):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tw = TableWindow()
    tw.show()
    sys.exit(app.exec())
