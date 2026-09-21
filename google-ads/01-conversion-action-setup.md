# 01 — Create the "Submit lead form" Conversion Action (5 minutes, do this FIRST)

Your site already loads the Google Ads tag **`AW-600056315`** on every page — but nothing
fires when a candidate submits the `careers.html` job form. So right now Google Ads would
record **zero conversions**, and you'd have no idea whether the ₹20/day is working.

Two things happen in this file:
- **1A** — you create the conversion action in Google Ads and get a *label* (a short code)
- **1B** — I have already wired the code into `careers.html`; you paste your label into one spot

---

## 1A — Create the conversion action

1. Go to https://ads.google.com → **Tools** (wrench icon, top right) →
   under *Measurement* → **Conversions**
2. Click **+ New conversion action**
3. Choose **Import** → *Other or third-party analytics*? **No.** Choose **Website**.
4. **Website URL:** `https://ardashomehealthcare.github.io/Ardas-Home-Health-Care-/careers.html`
   → Click **Scan**. Google will offer to auto-detect forms.
   - **Ignore the auto-detected result** and click **"Add a conversion action manually"**
     (bottom of the scan panel). Auto-detect on this page finds the file inputs, not the
     successful-submit event, and would double-count failed submissions.
5. Fill in exactly this:

| Field | Enter | Why |
|---|---|---|
| **Goal or action whose conversions you want to track** | Select **"Submit lead form"** | Correct category for a job application |
| **Conversion name** | `Caretaker Job Form Submit` | You'll see this in every report |
| **Goal / action type** | Submit lead form | |
| **Value** | Select **"Use the same value for each conversion"** → `₹100` | Not real revenue — it just lets Google rank keywords by value later. A ₹100 placeholder is standard for lead gen. (You can also pick "Don't assign a value".) |
| **Count** | **One** | If one person applies twice you want 1 lead, not 2 |
| **Click-through window** | **7 days** | Job applicants convert same-day or not at all |
| **Engaged-view conversion window** | 1 day | |
| **View-through conversion window** | **1 day** | Keeps your numbers honest |
| **Include in "Conversions"** | **Yes** (Primary) | Required for the campaign goal + bid strategy |
| **Attribution model** | **Data-driven** (default) | Fine |
| **Enhanced conversions for web** | Leave OFF for now | Needs a hashed email/phone field; your form posts to Apps Script, so enable later if you want |

6. Click **Done** → **Save and continue**
7. On the *"Install the tag"* screen choose **"Install the tag yourself"**
8. You will see a snippet like this:

```html
<!-- Event snippet for Caretaker Job Form Submit conversion page -->
<script>
  gtag('event', 'conversion', {'send_to': 'AW-600056315/AbCdEfGhIjKlMnOpQrSt'});
</script>
```

9. **Copy ONLY the part after the slash.** In the example above that is:

```
AbCdEfGhIjKlMnOpQrSt
```

That string is your **conversion label**. Yours will be different — it's random per account.

---

## 1B — Put your label into the website

Open `careers.html` in this repository and find this line (it is inside the form's
success handler, right after the "Application submitted successfully!" toast):

```js
gtag('event', 'conversion', {
  'send_to': 'AW-600056315/REPLACE_WITH_CONVERSION_LABEL'
});
```

Replace `REPLACE_WITH_CONVERSION_LABEL` with your real label so it reads, e.g.:

```js
'send_to': 'AW-600056315/AbCdEfGhIjKlMnOpQrSt'
```

Also replace the same placeholder in the second block (`gtag('config', ...)` area near the
top of the file is **not** touched — only the two `REPLACE_WITH_CONVERSION_LABEL` spots).

Then commit + push to `main` so GitHub Pages redeploys:

```bash
git add careers.html
git commit -m "Fire Google Ads conversion on job form submit"
git push origin main
```

Wait ~2 minutes, then hard-refresh
https://ardashomehealthcare.github.io/Ardas-Home-Health-Care-/careers.html
(Ctrl+Shift+R) to confirm the new code is live.

> **If you leave the placeholder in place**, nothing breaks — the page works normally and
> the only effect is a silent `gtag` error in the browser console. No conversion is
> recorded until you paste the real label.

### What the code does

```js
// 1. GA4 event (works today, no label needed) — visible in GA4 > Reports > Engagement > Events
gtag('event', 'job_form_submit', {
  'event_category': 'Lead',
  'event_label': 'Caretaker job application - careers.html'
});

// 2. Google Ads conversion (needs your label) — this is what the campaign optimises on
gtag('event', 'conversion', { 'send_to': 'AW-600056315/YOUR_LABEL' });
```

It fires **only after** `uploadWithProgress()` resolves — i.e. only when the application
actually reached your Google Sheet. Failed submissions do not count. That is the correct
behaviour: you never pay-per-click toward a lead you didn't receive.

### Backup plan (if you'd rather not touch the code again)

The GA4 event `job_form_submit` works with **no label at all**. You can import it into
Google Ads as a conversion:

**GA4 → Admin → Events → `job_form_submit` → toggle "Mark as key event"**
then in Google Ads → **Tools → Conversions → + New conversion action → Import →
Google Analytics (GA4) → key events → tick `job_form_submit`**.

Downside: GA4-imported conversions report with a ~24 h delay, so keep the native
`gtag` snippet as your primary and treat the GA4 import as a cross-check.

---

## 1C — Verify it works (do this before spending a rupee)

1. **Google Tag Assistant** → https://tagassistant.google.com →
   enter `https://ardashomehealthcare.github.io/Ardas-Home-Health-Care-/careers.html`
   → confirm `AW-600056315` shows **green/No issues**
2. Submit a real test application (name it `TEST-DO-NOT-HIRE`, use a dummy Aadhaar image)
3. In Tag Assistant's live stream you should see the **conversion event fire**
4. Google Ads → **Tools → Conversions** → status changes from
   **"Unverified"** → **"Recording conversions"** (can take up to 24 h, often ~3 h)
5. Delete the `TEST-DO-NOT-HIRE` row from your Google Sheet, and in Google Ads
   mark that conversion as invalid: **Conversions → open the action → More → "Remove
   conversion from total"** — or simply subtract 1 mentally for that day.

Only after step 4 shows **"Recording conversions"** should you switch the campaign to
**Enabled** (file `02`, Step 9).
