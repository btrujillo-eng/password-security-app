from backend.app.schemas import PasswordBase, PasswordAnalyzed
from backend.app.core import(
    IPasswordAnalyzer, get_lowercase_letter, get_capital_letter, get_ascending_sequence,
    get_descending_sequence, get_special_character, get_minimum_length, get_numbers
)
class PasswordAnalyzer(IPasswordAnalyzer):
    def analyze(self, password: PasswordBase) -> PasswordAnalyzed:
        """Analyzes the security of a provided password.

        Args:
            password (PasswordBase): Password that will be subject to security analysis

        Returns:
            PasswordAnalyzed: Raw data (Booleans True-False) which contain information about
                the password.
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