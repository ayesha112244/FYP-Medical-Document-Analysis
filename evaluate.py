# ============================================================
# FYP - Medical Document Analysis
# evaluate.py - Phase 3: Evaluation
# Student: Ayesha Sohail (U2386691)
# ============================================================

import os
import json
import pandas as pd

# ── Paths ────────────────────────────────────────────────────
BASE_DIR             = os.path.dirname(os.path.abspath(__file__))
LABELS_PATH          = os.path.join(BASE_DIR, "Labels", "Book1_Master_data.xlsx")
EXTRACTED_FIELDS_DIR = os.path.join(BASE_DIR, "extracted_fields")

print("=" * 60)
print("FYP - Phase 3: Evaluation")
print("=" * 60)

# ── Load Master CSV ──────────────────────────────────────────
df = pd.read_excel(LABELS_PATH, header=1)

# ── CSV Column → JSON Field Mapping ─────────────────────────
FIELD_MAP = {
    "patient_name":   "patient_name",
    "patient_gender": "sex",
    "test_date":      "test_date",
    "test_type":      "test_type",
    "Haemoglobin":  "Hb_value",
    "RBC":          "RBC_value",
    "WBC":          "WBC_value",
    "Platelets":    "Platelets_value",
    "MCV":          "MCV_value",
    "MCH":          "MCH_value",
    "PCV_HCT":      "PCV_HCT_value",
    "MCHC":         "MCHC_value",
    "RDW":          "RDW_value",
    "Neutrophils":  "Neutrophils_value",
    "Lymphocytes":  "Lymphocytes_value",
    "ALT":              "ALT/SGPT_value",
    "AST":              "AST/SGO_value",
    "Bilirubin_Total":  "Bilirubin_Total_value",
    "ALP":              "ALP_value",
    "Albumin":          "Albumin_value",
    "GGT":              "GGT_value",
    "Creatinine":   "Creatinine_value",
    "Urea":         "Urea_BUN_value",
    "Uric_Acid":    "Uric_Acid_value",
    "eGFR":         "eGFR_value",
    "Fasting_Glucose":  "Fasting_Glucose_value",
    "HbA1c":            "HbA1c_value",
    "Random_Glucose":   "Random_Glucose_value",
    "Total_Cholesterol": "Total_Cholesterol_value",
    "HDL":               "HDL_value",
    "LDL":               "LDL_value",
    "Triglycerides":     "Triglycerides_value",
    "VLDL":              "VLDL_value",
}

# ── Helper Functions ─────────────────────────────────────────

def is_na(val):
    """Check if value is N/A, None, or empty"""
    if val is None:
        return True
    s = str(val).strip().upper()
    return s in ["N/A", "NA", "NAN", "", "-", "NONE"]


