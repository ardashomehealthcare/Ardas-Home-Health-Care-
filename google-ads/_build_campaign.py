#!/usr/bin/env python3
"""
Builds the Google Ads bulk-paste files for the ARDAS Caretaker Jobs campaign.

Run:  python3 google-ads/_build_campaign.py
It regenerates every .csv / .txt paste file in this folder and prints a
validation report (character limits, duplicate keywords, etc.).
"""
import csv
import os
from collections import Counter

OUT = os.path.dirname(os.path.abspath(__file__))

CAMPAIGN = "SRCH | Caretaker Jobs | Bathinda +50km"

# --------------------------------------------------------------------------
# 1. CAMPAIGN / AD GROUP SETTINGS  (must be created by hand in the UI first)
# --------------------------------------------------------------------------
ADGROUPS = [
    # (name, status, default max CPC in INR)
    ("AG-1 Caregiver Job Bathinda", "Enabled", "3.00"),
    ("AG-2 Patient Attendant Job", "Paused", "2.50"),
    ("AG-3 Hindi-Punjabi Caretaker", "Paused", "2.00"),
]

# --------------------------------------------------------------------------
# 2. POSITIVE KEYWORDS  (job-seeker intent only)
# --------------------------------------------------------------------------
KEYWORDS = {
    "AG-1 Caregiver Job Bathinda": [
        ("[caretaker job bathinda]", "Exact"),
        ("[caretaker jobs in bathinda]", "Exact"),
        ("[caregiver job bathinda]", "Exact"),
        ("[caregiver jobs in bathinda]", "Exact"),
        ("[caretaker job vacancy bathinda]", "Exact"),
        ("[caretaker vacancy bathinda]", "Exact"),
        ("[caretaker required in bathinda]", "Exact"),
        ("[caregiver required bathinda]", "Exact"),
        ("[caregiver vacancy bathinda]", "Exact"),
        ("[caretaker job punjab]", "Exact"),
        ("[caretaker jobs punjab]", "Exact"),
        ("[caregiver job punjab]", "Exact"),
        ("[caretaker job near me]", "Exact"),
        ("[caretaker jobs near me]", "Exact"),
        ("[caregiver jobs near me]", "Exact"),
        ("[home caretaker job]", "Exact"),
        ("[caregiver job]", "Exact"),
        ("[caretaker job]", "Exact"),
        ('"caretaker job bathinda"', "Phrase"),
        ('"caregiver job bathinda"', "Phrase"),
        ('"caretaker job punjab"', "Phrase"),
        ('"caregiver job vacancy"', "Phrase"),
        ('"caretaker job vacancy"', "Phrase"),
        ('"home caretaker job"', "Phrase"),
        ('"elderly caretaker job"', "Phrase"),
        ('"old age care job bathinda"', "Phrase"),
    ],
    "AG-2 Patient Attendant Job": [
        ("[patient attendant job bathinda]", "Exact"),
        ("[patient attendant jobs in bathinda]", "Exact"),
        ("[patient attendant vacancy bathinda]", "Exact"),
        ("[patient attendant required bathinda]", "Exact"),
        ("[attendant job bathinda]", "Exact"),
        ("[ward boy job bathinda]", "Exact"),
        ("[home attendant job]", "Exact"),
        ("[24 hour caretaker job]", "Exact"),
        ("[12 hour duty caretaker job]", "Exact"),
        ("[live in caretaker job]", "Exact"),
        ("[live in caregiver job]", "Exact"),
        ("[night shift caretaker job]", "Exact"),
        ("[night duty patient attendant job]", "Exact"),
        ("[day shift caretaker job]", "Exact"),
        ("[lady caretaker job bathinda]", "Exact"),
        ("[male caretaker job bathinda]", "Exact"),
        ('"patient attendant job bathinda"', "Phrase"),
        ('"patient attendant job vacancy"', "Phrase"),
        ('"24 hour caretaker job"', "Phrase"),
        ('"live in caretaker job"', "Phrase"),
    ],
    "AG-3 Hindi-Punjabi Caretaker": [
        ("[caregiver naukri bathinda]", "Exact"),
        ("[caretaker naukri bathinda]", "Exact"),
        ("[caretaker bharti bathinda]", "Exact"),
        ("[caretaker bharti punjab]", "Exact"),
        ("[caregiver bharti punjab]", "Exact"),
        ("[sevak job bathinda]", "Exact"),
        ("[sevadarni job bathinda]", "Exact"),
        ("[budhape ki dekhbhal job]", "Exact"),
        ("[mariz ki dekhbhal job]", "Exact"),
        ("[patient dekhbhal job bathinda]", "Exact"),
        ("[caretaker ki naukri]", "Exact"),
        ("[caregiver kaam bathinda]", "Exact"),
        ('"caretaker naukri"', "Phrase"),
        ('"caregiver naukri bathinda"', "Phrase"),
        ('"caretaker bharti"', "Phrase"),
        ('"sevak job bathinda"', "Phrase"),
    ],
}

