import random
import string

BASE_URL = "https://www.saucedemo.com"

CREDENTIALS = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked": {"username": "locked_out_user", "password": "secret_sauce"},
    "problem": {"username": "problem_user", "password": "secret_sauce"},
    "performance": {"username": "performance_glitch_user", "password": "secret_sauce"},
	"error": {"username": "error_user", "password": "secret_sauce"},
	"visual": {"username": "visual_user", "password": "secret_sauce"},
}


DATA = {
    "valid_checkout": {
        "first_name": "Juan",
        "last_name": "Pérez",
        "zip_code": "C1425"
    },
    "random_checkout": lambda: {
        "first_name": ''.join(random.choices(string.ascii_letters, k=8)),
        "last_name": ''.join(random.choices(string.ascii_letters, k=10)),
        "zip_code": ''.join(random.choices(string.digits, k=5))
    }
}