import random
import string

_pool = string.ascii_lowercase + string.digits

def generate_short_code(length: int = 7) -> str:
    """
    generating short url code
    """    
    return "".join(random.choice(_pool) for _ in range(length))