# --------------------------------------------------------------------------
# 3. NEGATIVE KEYWORDS  (campaign level)
# --------------------------------------------------------------------------
NEGATIVES = {
    # --- A. Hospital / institution jobs: the #1 waste you asked to block ---
    "HOSPITAL-INSTITUTION": [
        "hospital", "hospitals", "hospital job", "hospital jobs", "govt hospital",
        "government hospital", "sarkari hospital", "civil hospital", "military hospital",
        "cantonment", "cantt", "medical college", "medical", "clinic", "nursing home",
        "nursing homes", "icu", "emergency room", "operation theatre", "ot technician",
        "ot assistant", "dialysis", "pathology", "radiology", "x ray", "ultrasound",
        "sonographer", "pharmacy", "chemist", "medical store", "diagnostic", "lab technician",
        "disease", "treatment center", "rehabilitation centre", "rehab centre", "ashram",
        "old age home", "orphanage", "ngos", "ngo", "trust", "sanjeevani", "institution",
        "corporate", "company job", "office job",
    ],
    # --- B. Other job roles / professions (not caretaking) ---
    "OTHER-ROLES": [
        "doctor", "mbbs", "bds", "dentist", "dental", "bams", "bhms", "physician",
        "surgeon", "anesthetist", "anaesthetist", "gnm", "anm", "bsc nursing",
        "b sc nursing", "post basic", "nursing officer", "staff nurse", "nurse vacancy",
        "nursing job", "nursing jobs", "nursing college", "nursing admission", "norinor",
        "cho", "community health officer", "asha worker", "asha", "anganwadi",
        "anm da", "gnm da", "pharmacist", "d pharmacist", "physiotherapist",
        "physiotherapy", "physio", "radiographer", "technician", "technicians",
        "operator", "driver", "drivers", "delivery", "delivery boy", "zomato", "swiggy",
        "blinkit", "zepto", "dunzo", "amazon", "flipkart", "courier", "loader",
        "security guard", "security", "bouncer", "guard", "housekeeping", "cleaner",
        "sweeper", "maid", "maid job", "cooking", "cook", "chef", "kitchen",
        "receptionist", "data entry", "accountant", "accounts", "cashier", "salesman",
        "sales", "marketing", "business development", "bde", "telecaller",
        "telecalling", "customer care executive", "call center", "bpo", "kpo",
        "it job", "software", "engineer", "engineering", "teacher", "teaching",
        "tutor", "school", "principal", "clerk", "peon", "helper", "electrician",
        "plumber", "carpenter", "mason", "mistri", "tailor", "beautician",
        "hairdresser", "gym trainer", "trainer", "yoga", "farmer", "agriculture",
        "tractor", "machine operator", "cnc", "welder", "fitter", "factory",
        "industry", "industrial", "mill", "showroom", "retail", "store",
    ],
    # --- C. Fake-job / fee / easy-money seekers (worst lead quality) ---
    "SCAM-FEE-EASY-MONEY": [
        "registration fee", "fees", "fee", "charges", "advance", "advance salary",
        "loan", "no investment", "investment", "commission", "earning", "earn money",
        "earn", "income", "daily income", "monthly income", "instant", "part time earning",
        "work from home", "wfh", "online job", "online jobs", "online work",
        "online earning", "mobile job", "typing job", "form filling", "ad posting",
        "captcha", "reseller", "mlm", "pyramid", "scheme", "freelance", "freelancing",
        "gig", "side income", "passive income", "no experience needed", "no interview",
        "direct joining", "guaranteed", "fixed salary job", "sponsorship",
    ],
    # --- D. Training / course / certificate seekers ---
    "TRAINING-COURSE": [
        "course", "courses", "class", "classes", "training", "trainee", "trainer course",
        "institute", "academy", "coaching", "tutorial", "tutorials", "books", "notes",
        "pdf", "syllabus", "exam", "exams", "exam date", "admit card", "result",
        "results", "cut off", "cutoff", "previous papers", "question paper", "sample paper",
        "diploma", "certification", "certificate course", "degree", "college",
        "university", "admission", "scholarship", "student", "students", "internship",
        "intern", "fresher course", "learn", "learning", "how to become", "how to apply",
        "kya hota hai", "ka matlab", "meaning", "full form", "information", "details",
        "wikipedia", "salary after course", "best institute", "fee structure",
    ],
    # --- E. Service SEEKERS (families wanting to HIRE a caretaker = wrong intent) ---
    "SERVICE-SEEKER": [
        "hire", "hiring service", "book", "booking", "need a", "we need",
        "for my father", "for my mother", "for my parents", "for patient",
        "for parents", "for old", "for baby", "for newborn", "for child",
        "at home service", "home service", "home services", "services", "service provider",
        "providers", "provider", "agency services", "bureau", "near me service",
        "on rent", "rent", "monthly basis", "per month rate", "per day rate",
        "per day charge", "rate", "rates", "price", "prices", "pricing", "quote",
        "cost", "costs", "how much", "kitna", "kharcha", "cheap", "cheapest",
        "best agency", "top agency", "compare", "reviews", "review", "rating",
        "complaint", "complaints", "nri", "nri service", "for nri",
    ],
    # --- F. Government exam / result / notification chasers ---
    "GOVT-EXAM": [
        "sarkari", "sarkari naukri", "govt naukri", "govt", "govt job", "govt jobs", "government",
        "government job", "government jobs", "psc", "ppsc", "upsc", "ssc", "railway",
        "railways", "bank", "banking", "ibps", "sbi", "rbi", "police", "army",
        "navy", "air force", "defence", "defense", "paramilitary", "crpf", "bsf",
        "patwari", "panchayat", "gram sachiv", "revenue", "excise", "forest",
        "board", "notification", "notifications", "result 2026",
        "result 2025", "syllabus 2026", "apply online last date", "last date",
        "eligibility", "age limit", "eligibility criteria", "counseling", "merit list",
        "selection list", "waiting list", "answer key", "nvs", "kvs", "esic",
        "aiims", "pgimer", "pgi", "bhu", "du", "punjab university",
    ],
    # --- G. Salary-research-only (no intent to apply) ---
    "SALARY-ONLY": [
        "salary", "salaries", "salary slip", "salary per month", "salary package",
        "pay scale", "payscale", "scale", "grade pay", "in hand", "take home",
        "increments", "per month salary", "kitni salary", "tankhwah", "vetan",
        "majdoori", "minimum wages", "wage", "wages", "salary of", "highest salary",
        "lowest salary", "average salary",
    ],
    # --- H. Overseas / relocation seekers (cannot join a Bathinda duty) ---
    "OVERSEAS": [
        "abroad", "foreign", "overseas", "gulf", "dubai", "saudi", "saudi arabia",
        "qatar", "kuwait", "oman", "bahrain", "malaysia", "singapore", "italy",
        "germany", "uk", "usa", "america", "canada", "australia", "new zealand",
        "japan", "korea", "africa", "ireland", "portugal", "croatia", "romania",
        "poland", "greece", "malta", "cyprus", "israel", "visa", "visas", "work permit",
        "work visa", "immigration", "immigrate", "sponsor", "sponsorship", "relocation",
        "relocate", "delhi", "mumbai", "chennai", "bangalore", "bengaluru", "hyderabad",
        "kolkata", "pune", "noida", "gurgaon", "chandigarh", "ludhiana", "amritsar",
        "jalandhar", "patiala", "mohali", "haryana", "himachal", "rajasthan", "uttar pradesh",
        "bihar", "goa", "kerala", "tamil nadu", "gujarat", "maharashtra",
    ],
    # --- I. Minors / school-age (child-labour risk: never serve to these) ---
    "MINORS": [
        "under 18", "below 18", "16 year", "17 year", "15 year", "14 year",
        "10th pass student", "12th pass student", "school boy", "school girl",
        "college student", "part time for student", "for students",
    ],
    # --- J. Competitors / job portals (their brand traffic converts badly) ---
    "COMPETITOR-PORTAL": [
        "apollo", "apollo home", "portea", "portea medical", "nightingales",
        "care24", "emoha", "samarthan", "helpage", "help age", "age care india",
        "anthara", "khyaal", "nibrus", "kITES", "senior care", "elder care india",
        "naukri com", "naukri com jobs", "indeed", "indeed com", "linkedin", "monster com",
        "quikr jobs", "olx jobs", "apna app", "job hai", "sarkari result", "free job alert",
        "freshersworld", "times jobs", "glassdoor", "internshala", "cutshort",
    ],
    # --- K. Misc junk that matches "caretaker / attendant" ---
    "MISC-JUNK": [
        "dog", "dogs", "pet", "pets", "cat", "cow", "cattle", "buffalo", "animal",
        "babysitter for my", "nanny for my", "car", "car caretaker", "bike",
        "property", "property caretaker", "society caretaker", "building caretaker",
        "estate", "farm house", "farmhouse", "office caretaker", "shop caretaker",
        "movie", "film", "song", "video", "photo", "images", "image", "wallpaper",
        "quotes", "status", "whatsapp status", "joke", "jokes", "meme", "memes",
        "news", "latest news", "youtube", "instagram", "facebook", "twitter",
        "app download", "apk", "mod", "game", "games", "download",
        "business", "franchise", "distributor", "dealer", "shop", "startup",
        "insurance", "loan agent", "real estate", "plots", "property dealer",
    ],
}

