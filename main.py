# main.py
import os
import sys

import yt_dlp
from dotenv import load_dotenv

from src.fetcher import process_playlist_videos


def main():
    """Main function to run the video fetching and saving process."""
    load_dotenv()

    # --- Configuration from .env ---
    csv_filename = os.getenv("CSV_FILENAME", "watch_later_public.csv")
    csv_filename_private = os.getenv("CSV_FILENAME_PRIVATE", "watch_later_private.csv")
    browser = os.getenv("BROWSER", "").lower()

    # --- Validate Browser and Get Optional Profile Path ---
    supported_browsers = ["firefox", "chrome"]
    if not browser or browser not in supported_browsers:
        print("ERROR: You must set a valid BROWSER in your .env file.", file=sys.stderr)
        print(
            f"Supported browsers are: {', '.join(supported_browsers)}", file=sys.stderr
        )
        sys.exit(1)

    profile_path = os.getenv(f"{browser.upper()}_PROFILE_PATH")

    # --- Process all videos in the playlist ---
    try:
        print(
            f"Starting the process to fetch videos using {browser.capitalize()} cookies..."
        )
        if profile_path:
            print(f"Using specified profile path: {profile_path}")
        else:
            print("Using default browser profile.")

        process_playlist_videos(
            browser=browser,
            profile_path=profile_path,
            output_filename=csv_filename,
            private_output_filename=csv_filename_private,
        )

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting gracefully.")
        sys.exit(0)

    except yt_dlp.utils.DownloadError as e:
        print(
            f"\n❌ CRITICAL ERROR: Could not fetch the YouTube playlist using {browser.capitalize()} cookies.",
            file=sys.stderr,
        )
        print(f"   yt-dlp error: {e}", file=sys.stderr)
        print("\n--- Common Solutions ---", file=sys.stderr)
        print(
            f"1. Ensure your browser ({browser.capitalize()}) is completely closed.",
            file=sys.stderr,
        )
        print(
            f"2. Make sure you are logged into YouTube in the correct {browser.capitalize()} profile.",
            file=sys.stderr,
        )
        print(
            "3. If you use a non-default profile, ensure the correct profile path is set in your .env file.",
            file=sys.stderr,
        )
        sys.exit(1)

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
