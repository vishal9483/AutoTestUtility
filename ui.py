"""
UI logic for AutoTestUtility.
"""

import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from logger import Logger
from modules.data_extraction import run as data_extraction_run
from modules.io_json import run as io_json_run
from modules.output_json_windows import run as output_json_windows_run
from modules.output_json_linux import run as output_json_linux_run
from modules.auto_drawing import run as auto_drawing_run

MODULES = [
    ("Data Extraction", data_extraction_run),
    ("Input & Output JSON", io_json_run),
    ("Output JSON (Windows)", output_json_windows_run),
    ("Output JSON (Linux)", output_json_linux_run),
    ("Auto Drawing Creation", auto_drawing_run),
]


class AutoTestApp(tk.Tk):
    """
    Main application window for AutoTestUtility.
    """

    def __init__(self):
        super().__init__()
        self.title("AutoTestUtility")
        self.geometry("800x600")

        self.cad_folder = ""
        self.input_folder = ""
        self.output_folder = ""
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

        self._build_ui()
        self.logger = Logger(callback=self._append_log)

    def _build_ui(self):
        input_frame = ttk.LabelFrame(self, text="Inputs")
        input_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(input_frame, text="CAD Files Folder:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Button(input_frame, text="Select Folder", command=self._select_cad_folder).grid(row=0, column=1, padx=5, pady=2)
        self._cad_folder_label = ttk.Label(input_frame, text="None")
        self._cad_folder_label.grid(row=0, column=2, sticky="w", padx=5, pady=2)

        ttk.Label(input_frame, text="Input Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Button(input_frame, text="Select Folder", command=self._select_input_folder).grid(row=1, column=1, padx=5, pady=2)
        self._input_folder_label = ttk.Label(input_frame, text="None")
        self._input_folder_label.grid(row=1, column=2, sticky="w", padx=5, pady=2)

        ttk.Label(input_frame, text="Output Folder:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        ttk.Button(input_frame, text="Select Folder", command=self._select_output_folder).grid(row=2, column=1, padx=5, pady=2)
        self._output_folder_label = ttk.Label(input_frame, text="None")
        self._output_folder_label.grid(row=2, column=2, sticky="w", padx=5, pady=2)

        modules_frame = ttk.LabelFrame(self, text="Modules")
        modules_frame.pack(fill="x", padx=5, pady=5)
        self._module_vars = []
        for idx, (name, _) in enumerate(MODULES):
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(modules_frame, text=name, variable=var)
            chk.grid(row=0, column=idx, sticky="w", padx=5, pady=2)
            self._module_vars.append(var)

        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill="x", padx=5, pady=5)
        self._run_button = ttk.Button(controls_frame, text="RUN", command=self._start)
        self._run_button.grid(row=0, column=0, padx=5)
        self._pause_button = ttk.Button(controls_frame, text="Pause", command=self._toggle_pause, state="disabled")
        self._pause_button.grid(row=0, column=1, padx=5)
        self._cancel_button = ttk.Button(controls_frame, text="Cancel", command=self._cancel, state="disabled")
        self._cancel_button.grid(row=0, column=2, padx=5)

        status_frame = ttk.Frame(self)
        status_frame.pack(fill="x", padx=5, pady=5)
        self._progress_var = tk.DoubleVar()
        ttk.Progressbar(status_frame, variable=self._progress_var, maximum=100).pack(fill="x", padx=5, pady=2)
        self._status_label = ttk.Label(status_frame, text="Status: Idle")
        self._status_label.pack(anchor="w", padx=5)
        self._module_label = ttk.Label(status_frame, text="Module: None")
        self._module_label.pack(anchor="w", padx=5)
        self._file_label = ttk.Label(status_frame, text="File: None")
        self._file_label.pack(anchor="w", padx=5)
        self._count_label = ttk.Label(status_frame, text="Processed: 0 Failed: 0")
        self._count_label.pack(anchor="w", padx=5)

        log_frame = ttk.LabelFrame(self, text="Log")
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        # Export‑Logs button inside the Log panel; pack first so its space is reserved
        self._export_button = ttk.Button(log_frame, text="Export Logs", command=self._export_log)
        self._export_button.pack(side="bottom", anchor="e", padx=5, pady=5)

        self._log_text = tk.Text(log_frame, state="disabled")
        self._log_text.pack(side="top", fill="both", expand=True, padx=5, pady=5)

    def _select_cad_folder(self):
        folder = filedialog.askdirectory(title="Select CAD files folder")
        if folder:
            self.cad_folder = folder
            self._cad_folder_label.config(text=self.cad_folder)

    def _select_input_folder(self):
        folder = filedialog.askdirectory(title="Select input folder")
        if folder:
            self.input_folder = folder
            self._input_folder_label.config(text=self.input_folder)

    def _select_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder = folder
            self._output_folder_label.config(text=self.output_folder)

    def _start(self):
        selected = [(name, func) for (name, func), var in zip(MODULES, self._module_vars) if var.get()]
        if not selected:
            messagebox.showwarning("Warning", "Select at least one module.")
            return
        if not self.cad_folder and not self.input_folder:
            messagebox.showwarning("Warning", "Select CAD files folder or input folder.")
            return
        if not self.output_folder:
            messagebox.showwarning("Warning", "Select output folder.")
            return

        self._run_button.config(state="disabled")
        self._pause_button.config(state="normal", text="Pause")
        self._cancel_button.config(state="normal")
        self._stop_event.clear()
        self._pause_event.clear()
        self._status_label.config(text="Status: Running")
        self.thread = threading.Thread(target=self._run_modules, args=(selected,), daemon=True)
        self.thread.start()

    def _toggle_pause(self):
        if not self._pause_event.is_set():
            self._pause_event.set()
            self._pause_button.config(text="Resume")
            self.logger.log("Paused")
        else:
            self._pause_event.clear()
            self._pause_button.config(text="Pause")
            self.logger.log("Resumed")

    def _cancel(self):
        if messagebox.askyesno("Cancel", "Cancel execution?"):
            self._stop_event.set()
            self.logger.log("Cancellation requested")

    def _run_modules(self, modules):
        total_tasks = len(modules)
        processed = 0
        failed = 0

        for name, func in modules:
            if self._stop_event.is_set():
                break
            self._update_module(name)
            self.logger.log(f"Starting module: {name}")

            try:
                # Pass the CAD folder, input folder, and output folder to the module function
                success, msg = func(self.cad_folder, self.input_folder, self.output_folder)
                if success:
                    self.logger.log(f"[SUCCESS] {name}: {msg}")
                else:
                    self.logger.log(f"[FAIL] {name}: {msg}")
                    failed += 1
            except Exception as e:
                self.logger.log(f"[ERROR] {name}: {e}")
                failed += 1

            processed += 1
            percent = (processed / total_tasks * 100) if total_tasks else 0
            self._update_progress(processed, failed, percent)

            self.logger.log(f"Finished module: {name}")

        status = "Completed" if not self._stop_event.is_set() else "Cancelled"
        self._update_status(status)
        self.after(0, self._on_run_complete)

    def _update_module(self, module_name):
        self.after(0, lambda: self._module_label.config(text=f"Module: {module_name}"))

    def _update_file(self, file_path):
        name = os.path.basename(file_path)
        self.after(0, lambda: self._file_label.config(text=f"File: {name}"))

    def _update_progress(self, processed, failed, percent):
        def inner():
            self._progress_var.set(percent)
            self._count_label.config(text=f"{processed} completed, {failed} failed")
        self.after(0, inner)

    def _update_status(self, status):
        self.after(0, lambda: self._status_label.config(text=f"Status: {status}"))

    def _on_run_complete(self):
        self._run_button.config(state="normal")
        self._pause_button.config(state="disabled")
        self._cancel_button.config(state="disabled")

    def _append_log(self, message):
        self._log_text.config(state="normal")
        self._log_text.insert("end", message + "\n")
        self._log_text.see("end")
        self._log_text.config(state="disabled")

    def _export_log(self):
        path = filedialog.asksaveasfilename(
            title="Save log file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            try:
                self.logger.export(path)
                messagebox.showinfo("Export Log", f"Log exported to {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export log: {e}")