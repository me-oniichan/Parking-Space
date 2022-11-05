import mysql.connector as connect

with open("password.txt") as f: password = f.read()

conn = connect.connect(user = "root", password=password)
cur = conn.cursor()
try:
    cur.execute("create database Parking;")
except:
    pass

cur.execute("use Parking;")