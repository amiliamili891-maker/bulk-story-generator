# Bulk Story Generator

Single-file, client-side web app for bulk-editing Instagram images. No backend, no build step — open the HTML in a browser or deploy as static files.

## Pages

- **`index.html`** — Bulk Instagram Story generator (1080×1920)
- **`post.html`** — Bulk Instagram Post generator (4:5 1080×1350, 3:4 1080×1440, 9:16 1080×1920)
- **`editor.html`** — Single-image story editor

## Features

- Drag & drop up to 150 images
- Per-image zoom / reposition
- Fit modes: fill & crop, fit, pad with blurred background, stretch
- Bulk export as ZIP (JSZip from CDN)
- 100% client-side — images never leave the browser

## Local use

```
open post.html
```

Or serve statically:

```
python3 -m http.server 8000
```

## Deploy

Works on any static host (Vercel, Netlify, GitHub Pages, Cloudflare Pages). No config required — just point at the repo root.
