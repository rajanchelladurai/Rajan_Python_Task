import sqlite3

conn = sqlite3.connect('atm1.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        balance INTEGER NOT NULL
    )
''')
conn.commit()
print("Table created successfully ... ")

total_balance = {}


class ATM():
    total_balance = {}

    def __init__(self):
        total_balance = self.total_balance

    def deposit(self):
        self.original_ = {20: [], 10: [], 5: []}
        self.total_balance = {}
        val_20 = int(input('Enter  val 20 :'))
        val_10 = int(input('Enter val 10 :'))
        val_5 = int(input('Enter val 5 : '))

        if val_20 == 20:
            self.original_[20].append(20)
        if val_10 == 10:
            self.original_[10].append(10)
        if val_10 == 10:
            self.original_[5].append(5)

        s = self.original_[20][0]
        for i in self.original_[20]:
            if len(self.original_[20]) == 1:
                s = i
            else:
                s += i

        v = self.original_[10][0]
        for i in self.original_[10]:
            if len(self.original_[10]) == 1:
                v = i
            else:
                v += i

        u = self.original_[5][0]
        for i in self.original_[5]:
            if len(self.original_[5]) == 1:
                u = i
            else:
                u += i
        self.total_balance[20] = s
        self.total_balance[10] = v
        self.total_balance[5] = u

        print("Net Balance : ", self.total_balance)
        total = self.total_balance[20]
        for i, j in self.total_balance.items():
            total += j
        print("Balance : ", total)
        conn = sqlite3.connect('atm1.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, balance) VALUES (?, ?)", ('Alice', total))
        conn.commit()
        conn.close()
        print('Balance stored sucessfully ...')

    def withdrawl(self):
        val = int(input('Enter your withdrawl amount : '))
        query = 'select * from users;'
        cursor.execute(query)
        queryset = cursor.fetchall()
        bal = queryset[0][2]
        amt = bal - val
        print("After Withdral balance : ", amt)

    def check_balance(self):
        conn = sqlite3.connect('atm1.db')
        cursor = conn.cursor()
        query = 'select * from users;'
        cursor.execute(query)
        queryset = cursor.fetchall()
        bal = queryset[0][2]
        print("Your Balance is : ", bal)


value = int(input('Enter 1 : Deposit\nEnter 2 : Withdrawl\n Enter 3 : Check Balance :\n Enter You option : '))
o = ATM()
if value == 1:
    o.deposit()
elif value == 2:
    o.withdrawl()
elif value == 3:
    o.check_balance()



