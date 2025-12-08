import puppeteer from "puppeteer";

const browser = await puppeteer.launch();
const page = await browser.newPage();

await page.goto("https://yourwebsite.com", { waitUntil: "networkidle0" });

await page.screenshot({
    path: "screenshot.png",
    fullPage: true,
    type: "png",
    captureBeyondViewport: true,
    clipScale: 3,       // super high DPI
});

await browser.close();
