// Typst template for Pilot's Operating Handbook
// Customized for RV aircraft

// Define horizontal rule for Pandoc output
#let horizontalrule = line(length: 100%, stroke: 0.5pt)

#let project(
  title: "",
  aircraft-type: "RV-10",
  n-number: "NXXXXX",
  revision: "1.0",
  builder: "",
  serial: "",
  construction-dates: "",
  body,
) = {
  // Document settings
  set document(title: title, author: n-number)

  set page(
    paper: "us-letter",
    margin: (top: 1in, bottom: 1in, left: 1in, right: 1in),
    header: context {
      if counter(page).get().first() > 1 {
        [Pilot's Operating Handbook #h(1fr) #aircraft-type]
        line(length: 100%, stroke: 0.5pt)
      }
    },
    footer: context {
      line(length: 100%, stroke: 0.5pt)
      v(4pt)
      [Revision #revision #h(1fr) #counter(page).display("1 of 1", both: true) #h(1fr) #emph(n-number)]
    },
  )

  // Font settings
  set text(font: "New Computer Modern", size: 11pt)

  // Heading styles
  set heading(numbering: "1.1")

  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(0.5em)
    text(size: 18pt, weight: "bold", it)
    v(0.5em)
  }

  show heading.where(level: 2): it => {
    v(0.5em)
    text(size: 14pt, weight: "bold", style: "italic", it)
    v(0.3em)
  }

  show heading.where(level: 3): it => {
    v(0.3em)
    text(size: 12pt, weight: "bold", it)
    v(0.2em)
  }

  // Table styling
  set table(
    stroke: 0.5pt,
    inset: 6pt,
  )

  // Title page
  align(center)[
    #v(1in)
    #text(size: 16pt)[#aircraft-type]

    #text(size: 24pt, weight: "bold", style: "italic")[#n-number]

    #text(size: 20pt, weight: "bold")[#title]

    #v(0.5em)
    #text(size: 14pt)[Revision #revision]

    #v(2in)

    // Placeholder for aircraft photo
    #rect(width: 80%, height: 3in, stroke: 1pt)[
      #align(center + horizon)[
        _Insert aircraft photo here_

        `images/aircraft.jpg`
      ]
    ]

    #v(1in)

    #align(right)[
      #text(size: 12pt)[
        Constructed by: \
        #builder \
        Serial number #serial \
        Construction: #construction-dates
      ]
    ]
  ]

  pagebreak()

  // Table of contents (page 2 - back of title page sheet)
  outline(
    title: [Table of Contents],
    depth: 2,
    indent: 1em,
  )

  // Content starts on page 3 (new sheet)
  // Each chapter (level 1 heading) will start on a new page
  body
}

// Apply the template
#show: project.with(
  $if(title)$title: "$title$",$endif$
  $if(aircraft-type)$aircraft-type: "$aircraft-type$",$endif$
  $if(n-number)$n-number: "$n-number$",$endif$
  $if(revision)$revision: "$revision$",$endif$
  $if(builder)$builder: "$builder$",$endif$
  $if(serial)$serial: "$serial$",$endif$
  $if(construction-dates)$construction-dates: "$construction-dates$",$endif$
)

$body$
