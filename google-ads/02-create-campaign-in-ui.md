# 02 — Create the Campaign in Google Ads (do this BEFORE the bulk paste)

> Why manual? Google Ads **Bulk actions** on the web can paste keywords, negative
> keywords and ads — but it **cannot create a campaign or ad group**. So you build
> the 2 levels by hand once (≈6 minutes), then paste everything else in bulk.
> Every value below is copy-paste ready.

**Where:** https://ads.google.com → sign in with the account that holds tag `AW-600056315`

---

## STEP 1 — Create the campaign

1. Left menu → **Campaigns** → blue **+** → **New campaign**
2. **Objective:** select **Leads**
3. **Conversion goals:** tick ONLY your `Caretaker Job Form Submit` goal (from file `01`).
   If it doesn't exist yet — stop and do file `01` first.
4. **How do you want to reach your goal?** → choose **Website**
   - ⚠️ Do **NOT** pick "Lead form" or "Phone calls". Your own `careers.html` form
     writes to your Google Sheet; a Google-hosted lead form would need >$1,000 spend
     + Advertiser Verification and would bypass your Sheet.
5. Enter website: `https://ardashomehealthcare.github.io/Ardas-Home-Health-Care-/careers.html` → **Next**

## STEP 2 — Campaign settings (the money-saver screen)

