# src/logger.py
import sys


class YtDlpLogger:
    """A custom logger for yt-dlp that can integrate with a tqdm progress bar."""

    def __init__(self):
        self.pbar = None

    def set_pbar(self, pbar_instance):
        """Sets the tqdm progress bar instance to be used for logging."""
        self.pbar = pbar_instance

    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        if "ffmpeg not found" not in msg:
            formatted_msg = f"WARNING: {msg}"
            if self.pbar:
                self.pbar.write(formatted_msg)
            else:
                print(formatted_msg, file=sys.stderr)

    def error(self, msg):
        formatted_msg = f"ERROR: {msg}"
        if self.pbar:
            self.pbar.write(formatted_msg)
        else:
            print(formatted_msg, file=sys.stderr)
