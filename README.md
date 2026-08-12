# ARDAS Home Health Care

Static website for ARDAS Home Health Care, Bathinda.

## Why images were missing on the live site

The page looked for photos at `images/...`, but the files were left in the repository root. The gallery also pointed at `images/gallery/Screenshot_*.jpg`, which were never uploaded — `images/gallery` was a text note, not a photo folder.

Service, hero, and logo images now live in `images/` and every `<img>` path matches a real file.

## Local preview

Open `index.html` or serve the folder:

```bash
python3 -m http.server 8080
```
