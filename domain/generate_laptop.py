import random
from datetime import datetime
from uuid import uuid4

constructors = ["Apple", "Lenovo", "Microsoft"]
models = {
    "Apple": ["MacBookPro", "MacBookAir", "MacBook", "iMac"],
    "Lenovo": ["Thinkpad", "Yoga", "IdeaPad"],
    "Microsoft": ["Surface", "Surface Pro"],
}


def generate_laptop() -> dict:
    """Function used to generate a small dummy dict object"""
    constructor: str = random.choice(constructors)
    model: str = random.choice(models[constructor])

    return {
        "uuid": uuid4(),
        "constructor": constructor,
        "model": model,
        "year": random.randint(2010, 2024),
        "timestamp": datetime.now(),
    }
