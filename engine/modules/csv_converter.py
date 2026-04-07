import os
import subprocess
import shutil
from engine.core.base_engine import BaseConverter, validate_file, check_environment_dependencies
from engine.config import SUPPORTED_CONVERSIONS

try:
    import pandas as pd
except ImportError:
    pd = None

class CsvConverter(BaseConverter):
    """
    Handles intercepting mapping logic for Comma-Separated Values (.csv).
    """
    def validate_requirements(self) -> bool:
        if not validate_file(self.input_file): return False
        
        _, input_ext = os.path.splitext(self.input_file)
        _, output_ext = os.path.splitext(self.output_file)
        input_ext, output_ext = input_ext.lower(), output_ext.lower()
        
        if output_ext not in SUPPORTED_CONVERSIONS.get(input_ext, []):
            self.logger.error(f"Config matrix blocked conversion intelligently: {input_ext} -> {output_ext}")
            return False
        
        if output_ext == ".xlsx" and pd is None:
            self.logger.error("Missing pandas. Install via: pip install pandas openpyxl")
            return False
            
        if output_ext == ".pdf":
            if not check_environment_dependencies(["soffice", "soffice.exe"]):
                 self.logger.warning("LibreOffice 'soffice' executable not natively detected properly.")
        
        self.logger.info("CSV extraction validation cleanly succeeded.")
        return True

    def convert(self) -> bool:
        _, output_ext = os.path.splitext(self.output_file)
        output_ext = output_ext.lower()
        try:
            if output_ext == ".xlsx": 
                return self._convert_to_xlsx()
            elif output_ext == ".pdf": 
                return self._convert_via_libreoffice("pdf")
            else:
                self.logger.error("Invalid routine mapping called natively.")
                return False
        except Exception as e:
            self.logger.exception(f"Engine CSV logic corrupted cleanly: {e}")
            return False

    def _convert_to_xlsx(self) -> bool:
        self.logger.info(f"Parsing CSV natively out structurally into XLSX target mapping: {self.input_file}")
        try:
            df = pd.read_csv(self.input_file)
            df.to_excel(self.output_file, index=False)
            self.logger.info(f"Successfully generated complex matrix spreadsheet reliably: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Data mapping explicitly bypassed natively: {e}")
            return False

    def _convert_via_libreoffice(self, target_format: str) -> bool:
        self.logger.info(f"Invoking LibreOffice to synthesize {target_format.upper()} payload logically natively.")
        outdir = os.path.dirname(self.output_file)
        
        command = [
            "soffice", 
            "--headless", 
            "--nologo", 
            "--nofirststartwizard", 
            "--convert-to", target_format, 
            self.input_file, 
            "--outdir", outdir
        ]
        
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                self.logger.error(f"LibreOffice subsystem violently halted natively:\n{result.stderr}")
                return False
                
            base_filename = os.path.basename(self.input_file)
            name_no_ext, _ = os.path.splitext(base_filename)
            lo_output_file = os.path.join(outdir, f"{name_no_ext}.{target_format}")
            
            if lo_output_file != self.output_file and os.path.exists(lo_output_file):
                shutil.move(lo_output_file, self.output_file)
                
            self.logger.info(f"Successfully printed out {target_format.upper()} structure natively.")
            return True
        except Exception as e:
            self.logger.error(f"OS-Level system command completely failed natively: {e}")
            return False
