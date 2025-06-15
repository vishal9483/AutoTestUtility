# AutoTestUtility

AutoTestUtility is a Python-based desktop application for automated testing and processing of CAD drawing files. It supports data extraction, JSON input/output generation, and auto drawing creation in a modular, extensible framework, all via a responsive GUI.

## Features
- Batch process single or multiple CAD files via file selector or input folder
- Modular pipeline with selectable steps:
  - Data Extraction
  - Input & Output JSON
  - Output JSON (Windows)
  - Output JSON (Linux)
  - Auto Drawing Creation
- Live status updates: current module, file, progress and failure counts
- Pause, resume, and cancel execution
- Detailed runtime log panel with export to plain-text log file

## Requirements
- Python 3.7+
- Tkinter (standard with most Python installations)

## Installation & Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/vishal9483/AutoTestUtility.git
   cd AutoTestUtility
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Install any required dependencies (if added later):
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application:
```bash
python main.py
```

1. Select individual CAD files or an input folder.
2. Choose an output folder for results.
3. Enable one or more modules via the checkbox interface.
4. Click **RUN** to start processing. Use **Pause**, **Resume**, or **Cancel** as needed.
5. Monitor progress via the status labels and live log panel.
6. Export the full log to a text file using **Export to log file**.

## Project Structure
```
AutoTestUtility/
├── main.py              # Application entry point
├── ui.py                # GUI logic (Tkinter)
├── logger.py            # Logging utility and export
├── modules/             # Processing modules (placeholders)
│   ├── data_extraction.py
│   ├── io_json.py
│   ├── output_json_windows.py
│   ├── output_json_linux.py
│   └── auto_drawing.py
├── utils/               # Helper utilities
│   └── helpers.py
├── specification.md     # Software specification document
├── TODO.txt             # Pending tasks and roadmap
├── log.txt              # Sample/exported log file (empty placeholder)
└── README.md            # Project overview and instructions
```

## Modules
Each module in `modules/` exposes a `run(file_path, output_folder)` function that returns `(success: bool, message: str)`. Placeholder implementations simulate work; replace with real CAD-processing logic as needed.

## Roadmap & Contributing
See [TODO.txt](TODO.txt) for a detailed list of pending tasks and next steps for each module, UI enhancements, and packaging instructions.

## Specification
Full requirements and design details are in [specification.md](specification.md).