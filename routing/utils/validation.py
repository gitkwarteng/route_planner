import re

def is_valid_us_address(address:str)-> bool:
    """Check if the given address is a valid US address.

    Args:
        address (str): The address to check.

    Returns:
        bool: True if the address is valid, False otherwise.
    """
    if not address:
        return False

    us_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    }

    pattern = r'^[\w\s]+,\s*([A-Z]{2})(?:,\s*(?:USA|US))?$'
    match = re.match(pattern, address.strip(), re.IGNORECASE)

    if not match:
        return False

    state = match.group(1).upper()
    return state in us_states