def normalize_date(val):
    """Normalize date string to DD-Mon-YYYY for comparison"""
    import re
    from datetime import datetime

    s = str(val).strip()
    s = re.sub(r'\s+\d{2}:\d{2}:\d{2}$', '', s).strip()
    month_fix = {
        'January':'Jan','February':'Feb','March':'Mar',
        'April':'Apr','June':'Jun','July':'Jul',
        'August':'Aug','September':'Sep','October':'Oct',
        'November':'Nov','December':'Dec'
    }
    for full, short in month_fix.items():
        s = s.replace(full, short)
    formats = [
        "%d-%b-%Y", "%d/%m/%Y", "%d-%m-%Y",
        "%Y-%m-%d", "%d/%b/%Y", "%d %b %Y",
        "%d-%b-%y", "%m/%d/%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).strftime("%d-%b-%Y")
        except ValueError:
            continue
    return s.lower()


def compare_values(extracted, ground_truth, tolerance=0.15):
    """Compare extracted vs ground truth."""
    from datetime import datetime

    if is_na(ground_truth):
        return "SKIP"

    if str(extracted).strip().upper() == "NOT_FOUND":
        return "WRONG"

    gt_str  = str(ground_truth).strip()
    ext_str = str(extracted).strip()

    if any(c in gt_str for c in ['-', '/']):
        try:
            norm_ext = normalize_date(ext_str)
            norm_gt  = normalize_date(gt_str)
            if norm_ext == norm_gt:
                return "CORRECT"
            try:
                d1 = datetime.strptime(norm_ext, "%d-%b-%Y")
                d2 = datetime.strptime(norm_gt,  "%d-%b-%Y")
                if abs((d1 - d2).days) <= 1:
                    return "CORRECT"
            except ValueError:
                pass
        except Exception:
            pass

    try:
        ext_num = float(ext_str)
        gt_num  = float(str(ground_truth).strip())
        if abs(ext_num - gt_num) <= tolerance:
            return "CORRECT"
        else:
            return "WRONG"
    except (ValueError, TypeError):
        pass

    ext_s = ext_str.upper()
    gt_s  = gt_str.upper()
    gender_map = {"M": "MALE", "F": "FEMALE"}
    ext_s = gender_map.get(ext_s, ext_s)
    gt_s  = gender_map.get(gt_s, gt_s)
    if ext_s == gt_s:
        return "CORRECT"
    if ext_s.split()[0] == gt_s.split()[0]:
        return "CORRECT"
    return "WRONG"


def calc_prf(tp, fp, fn):
    """Calculate Precision, Recall, F1"""
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1        = (2 * precision * recall / (precision + recall)
                 if (precision + recall) > 0 else 0.0)
    return precision, recall, f1


# ── Run Evaluation ───────────────────────────────────────────

records = []
summary = {}

for _, row in df.iterrows():
    doc_id = str(row.iloc[0]).strip()
    if doc_id in ["nan", "", "doc_id"]:
        continue

    json_path = os.path.join(EXTRACTED_FIELDS_DIR, doc_id + ".json")
    if not os.path.exists(json_path):
        print(f"  MISSING JSON: {doc_id}.json")
        continue

    with open(json_path, "r", encoding="utf-8") as f:
        extracted = json.load(f)

    source_type = str(row.get("source_type", "")).strip()
    file_type   = str(row.iloc[7]).strip().upper()

    for json_key, csv_col in [
            # patient_name: SKIPPED — CSV has anonymized names
            ("patient_gender", "sex"),
            ("test_date",      "test_date"),
            ("test_type",      "test_type"),
        ]:
        ext_val = extracted.get(json_key, "NOT_FOUND")
        gt_val  = row.get(csv_col, None)
        result  = compare_values(ext_val, gt_val)

        records.append({
            "doc_id":       doc_id,
            "source_type":  source_type,
            "file_type":    file_type,
            "field":        json_key,
            "extracted":    ext_val,
            "ground_truth": gt_val,
            "result":       result,
        })
        if result != "SKIP":
            if json_key not in summary:
                summary[json_key] = {"correct": 0, "wrong": 0}
            if result == "CORRECT":
                summary[json_key]["correct"] += 1
            else:
                summary[json_key]["wrong"] += 1

    med_vals = extracted.get("medical_values", {})

    for json_key, csv_col in FIELD_MAP.items():
        if json_key in ["patient_name", "patient_gender",
                        "test_date", "test_type"]:
            continue
        if csv_col not in df.columns:
            continue

        ext_val = med_vals.get(json_key, "NOT_FOUND")
        gt_val  = row.get(csv_col, None)
        result  = compare_values(ext_val, gt_val)

        records.append({
            "doc_id":       doc_id,
            "source_type":  source_type,
            "file_type":    file_type,
            "field":        json_key,
            "extracted":    ext_val,
            "ground_truth": gt_val,
            "result":       result,
        })
        if result != "SKIP":
            if json_key not in summary:
                summary[json_key] = {"correct": 0, "wrong": 0}
            if result == "CORRECT":
                summary[json_key]["correct"] += 1
            else:
                summary[json_key]["wrong"] += 1

# ── Save Detailed CSV ────────────────────────────────────────
results_df = pd.DataFrame(records)
csv_path = os.path.join(BASE_DIR, "evaluation_results.csv")
results_df.to_csv(csv_path, index=False)
print(f"\n  Detailed results saved: evaluation_results.csv")

# ── Print Results ────────────────────────────────────────────

print("\n" + "=" * 60)
print("FIELD-LEVEL ACCURACY")
print("=" * 60)

groups = {
    "Basic Fields":  ["patient_gender", "test_date", "test_type"],
    "CBC Values":    ["Haemoglobin", "RBC", "WBC", "Platelets",
                      "MCV", "MCH", "PCV_HCT", "MCHC", "RDW",
                      "Neutrophils", "Lymphocytes"],
    "LFT Values":    ["ALT", "AST", "Bilirubin_Total",
                      "ALP", "Albumin", "GGT"],
    "RFT Values":    ["Creatinine", "Urea", "Uric_Acid", "eGFR"],
    "BSG Values":    ["Fasting_Glucose", "HbA1c", "Random_Glucose"],
    "Lipid Values":  ["Total_Cholesterol", "HDL", "LDL",
                      "Triglycerides", "VLDL"],
}

total_correct = 0
total_total   = 0

for group_name, fields in groups.items():
    print(f"\n  {group_name}:")
    print(f"  {'Field':<25} {'Correct':>7} {'Total':>7} {'Accuracy':>9}")
    print(f"  {'-'*25} {'-'*7} {'-'*7} {'-'*9}")

    for field in fields:
        if field not in summary:
            continue
        c = summary[field]["correct"]
        t = summary[field]["correct"] + summary[field]["wrong"]
        pct = (c / t * 100) if t > 0 else 0
        print(f"  {field:<25} {c:>7} {t:>7} {pct:>8.1f}%")
        total_correct += c
        total_total   += t

overall = (total_correct / total_total * 100) if total_total > 0 else 0
print(f"\n{'='*60}")
print(f"  OVERALL ACCURACY: {total_correct}/{total_total} = {overall:.1f}%")
print(f"{'='*60}")

# ── Source Type Breakdown ────────────────────────────────────
print("\n" + "=" * 60)
print("ACCURACY BY SOURCE TYPE")
print("=" * 60)

source_stats = {}
for rec in records:
    if rec["result"] == "SKIP":
        continue
    src = rec["source_type"]
    if src not in source_stats:
        source_stats[src] = {"correct": 0, "total": 0}
    source_stats[src]["total"] += 1
    if rec["result"] == "CORRECT":
        source_stats[src]["correct"] += 1

print(f"\n  {'Source Type':<20} {'Correct':>7} {'Total':>7} {'Accuracy':>9}")
print(f"  {'-'*20} {'-'*7} {'-'*7} {'-'*9}")
for src, stats in sorted(source_stats.items()):
    c   = stats["correct"]
    t   = stats["total"]
    pct = (c / t * 100) if t > 0 else 0
    print(f"  {src:<20} {c:>7} {t:>7} {pct:>8.1f}%")

# ── File Type Breakdown ──────────────────────────────────────
print("\n" + "=" * 60)
print("ACCURACY BY FILE TYPE (PDF vs PNG vs JPEG)")
print("=" * 60)

filetype_stats = {}
for rec in records:
    if rec["result"] == "SKIP":
        continue
    ft = rec["file_type"]
    if ft not in filetype_stats:
        filetype_stats[ft] = {"correct": 0, "total": 0}
    filetype_stats[ft]["total"] += 1
    if rec["result"] == "CORRECT":
        filetype_stats[ft]["correct"] += 1

print(f"\n  {'File Type':<10} {'Correct':>7} {'Total':>7} {'Accuracy':>9}")
print(f"  {'-'*10} {'-'*7} {'-'*7} {'-'*9}")
for ft, stats in sorted(filetype_stats.items()):
    c   = stats["correct"]
    t   = stats["total"]
    pct = (c / t * 100) if t > 0 else 0
    print(f"  {ft:<10} {c:>7} {t:>7} {pct:>8.1f}%")

# ── Synthetic vs Online ──────────────────────────────────────
print("\n" + "=" * 60)
print("ACCURACY: SYNTHETIC vs ONLINE")
print("=" * 60)

syn_c = syn_t = onl_c = onl_t = 0
for rec in records:
    if rec["result"] == "SKIP":
        continue
    src = str(rec["source_type"]).lower()
    if "synthetic" in src:
        syn_t += 1
        if rec["result"] == "CORRECT":
            syn_c += 1
    elif "online" in src:
        onl_t += 1
        if rec["result"] == "CORRECT":
            onl_c += 1

syn_pct = (syn_c / syn_t * 100) if syn_t > 0 else 0
onl_pct = (onl_c / onl_t * 100) if onl_t > 0 else 0

print(f"\n  {'Category':<15} {'Correct':>7} {'Total':>7} {'Accuracy':>9}")
print(f"  {'-'*15} {'-'*7} {'-'*7} {'-'*9}")
print(f"  {'Synthetic':<15} {syn_c:>7} {syn_t:>7} {syn_pct:>8.1f}%")
print(f"  {'Online':<15} {onl_c:>7} {onl_t:>7} {onl_pct:>8.1f}%")

# ── Precision, Recall, F1 ────────────────────────────────────
print("\n" + "=" * 60)
print("PRECISION, RECALL AND F1 SCORE")
print("=" * 60)
print("""
Definitions used:
  TP (True Positive)  = CORRECT  — extracted and matched ground truth
  FP (False Positive) = WRONG    — extracted but did not match
  FN (False Negative) = WRONG    — NOT_FOUND when value existed
  (SKIP records excluded — field not present in that report type)
""")

# ── Per-field P/R/F1 ────────────────────────────────────────
print(f"  {'Field':<25} {'TP':>5} {'FP':>5} {'FN':>5} "
      f"{'Prec':>7} {'Rec':>7} {'F1':>7}")
print(f"  {'-'*25} {'-'*5} {'-'*5} {'-'*5} "
      f"{'-'*7} {'-'*7} {'-'*7}")

all_groups = {**{k: v for d in [
    {"Basic Fields":  ["patient_gender", "test_date", "test_type"]},
    {"CBC Values":    ["Haemoglobin", "RBC", "WBC", "Platelets",
                       "MCV", "MCH", "PCV_HCT", "MCHC", "RDW",
                       "Neutrophils", "Lymphocytes"]},
    {"LFT Values":    ["ALT", "AST", "Bilirubin_Total",
                       "ALP", "Albumin", "GGT"]},
    {"RFT Values":    ["Creatinine", "Urea", "Uric_Acid", "eGFR"]},
    {"BSG Values":    ["Fasting_Glucose", "HbA1c", "Random_Glucose"]},
    {"Lipid Values":  ["Total_Cholesterol", "HDL", "LDL",
                       "Triglycerides", "VLDL"]},
] for k, v in d.items()}}

# Build per-field TP/FP/FN from records
field_counts = {}
for rec in records:
    if rec["result"] == "SKIP":
        continue
    f = rec["field"]
    if f not in field_counts:
        field_counts[f] = {"tp": 0, "fp": 0, "fn": 0}
    if rec["result"] == "CORRECT":
        field_counts[f]["tp"] += 1
    else:
        # WRONG: if extracted != NOT_FOUND → FP; if NOT_FOUND → FN
        ext = str(rec["extracted"]).strip().upper()
        if ext == "NOT_FOUND":
            field_counts[f]["fn"] += 1
        else:
            field_counts[f]["fp"] += 1

all_field_list = []
for grp_fields in all_groups.values():
    all_field_list.extend(grp_fields)

total_tp = total_fp = total_fn = 0
for field in all_field_list:
    if field not in field_counts:
        continue
    tp = field_counts[field]["tp"]
    fp = field_counts[field]["fp"]
    fn = field_counts[field]["fn"]
    p, r, f1 = calc_prf(tp, fp, fn)
    print(f"  {field:<25} {tp:>5} {fp:>5} {fn:>5} "
          f"{p*100:>6.1f}% {r*100:>6.1f}% {f1*100:>6.1f}%")
    total_tp += tp
    total_fp += fp
    total_fn += fn

# ── Overall P/R/F1 ───────────────────────────────────────────
overall_p, overall_r, overall_f1 = calc_prf(total_tp, total_fp, total_fn)
print(f"\n{'='*60}")
print(f"  OVERALL METRICS:")
print(f"  TP={total_tp}  FP={total_fp}  FN={total_fn}")
print(f"  Precision : {overall_p*100:.1f}%")
print(f"  Recall    : {overall_r*100:.1f}%")
print(f"  F1 Score  : {overall_f1*100:.1f}%")
print(f"{'='*60}")

# ── P/R/F1 by Test Category ──────────────────────────────────
print("\n" + "=" * 60)
print("PRECISION, RECALL, F1 BY TEST CATEGORY")
print("=" * 60)

category_field_map = {
    "CBC":   ["Haemoglobin", "RBC", "WBC", "Platelets", "MCV",
              "MCH", "PCV_HCT", "MCHC", "RDW", "Neutrophils", "Lymphocytes"],
    "LFT":   ["ALT", "AST", "Bilirubin_Total", "ALP", "Albumin", "GGT"],
    "RFT":   ["Creatinine", "Urea", "Uric_Acid", "eGFR"],
    "BSG":   ["Fasting_Glucose", "HbA1c", "Random_Glucose"],
    "Lipid": ["Total_Cholesterol", "HDL", "LDL", "Triglycerides", "VLDL"],
}

print(f"\n  {'Category':<10} {'TP':>5} {'FP':>5} {'FN':>5} "
      f"{'Prec':>7} {'Rec':>7} {'F1':>7}")
print(f"  {'-'*10} {'-'*5} {'-'*5} {'-'*5} "
      f"{'-'*7} {'-'*7} {'-'*7}")

for cat, fields in category_field_map.items():
    cat_tp = cat_fp = cat_fn = 0
    for field in fields:
        if field in field_counts:
            cat_tp += field_counts[field]["tp"]
            cat_fp += field_counts[field]["fp"]
            cat_fn += field_counts[field]["fn"]
    p, r, f1 = calc_prf(cat_tp, cat_fp, cat_fn)
    print(f"  {cat:<10} {cat_tp:>5} {cat_fp:>5} {cat_fn:>5} "
          f"{p*100:>6.1f}% {r*100:>6.1f}% {f1*100:>6.1f}%")

# ── P/R/F1 by Source Type ────────────────────────────────────
print("\n" + "=" * 60)
print("PRECISION, RECALL, F1 BY SOURCE TYPE")
print("=" * 60)

source_prf = {}
for rec in records:
    if rec["result"] == "SKIP":
        continue
    src = rec["source_type"]
    if src not in source_prf:
        source_prf[src] = {"tp": 0, "fp": 0, "fn": 0}
    if rec["result"] == "CORRECT":
        source_prf[src]["tp"] += 1
    else:
        ext = str(rec["extracted"]).strip().upper()
        if ext == "NOT_FOUND":
            source_prf[src]["fn"] += 1
        else:
            source_prf[src]["fp"] += 1

print(f"\n  {'Source Type':<20} {'TP':>5} {'FP':>5} {'FN':>5} "
      f"{'Prec':>7} {'Rec':>7} {'F1':>7}")
print(f"  {'-'*20} {'-'*5} {'-'*5} {'-'*5} "
      f"{'-'*7} {'-'*7} {'-'*7}")

for src, counts in sorted(source_prf.items()):
    p, r, f1 = calc_prf(counts["tp"], counts["fp"], counts["fn"])
    print(f"  {src:<20} {counts['tp']:>5} {counts['fp']:>5} {counts['fn']:>5} "
          f"{p*100:>6.1f}% {r*100:>6.1f}% {f1*100:>6.1f}%")

print("\n" + "=" * 60)
print("EVALUATION COMPLETE")
print(f"  Detailed results: evaluation_results.csv")
print("=" * 60)

# ============================================================
# CHART GENERATION
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Create charts directory if it doesn't exist
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

print("\n" + "=" * 60)
print("GENERATING CHARTS...")
print("=" * 60)

# Colour palette matching report theme
NAVY   = '#1F4E79'
BLUE   = '#2E75B6'
GREEN  = '#70AD47'
ORANGE = '#ED7D31'
PURPLE = '#9B59B6'

# ── Chart 1: Precision, Recall, F1 by Source Type ────────────
# Calculate actual values from records
source_prf_chart = {}
for rec in records:
    if rec["result"] == "SKIP":
        continue
    src = rec["source_type"]
    if src not in source_prf_chart:
        source_prf_chart[src] = {"tp": 0, "fp": 0, "fn": 0}
    if rec["result"] == "CORRECT":
        source_prf_chart[src]["tp"] += 1
    else:
        ext = str(rec["extracted"]).strip().upper()
        if ext == "NOT_FOUND":
            source_prf_chart[src]["fn"] += 1
        else:
            source_prf_chart[src]["fp"] += 1

source_labels = []
prec_vals  = []
rec_vals   = []
f1_vals    = []

for src in sorted(source_prf_chart.keys()):
    counts = source_prf_chart[src]
    p, r, f = calc_prf(counts["tp"], counts["fp"], counts["fn"])
    source_labels.append(src.replace("_", "\n"))
    prec_vals.append(round(p * 100, 1))
    rec_vals.append(round(r * 100, 1))
    f1_vals.append(round(f * 100, 1))

x = np.arange(len(source_labels))
w = 0.25

fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

b1 = ax.bar(x - w,   prec_vals, w, label='Precision', color=NAVY,  edgecolor='white')
b2 = ax.bar(x,       rec_vals,  w, label='Recall',    color=BLUE,  edgecolor='white')
b3 = ax.bar(x + w,   f1_vals,   w, label='F1 Score',  color=GREEN, edgecolor='white')

for bars in [b1, b2, b3]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                f'{h:.1f}', ha='center', va='bottom',
                fontsize=8.5, fontweight='bold', color='#333333')

