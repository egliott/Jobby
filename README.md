# Jobby

**Jobby** is a Windows desktop app that aggregates job listings from multiple platforms into a single Excel file. Ideated for who in not able to code.

Built on top of [JobSpy](https://github.com/Bunsly/JobSpy).

---

## Features

- Search across **LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google, Bayt, BDJobs** (configurable)
- Run multiple search terms in one go
- Filter by location, job type, recency, remote, and distance
- Export everything to a single `.xlsx` file
- Clean GUI — without terminal

---

## Requirements

- Windows 10/11
- Python 3.10+ (or use the prebuilt `.exe`)
- Conda (recommended) or a standard virtual environment

---

## Installation (from source)

```bash
conda create -n jobby python=3.11
conda activate jobby
pip install jobspy pandas openpyxl
```

Then clone or download this repository.

---

## Usage

### Run from source

```bash
conda activate jobby
cd "path\to\Actual jobby"
python jobby.py
```

### Run the prebuilt executable

Download `Jobby --v.1.0.exe` from the [Releases](../../releases) page and double-click it. No installation required.

---

## GUI walkthrough

| Field | Description |
|---|---|
| **Parole chiave** | Search terms, one per line or comma-separated |
| **Siti di ricerca** | Pick which platforms to scrape (default: all) |
| **Cartella output** | Where to save the Excel file |
| **Nome file output** | Output filename (`.xlsx`) |
| **Numero risultati** | Max results per search term per site |
| **Zona** | City/region to search in |
| **Annunci degli ultimi N giorni** | Only show listings posted within N days |
| **Paese per Indeed** | Country code used by Indeed |
| **Tipo di lavoro** | Full-time, part-time, or internship |
| **Verbosità** | Log level: 0 = errors only, 1 = warnings, 2 = all |
| **Distanza** | Search radius in km |
| **Solo remoto** | Filter for remote positions only |

---

## Build executable (optional)

```bash
conda activate jobby
cd "path\to\Actual jobby"
pyinstaller jobby.py --noconsole --name Jobby --onefile --clean --noconfirm ^
  --exclude-module polars --exclude-module matplotlib ^
  --exclude-module PyQt5 --exclude-module PyQt5-sip ^
  --exclude-module qtpy --exclude-module pyside2 ^
  --exclude-module jupyterlab --exclude-module jupyter ^
  --exclude-module jupyter-console --exclude-module notebook
```

The `.exe` will be in the `dist\` folder.

---

## License

[MIT](LICENSE) — Elia Casiraghì 2025
