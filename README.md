# 🛠 Smart Pricing Engine — Full Bathroom Renovation

## 📌 Objective

Transform a messy renovation voice transcript into a **structured, professional JSON renovation quote**  using modular Python logic.

Example input transcript:

> "Client wants to renovate a small 4m² bathroom. They’ll remove the old tiles, redo the plumbing for the shower, replace the toilet, install a vanity, repaint the walls, and lay new ceramic floor tiles. Budget-conscious. Located in Marseille."

---

## 🗂 Project Structure

bathroom-pricing-engine/
│
├── pricing_engine.py # Main script orchestrating parsing and pricing
├── pricing_logic/
│ ├── material_db.py # Material costs by city/task
│ ├── labor_calc.py # Labor hours and hourly cost logic
│ ├── vat_rules.py # VAT rules per task and city context
│ ├── transcript_parser.py # Parses messy transcript into structured data
│ ├── feedback.py # Feedback loop: adjusts margins by quote acceptance
│ ├── vector_memory.py # (Bonus) Vector search for past similar quotes
│ └── supplier_api.py # (Bonus) Simulated real-time supplier price updates
│
├── data/
│ ├── materials.json # Material cost database
│ ├── price_templates.csv # (Optional) template pricing data
│ └── input_transcript.txt # Transcript input file
│
├── output/
│ └── sample_quote.json # Generated structured quote JSON
│
├── tests/
│ └── test_logic.py # Unit/integration tests
│
├── README.md


---

## 🚀 How to Run

1. **Clone the repository:**
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>


2. **Create and activate a virtual environment:**
python -m venv venv

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate


3. **Install dependencies:**
pip install -r requirements.txt

4. **Edit transcript:**
Update `data/input_transcript.txt` with your messy renovation job transcript.

5. **Run the engine:**
python pricing_engine.py


6. **Check results:**
- Open `output/sample_quote.json` for the generated structured quote.
- Terminal output will also show any similar past quotes from vector memory.

---

## 📄 Output JSON Schema

The generated JSON contains:

- `zone`: Renovation area (e.g., `"bathroom"`)
- `city`: City of the job
- `size_m2`: Size in square meters
- `tasks`: Array of task objects:
- `name`: Task/material name
- `labor`: `{hours, cost}`
- `materials`: `{item, cost}`
- `estimated_duration_hr`
- `vat_rate`: VAT %
- `subtotal`: Pre-margin, pre-VAT cost
- `margin`: Profit margin value
- `total_price`: Final total including margin + VAT
- `confidence`: Task-level parsing confidence
- `overall_total`: Total project cost
- `overall_margin`: Total margin amount
- `confidence_score`: Global parsing confidence
- `quote_id`: Unique ID (UUID format)

---

### Example Output (shortened)
{
"zone": "bathroom",
"city": "Marseille",
"size_m2": 4.0,
"tasks": [
{
"name": "Ceramic Floor Tiles",
"labor": {"hours": 6.0, "cost": 180.0},
"materials": {"item": "Ceramic Floor Tiles", "cost": 80.0},
"estimated_duration_hr": 6.0,
"vat_rate": 10,
"subtotal": 260.0,
"margin": 39.0,
"total_price": 328.9,
"confidence": 0.95
}
],
"overall_total": 1237.5,
"overall_margin": 145.65,
"confidence_score": 1.0,
"quote_id": "uuid-here"
}


---

## 💡 Pricing & Margin Logic

1. **Materials** — Price from `materials.json`, adjusted for city.
2. **Labor** — Hours & rate from `labor_calc.py`.
3. **Subtotal** = Materials + Labor.
4. **Margin** — Added as % of subtotal (adjusted via feedback loop).
5. **VAT** — Task-specific % from `vat_rules.py`.
6. **Total Price** = Subtotal + Margin + VAT.
7. **Overall totals** are sum of all tasks.
8. **Confidence score** — Drops if missing key details.

---

## ⚠ Assumptions / Edge Cases

- Default city = Marseille if not found in transcript.
- Missing size reduces confidence score.
- Unknown tasks skipped or priced with defaults.
- Vector search results require at least one stored past quote.

---

## ✨ Bonus Features Implemented

- ✅ **City-based pricing variation**
- ✅ **Feedback loop** — adjusts margins based on accept/reject history
- ✅ **Vector memory (ChromaDB)** — retrieve similar past quotes
- ✅ **Confidence scoring** — lower if size/city/tasks missing
- ✅ **Supplier API simulation** — ±10% fluctuation in material prices

---

## 📈 Future Improvements

- Real supplier API integration
- Use ML/NLP models for smarter parsing beyond keywords
- Multi-zone project support
- Web UI built on top of the engine

---

## 🧪 Running Tests

From the project root:
pytest tests/

Or to run a single file:
python tests/test_logic.py


---

## 🧑‍💻 Author

**Ananya Tiwari**  
Gmail: ananyatiwari1508@gmail.com

