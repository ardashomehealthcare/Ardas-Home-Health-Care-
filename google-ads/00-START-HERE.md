# Hiring Caretakers on Google Ads — ₹20/day Kit for ARDAS Home Health Care

**Your choices (from last message):**
- **Lead form =** your existing `careers.html` form → writes to your Google Sheet and fires a Google Ads conversion. No Google-hosted Lead Form needed.
- **Upload =** Google Ads web UI → Bulk actions → paste from clipboard (no Editor needed).
- **Geo =** Bathinda + 50 km radius (`Presence: people in this location` — critical).
- **Conversion =** you didn't have a label yet → file `01` shows you how to create it.

**Live site:** `https://ardashomehealthcare.github.io/Ardas-Home-Health-Care-/careers.html`
**Google Ads tag already on site:** `AW-600056315` + GA4 `G-TT9HC615J6`
**This kit is already validated:** 62 keywords, 580 negatives, 3 responsive ads, all within 30/90 char limits.

---

## What you will spend

| Budget | What happens | Recommendation |
|---|---|---|
| **₹20 / day** | ~₹608 / month cap. Google may spend 0–40 on any single day, never more than 608/month. | Use exactly this. Do **not** set ₹30 expecting "more reach" — it just spends faster with same quality. |
| Actual cost per click in Bathinda for these job keywords | ₹1.50 – ₹4.00 | Set max CPC to ₹3–4 so ₹20 buys 5–13 clicks/day |
| Expected leads | **~8–10 form submits / month** (~1 per week) at ₹60–75 per lead | Honest math: your form needs 3 file uploads, so ~4% of clickers submit. This is *good* — it filters out time-wasters. |

Why not Google-hosted Lead Forms? Google now requires **₹85,000+ lifetime spend OR ₹1,000+ + Advertiser Verification** before you can even create one. Your own `careers.html` form works on day one and actually writes to your Google Drive folder `1Dbtie1BIgCgYEP-oujQt8YzFz2I-a4ok` — a Lead Form would bypass it.

---

## Do these 4 files in order — ~15 minutes total

### ① `01-conversion-action-setup.md` — 5 min — DO THIS FIRST
Create **Tools → Conversions → + New → Website → Submit lead form → name: `Caretaker Job Form Submit` → Value ₹100 → Count: One**.

You will get a snippet like:
```html
gtag('event', 'conversion', {'send_to': 'AW-600056315/AbCdEfGhIjKlMnOpQrSt'});
```
Copy the part after the slash (`AbCdEfGhIjKlMnOpQrSt`) and paste it into `careers.html` where you see `REPLACE_WITH_CONVERSION_LABEL`, then `git push origin main`. The page already fires the conversion — it just needs your label to credit the right keyword.

*Until you do this, `careers.html` still works fine — you just won't see conversions in Google Ads.*

### ② `02-create-campaign-in-ui.md` — 6 min
Manually create ONE campaign + ONE ad group. Every field value is copy-paste ready:
- **Campaign name:** `SRCH | Caretaker Jobs | Bathinda +50km` ← must be exact or bulk paste fails
- **Network:** Search only, **uncheck** Search partners + Display
- **Locations:** Bathinda 50 km radius + `Presence: People in or regularly in` + exclude Ludhiana/Moga/Barnala/Sangrur/Delhi etc.
- **Budget:** ₹20/day — **Bidding: Manual CPC** (or Maximize clicks with Max CPC ₹4 cap)
- **Ad group:** `AG-1 Caregiver Job Bathinda` — Max CPC ₹3.00

Leave the campaign **Paused** until step ④ is done.

### ③ Bulk paste — 3 min per file — from this folder

| File | Where to paste in Google Ads | What it does |
|---|---|---|
| `03-keywords-bulk-paste.csv` | Keywords → Bulk actions → Paste from clipboard | **62 positive keywords** — only job-seeker intent. AG-1 Enabled, AG-2/3 Paused. Exact `[brackets]` + Phrase `"quotes"` so you do not pay for broad junk. |
| `04-negative-keywords-bulk-paste.csv`<br>**or** `04b-negative-keywords-plain-list.txt` if your UI has no Label column | Negative keywords → Bulk actions → Paste | **580 negative keywords in 11 themed groups** — blocks hospital/government/office/online-earning/training/service-seeker/overseas/minor/competitor traffic. **This is why you won't get hospital-job clicks.** Paste in 3–4 batches if the UI caps. |
| `05-ads-bulk-paste.csv` | Ads → Bulk actions → Paste from clipboard | **3 Responsive Search Ads** (15 headlines + 4 descriptions each) landing on `careers.html`. Hindi + Punjabi mixed in AG-3. No salary promises, no get-rich-quick wording — employment-policy safe. |
| `06-assets-checklist.csv` | Ads & assets → Assets → + | 4 Sitelinks, 5 Callouts, 2 Structured snippets, Location link (biggest CTR win). Skip Call asset for 2 weeks at ₹20/day. |

*All CSVs are UTF-8, header row included, comma-separated — open in Notepad/VS Code, Ctrl+A, paste. If a column says "Not importing", pick it from the dropdown.*

### ④ Enable + test
Campaign → **Enabled** → wait for ad review (<1h usually). Submit a test entry named `TEST-DO-NOT-HIRE` on `careers.html`, confirm **Tools → Conversions → Caretaker Job Form Submit** flips to **Recording conversions** (~3h), then delete that row from your Sheet.

---

## Why you won't waste money on hospital jobs

The 580 negatives include:

- `HOSPITAL-INSTITUTION` (hospital, civil hospital, medical college, nursing home, ICU, pharmacy, diagnostic…)
- `OTHER-ROLES` (doctor, GNM/ANM/BSc Nursing, ASHA, driver, delivery, security, housekeeping, receptionist, BPO, IT, teacher…)
- `SCAM-FEE-EASY-MONEY` (registration fee, earn money, work from home, online job, typing job, MLM…)
- `TRAINING-COURSE` (course, admission, exam, result, syllabus, diploma, internship…)
- `SERVICE-SEEKER` (hire, need a caretaker for my father, how much, price, per day rate… — families wanting to **hire** you, not work for you)
- `GOVT-EXAM` (sarkari naukri, govt job, railway, bank, police, PPSC notifications…)
- `OVERSEAS` (Dubai, Canada, UK, visa, plus other Indian cities — Delhi/Mumbai/Chandigarh…)
- `COMPETITOR-PORTAL` (Naukri.com, Indeed, OLX, Apna… brand terms)
- …and 3 more groups. Every negative is campaign-level so it protects all 3 ad groups.

## Files you can regenerate

```bash
python3 google-ads/_build_campaign.py
```

Edits live in that one Python file — change keywords/ads there and re-run. It re-creates the 5 CSV/TXT assets and prints a validation report (30-char headlines / 90-char descriptions / duplicate & collision checks). The two `.md` guides are hand-written and not overwritten.

## If Google disapproves the ad

Three common reasons for caretaker-job ads on a `github.io` domain — all fixable:
1. **Employment / HEC policy:** Do not target/exclude by age, gender, parental status — leave demographics at *All*. Your ad copy may say "Male & Female Caregivers" — that's allowed, targeting is not.
2. **Compensated acts / Unacceptable business practices:** Never write salary figures like "Earn ₹25,000" — the ads in this kit deliberately avoid numbers.
3. **Destination not working:** `github.io` is allowed but flagged sometimes. Fix is to put the same `careers.html` on `ardashomehealthcare.com` and keep the same path — no other change needed.

Questions? Open `01-conversion-action-setup.md` → `02-create-campaign-in-ui.md` in order — every click is documented.
