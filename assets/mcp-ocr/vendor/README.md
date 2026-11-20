# MCP card OCR runtime assets

The tracker lazy-loads these files from the same site. They are included so that using OCR on a private MCP card does not require any remote OCR API or third-party CDN. Only the English model and the portable non-SIMD LSTM core are bundled.

| Files | Upstream npm package / path |
| --- | --- |
| `tesseract.esm.min.js`, `worker.min.js` and JavaScript license notices | `tesseract.js@7.0.0`, `dist/` |
| `tesseract-core-lstm.wasm.js` (contains WebAssembly) | `tesseract.js-core@7.0.0` |
| `eng.traineddata.gz` | `@tesseract.js-data/eng@1.0.0`, `4.0.0_best_int/` |

The upstream [Tesseract.js](https://github.com/naptha/tesseract.js), [core](https://github.com/naptha/tesseract.js-core), and [language data packaging](https://github.com/naptha/tessdata) license files are included here. Keep the runtime and worker on the same release when updating.
