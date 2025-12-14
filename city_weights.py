import pandas as pd

def get_city_weights():
    """
    Approximate demand influence by city
    (can be justified via population + e-commerce penetration)
    """
    return {
        "Jaipur": 0.95,
        "Indore": 0.85,
        "Kochi": 0.80,
        "Surat": 0.90,
        "Coimbatore": 0.82
    }
