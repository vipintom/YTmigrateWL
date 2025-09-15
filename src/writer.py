# src/writer.py
import csv
from typing import List

from .types import FlatVideoInfo


class CsvWriter:
    def __init__(self, filename: str, header: List[str]):
        self.filename = filename
        self.header = header
        self.file_handle = None
        self.writer = None

    def __enter__(self):
        # Open in write mode ('w') to always overwrite the file
        self.file_handle = open(self.filename, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file_handle)

        # Write the header as the first line of the new file
        self.writer.writerow(self.header)
        self.file_handle.flush()
        print(f"Created new CSV file (overwriting if exists): '{self.filename}'")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_handle:
            self.file_handle.close()

    def write_video(self, video: FlatVideoInfo):
        if self.writer and self.file_handle:
            self.writer.writerow(
                [
                    video.get("id", "N/A"),
                    video.get("title", "N/A"),
                ]
            )
            self.file_handle.flush()
