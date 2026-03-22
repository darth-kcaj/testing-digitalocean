from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Hello World</title>
  <style>
    body {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      background-color: #0069ff;
      font-family: Arial, sans-serif;
      color: #ffffff;
    }
    h1 { font-size: 3rem; margin-bottom: 0.5rem; }
    p  { font-size: 1.25rem; opacity: 0.85; }
  </style>
</head>
<body>
  <h1>Hello, World!</h1>
  <p>This page has been visited <strong id="count">…</strong> time<span id="plural">s</span>.</p>
  <script>
    (function () {
      const key = "visitCount";
      const count = (parseInt(localStorage.getItem(key) || "0", 10)) + 1;
      localStorage.setItem(key, count);
      document.getElementById("count").textContent = count;
      document.getElementById("plural").textContent = count === 1 ? "" : "s";
    })();
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML
