from PyQt5.QtWidgets import *
import sys
import sqlite3

width = 1050
height = 450


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)
        self.db = 0
        self.setWindowTitle("Таблицы")
        self.setFixedSize(width, height)

        mainMenu = self.menuBar()
        menu = mainMenu.addMenu("Menu")

        setConnection = QAction("Set connection", self)
        setConnection.triggered.connect(self.getCon)
        menu.addAction(setConnection)

        close = QAction("Close", self)
        close.triggered.connect(self.closeCon)
        menu.addAction(close)

        self.btn1 = QPushButton("1. get names", self)
        self.btn1.move(50, 50)
        self.btn1.resize(120, 35)
        self.btn1.clicked.connect(self.button1)

        '''self.fg1 = QLineEdit(self)
        self.fg1.move(50, 100)
        self.fg1.resize(120, 35)
        self.fg1.setText('name')
        self.fg1.setPlaceholderText("column name")'''

        self.lb1 = QLabel('Please select the column', self)
        self.lb1.move(40, 200)
        self.lb1.resize(145, 50)

        self.myQComboBox = QComboBox(self)
        self.myQComboBox.addItems(["birthday", "name", "surname", "favorite_dish", "weight", 'desired_weight'])
        self.myQComboBox.resize(120, 35)
        self.myQComboBox.move(50, 250)
        self.myQComboBox.currentTextChanged.connect(self.select_c)

        self.btn2 = QPushButton("2. get weight_diff", self)
        self.btn2.move(50, 100)
        self.btn2.resize(120, 35)
        self.btn2.clicked.connect(self.button2)

        self.btn3 = QPushButton("3. get bd and dish", self)
        self.btn3.move(50, 150)
        self.btn3.resize(120, 35)
        self.btn3.clicked.connect(self.button3)

        self.tables = QTabWidget(self)
        self.tables.setFixedSize(780, 250)
        self.tables.move(200, 50)

        self.tab1 = QTableWidget(self)
        self.tab2 = QTableWidget(self)
        self.tab3 = QTableWidget(self)
        self.tab4 = QTableWidget(self)
        self.tab5 = QTableWidget(self)

        self.tables.addTab(self.tab1, "Table 1")
        self.tables.addTab(self.tab2, "Table 2")
        self.tables.addTab(self.tab3, "Table 3")
        self.tables.addTab(self.tab4, "Table 4")
        self.tables.addTab(self.tab5, "Table 5")

    def getCon(self):
        conn = sqlite3.connect('lab.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE if not exists people
                     (birthday, name, surname, favorite_dish, weight,desired_weight)''')
        lines = [('2000-01-25', 'Ann', 'Skidanova', 'rolls', 65.50, 62.00),
                 ('1996-12-20', 'Yar', 'Solovev', 'dumplings', 84.00, 78.00),
                 ('1973-08-04', 'Svetlana', 'Pulkina', 'stewed cabbage', 70.00, 48.00),
                 ('2008-11-06', 'Olga', 'Romanova', 'ice-cream', 62.20, 60.00),
                 ('1972-10-31', 'Pavel', 'Bobrov', 'food of the gods', 120.60, 115.00)]

        if (c.execute('SELECT count(*) FROM people').fetchall()[0][0] == 0):
            c.executemany('INSERT INTO people VALUES (?,?,?,?,?,?)', lines)
            conn.commit()

        for_name = c.execute('PRAGMA table_info(people)').fetchall()
        self.tab1.setColumnCount(len(for_name))
        columnsName = []
        for name in for_name:
            columnsName.append(name[1])
        self.tab1.rowCount()
        self.tab1.setHorizontalHeaderLabels(columnsName)

        data_for_table = c.execute('SELECT * FROM people').fetchall()
        if self.tab1.rowCount() == 0:
            for l in data_for_table:
                self.add_row(self.tab1, l)

        self.tables.setCurrentIndex(0)
        self.db = conn

    def closeCon(self):
        if self.db != 0:
            for i in range(self.tables.count()):
                self.tables.widget(i).setRowCount(0)
                self.tables.widget(i).setColumnCount(0)

            self.db.close()
            self.db = 0

    def select_c(self, val):
        if self.db != 0:
            data = self.db.cursor().execute('SELECT ' + val + ' FROM people').fetchall()

            self.tab3.setColumnCount(1)
            columnsName = [val]
            self.tab3.rowCount()
            self.tab3.setHorizontalHeaderLabels(columnsName)
            self.tab3.setRowCount(0)

            for row in data:
                self.add_row(self.tab3, row)
            self.tables.setCurrentIndex(2)

    def button1(self):
        if self.db != 0:
            names = self.db.cursor().execute('SELECT name FROM people').fetchall()
            columnsName = ['name']
            self.tab2.setColumnCount(1)
            self.tab2.rowCount()
            self.tab2.setHorizontalHeaderLabels(columnsName)

            if self.tab2.rowCount() == 0:
                for row in names:
                    self.add_row(self.tab2, row)
            self.tables.setCurrentIndex(1)

    def button2(self):
        if self.db != 0:
            data = self.db.cursor().execute('SELECT weight,desired_weight FROM people').fetchall()
            new_data = []
            for i in data:
                new_data.append(abs(i[0] - i[1]))
            columnsName = ['weight_difference']

            self.tab4.setColumnCount(1)
            self.tab4.rowCount()
            self.tab4.setHorizontalHeaderLabels(columnsName)

            if self.tab4.rowCount() == 0:
                row = self.tab4.rowCount()
                self.tab4.setRowCount(row + 5)
                col = 0
                for item in new_data:
                    cell = QTableWidgetItem(str(item))
                    self.tab4.setItem(row, col, cell)
                    col += 1
            self.tables.setCurrentIndex(3)

    def button3(self):
        if self.db != 0:
            names = self.db.cursor().execute('SELECT birthday,favorite_dish FROM people ORDER BY birthday').fetchall()
            columnsName = ['birthday', 'favorite_dish']
            self.tab5.setColumnCount(2)
            self.tab5.rowCount()
            self.tab5.setHorizontalHeaderLabels(columnsName)

            if self.tab5.rowCount() == 0:
                for row in names:
                    self.add_row(self.tab5, row)
            self.tables.setCurrentIndex(4)

    def add_row(self, table, row_data):
        col = 0
        row = table.rowCount()
        table.setRowCount(row + 1)
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
