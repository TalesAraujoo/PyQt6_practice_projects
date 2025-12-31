from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QComboBox, QDateEdit, QTableWidget, QMessageBox, QTableWidgetItem
)
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
from pathlib import Path
import os


class TrackerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Expense Tracker')
        self.resize(525, 400)


        self.master_column = QVBoxLayout()
        self.first_row = QHBoxLayout()
        self.second_row = QHBoxLayout()
        self.third_row = QHBoxLayout()
        
        self.date_label = QLabel('Date:')
        self.date_panel = QDateEdit()
        self.category_label = QLabel('Category:')
        self.category_panel = QComboBox()
        self.amount_label = QLabel('Amount:')
        self.amount_panel = QLineEdit()
        self.description_label = QLabel('Description:')
        self.description_panel = QLineEdit()
        self.add_expense = QPushButton('Add Expense')
        self.del_expense = QPushButton('Delete Expense')
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(['ID', 'Date', 'Category', 'Amount', 'Description'])


        self.first_row.addWidget(self.date_label)
        self.first_row.addWidget(self.date_panel)
        self.first_row.addWidget(self.category_label)
        self.first_row.addWidget(self.category_panel)
        self.second_row.addWidget(self.amount_label)
        self.second_row.addWidget(self.amount_panel)
        self.second_row.addWidget(self.description_label)
        self.second_row.addWidget(self.description_panel)
        self.third_row.addWidget(self.add_expense)
        self.third_row.addWidget(self.del_expense)
        

        self.master_column.addLayout(self.first_row)
        self.master_column.addLayout(self.second_row)
        self.master_column.addLayout(self.third_row)
        self.master_column.addWidget(self.data_table)

        self.setLayout(self.master_column)
        self.load_database_table()


    def load_database_table(self):
        self.data_table.setRowCount(0)

        query = QSqlQuery("""
            SELECT * FROM expenses
        """)

        row = 0
        while query.next():
            expense_id = query.value(0)
            expense_date = query.value(1)
            expense_category = query.value(2)
            expense_amount = query.value(3)
            expense_description = query.value(4)

            # Add values to tables
            self.data_table.insertRow(row)
            self.data_table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.data_table.setItem(row, 1, QTableWidgetItem(expense_date))
            self.data_table.setItem(row, 2, QTableWidgetItem(expense_category))
            self.data_table.setItem(row, 3, QTableWidgetItem(str(expense_amount)))
            self.data_table.setItem(row, 4, QTableWidgetItem(expense_description))    

            row += 1





# App exec
if __name__ == '__main__':
    app = QApplication([])
    
        # Database
    database = QSqlDatabase.addDatabase("QSQLITE")

    script_dir = Path(__file__).parent.resolve()
    db_path = os.path.join(script_dir, 'tracker.db')
    database.setDatabaseName(db_path)
    
    if not database.open():
        QMessageBox.critical(None, "Error", "could not load the database")
        sys.exit(1)

    query = QSqlQuery()
    query.exec("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    category TEXT, 
                    amount REAL,
                    description TEXT
                )            
                """)
    
    main_window = TrackerApp()
    main_window.show()
    app.exec()