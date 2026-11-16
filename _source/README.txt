TRAVERSIQ GLOBAL — SITE SOURCE

DEPLOY
  Upload everything in this folder to the root of the GitHub Pages repo,
  replacing the old index.html. Keep your existing brand-logo.jpg,
  usa-photos/, robots.txt and CNAME where they are.

EDIT
  All page content lives in _source/template.html. Blocks wrapped in
  <!--@only KEY--> ... <!--@end--> appear only on that page
  (home, us-visa, global-visas, passport, flights). Everything else
  (header, enquiry desk, reviews, founder, footer, scripts) is shared.
  Titles, descriptions and URLs are in the PAGES table in _source/build.py.
  Policy text is in _source/policy-content.html.

  After editing, run from the site root:
      python3 _source/build.py
  Do not edit the generated index.html files by hand; they are overwritten.

REPLACE THE TAILWIND CDN (one time, needs Node.js)
  From the site root:
      npx tailwindcss@3 -c _source/tailwind.config.js -i _source/input.css -o assets/site.css --minify
      python3 _source/build.py
  build.py switches every page to /assets/site.css once that file exists.
  Re-run both commands whenever you add new Tailwind classes.
