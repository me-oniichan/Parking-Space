from databse import *

def verify_user(user, password):
    cursor.execute(f"select Uid from user where password = '{password}' and Uid = {user}")
    if cursor is not None:
        return cursor.fetchone()
    else: 
        return False