# This code generates and saves to files fake bank data for my project

import csv
from faker import Faker

fake = Faker()

customer_rows = []
for _ in range(100):
    customer_id = fake.unique.random_int(min=1, max=100)
    name = fake.name()
    address = fake.city()
    phone = fake.phone_number()
    customer_rows.append([customer_id, name, address, phone])

with open('customers.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['customer_id', 'name', 'address', 'phone'])
    writer.writerows(customer_rows)

transaction_rows = []
for i in range(1, 101):
    transaction_id = i
    customer_id = fake.random_int(min=1, max=100)
    amount = fake.pyfloat(left_digits=3, right_digits=2, positive=True)
    date = fake.date_between(start_date='-1y', end_date='today')
    transaction_rows.append([transaction_id, customer_id, amount, date])

with open('transactions.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['transaction_id', 'customer_id', 'amount', 'date'])
    writer.writerows(transaction_rows)
