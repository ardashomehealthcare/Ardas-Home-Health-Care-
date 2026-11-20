# Ardas-Home-Health-Care-
## SEO & AI-Search (ChatGPT / Gemini / Perplexity) Setup

This site is optimised for both traditional search engines and AI assistants:

- **`robots.txt`** — explicitly allows search engines AND AI crawlers (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) so the site can be cited in AI answers.
- **`sitemap.xml`** — lists all pages; submit it in [Google Search Console](https://search.google.com/search-console) (already verified via `googlec366c670576d1948.html`) and [Bing Webmaster Tools](https://www.bing.com/webmasters) (feeds ChatGPT search).
- **`llms.txt` / `llms-full.txt`** — machine-readable business summary, services, areas and FAQs that LLMs can read directly.
- **Structured data (JSON-LD)** on every page: `MedicalBusiness` + `LocalBusiness` with ratings/reviews, `Service`, `BreadcrumbList` and `FAQPage` schemas.
- **One keyword-targeted page per service** (elderly care, home nursing, patient attendant, post-surgical care, physiotherapy, babysitter, lab test at home), all interlinked with the home page.

### Recommended off-site actions (biggest ranking lever)
1. Keep the **Google Business Profile** complete and collect Google reviews — critical for "near me" and AI answers.
2. List the business on **Justdial, Practo, Sulekha, IndiaMART** with the same name/phone/address everywhere (NAP consistency).
3. Submit the site in Google Search Console → Sitemaps, and request indexing after each update.

## Immunization tracker: MCP card photo import

In `immunization-tracker.html`, open **Review previous vaccination record → Add dates from an MCP card photo**. Tap **Take a photo** to request the rear camera on supported devices, or **Choose an existing photo** for the gallery or file picker. The static site reads the selected image locally with a self-hosted OCR worker. It does not send or save the photo. Draft dates can be edited or cleared before the user confirms and saves them to the browser's existing record. A date shared by several doses in a visit box is only offered as a per-dose suggestion. **Enter dates manually** is available with or without a photo and jumps to an unreadable date when one is flagged.

The importer is conservative: it works best with clear English dose labels and four-digit numeric dates. It tries to separate dates actually given from due dates; review every suggestion against the card. Unsupported layouts, unclear handwriting, or ambiguous dates may require manual entry. Use the format selector if the card's date order is known. Once the history is saved, calendar reminders exclude those recorded doses.

Run parser regression tests with `node --test tests/mcp-card.test.mjs`. To try the feature locally, serve the repository over HTTP and open `immunization-tracker.html` (dynamic imports and browser workers do not work from `file://`). See `assets/mcp-ocr/vendor/README.md` for the bundled runtime assets and their sources.
