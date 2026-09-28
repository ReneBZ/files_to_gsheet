# CSV to Google Sheets Auto-Uploader

Upload a `.csv` file to Google Drive, convert it to a Google Sheet, and open it in your browser.

Works the same on every Mac: **double-click** a CSV, or **right-click → Upload to Sheets** for downloaded files.

## Prerequisites

1. **Python 3** (macOS built-in or Homebrew)
2. **Google Cloud Project** with the Drive API enabled
3. **`Csv_to_Sheets_rbz.app`** in iCloud Drive (source Automator app)

## Setup (run on each Mac)

Clone or pull this repo, then run the installer:

```bash
cd /Users/renebravo/Python/files_to_gsheet
./install.sh
```

This installs everything:

- Python virtual environment (`.venv/`) with dependencies
- **Double-click default** — `~/Applications/Upload to Sheets.app`
- **Right-click action** — Quick Action "Upload to Sheets" in Finder

### Google credentials (once per repo)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project.
3. Enable the **Google Drive API**.
4. Create **OAuth credentials** (Desktop app).
5. Download the JSON and save as `credentials.json` in this folder.

You can copy `credentials.json` between Macs (it is gitignored).

### First-time authentication (once per Mac)

```bash
./launcher.sh test.csv
```

A browser window opens for Google sign-in. This creates `token.pickle` on that Mac.

## Usage

| Action | When to use |
|---|---|
| **Double-click** a `.csv` | Normal files |
| **Right-click → Upload to Sheets** | Downloaded files (avoids Gatekeeper issues) |

## Keeping Macs in sync

After pulling updates on any Mac, re-run:

```bash
./install.sh
```

Shared via git: `launcher.sh`, `csv_to_sheets.py`, workflows, install script.

Per-machine (not in git): `.venv/`, `credentials.json`, `token.pickle`, `~/Applications/Upload to Sheets.app`, `~/Library/Services/UploadToSheets.workflow`.

## Troubleshooting

**`RefreshError: invalid_grant` / Automator "Run Shell Script" error**  
The saved Google login (`token.pickle`) was revoked or expired. Re-authenticate from a terminal:

```bash
./launcher.sh test.csv
```

Sign in in the browser that opens. After that, double-clicking a CSV works again.

If this keeps happening after about a week, the Google Cloud OAuth app is likely still in **Testing**. In [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → OAuth consent screen, set the publishing status to **In production** (or re-auth when the token expires). Testing-mode refresh tokens expire after 7 days.

**Downloaded CSV blocked by macOS ("cannot verify malware")**  
Use **Right-click → Upload to Sheets** instead of double-click.

**Double-click opens Numbers instead of uploading**  
Re-run `./install.sh`, or set manually: right-click CSV → Get Info → Open with → Upload to Sheets → Change All.
