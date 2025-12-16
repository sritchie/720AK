#!/bin/bash
set -e

mkdir -p output

case "${1:-all}" in
  pdf)
    echo "Building PDF..."
    pandoc metadata.yaml sections/*.md \
      --to=typst \
      --template=template.typ \
      --toc \
      --number-sections \
      -o output/poh.pdf
    echo "Done: output/poh.pdf"
    ;;

  html)
    echo "Building HTML site..."
    pandoc metadata.yaml sections/*.md \
      --to=html5 \
      --standalone \
      --toc \
      --toc-depth=2 \
      --number-sections \
      --metadata title="Pilot's Operating Handbook" \
      --css=style.css \
      -o output/index.html

    # Copy CSS if not exists
    if [ ! -f output/style.css ]; then
      cp style.css output/ 2>/dev/null || cat > output/style.css << 'EOF'
body { max-width: 800px; margin: 0 auto; padding: 2rem; font-family: system-ui, sans-serif; }
h1, h2, h3 { color: #333; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border: 1px solid #ddd; padding: 0.5rem; text-align: left; }
th { background: #f5f5f5; }
#TOC { background: #f9f9f9; padding: 1rem; margin-bottom: 2rem; }
#TOC ul { list-style: none; padding-left: 1rem; }
blockquote { border-left: 3px solid #ccc; padding-left: 1rem; color: #666; }
EOF
    fi

    # Copy images if they exist
    cp -r images output/ 2>/dev/null || true

    echo "Done: output/index.html"
    ;;

  all)
    $0 pdf
    $0 html
    ;;

  *)
    echo "Usage: ./build.sh [pdf|html|all]"
    exit 1
    ;;
esac
