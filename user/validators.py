from django.core.exceptions import ValidationError


def validate_password_strength(password):
    """Validate that a password is at least 8 characters long and contains at least one uppercase letter, one lowercase letter, and one digit."""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit.")
    if not any(char.islower() for char in password):
        raise ValidationError(
            "Password must contain at least one lowercase letter.")
    if not any(char.isupper() for char in password):
        raise ValidationError(
            "Password must contain at least one uppercase letter.")
    if len(password) > 32:
        raise ValidationError("Password must be less than 32 characters long.")
