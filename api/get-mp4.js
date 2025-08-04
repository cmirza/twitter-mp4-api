import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const execAsync = promisify(exec);

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).send("Method Not Allowed");
  }

  const { url } = req.body;
  if (!url || typeof url !== "string") {
    return res.status(400).send("Missing or invalid 'url'");
  }

  try {
    const { stdout } = await execAsync(`${__dirname}/yt-dlp -j "${url}"`);
    const json = JSON.parse(stdout);

    const httpFormats = json.formats.filter((f) =>
      f.format_id.startsWith("http-")
    );

    if (!httpFormats.length) {
      return res.status(404).send("No MP4 formats found");
    }

    const best = httpFormats.sort((a, b) => (b.height || 0) - (a.height || 0))[0];
    return res.status(200).send(best.url);
  } catch (err) {
    return res.status(500).send(err.message || "yt-dlp error");
  }
}
