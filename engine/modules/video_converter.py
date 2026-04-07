import os
from engine.core.base_engine import BaseConverter, validate_file
from engine.config import SUPPORTED_CONVERSIONS

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    VideoFileClip = None

class VideoConverter(BaseConverter):
    """
    Handles intercepting video files and structurally converting them into audio formats.
    """
    def validate_requirements(self) -> bool:
        if not validate_file(self.input_file): return False
        
        _, input_ext = os.path.splitext(self.input_file)
        _, output_ext = os.path.splitext(self.output_file)
        input_ext, output_ext = input_ext.lower(), output_ext.lower()
        
        if output_ext not in SUPPORTED_CONVERSIONS.get(input_ext, []):
            self.logger.error(f"Video format conversion formally blocked natively: {input_ext} -> {output_ext}")
            return False
        
        if VideoFileClip is None:
            self.logger.error("Missing standard video library moviepy. Install via: pip install moviepy")
            return False
            
        self.logger.info("Video framework mapping successfully validated internally.")
        return True

    def convert(self) -> bool:
        _, output_ext = os.path.splitext(self.output_file)
        output_ext = output_ext.lower()
        try:
            if output_ext == ".mp3": 
                return self._convert_mp4_to_mp3()
            return False
        except Exception as e:
            self.logger.exception(f"Video logic severely failed explicitly: {e}")
            return False

    def _convert_mp4_to_mp3(self) -> bool:
        self.logger.info(f"Extracting audio track organically natively: {self.input_file}")
        try:
            video = VideoFileClip(self.input_file)
            audio = video.audio
            
            if audio is None:
                self.logger.error("Video file does not contain an audio track categorically.")
                video.close()
                return False
                
            # Write the audio track out as an MP3 file
            audio.write_audiofile(self.output_file, logger=None)
            
            audio.close()
            video.close()
            
            self.logger.info(f"Successfully generated new audio template smoothly natively: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Audio extraction mapping failed severely logically: {e}")
            return False
