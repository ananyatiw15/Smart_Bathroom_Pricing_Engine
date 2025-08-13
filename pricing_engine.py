import json
import uuid

from pricing_logic.labor_calc import estimate_labor
from pricing_logic.vat_rules import get_vat_rate
from pricing_logic.transcript_parser import parse_transcript
from pricing_logic.feedback import save_feedback, adjust_margin
from pricing_logic.vector_memory import add_quote_to_memory, search_similar_quotes
from pricing_logic.supplier_api import get_live_material_price

# === Load Materials Database ===
with open("data/materials.json", "r", encoding="utf-8") as f:
    MATERIALS = json.load(f)

# === Read Transcript from File (UTF-8 to fix encoding issues) ===
with open("data/input_transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

# === Parse Transcript ===
parsed = parse_transcript(transcript)
city = parsed["city"]
size_m2 = parsed["size_m2"]
tasks = parsed["tasks"]
confidence_score = parsed["confidence"]

# === Generate Quote ID & Adjust Margin from Feedback ===
quote_id = str(uuid.uuid4())
MARGIN_PERCENT = adjust_margin(15)  # base margin 15%

# === Build the Quote Structure ===
quote = {
    "quote_id": quote_id,
    "zone": "bathroom",
    "city": city,
    "size_m2": size_m2,
    "tasks": [],
    "overall_total": 0,
    "overall_margin": 0,
    "confidence_score": confidence_score
}

# === Calculate Costs for Each Task ===
for t in tasks:
    # Materials
    mat_info = MATERIALS[t["material"]]
    unit_price = mat_info["base_price"][city]
    unit_price = get_live_material_price(mat_info["name"], unit_price)  # simulate supplier API
    
    if mat_info["unit"] == "sqm":
        material_cost = size_m2 * unit_price
    else:
        material_cost = unit_price

    # Labor
    hours, labor_cost = estimate_labor(t["code"], size_m2, city)

    # VAT
    vat_rate = get_vat_rate(t["code"], city)

    # Pricing calculations
    subtotal = labor_cost + material_cost
    margin_value = subtotal * (MARGIN_PERCENT / 100)
    subtotal_with_margin = subtotal + margin_value
    total_price = subtotal_with_margin * (1 + vat_rate / 100)

    # Append task entry
    quote["tasks"].append({
        "name": mat_info["name"],
        "labor": {"hours": round(hours, 2), "cost": round(labor_cost, 2)},
        "materials": {"item": mat_info["name"], "cost": round(material_cost, 2)},
        "estimated_duration_hr": round(hours, 2),
        "vat_rate": vat_rate,
        "subtotal": round(subtotal, 2),
        "margin": round(margin_value, 2),
        "total_price": round(total_price, 2),
        "confidence": confidence_score
    })

    quote["overall_total"] += total_price
    quote["overall_margin"] += margin_value

# Round totals
quote["overall_total"] = round(quote["overall_total"], 2)
quote["overall_margin"] = round(quote["overall_margin"], 2)

# === Save Output JSON ===
with open("output/sample_quote.json", "w", encoding="utf-8") as f:
    json.dump(quote, f, indent=4)

print(f"Quote generated → output/sample_quote.json (Margin used: {MARGIN_PERCENT}%)")

# === Save Feedback (Simulate 'accepted' quote) ===
save_feedback(quote_id, accepted=True)

# === Store in Vector Memory ===
add_quote_to_memory(quote_id, transcript, quote)

# === Search for Similar Quotes ===
search_query = "renovate 5m² bathroom in Paris with tiling"
similar = search_similar_quotes(search_query)
print("\n🔍 Similar quotes found in memory:")

if similar.get("ids") and similar["ids"][0]:
    for idx, sim_id in enumerate(similar["ids"][0]):
        meta = similar["metadatas"][0][idx]
        
        print(f"\n--- Match {idx+1} ---")
        print(f"Quote ID       : {meta.get('quote_id')}")
        print(f"City           : {meta.get('city')}")
        print(f"Overall Total  : €{meta.get('overall_total')}")
        print(f"Confidence     : {meta.get('confidence_score')}")
        
        # Parse the stored JSON string
        try:
            stored_quote = json.loads(meta.get("quote_json", "{}"))
            print("Tasks:")
            for task in stored_quote.get("tasks", []):
                print(f"  - {task['name']}: €{task['total_price']} (VAT {task['vat_rate']}%)")
        except json.JSONDecodeError:
            print("⚠ Could not parse stored quote JSON.")
else:
    print("No similar quotes found.")
