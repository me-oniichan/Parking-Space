from databse import *
from datetime import datetime as dt

def verify_user(user, password):
    if not user.isdigit(): return False  ##if formate is false, reject
    cursor.execute(f"select Uid from user where password = '{password}' and Uid = {user}")
    data= cursor.fetchone()
    if data is not None:
        return data
    else: 
        return False

def add_user(user, password):
    try:
        cursor.execute(f"insert into user values({user}, now(), '{password}')")
        db.commit()
        return True
    except:
        return False

def verify_input(user, password, confirmpass):
    if not user.isdigit(): return False
    elif password != confirmpass: return -1

    cursor.execute(f"select Uid from user where Uid = {user}")
    existence= cursor.fetchone() 
    if existence != None: return -2  #if user already exist, reject

    if len(password) < 8: return -3

    return user.isdigit() and (len(user)==8 or len(user) == 5)

def show_all_parking(block = 'all'):
    condition = "" if block.lower() == 'all' else f" where block = {block}"
    cursor.execute(f"select * from parking_space left join booking on parking_space.pid = booking.pid{condition};")
    return cursor.fetchall()

def show_owned(user, block):
    condition = "" if block.lower() == 'all' else f" and block = {block}"
    cursor.execute(f"select * from parking_space left join booking on parking_space.pid = booking.pid where uid = {user}{condition};")
    return cursor.fetchall()

def book(uid, pid):
    try:
        cursor.execute(f"insert into booking values({uid}, '{pid}', now(), {dt.now().hour}{dt.now().minute});")
        db.commit()
        return True
    except:
        return False

def cancel(uid, pid):
    try:
        cursor.execute(f"delete from booking where pid='{pid}' and uid ={uid}")
        db.commit()
        return True
    except:
        return False