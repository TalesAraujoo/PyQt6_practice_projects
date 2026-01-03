def validate_expense_input(amount_text: str, description: str):
    errors = {}

    # Amount validation
    try:
        amount = float(amount_text)
        if amount < 0:
            errors["amount"] = 'Amount must be greater than zero'
    except ValueError:
        errors["amount"] = 'Amount must be a valid number'

    # description validation
    if not description:
        errors["description"] = "Description is required"

    return errors
    