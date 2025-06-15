🛠️ Software Specification Document: AutoDrawing Autotest Tool
📌 Objective
To develop a Python-based executable application capable of processing a large number of CAD files for automated testing of drawing-related modules like Data Extraction, JSON output generation, and Auto Drawing Creation. The tool should feature a user-friendly UI and support modular, extensible design principles.

✅ Functional Requirements
1. Executable Packaging
The application must be packaged as a standalone .exe using a tool like PyInstaller.

2. UI Inputs
CAD Files: File selector for one or more CAD input files.

Input Folder: Directory selector to choose folder with files for batch processing.

Output Folder: Directory selector for saving output results.

3. Module Selection
Checkbox interface to enable or disable the following modules:

✅ Data Extraction

✅ Input & Output JSON

✅ Output JSON (Windows)

✅ Output JSON (Linux)

✅ Auto Drawing Creation

4. Execution and Status Tracking
A “RUN” button to initiate processing.

Display runtime status:

Currently executing module

Name of file currently being processed

Number of files processed (e.g., “20 of 50 completed”)

Number of failed files (e.g., “3 tests failed”)

Support pause and cancel functionality during execution.

5. Threading
All backend processing must be performed in a separate thread to keep the UI responsive.

6. Progress Logging
A detailed log panel should display:

Start and end of each module

Success or failure messages per file, including:

Filename

Status: success or failure

Error message (if any)

7. Log Export
A button labeled “Export to a log file” must:

Export the full contents of the detailed log panel to a .txt file.

Allow the user to choose the location to save the file.

Ensure the format is human-readable (plain text).

🎨 UI/UX Requirements
1. Aesthetics
Keep the UI subtle but not boring.

Use colorful elements to enhance user experience (e.g., progress bar animation).

2. Tooltips and Help
Provide tooltips on all UI elements to explain their function.

Add information (i) icons/buttons where deeper context is helpful.

3. Progress Bar Enhancements
Add fun visual elements (e.g., animated bar, icons) to make long-running operations engaging.

🔄 Non-Functional Requirements
Scalability: Should efficiently handle large number of files.

Modularity: Codebase should be cleanly modular, with each module's logic separated.

Maintainability:

Follow Python coding standards (PEP 8).

Add code comments and docstrings for clarity.

Keep code structure simple, readable, and extensible.

Documentation:

Maintain specification.md with updates per code change.

Create and maintain a TODO.txt file listing pending tasks for each module.

📁 Folder & File Guidelines
Maintain the following files:

specification.md – Project specifications and version notes.

TODO.txt – Detailed pending items and next steps.

log.txt – Exported logs of execution runs.

🧩 Code Scaffold
Implement initial placeholder or mock functionality for each of the following modules:

Data Extraction

Input & Output JSON

Output JSON (Windows)

Output JSON (Linux)

Auto Drawing Creation

Provide a way to easily integrate real logic in place of placeholders later.

🚀 Deliverables
Standalone .exe for Windows

Full source code with:

main.py – Entry point

ui.py – UI logic (Tkinter or PyQt recommended)

logger.py – Logging and export

modules/ – Folder with individual module logic

utils/ – Folder with helper utilities

Documentation files as mentioned above
ZZZTEST

# Data Extraction Module

**Objective:** Automate data extraction from CAD files and validate the results against known reference data.

### 1. EXE Launcher
Launch the data extraction executable (e.g. `DataExtraction.exe`) with the CAD files folder path as input.
Wait until the process completes.

### 2. CSV Output Handling
- The executable emits a single CSV file (`data.csv`) under:

  ```text
  <OutputFolder>/DataExtraction/csv/data.csv
  ```

- The first column in the CSV corresponds to the CAD file name.
- Compare this output CSV against the reference CSV located at:

  ```text
  <InputFolder>/DataExtraction/csv/data.csv
  ```

- Perform numeric comparisons within a configurable tolerance.

### 3. JSON Output Handling
- One JSON file is generated per CAD file and saved to:

  ```text
  <OutputFolder>/DataExtraction/JSONs/{file_id}.json
  ```

- Compare each output JSON against its reference JSON at:

  ```text
  <InputFolder>/DataExtraction/JSONs/{file_id}.json
  ```

- Log any mismatches or pass/fail results.

📌 Module: Input & Output JSON Comparator
🔧 Requirements:
Directory Setup

Read all files from a folder named CAD Files.

For each file, run an external .exe that dumps:

input JSON

output JSON
to:

pgsql
Copy
Edit
C:\Temp\DataExtraction\*.json
Copy Files

After dump is complete, copy the JSONs from C:\Temp\DataExtraction\ to a defined output folder:

swift
Copy
Edit
output_folder/JSON/<CADFileName>/*.json
Folder Structure

Ensure the output folder structure is:

javascript
Copy
Edit
output_folder/
  └── JSON/
      └── <CADFileName>/
          ├── file1.json
          ├── file2.json
          └── ...
Maintain exact same structure for input_folder:

javascript
Copy
Edit
input_folder/
  └── JSON/
      └── <CADFileName>/
          ├── file1.json
          ├── file2.json
          └── ...
Comparison Logic

For each .json file in output_folder/JSON/<CADFileName>/, find the corresponding file in input_folder/JSON/<CADFileName>/.

Perform a deep field-by-field comparison.

Generate Report

Output a diff report capturing:

Which JSON file has changes

The specific field(s) that differ

The values in both input and output

The reason, if derivable, for the difference

Example Output Format (JSON or CSV):

json
Copy
Edit
{
  "CADFileName": "abc123",
  "Differences": [
    {
      "File": "file1.json",
      "Field": "dimension.width",
      "InputValue": 120.5,
      "OutputValue": 115.0,
      "DifferenceReason": "Precision loss during transformation"
    },
    ...
  ]
}
Enhancements (Optional, if time permits)

Handle missing files gracefully with a warning.

Support nested JSON structures.

Normalize field types before comparison (e.g., float vs int).

✅ Inputs to the Agent
Path to CAD Files

Path to input_folder

Path to output_folder

.exe file path to run for JSON dumping

💡 Notes
Ensure the .exe process completes before copying JSONs.

Consider using jsondiff, deepdiff, or custom recursive logic to compare fields.

Use logging to track mismatches and process failures.

Let me know if you'd like the full Python scaffolding or a .specification.md and todo.txt for this task.
