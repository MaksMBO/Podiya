from django.core.exceptions import ValidationError


def luhn_checksum(card_number: str) -> int:
    """Calculates the checksum using the Luna algorithm for the card number."""

    def digits_of(string_of_numbers: str or int) -> list[int]:
        """Converts a number to a list of its digits."""
        return [int(one_digit) for one_digit in str(string_of_numbers)]

    digits = digits_of(card_number)
    # Divide the digits into even and odd, counting from the end
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    # Calculate the checksum
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def is_luhn_valid(card_number: str) -> bool:
    """Checks whether the card number is valid according to the Luna algorithm."""
    return luhn_checksum(card_number) == 0


def validate_card_number(value: str) -> None:
    """Checks the validity of the card number and returns the last 4 digits."""
    if not is_luhn_valid(value):
        raise ValidationError(
            f'{value[-4:]} не є дійсним номером кредитної картки'
        )
