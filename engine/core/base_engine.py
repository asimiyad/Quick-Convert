import os
import shutil
import logging
import mimetypes
from abc import ABC, abstractmethod
from typing import List

# --- Logging Configuration ---
def setup_logger(name: str = "ConversionEngine") -> logging.Logger:
    """Configures the advanced logging system to output to console and file."""
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # Logging format: timestamp | error level | module | message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler for real-time output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Dynamically locate the project base directory to always log correctly
    # Assumes this script lives in -> "project_root/engine/core/base_engine.py"
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "engine.log")
    
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Initialize the root logger for the engine components
logger = setup_logger()


# --- Utility Functions ---

def validate_file(file_path: str) -> bool:
    """
    Checks if a file exists, isn't empty, and uses mimetypes and magic bytes 
    to verify the file extension matches its actual content.
    """
    if not os.path.exists(file_path):
        logger.error(f"Validation failed: File not found -> {file_path}")
        return False

    if os.path.getsize(file_path) == 0:
        logger.error(f"Validation failed: File is empty -> {file_path}")
        return False

    # Guess mime type based on file extension
    expected_mime, _ = mimetypes.guess_type(file_path)
    if not expected_mime:
        logger.warning(f"Could not reliably determine MIME type from extension for {file_path}")
        return True # Proceed with warning if we can't guess

    # Simple magic byte verification to ensure content matches the extension's MIME type.
    # Note: For production with many varied subtypes, third-party libraries like `python-magic` are recommended.
    magic_numbers = {
        'application/pdf': b'%PDF-',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': b'PK\x03\x04', # DOCX
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': b'PK\x03\x04', # XLSX
        'application/msword': b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1', # DOC
        'application/vnd.ms-excel': b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1', # XLS
        'image/jpeg': b'\xff\xd8\xff',
        'image/png': b'\x89PNG\r\n\x1a\n',
    }

    if expected_mime in magic_numbers:
        expected_magic = magic_numbers[expected_mime]
        try:
            with open(file_path, 'rb') as f:
                header = f.read(len(expected_magic))
                if not header.startswith(expected_magic):
                    logger.error(f"Validation failed: Content mismatch! Extension suggests {expected_mime} but file signature differs.")
                    return False
        except Exception as e:
            logger.error(f"Failed to read file for content validation: {e}")
            return False

    logger.info(f"File deeply validated (MIME: {expected_mime}): {file_path}")
    return True


def check_environment_dependencies(dependencies: List[str]) -> bool:
    """
    Utility to check if external dependencies (like Tesseract-OCR or LibreOffice) 
    are installed and available in the system's PATH.
    """
    missing = []
    for executable in dependencies:
        if shutil.which(executable) is None:
            missing.append(executable)
    
    if missing:
        logger.error(f"Missing external dependencies in PATH: {', '.join(missing)}")
        return False
        
    logger.info(f"All required environment dependencies found: {', '.join(dependencies)}")
    return True


# --- Abstract Base Class ---

class BaseConverter(ABC):
    """
    Blueprint that all future conversion modules (Word, PDF, Excel, etc.) must follow.
    """

    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        # Instantiate a module-specific logger reusing existing handlers
        self.logger = logging.getLogger(f"ConversionEngine.{self.__class__.__name__}")

    @abstractmethod
    def validate_requirements(self) -> bool:
        """
        Check if the specific converter has all necessary dependencies 
        and if the input file meets the module's needs.
        """
        pass

    @abstractmethod
    def convert(self) -> bool:
        """
        The core conversion logic to be implemented by child classes.
        Returns True if successful, False otherwise.
        """
        pass

    def run(self) -> bool:
        """
        Standard execution flow for any conversion process.
    """
        self.logger.info(f"Initiating conversion from {self.input_file} to {self.output_file}")

        if not self.validate_requirements():
            self.logger.error("Requirement validation failed. Process aborted.")
            return False
        
        try:
            success = self.convert()
            if success:
                self.logger.info("Conversion completed successfully.")
            else:
                self.logger.error("Conversion completed with errors.")
            return success
            
        except Exception as e:
            self.logger.exception(f"An unexpected error occurred during the conversion workflow: {e}")
            return False
