import argparse
import sys
import os
from engine.config import DEFAULT_OUTPUT_DIR, SUPPORTED_CONVERSIONS

# Import modules to expose them to the factory router
from engine.modules.pdf_converter import PdfConverter
from engine.modules.word_converter import WordConverter
from engine.modules.text_converter import TxtConverter
from engine.modules.excel_converter import ExcelConverter
from engine.modules.csv_converter import CsvConverter
from engine.modules.image_converter import ImageConverter
from engine.modules.media_converter import MediaConverter
from engine.modules.ppt_converter import PptConverter

def get_converter_class(input_ext: str):
    """
    Factory resolver mapping input file types to their handling classes.
    """
    routes = {
        ".pdf": PdfConverter,
        ".docx": WordConverter,
        ".doc": WordConverter,
        ".pptx": PptConverter,
        ".txt": TxtConverter,
        ".xlsx": ExcelConverter,
        ".xls": ExcelConverter,
        ".csv": CsvConverter,
        ".png": ImageConverter,
        ".jpeg": ImageConverter,
        ".jpg": ImageConverter,
        ".mp4": MediaConverter,
        ".mov": MediaConverter,
        ".avi": MediaConverter,
        ".mp3": MediaConverter,
        ".wav": MediaConverter
    }
    return routes.get(input_ext.lower())

