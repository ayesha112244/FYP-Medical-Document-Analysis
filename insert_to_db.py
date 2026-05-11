# ============================================================
# FYP - Medical Document Analysis
# insert_to_db.py - Phase 4: Insert JSON data into MySQL
# Student: Ayesha Sohail (U2386691)
# ============================================================

import os
import json
import mysql.connector

# ── Paths ─────────────────────────────────────────────────
BASE_DIR             = os.path.dirname(os.path.abspath(__file__))
EXTRACTED_FIELDS_DIR = os.path.join(BASE_DIR, "extracted_fields")

# ── Database Connection ────────────────────────────────────
conn = mysql.connector.connect(
    host     = "localhost",
    user     = "root",
    password = "",          # XAMPP default = no password
    database = "fyp_medical"
)
cursor = conn.cursor()

print("=" * 60)
print("FYP - Phase 4: Inserting data into MySQL")
print("=" * 60)

# ── Admin user_id = 2 ─────────────────────────────────────
# Insert IGNORE — agar already exist karta hai to skip
cursor.execute("""
    INSERT IGNORE INTO users (id, name, email, password)
    VALUES (2, 'Admin', 'admin@fyp.com', 'admin123')
""")
conn.commit()

success = 0
failed  = 0

json_files = sorted([
    f for f in os.listdir(EXTRACTED_FIELDS_DIR)
    if f.endswith(".json")
])

for json_file in json_files:
    json_path = os.path.join(EXTRACTED_FIELDS_DIR, json_file)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        doc_id         = data.get("doc_id", "")
        source_type    = data.get("source_type", "")
        patient_name   = data.get("patient_name", "NOT_FOUND")
        patient_gender = data.get("patient_gender", "NOT_FOUND")
        test_date      = data.get("test_date", "NOT_FOUND")
        test_type      = data.get("test_type", "NOT_FOUND")
        lab_name       = data.get("lab_name", "NOT_FOUND")
        medical_values = data.get("medical_values", {})

        # Determine file_type from doc_id
        if "_img" in doc_id.lower():
            file_type = "JPEG" if "jpeg" in doc_id.lower() else "PNG"
        else:
            file_type = "PDF"

        # ── Insert into reports table ──────────────────────
        cursor.execute("""
            INSERT INTO reports
            (user_id, doc_id, patient_name, patient_gender,
             test_date, test_type, lab_name, source_type, file_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            2, doc_id, patient_name, patient_gender,
            test_date, test_type, lab_name, source_type, file_type
        ))

        report_id = cursor.lastrowid

        # ── Insert into medical_values table ───────────────
        for param_name, param_value in medical_values.items():
            cursor.execute("""
                INSERT INTO medical_values
                (report_id, param_name, param_value)
                VALUES (%s, %s, %s)
            """, (report_id, param_name, str(param_value)))

        conn.commit()
        success += 1
        print(f"  ✔  {doc_id} inserted (report_id={report_id},"
              f" params={len(medical_values)})")

    except Exception as e:
        conn.rollback()
        failed += 1
        print(f"  ✘  ERROR: {json_file} → {e}")

cursor.close()
conn.close()

print()
print("=" * 60)
print(f"  Successfully inserted : {success}")
print(f"  Failed                : {failed}")
print(f"  Total                 : {success + failed}")
print("=" * 60)
print("\n  Database population complete!")
print("  Check phpMyAdmin to verify data.")
