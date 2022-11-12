from databse import *

def verify_user(user, password):
    cursor.execute(f"select Uid from user where password = '{password}' and Uid = {user}")
    if cursor is not None:
        return cursor.fetchone()
    else: 
        return False

def show_all_parking():
    cursor.execute("select * from parking_space left join booking on parking_space.pid = booking.pid;")
    return cursor.fetchall()

def show_owned(user):
    cursor.execute(f"select * from parking_space left join booking on parking_space.pid = booking.pid where uid = {user};")
    return cursor.fetchall()