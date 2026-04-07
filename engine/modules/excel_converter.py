import os
import subprocess
import shutil
from engine.core.base_engine import BaseConverter, validate_file, check_environment_dependencies
from engine.config import SUPPORTED_CONVERSIONS

try:
    import pandas as pd
except ImportError:
    pd = None

class ExcelConverter(BaseConverter):
    """
    Handles structurally processing Excel configurations (.xlsx, .xls).
    """
    def validate_requirements(self) -> bool:
        if not validate_file(self.input_file): return False
        
        _, input_ext = os.path.splitext(self.input_file)
        _, output_ext = os.path.splitext(self.output_file)
        input_ext, output_ext = input_ext.lower(), output_ext.lower()
        
        if output_ext not in SUPPORTED_CONVERSIONS.get(input_ext, []):
            self.logger.error(f"Engine configuration natively blocks mapping: {input_ext} -> {output_ext}")
            return False
        
        if output_ext == ".csv" and pd is None:
            self.logger.error("Missing 'pandas'. Install via: pip install pandas openpyxl")
            return False
            
        if output_ext == ".pdf" or (input_ext == ".xls" and output_ext == ".xlsx"):
            if not check_environment_dependencies(["soffice", "soffice.exe"]):
                 self.logger.warning("LibreOffice 'soffice' executable not natively found inside Windows PATH.")
        
        self.logger.info("Excel format validation successful.")
        return True

    def convert(self) -> bool:
        _, input_ext = os.path.splitext(self.input_file)
        _, output_ext = os.path.splitext(self.output_file)
        
        input_ext, output_ext = input_ext.lower(), output_ext.lower()
        
        try:
            if output_ext == ".csv": 
                return self._convert_to_csv()
            elif output_ext == ".pdf": 
                return self._convert_via_libreoffice("pdf")
            elif input_ext == ".xls" and output_ext == ".xlsx": 
                return self._convert_via_libreoffice("xlsx")
            else:
                self.logger.error(f"Worker logic for {output_ext} is not cleanly mapped in ExcelConverter.")
                return False
        except Exception as e:
            self.logger.exception(f"Excel extraction subsystem crashed: {e}")
            return False

    def _convert_to_csv(self) -> bool:
        self.logger.info(f"Parsing Excel arrays natively to CSV: {self.input_file}")
        try:
            # Leverage Pandas to securely unpack the spreadsheet without launching Excel GUI
            df = pd.read_excel(self.input_file)
            df.to_csv(self.output_file, index=False)
            self.logger.info(f"Successfully generated clean CSV matrix payload: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Spreadsheet extraction strictly failed structurally: {e}")
            return False

    def _convert_via_libreoffice(self, target_format: str) -> bool:
        self.logger.info(f"Invoking headless LibreOffice to construct {target_format.upper()} payload output natively.")
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
                self.logger.error(f"LibreOffice backend halted violently:\n{result.stderr}")
                return False
                
            base_filename = os.path.basename(self.input_file)
            name_no_ext, _ = os.path.splitext(base_filename)
            lo_output_file = os.path.join(outdir, f"{name_no_ext}.{target_format}")
            
            if lo_output_file != self.output_file and os.path.exists(lo_output_file):
                shutil.move(lo_output_file, self.output_file)
                
            self.logger.info(f"Successfully constructed raw {target_format.upper()} object document.")
            return True
        except Exception as e:
            self.logger.error(f"LibreOffice subprocess utterly failed: {e}")
            return False
