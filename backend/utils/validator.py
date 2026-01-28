from email_validator import validate_email

def validate_email_address(email: str) -> str | None:
    """EmailNotValidError is raised if the email is not valid.
    Otherwise, return email address"""
    valid = validate_email(email, check_deliverability=False)
    return valid.email