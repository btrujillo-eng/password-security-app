from backend.app.schemas import PasswordBase, PasswordAnalyzed
from backend.app.core import(
    IPasswordAnalyzer, get_lowercase_letter, get_capital_letter, get_ascending_sequence,
    get_descending_sequence, get_special_character, get_minimum_length, get_numbers
)
class PasswordAnalyzer(IPasswordAnalyzer):
    async def analyze(self, password: PasswordBase) -> PasswordAnalyzed:
        """
        Analyzes a provided password and returns raw data (Booleans True-False) about the password's security.
        """
        return PasswordAnalyzed(
            minimum_length=get_minimum_length(password),
            ascending_sequence=get_ascending_sequence(password),
            descending_sequence=get_descending_sequence(password),
            capital_letter=get_capital_letter(password),
            lowercase_letter=get_lowercase_letter(password),
            special_character=get_special_character(password),
            numbers=get_numbers(password)
        )