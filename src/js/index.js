// src/js/index.js
import "dotenv/config";
import readline from "readline";
import { getVideoIdsFromCsv } from "./csvReader.js";
import {
  clearWatchLaterPlaylist,
  createPlaylistWithVideos,
  getAuthenticatedInstance,
} from "./youtubeService.js";

function prompt(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

function generatePlaylistName() {
  const today = new Date();
  const dateString = today.toISOString().split("T")[0]; // YYYY-MM-DD
  return `WL_${dateString}`;
}

async function main() {
  console.log("Starting the playlist migration process...");

  const publicCsvPath = process.env.CSV_FILENAME;
  if (!publicCsvPath) {
    console.error("ERROR: CSV_FILENAME is not defined in your .env file.");
    return;
  }

  try {
    // Step 1: Read public video IDs to create the new playlist.
    const publicVideoIds = await getVideoIdsFromCsv(publicCsvPath).catch(
      () => []
    );

    if (publicVideoIds.length === 0) {
      console.log(`No videos found in '${publicCsvPath}' to migrate.`);
      console.log(
        "You can still proceed to clear your Watch Later if you wish."
      );
    }

    // Step 2: Get user's cookie for authentication.
    const userCookie = await prompt(
      "\nPlease paste your YouTube cookie string and press Enter:\n> "
    );
    if (!userCookie) {
      console.error("A cookie is required to proceed. Exiting.");
      return;
    }
    const youtube = await getAuthenticatedInstance(userCookie);

    // Step 3: Create the new playlist if there are videos to migrate.
    if (publicVideoIds.length > 0) {
      const reversedPublicIds = [...publicVideoIds].reverse();
      const playlistName = generatePlaylistName();
      await createPlaylistWithVideos(youtube, playlistName, reversedPublicIds);
    }

    // Step 4: Ask for confirmation to clear the ENTIRE 'Watch Later' playlist.
    const confirmation = await prompt(
      `\nDo you want to clear your ENTIRE 'Watch Later' playlist now? (y/n): `
    );

    const affirmativeAnswers = ["yes", "y"];
    if (!affirmativeAnswers.includes(confirmation.toLowerCase())) {
      console.log(
        "Aborting. No changes will be made to your 'Watch Later' playlist."
      );
    } else {
      // Step 5: If confirmed, clear the playlist.
      await clearWatchLaterPlaylist(youtube);
    }

    console.log("\n✅ --- SCRIPT COMPLETE --- ✅");
  } catch (error) {
    if (error.code === "ENOENT") {
      console.error(`\n❌ --- FILE NOT FOUND --- ❌`);
      console.error(`Error: The file '${publicCsvPath}' was not found.`);
      console.error("Please ensure you have run the Python script first.");
    } else {
      console.error("\n❌ --- AN ERROR OCCURRED --- ❌");
      console.error("Error details:", error.message);
    }
  }
}

main();
