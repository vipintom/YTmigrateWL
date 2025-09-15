# RepoScribe – YouTube 'Watch Later' Exporter & Cleaner

RepoScribe is a powerful two-step tool designed to help you rescue, archive, and manage your YouTube "Watch Later" playlist. If your "Watch Later" has become an unmanageable backlog of hundreds or thousands of videos, this tool is for you.

It allows you to:

1. **Export** your entire "Watch Later" playlist—including titles and IDs—into clean, usable CSV files using your browser's cookies.
2. **Archive** these videos by creating a new, timestamped, private playlist on your YouTube account.
3. **Securely Clear** your entire "Watch Later" playlist, giving you a fresh start.

## Why Does This Tool Exist?

The native YouTube "Watch Later" playlist is a black box. It lacks essential features for management:

* There is no native "Export" functionality.
* You cannot sort, filter, or easily manage videos in bulk.
* Clearing a large playlist requires deleting videos one by one, which is incredibly tedious.

This tool solves these problems by using a robust Python script to extract the data and an interactive Node.js script to manage your playlists via the YouTube API.

## Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.13+**
* **Node.js v18+**
* A modern package manager like **pnpm** (recommended) or **npm**.
* **Firefox** or **Google Chrome** (logged into your YouTube account).
* **(Recommended)** **direnv** for automatic environment variable and virtual environment management.

## 1. Setup Instructions

**1. Clone the repository:**

```bash
git clone https://github.com/your-username/RepoScribe.git
cd RepoScribe
```

**2. Configure your environment:**
Create a `.env` file by copying the example. This file will store your local configuration.

```bash
cp .env.example .env
```

**This is a critical step.** You will need to edit this file in the next section.

**3. Set up the environment and install dependencies:**

* **With `direnv` (Recommended):**
    If you have `direnv` installed, simply run the following command. It will automatically create a Python virtual environment, activate it, and make your `.env` variables available.

    ```bash
    direnv allow
    ```

* **Manual Setup:**
    If you are not using `direnv`, create and activate a Python virtual environment manually:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    # On Windows, use: .venv\Scripts\activate
    ```

**4. Install dependencies:**
Install the Python and Node.js packages.

```bash
# Install Python packages
pip install .

# Install Node.js packages (pnpm is recommended)
pnpm install
# Or, if you use npm:
# npm install
```

## 2. Configuration

Open the `.env` file you created and configure it.

### `BROWSER` (Required)

Set this to the browser where you are logged into YouTube.

* **Supported values:** `"firefox"` or `"chrome"`.

### Profile Paths (Optional)

By default, the script will attempt to use the **default profile** for your selected browser. You only need to set these paths if you use a different, non-default profile.

* **`FIREFOX_PROFILE_PATH`**: To find this, navigate to `about:profiles` in Firefox.
* **`CHROME_PROFILE_PATH`**: To find this, navigate to `chrome://version` in Chrome.

Leave the variable for the browser you are *not* using blank.

## 3. Usage

The entire workflow can be run with a single command.

```bash
pnpm start
# Or, if you use npm:
# npm start
```

This command executes the two main stages in sequence:

### Stage 1: Fetch Video List

The Python script (`fetch-videos`) runs first. It securely uses your browser's cookies to access your "Watch Later" playlist and exports all video details into CSV files (e.g., `watch_later_public.csv`).

### Stage 2: Migrate Videos & Clear Playlist

Next, the interactive Node.js script (`migrate-videos`) runs. It will guide you through the following prompts:

1. **Create a New Playlist:** It will use the generated CSV file to create a new, private playlist on your YouTube account named `WL_YYYY-MM-DD`.
2. **Paste Your YouTube Cookie:** The script will then ask you to paste a cookie string. This is required for authentication to clear your playlist.
3. **Confirm Clearing 'Watch Later':** Finally, it will ask for explicit confirmation (`y/n`) before it begins clearing your "Watch Later" playlist. **This action is irreversible.**

---

### How to Get Your YouTube Cookie for Stage 2

When the script prompts you, follow these steps in your browser (Firefox or Chrome) to get the required cookie string:

1. Go to `https://www.youtube.com`.
2. Open **Developer Tools** (press `F12` or `Ctrl+Shift+I` / `Cmd+Option+I`).
3. Go to the **Network** tab.
4. In the filter bar, select **Fetch/XHR**.
5. Refresh the YouTube page (press `F5` or `Ctrl+R` / `Cmd+R`).
6. You will see a list of network requests. Click on any request to `www.youtube.com` (e.g., a request named `browse`).
7. In the new panel that appears, find the **Headers** tab. Scroll down to the **Request Headers** section.
8. Find the header named `cookie:`. **Copy the entire string of text** that follows it.

> **Warning:** Your cookie is sensitive data. It's like a temporary password. Do not share it with anyone. The script only uses it to make authenticated requests and does not save it anywhere.

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 [Your Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
