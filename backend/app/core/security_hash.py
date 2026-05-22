from backend.app.core.interfaces import IPasswordHasher

import bcrypt

class PasswordHasher(IPasswordHasher):
    
    def hash(self, password: str) -> str:
        """Hashes a plain text password using bcrypt with an auto-generated salt.

        Args:
            password (str): The plain text password to hasher.

        Returns:
            str: The hashed password as a 'UTF-8' enconded string.
        """
        password_bytes = password.encode()
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        return hashed_password.decode()
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifies a plain text password against a hashed one.

        Args:
            password: The plain text password provided by the user.
            hashed_password: The stored hashed password to compare against.

        Returns:
            True if the passwords match, False otherwise.
        """
        plain_bytes = password.encode()
        hashed_bytes = hashed_password.encode()
        
        return bcrypt.checkpw(plain_bytes, hashed_bytes)