import os
from engine.core.base_engine import BaseConverter, validate_file
from engine.config import SUPPORTED_CONVERSIONS

try:
    from PIL import Image
except ImportError:
    Image = None

class ImageConverter(BaseConverter):
    """
    Handles intercepting graphics and structurally converting visual layouts effectively.
    """
    def validate_requirements(self) -> bool:
        # Magic bytes are handled securely inside core validation mapping already.
        if not validate_file(self.input_file): return False
        
        _, input_ext = os.path.splitext(self.input_file)
        _, output_ext = os.path.splitext(self.output_file)
        input_ext, output_ext = input_ext.lower(), output_ext.lower()
        
        if output_ext not in SUPPORTED_CONVERSIONS.get(input_ext, []):
            self.logger.error(f"Graphical matrix formally blocked natively: {input_ext} -> {output_ext}")
            return False
        
        if Image is None:
            self.logger.error("Missing standard graphical library Pillow. Install via: pip install pillow")
            return False
            
        self.logger.info("Visual framework mapping successfully validated internally.")
        return True

    def convert(self) -> bool:
        _, output_ext = os.path.splitext(self.output_file)
        output_ext = output_ext.lower()
        try:
            if output_ext in [".png", ".jpg", ".jpeg"]: 
                return self._convert_image_format()
            elif output_ext == ".pdf": 
                return self._convert_to_pdf()
            return False
        except Exception as e:
            self.logger.exception(f"Graphics logic severely failed explicitly: {e}")
            return False

    def _convert_image_format(self) -> bool:
        self.logger.info(f"Re-rendering image structural bytes natively: {self.input_file}")
        try:
            img = Image.open(self.input_file)
            
            # Remove transparent Alpha channels strictly when mapping out to legacy formats like JPEG visually
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            img.save(self.output_file)
            self.logger.info(f"Successfully generated new graphical template smoothly natively: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Image rasterization mapping failed severely logically: {e}")
            return False

    def _convert_to_pdf(self) -> bool:
        self.logger.info(f"Mathematically embedding image explicitly into clean PDF canvas format natively: {self.input_file}")
        try:
            img = Image.open(self.input_file)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Embed image data straight into physical PDF objects graphically
            img.save(self.output_file, "PDF", resolution=100.0)
            self.logger.info(f"Successfully locked structure into graphical PDF document explicitly: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Graphics visual compilation pipeline mathematically halted: {e}")
            return False
