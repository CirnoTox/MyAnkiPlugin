# Incremental Reading prototype

Install dist/anki-ir.ankiaddon through Anki Desktop → Tools → Add-ons → Install from file, then restart. Open Tools → Incremental Reading → Reading Library. Import a title and plain text; click a library entry to read it. Search matches titles and content. Citations are displayed as plain text.

Data lives in <active profile>/incremental_reading/reading.sqlite3. This database is local and does not sync through AnkiWeb. Close Anki before copying this folder for a manual backup. This prototype does not create or modify native notes, cards, or schedules.

Build: `python build.py`. Test: `python -m unittest discover -s tests`.

## Validation and limitations

Automated storage test passed: Japanese content, persisted positions, search, input validation, and profile isolation. Package built successfully. No Anki/Qt runtime or Windows host was available, so installation, bridge API compatibility, shutdown behavior, and visual position restoration are unverified. The network proxy was unavailable, preventing verification and pinning of the current stable Anki version. No release compatibility is claimed yet.

Before release, pin the official stable Anki version and bundled Python/Qt versions; install in a disposable Windows profile; test Japanese/English reading, resizing, source switching, restart, profile switching, literal HTML rendering, storage errors, and unchanged collection state. Run a GUI smoke test against that version. Immediate scroll reporting saves positions during reading, but closing immediately after a scroll may race the webview bridge. Library search is a linear scan suitable for the prototype; large-library performance has not been measured.

Deferred: extraction, cards, queue, editing, backup UI, file/URL import, PDF and mobile/cloud.
