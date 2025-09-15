// src/js/youtubeService.js
import { Innertube } from "youtubei.js";

/**
 * Authenticates with YouTube using a provided cookie string.
 * @param {string} cookie - The YouTube cookie string.
 * @returns {Promise<Innertube>} An authenticated Innertube instance.
 */
export async function getAuthenticatedInstance(cookie) {
  console.log("\nAuthenticating with YouTube...");
  const youtube = await Innertube.create({ cookie });
  console.log("Authentication successful.");
  return youtube;
}

/**
 * Creates a new playlist and adds the given videos to it.
 * @param {Innertube} youtube - An authenticated Innertube instance.
 * @param {string} playlistName - The name of the new playlist.
 * @param {string[]} videoIds - An array of video IDs to add.
 */
export async function createPlaylistWithVideos(
  youtube,
  playlistName,
  videoIds
) {
  console.log(`\nCreating new private playlist named: "${playlistName}"...`);
  const playlistDetails = await youtube.playlist.create(playlistName, videoIds);
  const playlistId = playlistDetails.playlist_id;

  console.log(`Playlist "${playlistName}" created successfully.`);
  console.log(`Added ${videoIds.length} videos to the new playlist.`);
  console.log(
    `View it here: https://www.youtube.com/playlist/list=${playlistId}`
  );
}

/**
 * Continuously fetches pages of ~100 videos from 'Watch Later' and removes them
 * until the playlist is empty.
 * @param {Innertube} youtube - An authenticated Innertube instance.
 */
export async function clearWatchLaterPlaylist(youtube) {
  let totalSuccessCount = 0;
  let iteration = 1;
  const DELAY_MS = 500;

  while (true) {
    try {
      console.log(
        `\n--- Iteration ${iteration}: Fetching the next page of videos... ---`
      );
      const playlist = await youtube.getPlaylist("WL");

      if (playlist.videos.length === 0) {
        console.log("\n'Watch Later' is now empty. Process complete.");
        break;
      }

      const videosToRemove = playlist.videos;
      const videoIdsToRemove = videosToRemove.map((video) => video.id);

      console.log(
        `Found ${videosToRemove.length} videos. Attempting removal...`
      );

      try {
        await youtube.playlist.removeVideos("WL", videoIdsToRemove);
        totalSuccessCount += videosToRemove.length;
        console.log(`✅ Successfully removed ${videosToRemove.length} videos.`);
      } catch (error) {
        console.error(
          `❌ Failed to remove page of videos | Reason: ${error.message}`
        );
        console.error("Aborting to prevent further issues.");
        break;
      }

      await new Promise((resolve) => setTimeout(resolve, DELAY_MS));
      iteration++;
    } catch (error) {
      console.error(
        `\n❌ CRITICAL ERROR during fetch in iteration ${iteration}.`
      );
      console.error("Reason:", error.message);
      break;
    }
  }

  console.log(`\n\n--- FINAL SUMMARY ---`);
  console.log(`- Total videos successfully removed: ${totalSuccessCount}`);
  if (totalSuccessCount === 0 && iteration > 1) {
    console.log(
      "- It seems no videos were removed, despite multiple attempts."
    );
  }
}
