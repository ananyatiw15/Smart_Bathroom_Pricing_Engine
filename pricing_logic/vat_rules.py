# pricing_logic/vat_rules.py

# Task-specific VAT rates (in percent)
VAT_RATES = {
    "tile_removal": 10,
    "tiling": 10,
    "plumbing": 10,
    "toilet_installation": 10,
    "vanity_installation": 10,
    "painting": 10
}

DEFAULT_VAT = 20  # fallback for unknown tasks

def get_vat_rate(task_code, city=None):
    """
    Return VAT percent for the task.
    """
    return VAT_RATES.get(task_code, DEFAULT_VAT)
