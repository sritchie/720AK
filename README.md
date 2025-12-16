# RV-10 Pilot's Operating Handbook

Generate a professional POH PDF using Pandoc and Typst.

## Prerequisites

```bash
# macOS
brew install pandoc typst

# Linux
# Pandoc: https://pandoc.org/installing.html
# Typst: https://github.com/typst/typst/releases
```

## Directory Structure

```
rv10-poh/
├── README.md                 # This file
├── metadata.yaml             # Document title, author, revision
├── template.typ              # Typst template (header/footer/styling)
├── build.sh                  # Build script
├── json_to_markdown.py       # Convert checklist JSON to markdown
├── sections/
│   ├── 01-general.md
│   ├── 02-limitations.md
│   ├── 03-engine-info.md
│   ├── 04-emergency.md       # Generated from JSON
│   ├── 05-normal.md          # Generated from JSON
│   ├── 06-performance.md
│   ├── 07-weight-balance.md
│   ├── 08-systems.md
│   └── 09-servicing.md
├── images/
│   └── (your aircraft photos)
└── output/
    └── poh.pdf
```

## Quick Start

1. Edit `metadata.yaml` with your N-number and details
2. Fill in the section templates in `sections/`
3. Convert your checklist JSON:
   ```bash
   python3 json_to_markdown.py /path/to/checklist.json
   ```
4. Build the PDF:
   ```bash
   ./build.sh
   ```

## Build Command

```bash
pandoc metadata.yaml sections/*.md \
  --to=typst \
  --template=template.typ \
  --toc \
  --number-sections \
  -o output/poh.pdf
```

## Customization

### Aircraft Details
Edit `metadata.yaml`:
```yaml
title: "Pilot's Operating Handbook"
aircraft-type: "RV-10"
n-number: "N12345"
revision: "1.0"
builder: "Your Name"
serial: "41234"
```

### Styling
Edit `template.typ` to customize:
- Page headers and footers
- Fonts and sizes
- Table styling
- Section formatting

### Adding Images
Place images in `images/` and reference them:
```markdown
![My RV-10](images/aircraft.jpg)
```

### Tables
Use Pandoc pipe tables:
```markdown
| Parameter | Value |
|-----------|-------|
| Wing Span | 32' 9" |
| Length | 25' |
```

### Page Breaks
Insert `\pagebreak` where needed.

## Why Typst over LaTeX?

- Much faster compilation (instant vs seconds)
- Simpler syntax
- Better error messages
- Modern, actively developed
- No massive TeX distribution to install
