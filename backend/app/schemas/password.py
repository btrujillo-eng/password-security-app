from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class SecurityStatus(str, Enum):
    SAFE = "segura"
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
    
class PasswordBase(BaseModel):
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
    
class PasswordAnalysisCreate(PasswordBase):
    security_status: str = Field(description="Security status that was assigned to the password after for being analyzed")
    safety_color: str = Field(description="Color that represents the security status of the analyzed password")
    vulnerabilities: list[str] = Field(description="List of vulnerabilities found in the analyzed password", default=[])
    feedback: list[str] = Field(description="", default=[])
    
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)