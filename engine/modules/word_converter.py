import os
import subprocess
import shutil
from engine.core.base_engine import BaseConverter, validate_file, check_environment_dependencies
from engine.config import SUPPORTED_CONVERSIONS

try:
    import docx # python-docx
except ImportError:
    docx = None

class WordConverter(BaseConverter):
    """
    Handles converting Word files (.docx, .doc) into other formats (e.g., TXT, PDF).
    Relies on python-docx for native parsing and LibreOffice internally for PDF composition.
    """

    def validate_requirements(self) -> bool:
        """
        Validates input payload, verifies configuration mappings, and 
        securely checks for external software dependencies before engaging logic.
        """
        # 1. Base validation (Existence & Signature check)
        if not validate_file(self.input_file):
            return False

        # 2. Config mapped support check
        _, input_ext = os.path.splitext(self.input_file)
        _, output_ext = os.path.splitext(self.output_file)
        input_ext, output_ext = input_ext.lower(), output_ext.lower()
        supported_outputs = SUPPORTED_CONVERSIONS.get(input_ext, [])
        
        if output_ext not in supported_outputs:
            self.logger.error(f"Conversion from {input_ext} to {output_ext} is disabled/unsupported by config.")
            return False

        # 3. Dynamic Dependency Checks Based on Desired Output
        if output_ext == ".txt":
            # For reading text, python-docx specifically strictly targets .docx
            if input_ext == ".doc":
                self.logger.error("python-docx only natively supports .docx text extraction. Please use a .docx file.")
                return False
                
            if docx is None:
                self.logger.error("Missing Python module 'python-docx'. Aborting. Install via: pip install python-docx")
                return False

        if output_ext == ".pdf" or (input_ext == ".doc" and output_ext == ".docx"):
            # PDF Generation requires the LibreOffice Engine hooked via PATH
            if not check_environment_dependencies(["soffice", "soffice.exe"]):
                 # Attempt fallback check for exact windows paths if its not globally mapped in PATH
                 self.logger.warning("Standard LibreOffice 'soffice' executable not cleanly found in Global PATH. Logic may fail if it is completely uninstalled.")
                 # (We return True regardless to attempt execution, as sometimes Windows users alias it differently)

        self.logger.info("Word format validation and dependency mapping successful.")
        return True

    def convert(self) -> bool:
        """
        Root executor for Word logic.
        """
        _, output_ext = os.path.splitext(self.output_file)
        output_ext = output_ext.lower()
        
        try:
            if output_ext == ".txt":
                return self._convert_to_txt()
            elif output_ext == ".pdf":
                return self._convert_to_pdf_aspose()
            elif output_ext == ".docx":
                # Primarily used to upgrade legacy .doc to .docx securely
                return self._convert_via_libreoffice("docx")
            elif output_ext == ".pptx":
                return self._convert_via_libreoffice("pptx")
            else:
                self.logger.error(f"Worker logic for {output_ext} is not yet implemented in WordConverter.")
                return False
        except Exception as e:
            self.logger.exception(f"Critical error during physical Word conversion: {e}")
            return False

    def _convert_to_txt(self) -> bool:
        """
        Extracts structural text elements purely natively using python-docx.
        """
        self.logger.debug(f"Beginning text extraction sequence for: {self.input_file}")
        try:
            document = docx.Document(self.input_file)
            
            # Compress paragraphs cleanly
            text_content = [para.text for para in document.paragraphs if para.text.strip()]
            
            with open(self.output_file, 'w', encoding='utf-8') as text_file:
                text_file.write("\n\n".join(text_content))
                
            self.logger.info(f"Successfully generated clean TXT payload natively: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Physical text Extraction halted: {e}")
            return False

    def _convert_to_pdf_aspose(self) -> bool:
        self.logger.info("Engaging pure-Python Aspose.Words engine for DOCX -> PDF mapping.")
        try:
            import aspose.words as aw
            doc = aw.Document(self.input_file)
            doc.save(self.output_file)
            self.logger.info(f"Successfully generated pure PDF via Aspose engine: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Aspose rendering severely halted: {e}")
            return False

    def _convert_via_libreoffice(self, target_format: str) -> bool:
        """
        Constructs the output cleanly by bridging the engine to LibreOffice.
        If target is pptx, we utilize pure-python natively.
        """
        if target_format == "pptx":
            self.logger.info("Automatically architecting PPTX slide deck natively from DOCX formatting...")
            try:
                import pptx
                from pptx.util import Pt
                import docx as python_docx
                
                doc = python_docx.Document(self.input_file)
                prs = pptx.Presentation()
                
                for i in range(0, len(doc.paragraphs), 6):
                    slide = prs.slides.add_slide(prs.slide_layouts[1])
                    title = slide.shapes.title
                    title.text = f"Content Section {i//6 + 1}"
                    
                    tf = slide.placeholders[1].text_frame
                    chunk = doc.paragraphs[i:i+6]
                    for para in chunk:
                        if para.text.strip():
                            p = tf.add_paragraph()
                            p.text = para.text.strip()
                            p.font.size = Pt(16)
                            
                prs.save(self.output_file)
                self.logger.info(f"Presentation securely compiled fully successfully: {self.output_file}")
                return True
            except Exception as e:
                self.logger.error(f"Docx bridging halted explicitly physically: {e}")
                return False

        self.logger.info(f"Invoking headless LibreOffice to construct {target_format.upper()} payload... this may take a moment.")
        outdir = os.path.dirname(self.output_file)
        
        # Command: soffice --headless --convert-to pdf "input.docx" --outdir "output_dir"
        command = [
            # Check standard windows location as fallback or use global variable
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
                self.logger.error(f"LibreOffice failed with code {result.returncode}:\n{result.stderr}")
                self.logger.error("Verify LibreOffice is installed and mapped properly to your PATH environment.")
                return False
                
            # Libreoffice creates the file utilizing original filename + new extension.
            # E.g. "report.docx" -> "report.pdf". 
            base_filename = os.path.basename(self.input_file)
            name_no_ext, _ = os.path.splitext(base_filename)
            lo_output_file = os.path.join(outdir, f"{name_no_ext}.{target_format}")
            
            # If the user requested a specific filename mapping in CLI GUI:
            if lo_output_file != self.output_file and os.path.exists(lo_output_file):
                shutil.move(lo_output_file, self.output_file)
                
            self.logger.info(f"Successfully minted {target_format.upper()} payload via LibreOffice logic.")
            return True
            
        except FileNotFoundError:
             self.logger.error("CRITICAL: 'soffice' command totally unresolvable. Please install LibreOffice and add it to your Windows Environment Variables.")
             return False
        except Exception as e:
            self.logger.error(f"LibreOffice subsystem severely halted: {e}")
            return False
