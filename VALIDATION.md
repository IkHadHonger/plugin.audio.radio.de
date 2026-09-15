# Preparation validation — 2026-09-15

Passed locally:

- Python syntax and XML parsing, including the corrected settings.xml.
- Required package files, metadata identity and archive integrity.
- Two builds produce identical ZIP bytes.
- Every runtime Python file matches the user-supplied 1.1.13 archive byte for byte.
- Staging against a local copy of the current Piers catalogue preserves every
  existing addon entry. An AVDVPlus sentinel file remains unchanged.
- Repeated staging produces the same catalogue.
- Publication rejects an existing version with different ZIP bytes.

The supplied m3u_parser.py produces three invalid-escape SyntaxWarnings on
Python 3.12; parsing succeeds. These inherited expressions were not changed.

Not tested: execution of GitHub Actions, cross-repository credentials, actual
GitHub publication, Kodi installation, station APIs and live playback.
The originally proposed repository name was not accessible during preparation.
The user subsequently created `IkHadHonger/plugin.audio.radio.de`; repository
references were updated for import. No distribution repository was modified.
