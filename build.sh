#!/bin/bash
set -e

mkdir -p output

case "${1:-all}" in
  pdf)
    echo "Building PDF..."
    # Exclude SUMMARY.md (mdBook-only) from PDF build
    pandoc metadata.yaml \
      sections/00-introduction.md \
      sections/01-general.md \
      sections/02-limitations.md \
      sections/03-engine-info.md \
      sections/04-emergency.md \
      sections/04b-abnormal.md \
      sections/05-normal.md \
      sections/06-performance.md \
      sections/07-weight-balance.md \
      sections/08-systems.md \
      sections/09-servicing.md \
      --to=typst \
      --template=template.typ \
      --toc \
      --number-sections \
      -o output/poh.pdf
    echo "Done: output/poh.pdf"
    ;;

  html)
    echo "Building HTML site with mdBook..."
    mdbook build
    echo "Done: output/html/index.html"
    ;;

  serve)
    echo "Starting mdBook dev server..."
    mdbook serve --open
    ;;

  all)
    $0 pdf
    $0 html
    ;;

  *)
    echo "Usage: ./build.sh [pdf|html|serve|all]"
    echo ""
    echo "  pdf    - Build PDF using Pandoc/Typst"
    echo "  html   - Build static HTML site using mdBook"
    echo "  serve  - Start mdBook dev server with live reload"
    echo "  all    - Build both PDF and HTML"
    exit 1
    ;;
esac
