# pricing_logic/labor_calc.py
"""
Labor calculation module
- Returns estimated labor hours and cost for a given task & city
"""

# Hourly labor rates by city (EUR/hour)
LABOR_RATES = {
    "Marseille": 30,
    "Paris": 40
}

# Estimated hours per task type (per unit basis)
TASK_HOURS = {
    "tile_removal": 1.0,   # hours per sqm
    "tiling": 1.5,         # hours per sqm
    "plumbing": 5.0,       # fixed hours for job
    "toilet_installation": 3.0,  # fixed hours
    "vanity_installation": 2.5,  # fixed hours
    "painting": 0.5        # hours per sqm
}

def estimate_labor(task_code, size, city):
    """
    Estimate labor hours and cost for a given task.
    :param task_code: str, e.g. 'tile_removal', 'plumbing'
    :param size: float, size in sqm (or 1 if fixed job)
    :param city: str, e.g. 'Marseille'
    :return: (hours, cost)
    """
    if task_code not in TASK_HOURS:
        raise ValueError(f"Unknown task: {task_code}")

    hours_per_unit = TASK_HOURS[task_code]
    if task_code in ["plumbing", "toilet_installation", "vanity_installation"]:
        total_hours = hours_per_unit  # fixed job
    else:
        total_hours = size * hours_per_unit  # per sqm

    hourly_rate = LABOR_RATES.get(city, LABOR_RATES["Marseille"])
    cost = total_hours * hourly_rate

    return total_hours, round(cost, 2)