# --------------------------------------------------------------------------
# 4. RESPONSIVE SEARCH ADS  (30-char headlines / 90-char descriptions)
# --------------------------------------------------------------------------
ADS = {
    "AG-1 Caregiver Job Bathinda": {
        "final_url": "https://ardashomehealthcare.github.io/Ardas-Home-Health-Care-/careers.html",
        "path1": "jobs",
        "path2": "bathinda",
        "headlines": [
            "Caretaker Job in Bathinda",
            "Caregiver Job Vacancy",
            "Apply Online - No Fee",
            "Immediate Duty Placement",
            "Day, Night & 24 Hr Shifts",
            "Work Near Your Home",
            "Verified Home Care Work",
            "Elderly Care Job Bathinda",
            "Upload Aadhaar & Certificates",
            "Join WhatsApp Duty Group",
            "Male & Female Caregivers",
            "Bathinda + 50 Km Area",
            "Free Online Job Form",
            "ARDAS Home Health Care",
            "Caregiver Jobs in Punjab",
        ],
        "descriptions": [
            "Apply free online for caretaker jobs in Bathinda. Day, night and 24-hour shifts available.",
            "Caregiver work in Bathinda. Fill the job form with Aadhaar. We call you in 24-48 hours.",
            "ARDAS is hiring verified caregivers for home duty in Bathinda. No fee, no agent. Apply.",
            "Apply and join the ARDAS WhatsApp duty group for home care duty alerts near your area.",
        ],
    },
    "AG-2 Patient Attendant Job": {
        "final_url": "https://ardashomehealthcare.github.io/Ardas-Home-Health-Care-/careers.html",
        "path1": "jobs",
        "path2": "attendant",
        "headlines": [
            "Patient Attendant Job",
            "Attendant Job Bathinda",
            "24 Hour Duty Available",
            "Night Shift Care Work",
            "Apply Online Free Now",
            "Live-In Attendant Jobs",
            "Elderly Care Duty",
            "Duty Near Your Home",
            "No Registration Fee",
            "Immediate Joining",
            "12 & 24 Hour Shifts",
            "Home Care Duty Group",
            "Verified Staff Only",
            "ARDAS Is Hiring Now",
            "Submit Job Form Online",
        ],
        "descriptions": [
            "Patient attendant jobs in Bathinda. Care for elderly and post-surgery patients at home.",
            "Apply online free - no agent, no fee. Upload Aadhaar and certificate, we call you back.",
            "ARDAS is hiring attendants in Bathinda and 50 km around. Immediate duty for verified.",
            "Want duty near home? Join the ARDAS WhatsApp duty group and get home care duty alerts.",
        ],
    },
    "AG-3 Hindi-Punjabi Caretaker": {
        "final_url": "https://ardashomehealthcare.github.io/Ardas-Home-Health-Care-/careers.html",
        "path1": "jobs",
        "path2": "naukri",
        "headlines": [
            "Caretaker Naukri Bathinda",
            "Caregiver Bharti Punjab",
            "Ghar Par Dekhbhal Ka Kaam",
            "Online Apply Karein Free",
            "Koi Fee Nahin Dena",
            "Din Raat 24 Ghante Duty",
            "Buzurg Dekhbhal Naukri",
            "Apne Ghar Ke Paas Kaam",
            "Turant Duty Join Karein",
            "WhatsApp Duty Group",
            "Aadhaar Card Ke Sath",
            "Sevak Sevadarni Job",
            "Verified Kaam Milega",
            "ARDAS Home Health Care",
            "Form Bharein Aaj Hi",
        ],
        "descriptions": [
            "Bathinda me caretaker naukri ka form bharein. Din, raat, 24 ghante duty. Koi fee nahin.",
            "Buzurg aur mareez ki ghar par dekhbhal ka kaam. Aadhaar aur certificate upload karein.",
            "ARDAS me caretaker bharti - Bathinda aur 50 km tak. Turant duty, WhatsApp duty group.",
            "Ghar ke paas kaam chahiye? Job form bharein aur ARDAS WhatsApp duty group se judein.",
        ],
    },
}

