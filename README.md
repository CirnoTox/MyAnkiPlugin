# Anki Incremental Reading

A local-first reading prototype for Anki Desktop. Import plain text, browse a reading library, and save your place while reading.

**Status: early prototype.** Storage tests pass, but the add-on has not yet been tested inside Anki Desktop or on Windows. Use a disposable Anki profile for evaluation. No Anki release is currently verified as compatible.

## What you can do today

- Import pasted plain text with a title and optional URL or citation.
- Search source titles and text.
- Read Japanese and English text with paragraph breaks preserved.
- Save a reading position for each source.
- Keep reading data separate for each Anki profile.

Pasted HTML is displayed as text. A citation or URL is stored and displayed; entering a URL does not download an article.

The prototype does not create flashcards or change native notes, cards, schedules, or review history.

## Install on Anki Desktop

You do not need Python or Git to try the packaged add-on.

1. Download [anki-ir.ankiaddon](https://github.com/CirnoTox/MyAnkiPlugin/raw/refs/heads/main/dist/anki-ir.ankiaddon). Keep the `.ankiaddon` extension.
2. Open Anki Desktop and switch to a disposable test profile.
3. Choose **Tools → Add-ons → Install from file**.
4. Select the downloaded file and follow Anki’s prompts.
5. Restart Anki.
6. Open **Tools → Incremental Reading → Reading Library**.

Windows is the first planned manual test platform. macOS and Linux compatibility remains unverified. This Python add-on does not run in AnkiMobile, AnkiDroid, or AnkiWeb.

## First reading session

1. In the Reading Library, click **Import Text**.
2. Enter a title and paste the text you want to read.
3. Optionally enter a source URL or citation.
4. Click **Import**, then click the new library entry.
5. Scroll through the reader. Position updates are saved while you read.
6. Select another entry to switch sources, or reopen the library later to continue.

Use the search box to filter by title or text. Sources are loaded in most-recently-opened order when the list refreshes.

Position restoration is intended to return to the visible paragraph and its relative position. Resizing can change the layout, and restoration has not yet been verified in Anki. Closing immediately after scrolling may race a pending position update.

## Your data and backups

Reading data is stored in:

```text
<active Anki profile>/incremental_reading/reading.sqlite3
```

Each profile has its own database. Reading text and progress remain local and **do not sync through AnkiWeb**.

To make a manual backup:

1. Close Anki completely.
2. Copy the profile’s entire `incremental_reading` folder to a safe location.
3. Keep that copy separate from the live folder.

There is no backup or restore interface yet. A normal Anki collection export should not be treated as a backup of this separate reading database.

## Development

Python is needed to run the storage test and packaging script. Running the UI requires Anki Desktop and its bundled Qt environment; this is not a standalone reader application.

From the repository root:

```bash
python -m unittest discover -s tests
python build.py
```

The packaging command writes `dist/anki-ir.ankiaddon`. It includes the add-on code and reader assets, excluding Python cache directories.

| Path | Purpose |
| --- | --- |
| `addon/__init__.py` | Anki menus, library, import dialog, and reader integration |
| `addon/storage.py` | Profile-local SQLite persistence and position validation |
| `addon/web/reader.js` | Reader position reporting and restoration |
| `tests/test_storage.py` | Storage round-trip, search, validation, and profile-isolation checks |
| `build.py` | Add-on packaging |

## Validation and known limitations

Completed checks:

- Storage test covering Japanese text, persisted reading positions, search, invalid input, and profile isolation.
- Python compilation.
- Add-on ZIP packaging.

Still required before a tested release:

- Verify and record the target stable Anki version and its Python/Qt versions.
- Install and smoke-test the package in a disposable Windows profile.
- Check reader bridge compatibility, source switching, restart, resizing, and profile shutdown.
- Test literal HTML display, failed saves, and unchanged native collection state.

No Windows host or Anki/Qt runtime was available during initial development. Network access also failed when attempting to verify the current Anki release. The generated package is a prototype artifact, not a validated release.

Search scans stored records directly; performance with large libraries is unmeasured. Editing, deleting sources, and automatic recovery tools are not implemented.

## Roadmap

The intended workflow is **read → extract → create native Anki cards**, with reading revisits managed separately from Anki’s memory scheduler.

| Stage | Planned capability | Status |
| --- | --- | --- |
| Core prototype | Text import, library, reader, persisted positions | Implemented; desktop validation pending |
| Extraction | Nested extracts with source lineage | Planned |
| Flashcards | Native Cloze and Basic notes with citations | Planned |
| Reading queue and recovery | Priority, revisit dates, backup and restore | Planned |
| Documents | Text-selectable PDF support, then EPUB | Deferred |
| Mobile reading | Optional independent sync and iPad web app | Deferred |

PDF import, URL fetching, highlights, AI generation, and cloud sync are not included in the current package.

## Report a problem

[Open an issue](https://github.com/CirnoTox/MyAnkiPlugin/issues) with your Anki version, operating system, steps to reproduce, and any error message. Use a small sample passage when possible; avoid posting private reading material or profile databases.
