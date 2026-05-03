import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkfont


SITES = ["linkedin", "zip_recruiter", "indeed", "glassdoor", "google", "bayt", "bdjobs"]


class MultiSelectDropdown(ttk.Frame):
    """Pulsante che apre un popup con checkbox per selezione multipla."""

    def __init__(self, parent, options, colors, default_all=True, **kwargs):
        super().__init__(parent, style="App.TFrame", **kwargs)
        self._options = options
        self._vars = {opt: tk.BooleanVar(value=default_all) for opt in options}
        self._popup = None
        self._colors = colors

        self._btn_var = tk.StringVar()
        self._update_label()
        self._btn = ttk.Button(self, textvariable=self._btn_var, command=self._apri_popup)
        self._btn.pack(fill=tk.X)

    def _summary(self):
        sel = [o for o, v in self._vars.items() if v.get()]
        n, tot = len(sel), len(self._options)
        if n == tot:
            return f"Tutti ({tot})  ▾"
        if n == 0:
            return "Nessuno selezionato  ▾"
        if n <= 3:
            return ", ".join(sel) + "  ▾"
        return f"{n} siti selezionati  ▾"

    def _update_label(self):
        self._btn_var.set(self._summary())

    def _apri_popup(self):
        if self._popup and self._popup.winfo_exists():
            return

        popup = tk.Toplevel(self.winfo_toplevel())
        self._popup = popup
        popup.overrideredirect(True)
        popup.configure(background=self._colors["border"])

        inner = tk.Frame(popup, background=self._colors["panel"], padx=12, pady=8)
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        for opt in self._options:
            tk.Checkbutton(
                inner,
                text=opt,
                variable=self._vars[opt],
                background=self._colors["panel"],
                foreground=self._colors["text"],
                activebackground="#F9FAFB",
                selectcolor="#F3F4F6",
                font=("Segoe UI", 10),
                anchor="w",
                cursor="hand2",
            ).pack(fill=tk.X, pady=1)

        ttk.Separator(inner, orient="horizontal").pack(fill=tk.X, pady=(6, 4))

        btn_row = tk.Frame(inner, background=self._colors["panel"])
        btn_row.pack(fill=tk.X)

        def _chiudi():
            popup.grab_release()
            popup.destroy()
            self._popup = None
            self._update_label()

        for txt, cmd in [
            ("Tutti", lambda: [v.set(True) for v in self._vars.values()]),
            ("Nessuno", lambda: [v.set(False) for v in self._vars.values()]),
        ]:
            tk.Button(
                btn_row, text=txt, command=cmd,
                background="#F3F4F6", foreground=self._colors["text"],
                relief="flat", padx=8, pady=3, cursor="hand2", font=("Segoe UI", 9),
            ).pack(side=tk.LEFT, padx=(0, 4))

        tk.Button(
            btn_row, text="Conferma", command=_chiudi,
            background=self._colors["accent"], foreground="#FFFFFF",
            relief="flat", padx=10, pady=3, cursor="hand2", font=("Segoe UI", 9, "bold"),
        ).pack(side=tk.RIGHT)

        popup.update_idletasks()
        bx = self._btn.winfo_rootx()
        by = self._btn.winfo_rooty() + self._btn.winfo_height()
        popup.geometry(f"+{bx}+{by}")
        popup.lift()
        popup.grab_set()

    def get_selected(self):
        return [opt for opt, var in self._vars.items() if var.get()]


