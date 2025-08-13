# pricing_logic/transcript_parser.py
import re
import difflib

# Keywords mapped to task codes and materials
TASK_KEYWORDS = {
    "remove old tiles": ("tile_removal", "tile_removal_supplies"),
    "tile removal": ("tile_removal", "tile_removal_supplies"),
    "tiling": ("tiling", "tiles"),
    "ceramic floor tiles": ("tiling", "tiles"),
    "redo the plumbing": ("plumbing", "plumbing_kit"),
    "plumbing": ("plumbing", "plumbing_kit"),
    "replace the toilet": ("toilet_installation", "toilet"),
    "toilet": ("toilet_installation", "toilet"),
    "install a vanity": ("vanity_installation", "vanity"),
    "vanity": ("vanity_installation", "vanity"),
    "repaint the walls": ("painting", "paint"),
    "painting": ("painting", "paint")
}

CITIES = ["Marseille", "Paris"]

def parse_transcript(text):
    text_lower = text.lower()

    # --- Detect size ---
    size_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:m²|m2)', text_lower)
    size_m2 = float(size_match.group(1)) if size_match else 0

    # --- Detect city ---
    city = None
    for c in CITIES:
        if c.lower() in text_lower:
            city = c
            break
    if not city:
        city = "Marseille"

    # --- Detect tasks (fuzzy matching) ---
    tasks = []
    matches_found = 0
    for phrase, (task_code, material) in TASK_KEYWORDS.items():
        # Use ratio for fuzzy match
        ratio = difflib.SequenceMatcher(None, phrase, text_lower).ratio()
        if phrase in text_lower or ratio > 0.75:
            tasks.append({"code": task_code, "material": material})
            matches_found += 1

    # Remove duplicates (same task_code from multiple matches)
    unique_tasks = {t["code"]: t for t in tasks}
    tasks = list(unique_tasks.values())

    # --- Confidence scoring ---
    confidence = 1.0
    if size_m2 == 0:
        confidence -= 0.2
    if matches_found < len(TASK_KEYWORDS) * 0.3:
        confidence -= 0.2
    if matches_found == 0:
        confidence -= 0.4
    confidence = max(0, round(confidence, 2))

    return {
        "size_m2": size_m2,
        "city": city,
        "tasks": tasks,
        "confidence": confidence
    }
