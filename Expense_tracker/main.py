from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QComboBox, QDateEdit, QTableWidget, QMessageBox, QTableWidgetItem
)
from PyQt6.QtCore import QDate
from Data.db_utils import db_init, db_get_all_expenses, db_insert_expense, db_del_expense
from tracker_utils import validate_expense_input

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
        self.date_panel.setDate(QDate.currentDate())
        self.category_label = QLabel('Category:')
        self.category_panel = QComboBox()
        self.category_panel.addItems(['Shopping', 'Fixed Expenses', 'Groceries', 'Others'])
        self.amount_label = QLabel('Amount:')
        self.amount_panel = QLineEdit()
        self.description_label = QLabel('Description:')
        self.description_panel = QLineEdit()
        self.btn_add_expense = QPushButton('Add Expense')
        self.btn_del_expense = QPushButton('Delete Expense')
        
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
        self.third_row.addWidget(self.btn_add_expense)
        self.third_row.addWidget(self.btn_del_expense)
        

        self.master_column.addLayout(self.first_row)
        self.master_column.addLayout(self.second_row)
        self.master_column.addLayout(self.third_row)
        self.master_column.addWidget(self.data_table)

        self.setLayout(self.master_column)

        self.btn_add_expense.clicked.connect(self.add_expense)
        self.btn_del_expense.clicked.connect(self.del_expense)

        self.show_expenses()
    

    def show_expenses(self):
        expenses_list = db_get_all_expenses()
        self.data_table.setRowCount(0)
        row = 0
        for expense in expenses_list:
            
            if expense["amount"]:
                amount = float(expense["amount"])
                amount = f'{amount:.2f}'
            else:
                amount = f'{0:.2f}'

            self.data_table.insertRow(row)
            self.data_table.setItem(row, 0, QTableWidgetItem(str(expense["id"])))
            self.data_table.setItem(row, 1, QTableWidgetItem(expense["date"]))
            self.data_table.setItem(row, 2, QTableWidgetItem(expense["category"]))
            self.data_table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.data_table.setItem(row, 4, QTableWidgetItem(expense["description"]))

            row += 1


    def add_expense(self):  
        date = self.date_panel.date().toString("dd-MM-yyyy")
        category = self.category_panel.currentText()

        try:
            amount = float(self.amount_panel.text())
        except ValueError:
            QMessageBox.warning(None, "Amount", "Enter a valid number")
            return

        description = self.description_panel.text()

        if db_insert_expense(date, category, amount, description):
            self.date_panel.setDate(QDate.currentDate())
            self.category_panel.setCurrentIndex(0)
            self.amount_panel.clear()
            self.description_panel.clear()
            self.show_expenses()
    

    def del_expense(self):
        current_row = self.data_table.currentRow()

        if current_row >= 0:
            expense_id = int(self.data_table.item(current_row, 0).text())

            confirm = QMessageBox.question(None, "Delete Expense", "Are you sure?")

            if confirm == QMessageBox.StandardButton.Yes:
                if db_del_expense(expense_id):
                    self.show_expenses()
            else:
                return

        else:
            QMessageBox.warning(None, "Delete Expense", "No expense has been selected")


# App exec
if __name__ == '__main__':
    app = QApplication([])

    db_init()    
    main_window = TrackerApp()
    main_window.show()
    app.exec()