from schemas import SecurityStatus, PasswordVulnerabilities

from typing import List, Tuple, Dict

SAFETY_RULES : List[Tuple[str, bool, PasswordVulnerabilities]] = [
    ("minimum_length", False, PasswordVulnerabilities.HAS_MINIMUM_LENGTH),
    ("ascending_sequence", True, PasswordVulnerabilities.HAS_ASCENDING_SEQUENCE),
    ("descending_sequence", True, PasswordVulnerabilities.HAS_DESCENDING_SEQUENCE),
    ("capital_letter", False, PasswordVulnerabilities.HAS_UPPERCASE_LETTER),
    ("lowercase_letter", False, PasswordVulnerabilities.HAS_LOWERCASE_LETTER),
    ("special_character", False, PasswordVulnerabilities.HAS_SPECIAL_CHARACTER),
    ("numbers", False, PasswordVulnerabilities.HAS_NUMBERS)
]

VULNERABILITY_SCORES: Dict[PasswordVulnerabilities, int] = {
    PasswordVulnerabilities.HAS_MINIMUM_LENGTH: 4,
    PasswordVulnerabilities.HAS_ASCENDING_SEQUENCE: 2,
    PasswordVulnerabilities.HAS_DESCENDING_SEQUENCE: 2,
    PasswordVulnerabilities.HAS_UPPERCASE_LETTER: 2,
    PasswordVulnerabilities.HAS_LOWERCASE_LETTER: 2,
    PasswordVulnerabilities.HAS_SPECIAL_CHARACTER: 3,
    PasswordVulnerabilities.HAS_NUMBERS: 2,
    PasswordVulnerabilities.WITHOUT_VULNERABILITIES: 1
}

SECURITY_STATUS: List[Tuple[int, SecurityStatus]] = [
    (10, SecurityStatus.VERY_INSECURE),
    (5, SecurityStatus.UNSAFE),
    (2, SecurityStatus.SOMEWHAT_SAFE),
    (1, SecurityStatus.SAFE)
]

SAFETY_TIPS: Dict[PasswordVulnerabilities, str]= {
    PasswordVulnerabilities.HAS_MINIMUM_LENGTH: "Agreguele al menos 8 caracteres a su contraseña",
    PasswordVulnerabilities.HAS_ASCENDING_SEQUENCE: "Elimine cualquier tipo de secuencias ascendentes de su contraseña",
    PasswordVulnerabilities.HAS_DESCENDING_SEQUENCE: "Elimine cualquier tipo de secuencias descendentes de su contraseña",
    PasswordVulnerabilities.HAS_UPPERCASE_LETTER: "Agreguele al menos una letra mayúscula a su contraseña",
    PasswordVulnerabilities.HAS_LOWERCASE_LETTER: "Agreguele al menos una letra minúscula a su contraseña",
    PasswordVulnerabilities.HAS_SPECIAL_CHARACTER: "Agreguele al menos un caracter especial a su contraseña",
    PasswordVulnerabilities.HAS_NUMBERS: "Agreguele al menos tres números a su contraseña",
    PasswordVulnerabilities.WITHOUT_VULNERABILITIES: "Sin sugerencias"
}

COLOR_SECURITY_STATUS: Dict[SecurityStatus, str] = {
    SecurityStatus.SAFE: "green",
    SecurityStatus.SOMEWHAT_SAFE: "yelow",
    SecurityStatus.UNSAFE: "orange",
    SecurityStatus.VERY_INSECURE: "red"
}