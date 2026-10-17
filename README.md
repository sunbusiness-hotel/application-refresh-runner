# Application data refresh runner

A small GitHub Actions workflow that refreshes a privately hosted application's data.
The application URL, authentication, collector source, and application data are private.
This repository contains only the generic workflow. It stores no downloaded source,
application data, credentials, artifacts, or caches. Logs contain only completion status.
It uses standard Ubuntu runners, which are free for public repositories.
