# Synthetic static demo

This is a marketing/documentation **sample**, not a web dashboard, hosted connector,
account login, credential proxy or upload service.

- `sample.js` is generated only by `scripts/build_synthetic_site.py` from
  `examples/synthetic_demo.py` using the real local SQLite/JSON/CSV exporter.
- Dates, identifiers and values are invented. Display timestamps are normalized
  for reproducible builds. Never substitute a personal database or export.
- CSV/JSON download bytes are constructed in the browser from the static sample.
- No analytics, telemetry, third-party scripts, file uploads or credential inputs.
- `connect-src 'none'` prevents browser fetch/XHR connections from the page.
  As with any public web page, hosting infrastructure still handles page requests;
  do not interpret this as a claim that the hosting provider has no access logs.
- GitHub Pages publishes **only `site/`**, not the repository or local runtime data.
- Chinese is the default; `?lang=en` opens English.

Rebuild and check after installing development dependencies:

```sh
python scripts/build_synthetic_site.py
python -m pytest -q -p no:cacheprovider
python -m ruff check src tests scripts
```

The generator does not read a configured account, token, user's database or network.
Browser smoke testing should cover the four dataset buttons, language switching,
CSV BOM and full JSON downloads, keyboard focus and narrow-screen overflow.
