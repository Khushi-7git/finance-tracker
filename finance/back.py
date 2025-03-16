from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect('db.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            target INTEGER NOT NULL,
                            period TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS debts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            person TEXT NOT NULL,
                            amount INTEGER NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS calculations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            amount1 INTEGER NOT NULL,
                            amount2 INTEGER NOT NULL,
                            operation TEXT NOT NULL,
                            result INTEGER NOT NULL)''')
        conn.commit()

@app.before_first_request
def before_first_request():
    init_db()

# Home Route
@app.route('/')
def home():
    return render_template('budget.html')

# Budget Tracker
@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if request.method == 'POST':
        target = request.form['target']
        period = request.form['period']
        with sqlite3.connect('db.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO budgets (target, period) VALUES (?, ?)", (target, period))
            conn.commit()
        return redirect(url_for('budget'))
    
    # Fetch budgets
    with sqlite3.connect('db.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM budgets")
        budgets = cursor.fetchall()
    
    return render_template('budget.html', budgets=budgets)

# Debt Tracker
@app.route('/debt', methods=['GET', 'POST'])
def debt():
    if request.method == 'POST':
        person = request.form['person']
        amount = request.form['amount']
        with sqlite3.connect('db.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO debts (person, amount) VALUES (?, ?)", (person, amount))
            conn.commit()
        return redirect(url_for('debt'))

    # Fetch debts
    with sqlite3.connect('db.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM debts")
        debts = cursor.fetchall()

    return render_template('debt.html', debts=debts)

# Calculator Route
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        amount1 = int(request.form['amount1'])
        amount2 = int(request.form['amount2'])
        operation = request.form['operation']
        
        if operation == 'add':
            result = amount1 + amount2
        elif operation == 'subtract':
            result = amount1 - amount2
        elif operation == 'multiply':
            result = amount1 * amount2
        elif operation == 'divide':
            result = amount1 / amount2 if amount2 != 0 else 'Error: Division by Zero'

        with sqlite3.connect('db.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO calculations (amount1, amount2, operation, result) VALUES (?, ?, ?, ?)",
                           (amount1, amount2, operation, result))
            conn.commit()

    return render_template('calculator.html', result=result)

# Learn Finance
@app.route('/learn')
def learn():
    return render_template('learn.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
