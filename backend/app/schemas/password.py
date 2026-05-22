from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class SecurityStatus(str, Enum):
    """Enumeration of possible security levels for an analyzed password.

    Inherits from str to allow direct JSON serialization
    and string comparison without calling .value explicitly.

    Members:
        SAFE: The password meets all security criteria.
        SOMEWHAT_SAFE: The password meets most security criteria but has minor weaknesses.
        UNSAFE: The password has significant vulnerabilities.
        VERY_INSECURE: The password fails most security criteria and should not be used.
    """
    SAFE = "segura"
    SOMEWHAT_SAFE = "poco segura"
    UNSAFE = "insegura"
    VERY_INSECURE = "muy insegura"

class PasswordVulnerabilities(str, Enum):
    """Enumeration of possible vulnerabilities detected in an analyzed password.

    Inherits from str to allow direct JSON serialization
    and string comparison without calling .value explicitly.

    Each member represents a specific weakness. The enum value
    is a human-readable message in Spanish intended to be
    displayed directly to the end user.

    Note:
        Members prefixed with HAS_ do not always imply presence —
        some indicate absence of a required characteristic
        (e.g. HAS_UPPERCASE_LETTER means the password is missing
        an uppercase letter). Consider renaming to MISSING_ in
        a future refactor for semantic clarity.

    Members:
        HAS_ASCENDING_SEQUENCE: Password contains an ascending sequence of characters or digits.
        HAS_DESCENDING_SEQUENCE: Password contains a descending sequence of characters or digits.
        HAS_SPECIAL_CHARACTER: Password is missing at least one special character.
        HAS_UPPERCASE_LETTER: Password is missing at least one uppercase letter.
        HAS_LOWERCASE_LETTER: Password is missing at least one lowercase letter.
        HAS_MINIMUM_LENGTH: Password does not meet the minimum required length of 8 characters.
        HAS_NUMBERS: Password does not contain at least three numeric digits.
        WITHOUT_VULNERABILITIES: No vulnerabilities were detected.
    """
    HAS_ASCENDING_SEQUENCE = "La contraseña tiene secuencias ascendentes 'números - letras'"
    HAS_DESCENDING_SEQUENCE = "La contraseña tiene secuencias descendetes 'números - letras'"
    HAS_SPECIAL_CHARACTER = "La contraseña no tiene al menos un caracter especial"
    HAS_UPPERCASE_LETTER = "La contraseña no tiene al menos una letra mayúscula"
    HAS_LOWERCASE_LETTER = "La contraseña no tiene al menos una letra minúscula"
    HAS_MINIMUM_LENGTH = "La contraseña no tiene al menos de 8 caracteres"
    HAS_NUMBERS = "La contraseña no tiene al menos 3 números"
    WITHOUT_VULNERABILITIES = "Sin vulnerabilidades"
    
class PasswordBase(BaseModel):
    """Base schema containing the raw password to be analyzed.

    Used as the request body for the password analysis endpoint.
    The password is processed in memory and never persisted
    in the database.
    """
    password: str = Field(
        description="Password that will be subject to security analysis",
        min_length=1,
        max_length=40
    )
    
class PasswordAnalyzed(BaseModel):
    """Schema representing the raw boolean results of a password analysis.

    This is an intermediate schema used internally by the analysis
    pipeline. It is produced by PasswordAnalyzer and consumed by
    VulnerabilityDetector to determine which vulnerabilities are present.
    It is never returned directly to the client.
    """
    minimum_length: bool = Field(description="True if the password meets the minimum required length.")
    ascending_sequence: bool = Field(description="True if the password contains an ascending sequence of characters or digie")
    descending_sequence: bool = Field(description="True if the password contains a descending sequence of characters or digits.")
    capital_letter: bool = Field(description="True if the password contains at least one uppercase letter.")
    lowercase_letter: bool = Field(description="True if the password contains at least one lowercase letter.")
    special_character: bool = Field(description="True if the password contains at least one special character.")
    numbers: bool = Field(description="True if the password contains at least three numeric digits.")
    
class PasswordAnalysisCreate(PasswordBase):
    security_status: str = Field(description="Security status that was assigned to the password after for being analyzed")
    safety_color: str = Field(description="CSS color representing the security status. Used by the frontend to render visual feedback.")
    vulnerabilities: list[str] = Field(
        default=[],
        description="List of vulnerability messages detected in the password. Empty if no vulnerabilities were found.")
    feedback: list[str] = Field(
        default=[],
        description="List of actionable suggestions to improve the password strength." 
    )
    
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)