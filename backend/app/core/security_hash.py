from backend.app.core.interfaces import IPasswordHasher

import bcrypt

class PasswordHasher(IPasswordHasher):
    
    def hash(self, password: str) -> str:
        password_bytes = password.encode()
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        return hashed_password.decode()
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        plain_bytes = password.encode()
        hashed_bytes = hashed_password.encode()
        
        return bcrypt.checkpw(plain_bytes, hashed_bytes)