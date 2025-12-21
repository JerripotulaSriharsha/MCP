from openai import OpenAI
from pydantic import BaseModel
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
import pdfplumber
import pandas as pd
import os 
from dotenv import load_dotenv
load_dotenv()
# --------------------
# Data model
# --------------------
class Invoice(BaseModel):
    date: str
    name: str
    total: float
    taxes: float
    country: str


# --------------------
# Inputs
# --------------------
doc_path = r"D:\mcp\eval\ocr.pdf"
gt_path  = r"D:\mcp\eval\actual_labels.csv"


# --------------------
# Extract PDF text
# --------------------
with pdfplumber.open(doc_path) as pdf:
    invoice_text = "\n".join(
        page.extract_text() or "" for page in pdf.pages
    )

print("\n--- Invoice Text ---")
print(invoice_text)


# --------------------
# Prompt
# --------------------
prompt = f"""
Extract these fields from the invoice and return JSON only
(date, name, total, taxes, country).

Invoice text:
\"\"\"
{invoice_text}
\"\"\"
"""


# --------------------
# Run models
# --------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
models = ["gpt-4o-mini"]
preds = {}

for m in models:
    resp = client.beta.chat.completions.parse(
        model=m,
        messages=[{"role": "user", "content": prompt}],
        response_format=Invoice,
    )

    preds[m] = Invoice.model_validate_json(
        resp.choices[0].message.content
    )

    print(f"\n--- Prediction from {m} ---")
    print(preds[m])


# --------------------
# Ground truth
# --------------------
gt = Invoice(**pd.read_csv(gt_path).iloc[0].to_dict())

print("\n--- Ground Truth ---")
print(gt)


# --------------------
# GEval metric
# --------------------
metric = GEval(
    name="field-accuracy",
    criteria=(
        "Evaluate how correctly the data model is filled. "
        "Formatting is irrelevant. The content / truth matters. "
        "Divide the number of correctly filled fields by the number "
        "of total fields to determine the accuracy."
    ),
    model="gpt-4o-mini",
    threshold=0.5,
    evaluation_params=[
        LLMTestCaseParams.EXPECTED_OUTPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
)


# --------------------
# Evaluate all models
# --------------------
scores = {}

for m, p in preds.items():
    tc = LLMTestCase(
        input=invoice_text,
        actual_output=p.model_dump_json(),
        expected_output=gt.model_dump_json(),
    )

    score = metric.measure(tc)
    scores[m] = float(score)


# --------------------
# Results
# --------------------
print("\nG-Eval scores (1.0 = perfect match)")
for name, sc in scores.items():
    print(f"{name:<12}: {sc:.2f}")