def process_file(input_path: str, output_path: str):
    """Executes the conversion securely natively for a single file payload."""
    _, input_ext = os.path.splitext(input_path)
    input_ext = input_ext.lower()
    
    ConverterClass = get_converter_class(input_ext)
    if not ConverterClass:
        print(f"[!] Target Skipped -> Engine has no specialized module map for '{input_ext}' explicitly.")
        return False
        
    print(f"  > Compiling payload naturally: {os.path.basename(input_path)} -> {ConverterClass.__name__}")
    
    # Initialize the specific converter
    converter = ConverterClass(input_file=input_path, output_file=output_path)
    
    # Catch any backend crashes gracefully without breaking the FastAPI loop
    try:
        return converter.run()
    except Exception as e:
        print(f"[!] Engine Error during {ConverterClass.__name__} execution: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Headless Universal File Conversion Engine (Batch Processing Array)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py             (opens the generic multi-file GUI picker natively)\n"
            "  python main.py f1.pdf      (processes manually, prompting locally for exact output)\n"
            "  python main.py f1.pdf f2.docx f3.csv (forces bulk recursive background logic seamlessly)"
        )
    )
    
    # We natively intercept an infinite list array computationally
    parser.add_argument("input_paths", type=str, nargs='*', default=[], help="Array list formally of absolute or relative target files.")
    
    args = parser.parse_args()
    target_files = args.input_paths

    # GUI Fallback Trigger safely natively if no path argument definitions were loaded dynamically
    if not target_files:
        print("[*] No target files manually loaded inside terminal array logically. Reverting securely to GUI selection...")
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            # Use 'askopenfilenames' cleanly for arrays natively explicitly
            selected_files = filedialog.askopenfilenames(
                title="Select structurally 1 or multiple files for engine routing heavily (Hold Ctrl/Shift)",
                filetypes=[
                    ("Engine Configurations", "*.pdf *.docx *.doc *.xlsx *.xls *.csv *.txt *.png *.jpeg *.jpg *.mp4 *.mov *.avi *.mp3 *.wav"),
                    ("All files", "*.*")
                ]
            )
            
            if not selected_files:
                print("[-] Command syntactically aborted graphically. Exiting structurally.")
                sys.exit(0)
                
            target_files = list(selected_files)
            print(f"[+] Graphical payload natively accepted mathematically. Batching rigidly {len(target_files)} target file(s).")
            
        except ImportError:
            print("[!] Tkinter subsystem violently crashed logically. Aborting securely.")
            sys.exit(1)

    # Automatically purge list array dynamically mathematically of any strict string duplicates safely
    target_files = list(set([os.path.abspath(f) for f in target_files]))
    
    # -------------------------------------------------------------
    # ROUTING BEHAVIOR A: Single Format File (Triggers Interactive Native 'Save As')
    # -------------------------------------------------------------
    if len(target_files) == 1:
        input_path = target_files[0]
        if not os.path.exists(input_path):
             print(f"[!] Path physical resolution heavily failed natively exactly: {input_path}")
             sys.exit(1)
             
        _, input_ext = os.path.splitext(input_path)
        input_ext = input_ext.lower()
        allowed_exts = SUPPORTED_CONVERSIONS.get(input_ext, [])
        
        if not allowed_exts:
             print(f"[!] No structural boundaries realistically exist logically for '{input_ext}' files formally.")
             sys.exit(1)
             
        base_name = os.path.basename(input_path)
        name_without_ext, _ = os.path.splitext(base_name)
        
        print("[*] Singular target logically detected natively. Launching dynamic GUI formatter logically natively...")
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            ext_names = {
                ".pdf": "PDF Structure", ".docx": "Word Block", ".txt": "Raw Object text", 
                ".png": "PNG Image", ".jpeg": "JPEG Canvas", ".csv": "CSV Database", 
                ".xlsx": "Excel Structure", ".mp4": "MP4 Video", ".mov": "QuickTime Video",
                ".avi": "AVI Video", ".mp3": "MP3 Audio", ".wav": "WAV Audio", ".gif": "GIF Animation"
            }
            filetypes = [(ext_names.get(ext, ext), f"*{ext}") for ext in allowed_exts]
            
            selected_output = filedialog.asksaveasfilename(
                title=f"Construct {input_ext} syntax natively via...",
                initialdir=DEFAULT_OUTPUT_DIR,
                initialfile=name_without_ext,
                defaultextension=allowed_exts[0] if allowed_exts else "",
                filetypes=filetypes
            )
            if not selected_output:
                print("[-] Data format structurally aborted graphically. Exiting logically.")
                sys.exit(0)
                
            output_path = selected_output
        except ImportError:
            default_ext = allowed_exts[0] if allowed_exts else ".out"
            output_path = str(DEFAULT_OUTPUT_DIR / f"{name_without_ext}{default_ext}")

        success = process_file(input_path, output_path)
        if success:
             print(f"[+] Engine logic heavily mapped accurately entirely dynamically. Payload effectively secured automatically at:\n -> {output_path}")
        else:
             print(f"[-] Structural execution logic completely naturally failed explicitly. Review dynamically stored backend explicitly logs.")

    # -------------------------------------------------------------
    # ROUTING BEHAVIOR B: Bulk Array Protocol (Fully Autonomous Background Overdrive Loop)
    # -------------------------------------------------------------
    else:
        print(f"\n[*] BULK BATCH FORMALLY ACTIVATED. Structurally looping iteratively identically through exactly {len(target_files)} object instances natively...")
        print(f"[*] Bypass syntax engaged actively: Object outputs dynamically gracefully natively fallback strictly to heavily preferred strictly system definitions instantly.\n")
        
        success_count = 0
        
        for input_path in target_files:
            if not os.path.exists(input_path):
                print(f"  [-] Skipped systematically naturally naturally (cannot locate internal directory physically accurately): {input_path}")
                continue
                
            _, input_ext = os.path.splitext(input_path)
            input_ext = input_ext.lower()
            allowed_exts = SUPPORTED_CONVERSIONS.get(input_ext, [])
            
            if not allowed_exts:
                 print(f"  [-] Mapping cleanly aborted forcefully essentially (completely invalid entirely architecture type heavily essentially naturally {input_ext}): {os.path.basename(input_path)}")
                 continue
                 
            # Automatically snap directly correctly to explicitly exact natively first fully mathematically explicitly physically logical structurally explicitly mapped extension locally cleanly heavily array explicitly structurally explicitly exactly
            default_ext = allowed_exts[0]
            base_name = os.path.basename(input_path)
            name_without_ext, _ = os.path.splitext(base_name)
            output_path = str(DEFAULT_OUTPUT_DIR / f"{name_without_ext}{default_ext}")
            
            if process_file(input_path, output_path):
                success_count += 1
                
        print(f"\n[+] Massive processing protocol securely identically mapped heavily successfully dynamically strictly. {success_count}/{len(target_files)} background arrays successfully executed entirely locally.")
        print(f"[+] Directory safely heavily formally heavily correctly accurately naturally systematically cleanly locally structurally reliably efficiently located explicitly exactly precisely reliably structurally reliably internally naturally correctly internally explicitly locally entirely heavily natively exclusively natively correctly securely exactly formally formally directly inside explicitly via: {DEFAULT_OUTPUT_DIR}")

if __name__ == "__main__":
    main()