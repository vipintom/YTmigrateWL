# src/fetcher.py
from typing import List, Optional, Tuple, cast

import yt_dlp
from tqdm import tqdm

from .logger import YtDlpLogger
from .types import FlatPlaylistInfo, FlatVideoInfo
from .writer import CsvWriter


def _get_flat_playlist_info(
    browser: str,
    profile_path: Optional[str],
) -> Tuple[List[FlatVideoInfo], List[FlatVideoInfo]]:
    """
    Performs a quick, flat extraction of all videos from the 'Watch Later' playlist,
    partitioning them into valid and private lists.
    """
    # Dynamically build the cookies argument for yt-dlp.
    # If profile_path is provided, the arg is ('chrome', '/path/to/profile').
    # If not, the arg is just ('chrome',), which tells yt-dlp to find the default.
    cookies_arg = (browser, profile_path) if profile_path else (browser,)

    ydl_opts_flat = {
        "cookiesfrombrowser": cookies_arg,
        "quiet": True,
        "logger": YtDlpLogger(),
        "extract_flat": True,
    }

    target_url = "https://www.youtube.com/playlist?list=WL"

    with yt_dlp.YoutubeDL(ydl_opts_flat) as ydl:
        playlist_info = cast(
            Optional[FlatPlaylistInfo], ydl.extract_info(target_url, download=False)
        )

    if not (playlist_info and playlist_info.get("entries")):
        raise RuntimeError("Could not retrieve playlist contents.")

    all_videos = [video for video in playlist_info["entries"] if video]
    valid_videos, private_videos = [], []
    for video in all_videos:
        if video.get("title") == "[Private video]":
            private_videos.append(video)
        else:
            valid_videos.append(video)

    if private_videos:
        print(f"Found and separated {len(private_videos)} private videos.")
    return valid_videos, private_videos


def process_playlist_videos(
    browser: str,
    profile_path: Optional[str],
    output_filename: str,
    private_output_filename: str,
):
    """
    Orchestrates fetching and writing of 'Watch Later' videos, separating
    public and private videos into different files.
    """
    print("\nStep 1: Fetching and partitioning the list of videos...")
    public_videos, private_videos = _get_flat_playlist_info(browser, profile_path)

    # --- Process Public Videos ---
    if not public_videos:
        print("\nNo valid, public videos found to process.")
    else:
        public_videos.reverse()
        print(f"\nFound {len(public_videos)} public videos to write to CSV.")
        print(f"Step 2: Writing public videos to '{output_filename}'...")
        header = ["ID", "Title"]
        with (
            CsvWriter(output_filename, header) as writer,
            tqdm(
                total=len(public_videos), unit=" video", desc="Writing Public"
            ) as pbar,
        ):
            for video in public_videos:
                writer.write_video(video)
                pbar.update(1)

    # --- Process Private Videos ---
    if not private_videos:
        print("\nNo private videos found.")
    else:
        private_videos.reverse()
        print(f"\nStep 3: Writing private videos to '{private_output_filename}'...")
        header = ["ID", "Title"]
        with (
            CsvWriter(private_output_filename, header) as writer,
            tqdm(
                total=len(private_videos), unit=" video", desc="Writing Private"
            ) as pbar,
        ):
            for video in private_videos:
                writer.write_video(video)
                pbar.update(1)

    print("\nProcessing complete.")