ax.set_ylim(0, 115)
ax.set_ylabel('Score (%)', fontsize=12, color='#333333')
ax.set_xticks(x)
ax.set_xticklabels(source_labels, fontsize=10, color='#333333')
ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#cccccc')
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.tick_params(colors='#333333')
ax.legend(fontsize=11, framealpha=0.9, edgecolor='#cccccc')
plt.tight_layout()

chart1_path = os.path.join(CHARTS_DIR, "chart1_source_type_prf.png")
plt.savefig(chart1_path, dpi=180, bbox_inches='tight')
plt.close()
print(f"  Chart 1 saved: charts/chart1_source_type_prf.png")

# ── Chart 2: PNG vs JPEG Radar Chart ─────────────────────────
# Calculate PNG and JPEG metrics from actual records
ft_prf = {}
ft_acc = {}
for rec in records:
    if rec["result"] == "SKIP":
        continue
    ft = rec["file_type"]
    if ft not in ft_prf:
        ft_prf[ft] = {"tp": 0, "fp": 0, "fn": 0, "correct": 0, "total": 0}
    ft_prf[ft]["total"] += 1
    if rec["result"] == "CORRECT":
        ft_prf[ft]["tp"] += 1
        ft_prf[ft]["correct"] += 1
    else:
        ext = str(rec["extracted"]).strip().upper()
        if ext == "NOT_FOUND":
            ft_prf[ft]["fn"] += 1
        else:
            ft_prf[ft]["fp"] += 1

