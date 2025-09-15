import csv from "csv-parser";
import fs from "fs";

/**
 * Reads a CSV file and extracts all video IDs from the 'ID' column.
 * @param {string} filePath - The path to the CSV file.
 * @returns {Promise<string[]>} - A promise that resolves to an array of video IDs.
 */
export function getVideoIdsFromCsv(filePath) {
  return new Promise((resolve, reject) => {
    const videoIds = [];
    fs.createReadStream(filePath)
      .pipe(csv())
      .on("data", (row) => {
        if (row.ID && row.ID !== "N/A") {
          videoIds.push(row.ID);
        }
      })
      .on("end", () => {
        console.log(
          `Successfully read ${videoIds.length} video IDs from the CSV file.`
        );
        resolve(videoIds);
      })
      .on("error", (error) => {
        reject(error);
      });
  });
}
