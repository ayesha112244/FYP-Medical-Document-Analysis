import re

text = """HAEMOGLOBIN (Hb) 10.2 L g/dL Male: 13.0–17.0"""

patterns = [
    r"HAEMOGLOBIN\s*\([^)]*\)\s+(\d+\.?\d*)\s+[HLN]\b",
    r"H[ae]moglobin\s*\([^)]*\)\s+(\d+\.?\d*)",
    r"H[ae]moglobin\s+(\d+\.?\d*)\s+[HLN]\b",
    r"H[ae]moglobin\s+(\d+\.?\d*)",
]

for p in patterns:
    m = re.search(p, text, re.IGNORECASE)
    print(f"Pattern: {p[:50]}")
    print(f"Result:  {m.group(1) if m else 'NOT FOUND'}")
    print()