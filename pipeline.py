# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
# ============================================================
# FYP - Medical Document Analysis
# pipeline.py - Step 1: Verify all files are in correct place
# Student: Ayesha Sohail (U2386691)
# ============================================================

import os
import pandas as pd
from patterns import CBC_PATTERNS, LFT_PATTERNS, RFT_PATTERNS, BSG_PATTERNS, LIPID_PATTERNS

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
LABELS_PATH = os.path.join(BASE_DIR, "Labels", "Book1_Master_data.xlsx")
PDF_DIR     = os.path.join(BASE_DIR, "Data", "pdf_text")
IMAGE_DIR   = os.path.join(BASE_DIR, "Data", "images")

print("=" * 60)
print("FYP - Medical Document Analysis")
print("Step 1: Verifying all files...")
print("=" * 60)

df = pd.read_excel(LABELS_PATH, header=1)

found   = []
missing = []

for _, row in df.iterrows():
    doc_id    = str(row.iloc[0]).strip()
    file_type = str(row.iloc[7]).strip()

    if doc_id in ["nan", "", "doc_id"]:
        continue

    if file_type.upper() == "PDF":
        file_path = os.path.join(PDF_DIR, doc_id + ".pdf")
    elif file_type.upper() == "PNG":
        file_path = os.path.join(IMAGE_DIR, doc_id + ".png")
    elif file_type.upper() == "JPEG":
        file_path = os.path.join(IMAGE_DIR, doc_id + ".jpeg")
    else:
        file_path = None

    if file_path and os.path.exists(file_path):
        found.append(doc_id)
        print(f"  ✔  {doc_id}.{file_type.lower()}")
    else:
        missing.append(doc_id)
        print(f"  ✘  MISSING: {doc_id}.{file_type.lower()}")

print()
print("=" * 60)
print(f"  Total reports in CSV : {len(found) + len(missing)}")
print(f"  Found                : {len(found)}")
print(f"  Missing              : {len(missing)}")
print("=" * 60)

if len(missing) == 0:
    print("\n  All files verified! Ready to start extraction.")
else:
    print(f"\n  Fix missing files before proceeding!")

# ============================================================
# PHASE 1 - STEP 1: PDF Text Extraction using Apache Tika
# ============================================================

from tika import parser as tika_parser

EXTRACTED_TEXT_DIR = os.path.join(BASE_DIR, "extracted_text")

print("\n" + "=" * 60)
print("Phase 1: Extracting text from PDF files...")
print("=" * 60)

pdf_success = []
pdf_failed  = []

for _, row in df.iterrows():
    doc_id    = str(row.iloc[0]).strip()
    file_type = str(row.iloc[7]).strip()

    if doc_id in ["nan", "", "doc_id"]:
        continue
    if file_type.upper() != "PDF":
        continue

    pdf_path = os.path.join(PDF_DIR, doc_id + ".pdf")
    txt_path = os.path.join(EXTRACTED_TEXT_DIR, doc_id + ".txt")

    if os.path.exists(txt_path):
        print(f"  ⏭  SKIP: {doc_id}.txt already exists")
        pdf_success.append(doc_id)
        continue

    try:
        parsed   = tika_parser.from_file(pdf_path)
        raw_text = parsed.get("content", "")
        if raw_text and raw_text.strip():
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(raw_text.strip())
            pdf_success.append(doc_id)
            print(f"  ✔  {doc_id}.pdf → {doc_id}.txt")
        else:
            pdf_failed.append(doc_id)
            print(f"  ✘  EMPTY: {doc_id}.pdf (no text found)")
    except Exception as e:
        pdf_failed.append(doc_id)
        print(f"  ✘  ERROR: {doc_id}.pdf → {e}")

print()
print("=" * 60)
print(f"  PDFs processed successfully : {len(pdf_success)}")
print(f"  PDFs failed/empty           : {len(pdf_failed)}")
print("=" * 60)

# ============================================================
# PHASE 1 - STEP 2: Image OCR Extraction using Tesseract
# ============================================================