# Get PNG and JPEG values
def get_ft_metrics(ft_key):
    if ft_key not in ft_prf:
        return [0, 0, 0, 0]
    d = ft_prf[ft_key]
    acc = (d["correct"] / d["total"] * 100) if d["total"] > 0 else 0
    p, r, f = calc_prf(d["tp"], d["fp"], d["fn"])
    return [round(acc, 1), round(p*100, 1), round(r*100, 1), round(f*100, 1)]

png_metrics  = get_ft_metrics("PNG")
jpeg_metrics = get_ft_metrics("JPEG")

categories_radar = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
N = len(categories_radar)

# Compute angles for radar
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

png_vals_r  = png_metrics  + png_metrics[:1]
jpeg_vals_r = jpeg_metrics + jpeg_metrics[:1]

fig, ax = plt.subplots(figsize=(7, 7),
                       subplot_kw=dict(polar=True))
fig.patch.set_facecolor('white')
ax.set_facecolor('#f8f8f8')

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories_radar, fontsize=12,
                   color='#222222', fontweight='600')

ax.set_rlabel_position(30)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20', '40', '60', '80', '100'],
                   fontsize=9, color='#888888')
ax.set_ylim(0, 100)
ax.yaxis.grid(True, color='#cccccc', linestyle='--', alpha=0.6)
ax.xaxis.grid(True, color='#cccccc', linestyle='-', alpha=0.4)

