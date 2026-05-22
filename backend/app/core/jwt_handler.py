from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import cast
from dotenv import load_dotenv
import os

_ = load_dotenv()

SECRET_KEY: str = cast(str, os.getenv("SECRET_KEY"))
if not SECRET_KEY:
    raise RuntimeError("The database URL could not be found")

ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict) -> str:
    """Creates a signed JWT access token with an expiration time.

    Args:
        data: Payload to encode in the token. Typically contains
              the user identifier under the key 'sub'.

    Returns:
        A signed JWT token string encoded with the configured
        secret key and algorithm.

    Example:
        >>> token = create_access_token(data={"sub": "brayan123"})
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict | None:
    """Verifies and decodes a JWT access token.

    Args:
        token: The JWT token string to verify.

    Returns:
        The decoded payload as a dictionary if the token is valid,
        or None if the token is expired, malformed, or has an
        invalid signature.

    Example:
        >>> payload = verify_token(token)
        >>> if payload is None:
        ...     raise HTTPException(status_code=401)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None