import pytesseract
from PIL import Image, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_and_ocr(image_path):
    img = Image.open(image_path)
    img = img.convert('L')
    w, h = img.size
    img = img.resize((w * 2, h * 2), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    return pytesseract.image_to_string(img, config='--oem 3 --psm 6')

print("\n" + "=" * 60)
print("Phase 1 - Step 2: Extracting text from images (OCR)...")
print("=" * 60)

img_success = []
img_failed  = []

for _, row in df.iterrows():
    doc_id    = str(row.iloc[0]).strip()
    file_type = str(row.iloc[7]).strip()

    if doc_id in ["nan", "", "doc_id"]:
        continue
    if file_type.upper() not in ["PNG", "JPEG"]:
        continue

    ext        = ".png" if file_type.upper() == "PNG" else ".jpeg"
    image_path = os.path.join(IMAGE_DIR, doc_id + ext)
    txt_path   = os.path.join(EXTRACTED_TEXT_DIR, doc_id + ".txt")

    if os.path.exists(txt_path):
        print(f"  ⏭  SKIP: {doc_id}.txt already exists")
        img_success.append(doc_id)
        continue

    try:
        raw_text = preprocess_and_ocr(image_path)
        if raw_text and raw_text.strip():
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(raw_text.strip())
            img_success.append(doc_id)
            print(f"  ✔  {doc_id}{ext} → {doc_id}.txt")
        else:
            img_failed.append(doc_id)
            print(f"  ✘  EMPTY: {doc_id}{ext} (no text found)")
    except Exception as e:
        img_failed.append(doc_id)
        print(f"  ✘  ERROR: {doc_id}{ext} → {e}")

print()
print("=" * 60)
print(f"  Images processed successfully : {len(img_success)}")
print(f"  Images failed/empty           : {len(img_failed)}")
print("=" * 60)
print("\n" + "=" * 60)
print("PHASE 1 COMPLETE — EXTRACTION SUMMARY")
print("=" * 60)
print(f"  PDFs extracted  : {len(pdf_success)}/30")
print(f"  Images extracted: {len(img_success)}/20")
print(f"  Total extracted : {len(pdf_success) + len(img_success)}/50")
print("=" * 60)

# ============================================================
# PHASE 2 - STEP 1: Text Cleaning
# ============================================================

import re
import json

EXTRACTED_FIELDS_DIR = os.path.join(BASE_DIR, "extracted_fields")

print("\n" + "=" * 60)
print("Phase 2 - Step 1: Cleaning extracted text...")
print("=" * 60)

def clean_text(raw_text):
    text = raw_text
    text = re.sub(r'\|', 'I', text)
    text = re.sub(r'\bnow\b', 'LOW', text, flags=re.IGNORECASE)
    text = re.sub(r'["""]', '"', text)
    text = re.sub(r"[''']", "'", text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

clean_success = []
clean_failed  = []

for txt_file in sorted(f for f in os.listdir(EXTRACTED_TEXT_DIR) if f.endswith(".txt")):
    txt_path = os.path.join(EXTRACTED_TEXT_DIR, txt_file)
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            raw = f.read()
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(clean_text(raw))
        clean_success.append(txt_file)
        print(f"  ✔  Cleaned: {txt_file}")
    except Exception as e:
        clean_failed.append(txt_file)
        print(f"  ✘  ERROR: {txt_file} → {e}")

print()
print("=" * 60)
print(f"  Files cleaned successfully : {len(clean_success)}")
print(f"  Files failed               : {len(clean_failed)}")
print("=" * 60)

# ============================================================
# PHASE 2 - STEP 2: Field Extraction using Regex + spaCy
# ============================================================

import spacy
nlp = spacy.load("en_core_web_sm")

print("\n" + "=" * 60)
print("Phase 2 - Step 2: Extracting fields from text...")
print("=" * 60)

def extract_patient_name(text, nlp):
    text_clean = re.sub(
        r'(?:Referred?\s*By|Doctor|Dr\.?|Physician|Consultant|'
        r'Pathologist|Biochemist|Nephrologist|Cardiologist|'
        r'Diabetologist|Endocrinologist)\s*[:\-].*',
        '', text, flags=re.IGNORECASE)

    noise_words = [
        'lab','laboratory','report','repo','collected','collection',
        'sample','test','date','age','sex','gender','male','female',
        're','pt','dob','id','ref','phone','tel','centre','center',
        'hospital','clinic','diagnostics','medcare','pathology',
        'premier','greenfield','nexacare','optima','glucocare',
        'serenova','vitapath','cardiocare','alnoor',
        'no','no.','shl','gcd','mcp','nxc','opt','vpl','ccd','phd',
        'result','status','order','byes','stan','agesex',
    ]
    reject_values = [
        'patient name','patient','name','sydney','london','toronto',
        'singapore','auckland','johannesburg','dubai','al razi',
        'street','road','avenue','tower','building','floor'
    ]
    patterns = [
        r"Patient\s*Name\s*\n\s*([A-Za-z][A-Za-z ]{2,35})",
        r"Patient\s*[:\-]?\s*\n\s*([A-Za-z][A-Za-z ]{2,35})",
        r"Patient\s*Name\s*[:\-]\s*([A-Za-z][A-Za-z ]{2,35})",
        r"(?<!\w)Name\s*[:\-]\s*([A-Za-z][A-Za-z ]{2,35})",
        r"Patient\s*[:\-]\s*([A-Za-z][A-Za-z ]{2,35})",
    ]
    for pattern in patterns:
        m = re.search(pattern, text_clean, re.IGNORECASE)
        if m:
            name = m.group(1).strip()
            if name.lower() in reject_values:
                continue
            if any(w in name.lower() for w in
                   ['street','road','avenue','tower','floor','suite',
                    'razi','harbour','wellness','medipoint']):
                continue
            words = name.split()
            clean_words = []
            for w in words:
                if w.lower() in noise_words:
                    break
                clean_words.append(w)
            name = ' '.join(clean_words).strip()
            if len(name) > 2:
                return name
    doc = nlp(text_clean[:300])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            if name.lower() not in reject_values and len(name) > 2:
                return name
    return "NOT_FOUND"


def extract_patient_gender(text):
    patterns = [
        r"(?:Sex|Gender)\s*[:\-]\s*(Male|Female|M|F)\b",
        r"\b(Male|Female)\b",
        r"(?:Sex|Gender)\s*[:\-]\s*([MF])\b",
        r"\d+\s*Year[s]?\s*/\s*(Male|Female)",
        r"\d+[YyMmDd/]+\s*/\s*([MF])\b",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            for g in [g for g in m.groups() if g is not None]:
                v = g.strip().upper()
                if v in ["M","MALE"]: return "Male"
                if v in ["F","FEMALE"]: return "Female"
    return "NOT_FOUND"


def extract_test_date(text):
    patterns = [
        r"(?:Collection|Collected|Sample\s*Date|Test\s*Date|Report\s*Date|Date)\s*[:\-]?\s*(\d{1,2}[\-/]\w{3,9}[\-/]\d{4})",
        r"(?:Collection|Collected|Sample\s*Date|Test\s*Date|Report\s*Date|Date)\s*[:\-]?\s*(\d{1,2}[\-/]\d{1,2}[\-/]\d{4})",
        r"(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})",
        r"\b(\d{1,2}[\-/]\w{3,9}[\-/]\d{4})\b",
        r"\b(\d{1,2}[\-/]\d{1,2}[\-/]\d{4})\b",
    ]
    for pattern in patterns:
        for match in re.findall(pattern, text, re.IGNORECASE):
            if len(re.sub(r'\D','',match)) <= 8:
                return match.strip()
    return "NOT_FOUND"


def extract_test_type(text, doc_id):
    dl = doc_id.lower()
    if "cbc" in dl: return "CBC"
    if "lft" in dl: return "LFT"
    if "rft" in dl: return "RFT"
    if "bsg" in dl: return "BSG"
    if "lip" in dl: return "Lipid"
    tu = text.upper()
    if any(x in tu for x in ["COMPLETE BLOOD COUNT","HAEMOGLOBIN","HEMOGLOBIN","PLATELETS","NEUTROPHIL"]): return "CBC"
    if any(x in tu for x in ["LIVER FUNCTION","ALT","AST","BILIRUBIN","SGPT","SGOT"]): return "LFT"
    if any(x in tu for x in ["RENAL FUNCTION","CREATININE","UREA","EGFR","URIC ACID"]): return "RFT"
    if any(x in tu for x in ["GLUCOSE","HBA1C","BLOOD SUGAR","FASTING","INSULIN","DIABETES"]): return "BSG"
    if any(x in tu for x in ["LIPID","CHOLESTEROL","TRIGLYCERIDE","HDL","LDL","VLDL"]): return "Lipid"
    return "NOT_FOUND"


def extract_lab_name(text):
    top = text[:300]
    for pattern in [
        r"([A-Z][A-Za-z\s&]{4,40}(?:Laboratory|Laboratories|Diagnostics|Pathology|Lab\b))",
        r"([A-Z][A-Za-z\s&]{4,40}(?:Hospital|Medical\s*Center|Health\s*Centre|Clinic))",
    ]:
        m = re.search(pattern, top, re.IGNORECASE | re.MULTILINE)
        if m:
            lab = re.sub(r'\s*\n+\s*', ' ', m.group(1)).strip()
            if len(lab) < 60:
                return lab
    return "NOT_FOUND"


def extract_value(text, param_patterns):
    for pattern in param_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            val = m.group(1).strip()
            if re.match(r'^\d+\.?\d*$', val):
                return val
    return "NOT_FOUND"


def extract_medical_values(text, test_type):
    values = {}
    if test_type == "CBC":
        patterns_map = CBC_PATTERNS
    elif test_type == "LFT":
        patterns_map = LFT_PATTERNS
    elif test_type == "RFT":
        patterns_map = RFT_PATTERNS
    elif test_type == "BSG":
        patterns_map = BSG_PATTERNS
    elif test_type == "Lipid":
        patterns_map = LIPID_PATTERNS
    else:
        return values

    for param_name, param_patterns in patterns_map.items():
        values[param_name] = extract_value(text, param_patterns)

    return values

# ── Process all 50 files ─────────────────────────────────────
extract_success = []
extract_failed  = []

for _, row in df.iterrows():
    doc_id = str(row.iloc[0]).strip()
    if doc_id in ["nan", "", "doc_id"]:
        continue

    txt_path  = os.path.join(EXTRACTED_TEXT_DIR, doc_id + ".txt")
    json_path = os.path.join(EXTRACTED_FIELDS_DIR, doc_id + ".json")

    if not os.path.exists(txt_path):
        print(f"  ✘  MISSING txt: {doc_id}.txt")
        extract_failed.append(doc_id)
        continue

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        source_type = "NOT_FOUND"
        for col in df.columns:
            if "source" in str(col).lower():
                source_type = str(row[col]).strip()
                break

        test_type = extract_test_type(text, doc_id)

        result = {
            "doc_id":         doc_id,
            "source_type":    source_type,
            "patient_name":   extract_patient_name(text, nlp),
            "patient_gender": extract_patient_gender(text),
            "test_date":      extract_test_date(text),
            "test_type":      test_type,
            "lab_name":       extract_lab_name(text),
            "medical_values": extract_medical_values(text, test_type),
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        extract_success.append(doc_id)
        print(f"  ✔  {doc_id} → "
              f"name={result['patient_name'][:12]:12} | "
              f"gender={result['patient_gender']:6} | "
              f"date={result['test_date']:12} | "
              f"type={result['test_type']}")

    except Exception as e:
        extract_failed.append(doc_id)
        print(f"  ✘  ERROR: {doc_id} → {e}")

print()
print("=" * 60)
print(f"  Fields extracted successfully : {len(extract_success)}")
print(f"  Failed                        : {len(extract_failed)}")
print("=" * 60)

# ============================================================
# SINGLE FILE MODE 
# Usage: python pipeline.py "path/to/file.pdf"
# ============================================================

import sys

if len(sys.argv) > 1:
    single_file_path = sys.argv[1]
    selected_type_arg = sys.argv[2] if len(sys.argv) > 2 else ""

    if not os.path.exists(single_file_path):
        print(f"ERROR: File not found: {single_file_path}")
        sys.exit(1)

    ext    = os.path.splitext(single_file_path)[1].lower()
    doc_id = os.path.splitext(os.path.basename(single_file_path))[0]
    doc_id = re.sub(r'[^a-zA-Z0-9_-]', '_', doc_id)

    print("\n" + "=" * 60)
    print(f"SINGLE FILE MODE: {doc_id}{ext}")
    print("=" * 60)

    txt_path  = os.path.join(EXTRACTED_TEXT_DIR, doc_id + ".txt")
    json_path = os.path.join(EXTRACTED_FIELDS_DIR, doc_id + ".json")

    # Step 1: Extract text
    try:
        if ext == ".pdf":
            from tika import parser as tika_parser
            parsed   = tika_parser.from_file(single_file_path)
            raw_text = parsed.get("content", "")
        elif ext in [".png", ".jpg", ".jpeg"]:
            raw_text = preprocess_and_ocr(single_file_path)
        else:
            print(f"ERROR: Unsupported file type: {ext}")
            sys.exit(1)

        if not raw_text or not raw_text.strip():
            print("ERROR: No text extracted from file")
            sys.exit(1)

        # Clean and save text
        cleaned = clean_text(raw_text.strip())
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"  Text extracted: {len(cleaned)} characters")

    except Exception as e:
        print(f"ERROR during extraction: {e}")
        sys.exit(1)

    # Step 2: Extract fields
    try:
        # Use user-selected type if provided, otherwise auto-detect
        if selected_type_arg and selected_type_arg in ["CBC","LFT","RFT","BSG","Lipid","Other"]:
            test_type = selected_type_arg
            print(f"  test_type:  {test_type} (user selected)")
        else:
            test_type = extract_test_type(cleaned, doc_id)
            print(f"  test_type:  {test_type} (auto detected)")

        result = {
            "doc_id":         doc_id,
            "source_type":    "user_upload",
            "patient_name":   extract_patient_name(cleaned, nlp),
            "patient_gender": extract_patient_gender(cleaned),
            "test_date":      extract_test_date(cleaned),
            "test_type":      test_type,
            "lab_name":       extract_lab_name(cleaned),
            "medical_values": extract_medical_values(cleaned, test_type),
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"  Fields extracted successfully")
        print(f"  test_type:  {result['test_type']}")
        print(f"  patient:    {result['patient_name']}")
        print(f"  JSON saved: {json_path}")
        print("=" * 60)
        print("SINGLE FILE EXTRACTION COMPLETE")
        print("=" * 60)

    except Exception as e:
        print(f"ERROR during field extraction: {e}")
        sys.exit(1)