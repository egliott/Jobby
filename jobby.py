############# NON CANCELLARE QUESTI COMMENTI #############
# env: conda activate jobby
# cd "C:\Users\nergh\Desktop\DEV job\jobby\Actual jobby"
# pyinstaller jobby.py --noconsole --name Jobby --onefile --clean --noconfirm --exclude-module polars --exclude-module matplotlib --exclude-module PyQt5 --exclude-module PyQt5-sip --exclude-module qtpy --exclude-module pyside2 --exclude-module jupyterlab --exclude-module jupyter --exclude-module jupyter-console --exclude-module notebook
##########################################################

import os
import traceback
import tkinter as tk
from tkinter import messagebox

import pandas as pd
from jobspy import scrape_jobs

from jobby_gui import ottieni_configurazione


def _show_message(title, message, is_error=False):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    if is_error:
        messagebox.showerror(title, message, parent=root)
    else:
        messagebox.showinfo(title, message, parent=root)
    root.destroy()


def run_search(config: dict) -> tuple[pd.DataFrame, str]:
    lista_titoli = config["lista_titoli"]
    output_dir = config["output_dir"]
    nome_file = config["nome_aggregato"]
    risultati = config["risultati"]
    location = config["location"]
    time = config["days_old"]
    country_indeed = config["country_indeed"]
    job_type = config["job_type"]
    verbose = config["verbose"]
    distance = config["distance"]
    is_remote = config["is_remote"]
    site_name = config.get("site_name", ["linkedin", "indeed", "glassdoor"])

    os.makedirs(output_dir, exist_ok=True)

    all_jobs = pd.DataFrame()

    for search_term in lista_titoli:
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            location=location,
            results_wanted=risultati,
            hours_old=24 * time,
            country_indeed=country_indeed,
            job_type=job_type,
            verbose=verbose,
            linkedin_fetch_description=True,
            is_remote=is_remote,
            distance=distance,
        )

        print(f"{search_term} - ricerca completata, trovati {len(jobs)} lavori")

        jobs["search_term"] = search_term
        all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)

    filepath = os.path.join(output_dir, nome_file)
    all_jobs.to_excel(filepath, index=False)

    return all_jobs, filepath


def main():
    config = ottieni_configurazione()
    if not config:
        _show_message("Jobby", "Operazione annullata dall'utente.")
        return

    all_jobs, filepath = run_search(config)

    _show_message(
        "Jobby",
        f"Totale jobs raccolti: {len(all_jobs)}\nFile salvato in:\n{filepath}",
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        _show_message("Errore Jobby", f"Si e verificato un errore:\n{exc}\n\n{traceback.format_exc()}", is_error=True)
