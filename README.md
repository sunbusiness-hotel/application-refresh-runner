# Application data refresh runner

A small GitHub Actions workflow that refreshes a privately hosted application's data.
The application URL, authentication, collector source, and application data are private.
This repository contains only the generic workflow. It stores no downloaded source,
application data, credentials, artifacts, or caches. Logs contain only completion status.
It uses standard Ubuntu runners, which are free for public repositories.

A daily completion date is committed after a successful refresh, keeping the operational status visible and scheduled publishing active. No application data is included.

After successful collection, `sync-sheet.py` calls the existing private spreadsheet service with a source selector only. Its separate callback credential cannot use management actions or supply cell values. The service fetches verified current data and checks saved cell values before acknowledging success. A failed/ambiguous acknowledgement is retried once and fails the job if still unverified. Subsequent scheduled runs retry normally. `SHEET_SYNC_URL` and `SHEET_SYNC_TOKEN` are repository secrets. No extra polling workflow or new paid resource is added.

Run `python3 -m unittest test_sync_sheet.py` before changing this callback.

Sheet verification adds at most two 45-second requests and one 5-second wait. Job time limits include this acknowledgement window (stock 7 minutes, application 6 minutes); source subprocess limits and schedule cadence are unchanged.