# --------------------------------------------------------------------------
# 5. AD ASSETS (created manually in the UI - listed here as a checklist)
# --------------------------------------------------------------------------
SITELINKS = [
    ("Open the Job Form", "Fill the caretaker job form", "/careers.html"),
    ("What the Duty Involves", "Elderly care at home duties", "/elderly-care-bathinda.html"),
    ("Attendant Work Details", "Patient attendant day-to-day", "/patient-attendant-bathinda.html"),
    ("Our Privacy Policy", "How we handle your documents", "/privacy-policy.html"),
]
CALLOUTS = [
    "No Registration Fee",
    "Duty Near Your Home",
    "Day, Night & 24 Hr Shifts",
    "WhatsApp Duty Group",
    "Coordinator Calls in 24-48 Hrs",
]
STRUCTURED_SNIPPETS = {
    "Types": ["Caregiver", "Patient Attendant", "Elderly Care", "Live-In Duty"],
    "Service areas": ["Bathinda", "Rampura Phul", "Maur Mandi", "Talwandi Sabo", "Nathana", "Sangat", "Bhucho Mandi", "Goniana"],
}

BASE_URL = "https://ardashomehealthcare.github.io/Ardas-Home-Health-Care-"


def w(name, rows, header=None):
    path = os.path.join(OUT, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        if header:
            wr.writerow(header)
        wr.writerows(rows)
    return path


def main():
    report = []

    # ---- 03 keywords (bulk actions paste) ----
    rows = []
    for ag, kws in KEYWORDS.items():
        for kw, mt in kws:
            status = "Enabled" if "AG-1" in ag else "Paused"
            rows.append([CAMPAIGN, ag, kw, mt, status])
    w("03-keywords-bulk-paste.csv", rows,
      ["Campaign", "Ad group", "Keyword", "Criterion Type", "Status"])
    report.append(f"Keywords: {len(rows)} rows across {len(KEYWORDS)} ad groups")

    # plain list for single-column paste boxes
    with open(os.path.join(OUT, "03b-keywords-plain-list.txt"), "w", encoding="utf-8") as f:
        for ag, kws in KEYWORDS.items():
            f.write(f"\n### {ag}\n")
            f.write("\n".join(k for k, _ in kws) + "\n")

    # ---- 04 negative keywords ----
    neg_rows = []
    for group, terms in NEGATIVES.items():
        for t in terms:
            neg_rows.append([CAMPAIGN, t, group])
    w("04-negative-keywords-bulk-paste.csv", neg_rows,
      ["Campaign", "Keyword", "Label"])
    report.append(f"Negative keywords: {len(neg_rows)} in {len(NEGATIVES)} themed groups")

    with open(os.path.join(OUT, "04b-negative-keywords-plain-list.txt"), "w", encoding="utf-8") as f:
        f.write("Paste everything below into:\n")
        f.write("Google Ads > Campaigns > [your campaign] > Audience, keywords and content "
                "> Negative keywords > 'Add negative keywords' pencil > 'Add multiple'\n")
        f.write("(one per line, no commas)\n\n")
        for group, terms in NEGATIVES.items():
            f.write(f"\n===== {group} =====\n")
            f.write("\n".join(terms) + "\n")

    # ---- 05 responsive search ads ----
    ad_rows = []
    for ag, ad in ADS.items():
        status = "Enabled" if "AG-1" in ag else "Paused"
        row = [CAMPAIGN, ag, status, "Responsive search ad", ad["final_url"],
               ad["path1"], ad["path2"]]
        row += ad["headlines"] + [""] * (15 - len(ad["headlines"]))
        row += [""] * 15  # headline positions (left blank = no pinning)
        row += ad["descriptions"] + [""] * (4 - len(ad["descriptions"]))
        row += [""] * 4   # description positions
        ad_rows.append(row)
    header = (["Campaign", "Ad group", "Status", "Ad type", "Final URL", "Path 1", "Path 2"]
              + [f"Headline {i}" for i in range(1, 16)]
              + [f"Headline {i} position" for i in range(1, 16)]
              + [f"Description {i}" for i in range(1, 5)]
              + [f"Description {i} position" for i in range(1, 5)])
    w("05-ads-bulk-paste.csv", ad_rows, header)
    report.append(f"Responsive search ads: {len(ad_rows)}")

    # ---- 06 assets checklist ----
    with open(os.path.join(OUT, "06-assets-checklist.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["Asset type", "Name / Text", "Detail / URL", "Level", "Add it?"])
        for t, d, u in SITELINKS:
            wr.writerow(["Sitelink", t, BASE_URL + u, "Campaign", "YES"])
        for c in CALLOUTS:
            wr.writerow(["Callout", c, "", "Campaign", "YES"])
        for k, vals in STRUCTURED_SNIPPETS.items():
            wr.writerow(["Structured snippet", k, "; ".join(vals), "Campaign", "YES"])
        wr.writerow(["Location", "Link Google Business Profile: ARDAS Home Health Care",
                     "Needs GBP claimed + same login", "Account", "YES - biggest CTR win"])
        wr.writerow(["Call", "+91 98770 62683", "Call reporting ON. CAUTION at Rs 20/day - "
                     "call clicks eat the budget. Add only after week 2.", "Campaign", "OPTIONAL"])
        wr.writerow(["Image", "images/hero-elderly-care-bathinda.jpg",
                     "1.91:1 landscape, min 1200x628. Needs approval.", "Ad group AG-1", "OPTIONAL"])
        wr.writerow(["Price", "NOT USED", "You are hiring, not selling - skip price assets", "-", "NO"])
        wr.writerow(["Promotion", "NOT USED", "No discount on a job - would breach policy", "-", "NO"])
    report.append("Assets checklist written")

    # ------------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------------
    print("\n" + "=" * 74)
    print("VALIDATION REPORT")
    print("=" * 74)

    errors = 0
    for ag, ad in ADS.items():
        for i, h in enumerate(ad["headlines"], 1):
            if len(h) > 30:
                print(f"  !! {ag} Headline {i}: {len(h)} chars > 30 -> '{h}'")
                errors += 1
        for i, d in enumerate(ad["descriptions"], 1):
            if len(d) > 90:
                print(f"  !! {ag} Description {i}: {len(d)} chars > 90 -> '{d}'")
                errors += 1
        if len(ad["headlines"]) < 3 or len(ad["descriptions"]) < 2:
            print(f"  !! {ag}: needs >=3 headlines and >=2 descriptions")
            errors += 1
        if len(ad["path1"]) > 15 or len(ad["path2"]) > 15:
            print(f"  !! {ag}: path too long")
            errors += 1
    print(f"  Ad character limits: {'OK' if errors == 0 else str(errors) + ' ERRORS'}")

    # duplicate keyword check
    all_kw = [k for kws in KEYWORDS.values() for k, _ in kws]
    dupes = [k for k, c in Counter(all_kw).items() if c > 1]
    print(f"  Duplicate positive keywords: {'NONE' if not dupes else dupes}")

    # positives that collide with negatives (would be blocked)
    neg_set = {t.lower() for ts in NEGATIVES.values() for t in ts}
    collisions = []
    for k in all_kw:
        clean = k.strip('[]"').lower()
        for n in neg_set:
            if len(n) > 3 and " " not in n and n in clean.split():
                collisions.append((k, n))
    print(f"  Positive keywords blocked by a negative: {'NONE' if not collisions else collisions}")

    for line in report:
        print("  " + line)
    print("=" * 74)
    print("Files written to:", OUT)


if __name__ == "__main__":
    main()