class ConfigurazioneGUI:

    def __init__(self):
        self.risultato = None
        self.root = tk.Tk()
        self.root.title("Configurazione Jobby")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        self.dir_output_var = tk.StringVar()
        self.nome_aggregato_var = tk.StringVar(value="jobs_output.xlsx")
        self.numero_risultati = tk.StringVar(value=100)
        self.location = tk.StringVar(value="Milano, Lombardia, Italia")
        self.days_old = tk.StringVar(value=15)
        self.country_indeed = tk.StringVar(value="Italy")
        self.job_type_map = {
            "Tempo pieno": "fulltime",
            "Part-time": "parttime",
            "Stage": "internship",
        }
        self.job_type = tk.StringVar(value="Tempo pieno")
        self.verbose = tk.StringVar(value=2)
        self.distance = tk.StringVar(value=50)
        self.is_remote = tk.BooleanVar(value=False)

        self._configura_stile()
        self._crea_interfaccia()

    def _configura_stile(self):
        self.colors = {
            "bg": "#F4F1ED",
            "panel": "#FFFFFF",
            "accent": "#D97706",
            "accent_dark": "#B45309",
            "text": "#1F2937",
            "muted": "#6B7280",
            "border": "#E5E7EB",
        }

        self.root.configure(background=self.colors["bg"])
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        base_font = tkfont.nametofont("TkDefaultFont")
        base_font.configure(family="Segoe UI", size=10)
        self.root.option_add("*Font", base_font)

        style.configure("App.TFrame", background=self.colors["bg"])
        style.configure("Card.TLabelframe", background=self.colors["panel"], bordercolor=self.colors["border"])
        style.configure(
            "Card.TLabelframe.Label",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            font=("Segoe UI", 11, "bold"),
        )
        style.configure("App.TLabel", background=self.colors["panel"], foreground=self.colors["text"])
        style.configure("Muted.TLabel", background=self.colors["panel"], foreground=self.colors["muted"])
        style.configure("Title.TLabel", background=self.colors["bg"], foreground=self.colors["text"], font=("Segoe UI", 15, "bold"))
        style.configure("TEntry", fieldbackground="#FFFFFF")
        style.configure("TCheckbutton", background=self.colors["panel"])
        style.configure("Accent.TButton", background=self.colors["accent"], foreground="#FFFFFF", padding=(10, 6))
        style.map(
            "Accent.TButton",
            background=[("active", self.colors["accent_dark"]), ("pressed", self.colors["accent_dark"])],
        )

    def _crea_interfaccia(self):
        main = ttk.Frame(self.root, padding=20, style="App.TFrame")
        main.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        # ── Titolo ────────────────────────────────────────────────────────────
        ttk.Label(main, text="Configurazione Jobby", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 14)
        )

        # ── Colonna sinistra ──────────────────────────────────────────────────
        left = ttk.Frame(main, style="App.TFrame")
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)

        # Parole chiave
        kw_frame = ttk.Labelframe(left, text="Parole chiave", padding=12, style="Card.TLabelframe")
        kw_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        kw_frame.columnconfigure(0, weight=1)
        kw_frame.rowconfigure(1, weight=1)

        ttk.Label(kw_frame, text="Una per riga o separate da virgola", style="Muted.TLabel").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 8)
        )

        txt_wrap = ttk.Frame(kw_frame, style="App.TFrame")
        txt_wrap.grid(row=1, column=0, sticky="nsew")
        txt_wrap.columnconfigure(0, weight=1)
        txt_wrap.rowconfigure(0, weight=1)

        self.keywords_text = tk.Text(
            txt_wrap,
            wrap="word",
            background="#FFFFFF",
            foreground=self.colors["text"],
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 10),
        )
        self.keywords_text.grid(row=0, column=0, sticky="nsew")
        self.keywords_text.insert("1.0", "Senior Data Analyst\nData Analyst")

        sb = ttk.Scrollbar(txt_wrap, orient="vertical", command=self.keywords_text.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.keywords_text["yscrollcommand"] = sb.set

        # Siti di ricerca
        sites_frame = ttk.Labelframe(left, text="Siti di ricerca", padding=12, style="Card.TLabelframe")
        sites_frame.grid(row=1, column=0, sticky="ew", pady=(0, 0))
        sites_frame.columnconfigure(0, weight=1)

        ttk.Label(
            sites_frame,
            text="Seleziona i siti da cercare (default: tutti)",
            style="Muted.TLabel",
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 6))

        self.sites_dropdown = MultiSelectDropdown(
            sites_frame, SITES, self.colors, default_all=True
        )
        self.sites_dropdown.grid(row=1, column=0, sticky="ew")

        # ── Colonna destra ────────────────────────────────────────────────────
        right = ttk.Frame(main, style="App.TFrame")
        right.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right.columnconfigure(0, weight=1)

        # Salvataggio
        out_frame = ttk.Labelframe(right, text="Salvataggio", padding=12, style="Card.TLabelframe")
        out_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        out_frame.columnconfigure(1, weight=1)

        ttk.Label(out_frame, text="Cartella output", style="App.TLabel").grid(row=0, column=0, sticky=tk.W, pady=6)
        ttk.Entry(out_frame, textvariable=self.dir_output_var).grid(row=0, column=1, sticky="ew", pady=6, padx=6)
        ttk.Button(out_frame, text="Sfoglia", command=self._sfoglia_cartella).grid(row=0, column=2, pady=6)

        ttk.Label(out_frame, text="Nome file output", style="App.TLabel").grid(row=1, column=0, sticky=tk.W, pady=6)
        ttk.Entry(out_frame, textvariable=self.nome_aggregato_var).grid(row=1, column=1, sticky="ew", pady=6, padx=6)

        # Opzioni avanzate
        adv_frame = ttk.Labelframe(right, text="Opzioni avanzate", padding=12, style="Card.TLabelframe")
        adv_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        adv_frame.columnconfigure(1, weight=1)

        rows = [
            ("Numero risultati (x ricerca)", self.numero_risultati, "entry"),
            ("Zona", self.location, "entry"),
            ("Annunci degli ultimi N giorni", self.days_old, "entry"),
            ("Paese per Indeed", self.country_indeed, "entry"),
            ("Tipo di lavoro", self.job_type, "job_type"),
            ("Verbosità", self.verbose, "verbose"),
            ("Distanza (km)", self.distance, "entry"),
            ("Solo remoto", self.is_remote, "check"),
        ]

        for i, (label, var, kind) in enumerate(rows):
            ttk.Label(adv_frame, text=label, style="App.TLabel").grid(row=i, column=0, sticky=tk.W, pady=5)
            if kind == "entry":
                ttk.Entry(adv_frame, textvariable=var).grid(row=i, column=1, sticky="ew", pady=5, padx=6)
            elif kind == "job_type":
                ttk.Combobox(
                    adv_frame, textvariable=var,
                    values=list(self.job_type_map.keys()),
                    state="readonly",
                ).grid(row=i, column=1, sticky="ew", pady=5, padx=6)
            elif kind == "verbose":
                ttk.Combobox(
                    adv_frame, textvariable=var,
                    values=["0", "1", "2"],
                    state="readonly",
                ).grid(row=i, column=1, sticky="ew", pady=5, padx=6)
            elif kind == "check":
                ttk.Checkbutton(adv_frame, variable=var).grid(row=i, column=1, sticky=tk.W, pady=5, padx=6)

        ttk.Label(
            adv_frame, text="0=errori  1=avvisi  2=tutti i log", style="Muted.TLabel"
        ).grid(row=5, column=1, sticky=tk.W, padx=6, pady=(0, 4))

        # ── Pulsanti ──────────────────────────────────────────────────────────
        btn_frame = ttk.Frame(main, style="App.TFrame")
        btn_frame.grid(row=2, column=0, columnspan=2, sticky=tk.E, pady=(12, 0))
        ttk.Button(btn_frame, text="Annulla", command=self._annulla, width=12).pack(side=tk.RIGHT, padx=6)
        ttk.Button(btn_frame, text="Conferma", command=self._conferma, style="Accent.TButton", width=12).pack(side=tk.RIGHT, padx=6)

    def _sfoglia_cartella(self):
        self.root.update()
        cartella = filedialog.askdirectory(parent=self.root)
        if cartella:
            self.dir_output_var.set(cartella)

    def _conferma(self):
        raw = self.keywords_text.get("1.0", "end").strip()
        if not raw:
            messagebox.showwarning("Attenzione", "Inserire almeno una parola chiave")
            return

        parts = [p.strip() for line in raw.splitlines() for p in line.split(",") if p.strip()]
        if not parts:
            messagebox.showwarning("Attenzione", "Inserire almeno una parola chiave valida")
            return

        if not self.dir_output_var.get() or not self.nome_aggregato_var.get():
            messagebox.showwarning("Attenzione", "Selezionare la cartella di output e specificare il nome del file")
            return

        siti = self.sites_dropdown.get_selected()
        if not siti:
            messagebox.showwarning("Attenzione", "Selezionare almeno un sito di ricerca")
            return

        self.risultato = {
            "nome_aggregato": self.nome_aggregato_var.get(),
            "output_dir": self.dir_output_var.get(),
            "lista_titoli": parts,
            "risultati": int(self.numero_risultati.get()),
            "location": self.location.get(),
            "days_old": int(self.days_old.get()),
            "country_indeed": self.country_indeed.get(),
            "job_type": self.job_type_map.get(self.job_type.get(), self.job_type.get()),
            "verbose": int(self.verbose.get()),
            "distance": int(self.distance.get()),
            "is_remote": self.is_remote.get(),
            "site_name": siti,
        }
        self.root.quit()
        self.root.destroy()

    def _annulla(self):
        self.risultato = None
        self.root.quit()
        self.root.destroy()

    def mostra(self):
        self.root.mainloop()
        return self.risultato


def ottieni_configurazione():
    gui = ConfigurazioneGUI()
    return gui.mostra()


if __name__ == "__main__":
    config = ottieni_configurazione()
    if config:
        print("\nConfigurazione ottenuta:")
        for k, v in config.items():
            print(f"  {k}: {v}")
    else:
        print("Operazione annullata dall'utente")
