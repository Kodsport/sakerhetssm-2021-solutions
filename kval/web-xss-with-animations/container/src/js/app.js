const express = require('express')
const app = express()
const path = require('path');
const puppeteer = require('puppeteer');
const fs = require('fs');
const port = 3000

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../html/index.html'));
})

app.get('/source', (req, res) => {
  res.sendFile(path.join(__dirname, './app.js'));
})

app.get('/submit', (req, res) => {
  const link = req.query['link'];
  if (!(new RegExp("^/chall.*$").test(link))) {
    res.send("BAD URL")
    return
  }

  run_puppet(link).then((result) => {
    if(result === true) {
      res.sendFile(path.join(__dirname, '../html/flag.html'));
    } else {
      res.sendFile(path.join(__dirname, '../html/nope.html'));
    }
  })
})

app.get('/chall', (req, res) => {
  let dbg = req.query['debug'];
  let xss = req.query['xss'];
  let data;
  try {
    data = fs.readFileSync(path.join(__dirname, '../html/chall.html'), 'utf8')
  } catch (err) {
    console.error(err)
    res.status(500)
    res.render('error', { error: "bad stuff happened" })
    return
  }

  if (xss !== undefined) {
    xss = xss.replace(/{/g, "").replace(/}/g, "")
    xss = escapeHtml(xss)
  }

  if (dbg !== undefined) {
    dbg = dbg.replace(/{/g, "").replace(/}/g, "")
    dbg = escapeJS(escapeHtml(dbg));
  }

  data = data.replace("{{XSS HERE}}", xss).replace("{{COLOR HERE}}", dbg)

  res.send(data)
})

function escapeJS(unsafe) {
  return unsafe
    .replace(/\\/g, '\\\\')
    .replace(/</g, '\<')
    .replace(/>/g, '\>')
    .replace(/"/g, '\"')
    .replace(/'/g, "\'");
}

function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

async function run_puppet(link) {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
    ],
  })
  const page = await browser.newPage();
  let xsstriggered = false;
  page.on('dialog', async dialog => {
    await dialog.dismiss();
    xsstriggered = true;
  });
  try {
    await page.goto("http://localhost:3000" + link);
    await page.click("#btn");
    await delay(1000);
    await browser.close();
  } catch (error) {
    xsstriggered = false;
  }
  return xsstriggered;
}

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

app.listen(port, "0.0.0.0", () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
