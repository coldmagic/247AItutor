# Server/payfast.py

import hashlib
import urllib.parse

def generate_signature(data: dict, passphrase: str = '') -> str:
    """
    This function generates a PayFast security signature.
    """
    data_items = data.items()
    data_str = '&'.join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in data_items if v)
    if passphrase:
        data_str += f"&passphrase={passphrase}"

    return hashlib.md5(data_str.encode()).hexdigest()
  
