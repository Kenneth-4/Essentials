import ytdl from "ytdl-core";
import ffmpeg from "fluent-ffmpeg";
import ffmpegPath from "ffmpeg-static";
import { Readable } from "stream";

ffmpeg.setFfmpegPath(ffmpegPath!);

export async function youtubeToMp3(url: string): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    const stream = ytdl(url, { quality: "highestaudio" });
    const chunks: Buffer[] = [];
    const ff = ffmpeg(stream)
      .format("mp3")
      .on("data", (chunk: Buffer) => chunks.push(chunk))
      .on("end", () => resolve(Buffer.concat(chunks)))
      .on("error", reject)
      .pipe();
  });
}
