from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox
import sys, os


def db_init():
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

    return database
    

def db_get_all_expenses():

    query = QSqlQuery("""
                    SELECT id, date, category, amount, description
                    FROM expenses
                    ORDER BY id DESC
    """)

    expenses = []

    while query.next():
        expenses.append({
            "id": query.value(0),
            "date": query.value(1),
            "category": query.value(2),
            "amount": query.value(3),
            "description": query.value(4)
        })
    
    return expenses

 
def db_insert_expense(date, category, amount, description):

    query = QSqlQuery()
    query.prepare("""
                INSERT INTO expenses
                    (date, category, amount, description)
                VALUES 
                    (?, ?, ?, ?)
                """)

    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    if not query.exec():
        QMessageBox.critical(None, "Database Error", query.lastError().text())
        return False
    
    return True

    
def db_del_expense(expense_id):
    query = QSqlQuery()
    query.prepare("""
                DELETE FROM expenses
                WHERE id = ?
                """)

    query.addBindValue(expense_id)

    if not query.exec():
        QMessageBox.critical(None, "Database Error", query.lastError().text())
        return False

    return True
