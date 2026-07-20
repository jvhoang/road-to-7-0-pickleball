/**
 * Capture high-fidelity Amazon mock screenshots via Chrome headless.
 * Usage: node scripts/capture-screenshots.mjs
 */
import { spawn } from "child_process";
import { createServer } from "http";
import { readFileSync, existsSync, mkdirSync, statSync } from "fs";
import { join, extname, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const OUT = join(ROOT, "screenshots");
const CHROME =
  process.env.CHROME_PATH ||
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript",
  ".json": "application/json",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".md": "text/markdown",
};

function contentType(p) {
  return MIME[extname(p).toLowerCase()] || "application/octet-stream";
}

function startServer() {
  return new Promise((resolve) => {
    const server = createServer((req, res) => {
      let urlPath = decodeURIComponent((req.url || "/").split("?")[0]);
      if (urlPath === "/") urlPath = "/product.html";
      const filePath = join(ROOT, urlPath.replace(/^\//, ""));
      if (!filePath.startsWith(ROOT) || !existsSync(filePath) || statSync(filePath).isDirectory()) {
        res.writeHead(404);
        res.end("Not found");
        return;
      }
      const data = readFileSync(filePath);
      res.writeHead(200, { "Content-Type": contentType(filePath) });
      res.end(data);
    });
    server.listen(0, "127.0.0.1", () => {
      const { port } = server.address();
      resolve({ server, port });
    });
  });
}

function runChrome(args) {
  return new Promise((resolve, reject) => {
    const proc = spawn(CHROME, args, { stdio: ["ignore", "pipe", "pipe"] });
    let stderr = "";
    proc.stderr.on("data", (d) => (stderr += d.toString()));
    proc.on("error", reject);
    proc.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`Chrome exit ${code}: ${stderr.slice(0, 500)}`));
    });
  });
}

const SHOTS = [
  {
    name: "01-product-page.png",
    path: "/product.html",
    width: 1440,
    height: 1100,
    fullPage: false,
  },
  {
    name: "02-product-page-full.png",
    path: "/product.html",
    width: 1440,
    height: 900,
    fullPage: true,
  },
  {
    name: "03-look-inside-chapter.png",
    path: "/look-inside.html",
    width: 1200,
    height: 1600,
    fullPage: true,
  },
  {
    name: "04-reviews.png",
    path: "/reviews.html",
    width: 1440,
    height: 900,
    fullPage: true,
  },
  {
    name: "05-cover-detail.png",
    path: "/cover-detail.html",
    width: 1440,
    height: 900,
    fullPage: false,
  },
  {
    name: "06-mobile-product.png",
    path: "/mobile-product.html",
    width: 390,
    height: 1200,
    fullPage: true,
  },
];

async function capture({ port, shot }) {
  const outPath = join(OUT, shot.name);
  const url = `http://127.0.0.1:${port}${shot.path}`;
  const args = [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--force-device-scale-factor=2",
    `--window-size=${shot.width},${shot.height}`,
    `--screenshot=${outPath}`,
    ...(shot.fullPage ? ["--screenshot-full-size"] : []),
    // Chrome headless full page uses --virtual-time-budget + default screenshot;
    // for full page we use a larger height when needed via CDP alternative below.
    url,
  ];

  // Prefer CDP for reliable full-page captures
  // Fallback: large viewport screenshot
  if (shot.fullPage) {
    await captureFullPageCDP({ port, shot, outPath, url });
  } else {
    await runChrome(args);
  }
  if (!existsSync(outPath)) {
    throw new Error(`Screenshot missing: ${outPath}`);
  }
  const size = statSync(outPath).size;
  console.log(`OK ${shot.name} (${size} bytes)`);
}

async function captureFullPageCDP({ shot, outPath, url }) {
  // Use puppeteer-core style via chrome remote debugging if available;
  // Otherwise enlarge window and take screenshot.
  const height = shot.name.includes("look-inside")
    ? 4200
    : shot.name.includes("reviews")
      ? 3200
      : shot.name.includes("mobile")
        ? 1800
        : 2800;
  const args = [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--force-device-scale-factor=2",
    `--window-size=${shot.width},${height}`,
    `--screenshot=${outPath}`,
    url,
  ];
  await runChrome(args);
}

async function main() {
  if (!existsSync(CHROME)) {
    throw new Error(`Chrome not found at ${CHROME}`);
  }
  mkdirSync(OUT, { recursive: true });
  const { server, port } = await startServer();
  console.log(`Serving on http://127.0.0.1:${port}`);
  try {
    for (const shot of SHOTS) {
      await capture({ port, shot });
    }
  } finally {
    server.close();
  }
  console.log("All screenshots written to", OUT);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
