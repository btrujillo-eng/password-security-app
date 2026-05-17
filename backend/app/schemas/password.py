from pydantic import BaseModel, Field
from enum import Enum

class SecurityStatus(str, Enum):
    SAFE = "seg3ura"
    SOMEWHAT_SAFE = "poco segura"
    UNSAFE = "insegura"
    VERY_INSECURE = "muy insegura"

class PasswordVulnerabilities(str, Enum):
    HAS_ASCENDING_SEQUENCE = "La contraseña tiene secuencias ascendentes 'números - letras'"
    HAS_DESCENDING_SEQUENCE = "La contraseña tiene secuencias descendetes 'números - letras'"
    HAS_SPECIAL_CHARACTER = "La contraseña no tiene al menos un caracter especial"
    HAS_UPPERCASE_LETTER = "La contraseña no tiene al menos una letra mayúscula"
    HAS_LOWERCASE_LETTER = "La contraseña no tiene al menos una letra minúscula"
    HAS_MINIMUM_LENGTH = "La contraseña no tiene al menos de 8 caracteres"
    HAS_NUMBERS = "La contraseña no tiene al menos 3 números"
    WITHOUT_VULNERABILITIES = "Sin vulnerabilidades"
    
class PasswordData(BaseModel):
    password: str = Field(
        description="Password that will be subject to security analysis",
        min_length=3,
        max_length=40
    )
    
class PasswordAnalyzed(BaseModel):
    minimum_length: bool = Field(description="Stores the boolean value that indicates whether the password has a minimum secure length")
    ascending_sequence: bool = Field(description="Stores the boolean value that indicates whether the password contains any type of ascending sequence")
    descending_sequence: bool = Field(description="Stores the boolean value that indicates whether the passowrd containts any type of descending sequence")
    capital_letter: bool = Field(description="Stores the boolean value that indicates whether the password containts at least one uppercase letter")
    lowercase_letter: bool = Field(description="Stores the boolean value that indicates whether the password contains at least one lowercase letter")
    special_character: bool = Field(description="Stores the boolean value that indicates whether the password contains at leat two speacial characters")
    numbers: bool = Field(description="Stores the boolean value that indicates whether the password contains at least three numbers")
    
class PasswordResponse(BaseModel):
    password: str = Field(description="Password that was analyzed")
    status: str = Field(description="Security status that was assigned to the password after for being analyzed")
    color: str = Field(description="Color that represents the security status of the analyzed password")
    vulnerabilities: list[str] = Field(description="List of vulnerabilities found in the analyzed password")
    tips: list[str] = Field(description="")