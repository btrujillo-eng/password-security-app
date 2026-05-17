from pydantic import EmailStr

import sqlite3 as sql

def get_user_by_email(email: EmailStr, table_name: str = "students") -> bool:
    with sql.connect("uniminuto.db") as connection:
        cursor = connection.cursor()
            
        query = f"SELECT * FROM {table_name} WHERE email = ?"
        cursor.execute(query,(email,))
        if not cursor.fetchone():
            return False
            
        return True
            