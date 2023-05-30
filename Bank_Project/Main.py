import csv
import sqlite3
import matplotlib.pyplot as plt

customer_file = "customers.csv"
transaction_file = "transactions.csv"
database_file = "bank_data.db"


class Customer:
    def __init__(self, customer_id, name, address, phone):
        self._customer_id = customer_id
        self._name = name
        self._address = address
        self._phone = phone


    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        self._customer_id = customer_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone

    def __str__(self):
        return f' Customer_id - {self._customer_id}, Name - {self._name}, Address - {self._address},' \
               f' Phone - {self._phone} '


class Transaction:
    def __init__(self, transaction_id, customer_id, amount, date):
        self._transaction_id = transaction_id
        self._customer_id = customer_id
        self._amount = amount
        self._date = date

    @property
    def transaction_id(self):
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        self._transaction_id = transaction_id

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        self._customer_id = customer_id

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    def __str__(self):
        return f" Transaction_id - {self._transaction_id}, Customer_id - {self._customer_id}," \
               f" Amount - {self._amount}, Date - {self._date}"


class BankDataProcessor:
    def __init__(self):
        self._connection = None

    @property
    def connection(self):
        return self._connection

    def connect(self):
        self._connection = sqlite3.connect(database_file)

    def disconnect(self):
        self._connection.close()

    def commit(self):
        self._connection.commit()

    def create_tables(self):
        cursor = self._connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        address TEXT,
        phone TEXT)''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id))''')
        self._connection.commit()

    def load_customer_data(self):
        with open(customer_file, "r") as file:
            reader = csv.reader(file)
            next(reader)
            cursor = self._connection.cursor()
            for row in reader:
                customer = Customer(int(row[0]), row[1], row[2], row[3])
                cursor.execute(
                    "INSERT OR IGNORE INTO customers (customer_id, name, address, phone) VALUES (?, ?, ?, ?)",
                    (customer.customer_id, customer.name, customer.address, customer.phone))
            self.commit()

    def load_transaction_data(self):
        with open(transaction_file, "r") as file:
            reader = csv.reader(file)
            next(reader)
            cursor = self._connection.cursor()
            for row in reader:
                transaction = Transaction(int(row[0]), int(row[1]), float(row[2]), row[3])
                cursor.execute(
                    "INSERT OR IGNORE INTO transactions (transaction_id, customer_id, amount, date) VALUES (?, ?, ?, ?)",
                    (transaction.transaction_id, transaction.customer_id, transaction.amount, transaction.date))
            self.commit()

    def get_transactions_by_customer(self, customer_id):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE customer_id=?", (customer_id,))
        transactions = cursor.fetchall()
        return [Transaction(*transaction) for transaction in transactions]

    def get_customer_by_transaction(self, transaction_id):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT customers.* FROM customers JOIN transactions ON customers.customer_id = transactions.customer_id WHERE transaction_id=?",
            (transaction_id,))
        customer = cursor.fetchone()
        if customer:
            return Customer(*customer)
        return None

    def max_amount(self):
        cursor = self._connection.cursor()
        cursor.execute('''
            SELECT t.transaction_id, t.customer_id, MAX(t.amount), c.name, c.address, c.phone
            FROM main.transactions t JOIN main.customers c
            ON (t.customer_id = c.customer_id);''')
        return cursor.fetchall()

    def min_amount(self):
        cursor = self._connection.cursor()
        cursor.execute('''
                SELECT t.transaction_id, t.customer_id, MIN(t.amount), c.name, c.address, c.phone
                FROM main.transactions t JOIN main.customers c
                ON (t.customer_id = c.customer_id);''')
        return cursor.fetchone()

    def calculate_total_transaction_amount(self, customer_id):
        cursor = self._connection.cursor()
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE customer_id=?", (customer_id,))
        total_amount = cursor.fetchone()[0]
        return total_amount if total_amount else 0

    def visualize_transaction_amounts(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT amount FROM transactions")
        amounts = cursor.fetchall()
        amounts = [float(amount[0]) for amount in amounts]

        plt.hist(amounts, bins=10)
        plt.xlabel('Amount')
        plt.ylabel('Frequency')
        plt.title('Transaction Amount Distribution')
        plt.show()




def main():
    data_processor = BankDataProcessor()
    try:
        data_processor.connect()
        data_processor.create_tables()
        data_processor.load_customer_data()
        data_processor.load_transaction_data()

        transactions = data_processor.get_transactions_by_customer(48)
        print("Transactions for Customer 48: ")
        for transaction in transactions:
            print(transaction)

        print("*" * 150)

        customer = data_processor.get_customer_by_transaction(92)
        if customer:
            print("Customer for Transaction 92:")
            print(customer)
        else:
            print("Customer not found.")

        print("*" * 150)

        total_amount = data_processor.calculate_total_transaction_amount(20)
        print("Total Transaction Amount for Customer 20:", total_amount)
        print("*" * 150)
        Min_Amount = data_processor.min_amount()
        print("MIN Amount Person: ", Min_Amount)


        print("*" * 150)

        Max_Amount = data_processor.max_amount()
        print("Max Amount Person: ", Max_Amount)
        print("*" * 150)

        data_processor.visualize_transaction_amounts()

    except Exception as ex:
        print(ex)
    finally:
        data_processor.disconnect()


if __name__ == '__main__':
    main()
