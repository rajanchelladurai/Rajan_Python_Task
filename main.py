import os

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3


import requests
from sqlalchemy.testing import db

app = Flask(__name__)
app.secret_key = "secret_key"
DATABASE = 'Account_Summary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS atm (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        balance TEXT,
                        place TEXT
                    )''')
    # conn1 = sqlite3.connect(WEATHER)
    # cursor = conn1.cursor()
    conn.commit()
    conn.close()


@app.route('/',methods=['GET', 'POST'])
def index():
    """Display all records."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM atm")
    account_user_list = cursor.fetchall()
    print("account_user_list ",account_user_list)
    conn.close()
    return render_template('index.html', items=account_user_list )



@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """Add a new record."""

    if request.method == 'POST':
        name = request.form['name']
        amount_20 = request.form['amount_20']
        amount_10 = request.form['amount_10']
        amount_5 = request.form['amount_5']
        place = request.form['place']
        amt = int(amount_20) * 500 + int(amount_10) * 200 + int(amount_5) * 100
        print("Amount Desposite",amt)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO atm (name, balance,place) VALUES (?, ?, ?)", (name,amt,place))
        conn.commit()
        conn.close()

        flash("Amount added your account successfully!")
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/check_balance/<int:id>', methods=['GET', 'POST'])
def check_balance(id):
    """ To view the bank account balance"""
    print("balance check")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    query = (
        f"select balance from atm where id={id};"
    )
    cursor.execute(query)
    queryset = cursor.fetchall()
    print("view balance :",queryset)
    return render_template('balance_view.html', amt = queryset[0][0])

@app.route('/submit_withdrawal/<int:id>', methods=['POST'])
def submit_withdrawal(id):
    print("Processing withdrawal...")
    try:
        data = request.get_json()
        withdrawal_amount = data.get('withdrawalAmount')
        if withdrawal_amount is None:
            return jsonify({"error": "No withdrawal amount provided."}), 400
        print(f"Received ID: {id}, Withdrawal Amount: {withdrawal_amount}")
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        query = (
            f"select balance from atm where id={id};"
        )
        cursor.execute(query)
        queryset = cursor.fetchall()
        balance = queryset[0][0]
        print("bank balance",balance)
        balance = int(balance) - int(withdrawal_amount)
        cursor.execute("UPDATE atm SET balance = ? WHERE id = ?", (balance, id))
        conn.commit()
        conn.close()
        print(" Balance updated sucessfully .....")
        return jsonify({
            "message": "Withdrawal request processed successfully.",
            "id": id,
            "withdrawalAmount": withdrawal_amount
        })
    except ValueError:
        return jsonify({"error": "Withdrawal amount must be an integer."}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