# PNG line
ax.plot(angles, png_vals_r, 'o-', linewidth=2.5,
        color=NAVY, label='PNG (Screenshots)')
ax.fill(angles, png_vals_r, alpha=0.15, color=NAVY)

# JPEG line
ax.plot(angles, jpeg_vals_r, 's-', linewidth=2.5,
        color=ORANGE, label='JPEG (Camera photos)')
ax.fill(angles, jpeg_vals_r, alpha=0.15, color=ORANGE)

# Value labels
for angle, png_v, jpeg_v in zip(angles[:-1],
                                  png_metrics, jpeg_metrics):
    ax.text(angle, png_v + 5, f'{png_v}%',
            ha='center', va='center',
            fontsize=9, fontweight='bold', color=NAVY)
    ax.text(angle, jpeg_v - 8, f'{jpeg_v}%',
            ha='center', va='center',
            fontsize=9, fontweight='bold', color=ORANGE)

ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.15),
          fontsize=11, framealpha=0.9, edgecolor='#cccccc')

plt.tight_layout()
chart2_path = os.path.join(CHARTS_DIR, "chart2_png_vs_jpeg_radar.png")
plt.savefig(chart2_path, dpi=180, bbox_inches='tight')
plt.close()
print(f"  Chart 2 saved: charts/chart2_png_vs_jpeg_radar.png")

