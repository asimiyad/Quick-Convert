import os
from engine.core.base_engine import BaseConverter, validate_file
from engine.config import SUPPORTED_CONVERSIONS

try:
    from moviepy import VideoFileClip, AudioFileClip
except ImportError:
    VideoFileClip = None
    AudioFileClip = None

class MediaConverter(BaseConverter):
    """
    Handles intercepting multimedia inputs (audio/video) and smoothly converting logic natively.
    """
    def validate_requirements(self) -> bool:
        if not validate_file(self.input_file): return False
        
        _, input_ext = os.path.splitext(self.input_file)
        _, output_ext = os.path.splitext(self.output_file)
        input_ext, output_ext = input_ext.lower(), output_ext.lower()
        
        if output_ext not in SUPPORTED_CONVERSIONS.get(input_ext, []):
            self.logger.error(f"Media conversion formally blocked natively: {input_ext} -> {output_ext}")
            return False
            
        if VideoFileClip is None or AudioFileClip is None:
            self.logger.error("Missing standard video library moviepy. Please run: pip install moviepy imageio-ffmpeg")
            return False
            
        self.logger.info("Media framework mapping successfully validated internally.")
        return True

    def convert(self) -> bool:
        _, input_ext = os.path.splitext(self.input_file)
        _, output_ext = os.path.splitext(self.output_file)
        input_ext, output_ext = input_ext.lower(), output_ext.lower()
        
        video_exts = [".mp4", ".mov", ".avi"]
        audio_exts = [".mp3", ".wav"]
        
        try:
            if output_ext == ".gif" and input_ext in video_exts:
                return self._convert_to_gif()
            elif output_ext in audio_exts and input_ext in video_exts:
                return self._extract_audio()
            elif output_ext in video_exts and input_ext in video_exts:
                return self._convert_video()
            elif output_ext in audio_exts and input_ext in audio_exts:
                return self._convert_audio()
            else:
                self.logger.error("Unsupported media conversion requested.")
                return False
        except Exception as e:
            self.logger.exception(f"Media logic severely failed explicitly: {e}")
            return False

    def _convert_video(self) -> bool:
        self.logger.info(f"Swapping codecs formally natively: {self.input_file} -> {self.output_file}")
        try:
            video = VideoFileClip(self.input_file)
            video.write_videofile(self.output_file, logger=None)
            video.close()
            self.logger.info(f"Video format correctly mapped structurally: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Video codec swap massively halted logically: {e}")
            return False

    def _extract_audio(self) -> bool:
        self.logger.info(f"Extracting pure audio structures cleanly: {self.input_file} -> {self.output_file}")
        try:
            video = VideoFileClip(self.input_file)
            audio = video.audio
            if audio is None:
                self.logger.error("Video file does not contain an audio track categorically.")
                video.close()
                return False
                
            audio.write_audiofile(self.output_file, logger=None)
            audio.close()
            video.close()
            self.logger.info(f"Successfully rendered pure audio object format smoothly: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Audio extraction structurally failed explicitly: {e}")
            return False

    def _convert_to_gif(self) -> bool:
        self.logger.info(f"Synthesizing graphical looping GIF logically: {self.input_file} -> {self.output_file}")
        try:
            video = VideoFileClip(self.input_file)
            video.write_gif(self.output_file, logger=None)
            video.close()
            self.logger.info(f"Generated graphical continuous format safely globally: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"GIF rendering functionally crashed internally: {e}")
            return False
            
    def _convert_audio(self) -> bool:
        self.logger.info(f"Translating native audio format gracefully: {self.input_file} -> {self.output_file}")
        try:
            audio = AudioFileClip(self.input_file)
            audio.write_audiofile(self.output_file, logger=None)
            audio.close()
            self.logger.info(f"Audio converted explicitly smoothly globally: {self.output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Audio translation categorically aborted: {e}")
            return False
