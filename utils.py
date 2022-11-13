from databse import *

def verify_user(user, password):
    cursor.execute(f"select Uid from user where password = '{password}' and Uid = {user}")
    if cursor is not None:
        return cursor.fetchone()
    else: 
        return False

def show_all_parking(block = 'all'):
    condition = "" if block.lower() == 'all' else f" where block = {block}"
    print(f"select * from parking_space left join booking on parking_space.pid = booking.pid{condition};")
    cursor.execute(f"select * from parking_space left join booking on parking_space.pid = booking.pid{condition};")
    return cursor.fetchall()

def show_owned(user, block):
    condition = "" if block.lower() == 'all' else f" and block = {block}"
    cursor.execute(f"select * from parking_space left join booking on parking_space.pid = booking.pid where uid = {user}{condition};")
    return cursor.fetchall()