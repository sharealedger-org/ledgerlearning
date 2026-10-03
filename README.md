# LedgerLearning.com — Static Site

**Live site:** [ledgerlearning.com](https://ledgerlearning.com)  
**GitHub Pages source:** `docs/` branch served at the apex domain via DNS  
**Author & Copyright:** Kip M. Twitchell © 2016–2026. All rights reserved.  
**Organization:** [Sharealedger, NFP](https://sharealedger.org)

---

## About This Repository

This repository hosts the static HTML source for **LedgerLearning.com**, migrated from
WordPress (Bluehost) to zero-cost GitHub Pages in October 2026.

LedgerLearning is the educational and media gateway for Sharealedger — home to:
- **Conversations with Kip** — 250+ video episodes on financial systems, accounting history,
  data supply chains, REA modeling, and ledger innovation
- **Balancing Act** — a full online textbook (68 chapters + appendices)
- **Metric Engine Monograph** — a technical white paper on high-performance reporting engines
- **Courses** — free self-paced courses on reclassification, the accounting cycle, and more
- **Blog** — written commentary on financial systems, AI, and open-source innovation

---

## Repository Structure

```
docs/                   GitHub Pages root (served at ledgerlearning.com)
  index.html            Home page
  about.html            About page
  vlog.html             Full episode index
  books.html            Books landing page
  whitepapers.html      White papers & monographs
  courses.html          Courses & resources
  blog.html             Blog index
  assets/
    css/style.css       Shared stylesheet
    images/             Logos and thumbnails
  2016/ … 2022/         Post pages — /yyyy/mm/dd/slug/index.html
  books/                Balancing Act & Metric Engine chapter pages
  whitepapers/          Whitepaper detail pages
  courses/              Course sub-pages
scripts/
  generate_posts.py     Generates post pages from WXR export
  generate_book.py      Generates Balancing Act chapter pages from WXR export
website/
  ledgerlearning.WordPress.2026-10-02.xml   Source WXR export (do not delete)
```

---

## DNS Configuration

Point `ledgerlearning.com` at GitHub Pages:
- A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- `www` CNAME: `sharealedger-org.github.io`
- `docs/CNAME` file contains: `ledgerlearning.com`

---

## License

All video content, written articles, textbook chapters, and course materials are
copyright © Kip M. Twitchell. All rights reserved. No reproduction without permission.