# ── Chart 3: F1 Score by Test Category (Horizontal) ──────────
cat_f1_chart = {}
for cat, fields in category_field_map.items():
    cat_tp = cat_fp = cat_fn = 0
    for field in fields:
        if field in field_counts:
            cat_tp += field_counts[field]["tp"]
            cat_fp += field_counts[field]["fp"]
            cat_fn += field_counts[field]["fn"]
    _, _, f1 = calc_prf(cat_tp, cat_fp, cat_fn)
    cat_f1_chart[cat] = round(f1 * 100, 1)

cat_names  = list(cat_f1_chart.keys())
cat_scores = list(cat_f1_chart.values())
bar_colors = [NAVY, BLUE, GREEN, ORANGE, PURPLE]

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

bars = ax.barh(cat_names, cat_scores,
               color=bar_colors, edgecolor='white',
               height=0.55)

for bar, val in zip(bars, cat_scores):
    ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
            f'{val}%', va='center', fontsize=11,
            fontweight='bold', color='#333333')

ax.axvline(x=80, color='#cc0000', linestyle='--',
           linewidth=1.3, alpha=0.7, label='80% reference line')

ax.set_xlim(0, 110)
ax.set_xlabel('F1 Score (%)', fontsize=12, color='#333333')
ax.set_ylabel('Test Category', fontsize=12, color='#333333')
ax.xaxis.grid(True, linestyle='--', alpha=0.4, color='#cccccc')
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.tick_params(colors='#333333', labelsize=11)
ax.legend(fontsize=10, framealpha=0.9, edgecolor='#cccccc')
plt.tight_layout()

chart3_path = os.path.join(CHARTS_DIR, "chart3_f1_by_category.png")
plt.savefig(chart3_path, dpi=180, bbox_inches='tight')
plt.close()
print(f"  Chart 3 saved: charts/chart3_f1_by_category.png")

print("\n" + "=" * 60)
print("ALL CHARTS SAVED TO: fyp_project/charts/")
print("=" * 60)
