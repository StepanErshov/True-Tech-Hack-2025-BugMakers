import requests
import logging
from typing import Literal

KEY_PHONE = "b35b3b2cd044b762e804b2e4096ea654"
def valid_phone_number(
    phone_number: str, country_code: Literal["RU", "US", "KZ", "BY"] = "RU"
):
    response = requests.get(
        f"http://apilayer.net/api/validate?access_key={KEY_PHONE}&number={phone_number}&format=1&country_code={country_code}"
    )

    if response.status_code == 200:
        logging.info(f"{response.status_code}")
        return response.json()
    else:
        logging.error(f"Error: {response.status_code}")
        logging.error(response.text)
