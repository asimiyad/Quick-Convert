# [Website Link](https://quick-convert-atwj.onrender.com/)

# Quick Convert 🔄

**Quick Convert** is a universal, multi-format file conversion engine built with Python. It features both a headless batch-processing CLI/GUI hybrid natively, and a high-performance web API powered by FastAPI.

## ✨ Features

- **Universal File Support**: Seamlessly convert between documents, spreadsheets, images, and media files.
  - *Documents:* `.pdf`, `.docx`, `.doc`, `.txt`, `.pptx`
  - *Spreadsheets:* `.xlsx`, `.xls`, `.csv`
  - *Images:* `.png`, `.jpeg`, `.jpg`
  - *Media:* `.mp4`, `.mov`, `.avi`, `.mp3`, `.wav`
- **Dual Execution Modes**:
  - **Local/CLI (`main.py`)**: Run single payloads interactively (prompting for outputs via native GUI windows) or pass arrays of files for autonomous, silent batch processing.
  - **Web API (`app.py`)**: A fully threaded FastAPI server processing incoming payloads in the system's hidden temporary workspace. Auto-purges data upon completion.
- **Factory-Routed Engine**: Extensible class-based design mapping modular converters (e.g., `PdfConverter`, `ExcelConverter`, `MediaConverter`) to precise extensions.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed.

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally (CLI / GUI)

Use the primary engine script `main.py` directly from your terminal:

- **GUI Picker**: Open a native dialog to pick files.
  ```bash
  python main.py
  ```
- **Interactive Single File**: Processes a single payload and opens a "Save As" dialog to build the exact output.
  ```bash
  python main.py example.pdf
  ```
- **Bulk Batch Processing**: Pass multiple files to trigger the autonomous background overdrive loop. Output defaults to the engine's built-in target directory.
  ```bash
  python main.py f1.pdf f2.docx f3.csv
  ```

### Running the API Server

The API runs on port 5000 and serves static frontend web components over CORS natively.

```bash
python app.py
```
*Access the front-end interface natively at: `http://localhost:5000`*

## 🛠️ Project Architecture

```
Quick-Convert/
├── app.py                 # FastAPI Web Server routing layer
├── main.py                # Standalone CLI / Native GUI Engine
├── requirements.txt       # Dependencies
├── engine/                # Core modular conversion logic
│   ├── modules/           # Targeted converter classes (PDF, Meda, Word, etc.)
│   └── config.py          # Universal conversion routes and policies
└── frontend/              # Static HTML/JS UI files
```

## 📄 License

This repository is maintained by [@asimiyad](https://github.com/asimiyad).