| Setting | Enter exactly this | Why |
|---|---|---|
| **Campaign name** | `SRCH \| Caretaker Jobs \| Bathinda +50km` | Must match the CSVs or the bulk paste fails |
| **Networks** | ✅ Search Network<br>❌ **UNtick** "Include Google search partners"<br>❌ **UNtick** "Include Google Display Network" | Search partners + Display are the two biggest sources of junk clicks on a ₹20 budget |
| **Locations → Advanced search** | `Bathinda` → click it → set radius to **50 km** → **Add** | Your requested 50 km catchment |
| **Location options** (click "Advanced search" → *Location options*) | Select **"Presence: People in or regularly in your targeted locations"** | Default "Presence or interest" will show your ad to people *interested in* Bathinda who live in Delhi/Bihar. That burns your whole budget. **This single setting is worth more than any keyword.** |
| **Exclude locations** | `Ludhiana`, `Moga`, `Barnala`, `Sangrur`, `Mansa`, `Faridkot`, `Firozpur`, `Sri Muktsar Sahib`, `Abohar`, `Hanumangarh`, `Sirsa`, `Hisar`, `Chandigarh`, `Delhi` | 50 km from Bathinda overlaps these; candidates there can't reach a duty and you can't supervise them |
| **Languages** | `English`, `Hindi`, `Punjabi` | Your audience searches in all three |
| **Budget** | `20` (daily, INR) | Monthly cap Google will show ≈ ₹608. Google may spend up to 2× on a good day, never more than ₹608/month |
| **Bidding** → *What do you want to focus on?* | **Manual CPC**<br>(if the UI only offers Smart Bidding, pick **Maximize clicks** and set **Maximum CPC bid limit = ₹4.00**) | Manual CPC keeps a ₹20 budget predictable. Smart bidding needs 30–50 conversions/month to learn — you will have ~4. Maximize clicks *without* a bid cap will blow ₹20 in 3 clicks. |
| **Enhanced CPC** | ❌ **OFF** | ECPC can raise your bid above your manual max |
| **Ad rotation** | **Rotate: Show ads evenly** *(if only "Optimize" is offered, accept it — you have 1 enabled ad group so it doesn't matter yet)* | With 4 conversions/month, Google has no data to "optimize" on |
| **Ad schedule** | Show ads **Mon–Sun, 07:00 – 22:00** (account timezone Asia/Kolkata) | Night clicks from job seekers are near-zero quality; this stretches ₹20 over useful hours |
| **Campaign URL options** | leave blank | |

Then click **Next**.

## STEP 3 — Ad group

| Setting | Value |
|---|---|
| **Ad group name** | `AG-1 Caregiver Job Bathinda` ← must match the CSV exactly |
| **Default max CPC** | `3.00` |
| **Keywords** | Ignore the suggestions box entirely — leave it empty. You will bulk-paste in Step 5. |
| **Ad** | You can type one throwaway headline to get past the screen; it will be replaced by the bulk paste. Or skip to Step 5 and add the ad there. |

⚠️ **Turn OFF these two, or you defeat the whole negative-keyword strategy:**
- **Audiences** → *Audience expansion* → **OFF**
- **Optimized targeting** → **OFF**
- **Demographics (age / gender / parental status)** → do **not** target or exclude any.
  Job ads fall under Google's *Housing, Employment & Credit* rules — demographic
  targeting/exclusion is prohibited and can get the campaign disapproved.

Click **Next** → **Save and continue** (skip any "add more assets" prompts).

## STEP 4 — Set the campaign live but PAUSED

On the campaign row, toggle status to **Paused** until Steps 5–7 are done and you have
reviewed everything. Do not let a ₹20/day budget spend while you are still editing.

## STEP 5 — Bulk-paste the keywords

1. Left menu → **Keywords** (under *Audiences, keywords and content*)
2. Make sure the campaign `SRCH | Caretaker Jobs | Bathinda +50km` is selected
3. Click **Bulk actions** (⋮ or the "Bulk actions" button above the table) → **Paste from clipboard**
4. Open `03-keywords-bulk-paste.csv` in a text editor (Notepad / VS Code — **not** Excel,
   Excel re-quotes the `[brackets]` badly) → **Ctrl+A, Ctrl+C** → paste into the box
5. Check the column mapping row: `Campaign`, `Ad group`, `Keyword`, `Criterion Type`, `Status`.
   If any says **"Not importing"**, click its dropdown and pick the right one.
6. **Process** → review → **Apply / Post**

**Expected:** 26 keywords in AG-1 (Enabled), 20 in AG-2 (Paused), 16 in AG-3 (Paused) = **62 total**.

## STEP 6 — Bulk-paste the negative keywords

1. Left menu → **Negative keywords** (under *Audiences, keywords and content*)
2. Select the campaign → **Bulk actions** → **Paste from clipboard**
3. Open `04-negative-keywords-bulk-paste.csv`, copy all, paste
   - Columns: `Campaign`, `Keyword`, `Label`
   - If your UI has no Label column, use `04b-negative-keywords-plain-list.txt` instead and
     paste the words one-per-line into **"+ Add negative keywords" → "Add multiple"**,
     with **Add to: Campaign → Negative keywords** selected
4. Set all to **Campaign level** (not ad group) → **Save**

**Expected: ~580 negative keywords.** If the UI caps a single paste, do it in 3–4 batches
(one themed group at a time — HOSPITAL-INSTITUTION, OTHER-ROLES, etc.).

## STEP 7 — Bulk-paste the ads

1. Left menu → **Ads**
2. Select the campaign → **Bulk actions** → **Paste from clipboard**
3. Open `05-ads-bulk-paste.csv`, copy all, paste. 45 columns:
   `Campaign, Ad group, Status, Ad type, Final URL, Path 1, Path 2, Headline 1–15,
   Headline 1–15 position, Description 1–4, Description 1–4 position`
4. Fix any **"Not importing"** column via its dropdown → **Process** → review the 3 ad
   previews → **Post**
5. Delete the throwaway ad you typed in Step 3 (if any)

**Expected:** 3 Responsive Search Ads, all landing on `careers.html`,
ad strength should read **Good/Excellent** (15 headlines + 4 descriptions each).

## STEP 8 — Add the assets from `06-assets-checklist.csv`

Ads & assets → **Assets** → **+** → add each one at **Campaign** level:
- 4 × Sitelink, 5 × Callout, 2 × Structured snippet, 1 × Location (link your Google
  Business Profile — biggest CTR win you have)
- **Skip** the Call asset for the first 2 weeks: a call click costs the same as a form
  click and you cannot track it as a conversion. At ₹20/day it will eat the budget.

## STEP 9 — Enable and verify

1. Campaign status → **Enabled**
2. Wait for ad review (usually < 1 hour, sometimes 24 h)
3. **Tools → Conversions → `Caretaker Job Form Submit`** should move from
   *"Not recording"* to **"Recording conversions"**
4. Test it yourself: open `careers.html`, submit a real application (name it
   `TEST-CONVERSION`), then check Google Ads → Conversions within ~3 hours.
   Delete the test row from your Google Sheet afterwards.

---

## What ₹20/day will realistically buy you

| | Conservative | Likely | Good day |
|---|---|---|---|
| Actual CPC (Bathinda job keywords) | ₹4.00 | ₹2.50 | ₹1.50 |
| Clicks per day | 5 | 8 | 13 |
| Clicks per month | 150 | 240 | 390 |
| Form-start rate | — | ~25% | — |
| **Form submit (conversion) rate** | 2% | **4%** | 6% |
| **Leads per month** | **3** | **9–10** | **23** |

**Planning number: ~1 lead per week, ~8–10 per month, at ₹60–₹75 per lead.**

Why the submit rate is low: your form requires 3 file uploads (qualification certificate +
Aadhaar front + Aadhaar rear). That is heavy friction — it correctly filters out casual
clickers, but it means most genuine candidates abandon. Two optional fixes:
1. Add a **"Save & continue later"** / 2-step version where Aadhaar upload happens *after*
   the phone number is captured (you'd then fire the conversion on the phone-number step
   and get 3–4× more leads, at lower quality).
2. Add a **WhatsApp click** as a secondary conversion so you capture people who won't
   upload Aadhaar on a `github.io` domain.

**If you can only change one thing:** raise the budget to **₹50/day**. At ₹20 you get one
lead per week and Google's system never accumulates enough data to optimise. At ₹50/day
you cross into ~25 leads/month, which is where a recruitment pipeline actually works.

---

## Policy notes for this ad (read once, saves a disapproval)

1. **Employment ads = "HEC" category.** Google prohibits targeting or excluding by
   **age, gender, parental status or ZIP code** on job ads. Leave all demographics at
   "Unknown / All". Your ad copy may say "Male & Female Caregivers" — that's fine, it's
   the *targeting* that's restricted, not the copy.
2. **No income promises.** Never write "Earn ₹25,000/month" or "Guaranteed salary" in an
   ad — that trips the *Unacceptable business practices* / get-rich-quick policy. The copy
   in `05-ads-bulk-paste.csv` deliberately avoids all salary figures.
3. **Advertiser verification.** A brand-new Indian account is often asked to complete
   **Admin → Policy → Account → Advertiser verification** before ads serve. Do it on day 1;
   it takes 5–7 business days and will silently hold your campaign if you wait.
4. **`github.io` landing page.** Allowed, but it is not your own domain. If Google flags
   the campaign for *"Destination not working / Unacceptable content"*, the fix is to put
   the site on `ardashomehealthcare.com` (you already own the email domain) and keep the
   same `careers.html` path.
5. **Aadhaar collection.** Legal for private recruitment in India, but under the DPDP Act
   2023 you need explicit consent + a stated purpose + secure storage. Your
   `privacy-policy.html` should explicitly say *why* Aadhaar is collected, how long it is
   kept, and how a candidate can ask for deletion. Your form posts to a Google Apps Script
   that writes into Google Drive — make sure that Drive folder is not link-shareable.
