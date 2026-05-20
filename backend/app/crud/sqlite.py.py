from schemas import IdModel, UserBase, UserResponse
from core import ISqlRepository, get_user_by_email
from exceptions import EmailAlreadyExistsError, UserDoesNotExistsError

from typing import List
import sqlite3 as sql
import logging

logger = logging.getLogger(__name__)

class SqliteUserRepository(ISqlRepository):
    
    def get_all(self) -> List[UserResponse]:
        with sql.connect("uniminuto.db") as connection:
            connection.row_factory = sql.Row 
            cursor = connection.cursor()
        
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            return [UserResponse(**dict(r)) for r in rows]
            
    
    def get_user_by_id(self, id: IdModel) -> UserResponse:
        with sql.connect("uniminuto.db") as connection:
            cursor = connection.cursor()
            
            query = "SELECT * FROM students WHERE id = ? "
            cursor.execute(query, (id.id, ))
            row = cursor.fetchone()
            
            if not row:
                raise UserDoesNotExistsError(f"The user with ID {id.id} does not exist")
            
            return UserResponse(
                id=row[0], 
                username=row[1],
                email=row[2]
            )
                    
    def create(self, user_data: UserBase) -> UserResponse:
        with sql.connect("uniminuto.db") as connection:
            cursor = connection.cursor()
            
            if get_user_by_email(user_data.email):
                raise EmailAlreadyExistsError(f"The email {user_data.email} already exist")
            
            query = """
                INSERT INTO students (name, email) 
                VALUES (?, ?)
                RETURNING id, name, email
            """
            try:
                cursor.execute(query, (user_data.user_name, user_data.email))
                new_row = cursor.fetchone()
                connection.commit()
                
                return UserResponse(
                    id=new_row[0],
                    username=new_row[1],
                    email=new_row[2]
                )
            except sql.Error as e:
                logger.critical(f"DB error: {e}")
                raise
            
    def create_many(self, users: List[UserBase]) -> bool:
        with sql.connect("uniminuto.db") as connection:
            cursor = connection.cursor()
            
            query = "INSERT INTO students(name, email) VALUES (?, ?)"
            data = [(u.user_name, u.email) for u in users if not get_user_by_email(u.email)]
            
            try:
                cursor.executemany(query, data)
                return True
            except sql.Error as e:
                logger.critical(f"DB error: {e}")
                raise  
            
    def update(self, id: IdModel, user_data: UserBase) -> UserResponse:
        with sql.connect("uniminuto.db") as connection:
            cursor = connection.cursor()
            
            
            if not self.get_user_by_id(id):
                raise UserDoesNotExistsError(f"The user with ID {id.id} does not exist.")
            
            query = """
                UPDATE students SET name = ?, email = ? WHERE id = ?
                RETURNING id, name, email
            """
            try:
                cursor.execute(query, (user_data.user_name, user_data.email, id.id))
                modified_row = cursor.fetchone()
                connection.commit()
                
                return UserResponse(
                    id=modified_row[0],
                    username=modified_row[1],
                    email=modified_row[2]
                )
            except sql.Error as e:
                logger.critical(f"DB error: {e}")
                raise
            
    def delete(self, id: IdModel) -> bool:
        with sql.connect("uniminuto.db") as connection:
            cursor = connection.cursor()
            
            exist = self.get_user_by_id(id)
            if not exist:
                raise UserDoesNotExistsError(f"The user with ID {id.id} does not exist")
            
            query = """ 
                DELETE FROM students WHERE id = ?
            """
            cursor.execute(query, (id.id,))
            connection.commit()
            
            return True