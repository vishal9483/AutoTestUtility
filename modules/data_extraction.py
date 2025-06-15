"""
Data Extraction Module

This module launches the external data extraction executable, then
validates the resulting CSV and JSON outputs against reference data.
"""

import os
import subprocess
import csv
import json

TOLERANCE = 1e-6


def run(file_path, output_folder):
    """
    Execute the data extraction process and validate outputs.

    :param file_path: Path to a CAD file or CAD folder.
    :param output_folder: Base path for module outputs.
    :return: Tuple(success: bool, message: str).
    """
    # Accept folder path directly as input
    cad_input = file_path

    exe_name = "DataExtraction.exe"
    cmd = [exe_name, cad_input]
    try:
        subprocess.run(cmd, check=True)
    except Exception as exc:
        return False, f"Data extraction executable failed: {exc}"

    issues = []
    out_csv = os.path.join(output_folder, "DataExtraction", "csv", "data.csv")
    ref_csv = os.path.join(cad_input, "DataExtraction", "csv", "data.csv")
    try:
        with open(out_csv, newline="") as fo, open(ref_csv, newline="") as fr:
            reader_out = csv.reader(fo)
            reader_ref = csv.reader(fr)
            for row_out, row_ref in zip(reader_out, reader_ref):
                if row_out[0] != row_ref[0]:
                    issues.append(
                        f"CSV file name mismatch: '{row_out[0]}' vs '{row_ref[0]}'"
                    )
                for idx, (val_out, val_ref) in enumerate(zip(row_out[1:], row_ref[1:]), start=1):
                    try:
                        num_out = float(val_out)
                        num_ref = float(val_ref)
                        if abs(num_out - num_ref) > TOLERANCE:
                            issues.append(
                                f"CSV numeric mismatch at '{row_out[0]}' col {idx}: {num_out} vs {num_ref}"
                            )
                    except ValueError:
                        if val_out != val_ref:
                            issues.append(
                                f"CSV text mismatch at '{row_out[0]}' col {idx}: '{val_out}' vs '{val_ref}'"
                            )
    except FileNotFoundError as exc:
        return False, f"CSV comparison failed, file not found: {exc}"

    out_json_dir = os.path.join(output_folder, "DataExtraction", "JSONs")
    ref_json_dir = os.path.join(cad_input, "DataExtraction", "JSONs")
    if not os.path.isdir(out_json_dir) or not os.path.isdir(ref_json_dir):
        issues.append("JSON output or reference directory missing")
    else:
        for fname in os.listdir(out_json_dir):
            if not fname.lower().endswith(".json"):
                continue
            out_path = os.path.join(out_json_dir, fname)
            ref_path = os.path.join(ref_json_dir, fname)
            try:
                with open(out_path) as fo, open(ref_path) as fr:
                    data_out = json.load(fo)
                    data_ref = json.load(fr)
                if data_out != data_ref:
                    issues.append(f"JSON mismatch in '{fname}'")
            except FileNotFoundError:
                issues.append(f"JSON reference missing for '{fname}'")
            except json.JSONDecodeError as exc:
                issues.append(f"JSON decode error for '{fname}': {exc}")

    if issues:
        return False, "; ".join(issues)
    return True, "Data extraction and validation passed."