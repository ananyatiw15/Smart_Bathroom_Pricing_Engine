# pricing_logic/supplier_api.py

import random

def get_live_material_price(material_name, base_price):
    """
    Simulate fetching up-to-date price from a supplier API.
    This demo randomly fluctuates ±10%.
    """
    fluctuation = random.uniform(-0.1, 0.1)  # -10% to +10%
    updated_price = base_price * (1 + fluctuation)
    return round(updated_price, 2)
