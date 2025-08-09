from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
import requests
import webbrowser
from flask import Flask, render_template_string

# === Config ===
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "Enter_Your_API_Key"
MODEL_ID = "llama-3.3-70b-versatile"
MAX_ARTICLES = 5
MAX_WORKERS = 5  # Parallel threads for AI requests

# Flask app
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cyber Security Articles</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container my-5">
    <h1 class="mb-4 text-center">🤖 Cyber Security Articles</h1>
    {% for idx, resp in data %}
    <div class="card mb-4 shadow-sm">
        <div class="card-header bg-success text-white">
            <h5>Article {{ idx }}</h5>
        </div>
        <div class="card-body">
            {{ resp|safe }}
        </div>
    </div>
    {% endfor %}
</div>
</body>
</html>
"""

# === Send to Groq (AI Processing) ===
def send_to_groq(article_text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    instruction = (
        "Rewrite the following cybersecurity news article in easy English. "
        "Add headings, bullet points, numbered lists, and any extra features to make it engaging. "
        "Return the result in valid HTML only — do not include extra commentary outside HTML. "
        "Don't add 'follow us', 'share this', or unrelated stuff. Keep it short and to the point."
    )
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a professional news editor who outputs clean HTML articles."},
            {"role": "user", "content": f"{instruction}\n\n{article_text}"}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"<p>Error: {response.status_code} – {response.text}</p>"
    except Exception as e:
        return f"<p>Request failed: {e}</p>"

# === Scrape Articles (Normal Chrome) ===
def get_articles():
    driver = webdriver.Chrome()  # Normal Chrome window
    driver.get("https://cybernews.com/security/")
    sleep(2)

    all_element = driver.find_elements(By.TAG_NAME, "a")
    news_links = []
    seen = set()

    for tag in all_element:
        href = tag.get_attribute("href")
        if href and "/security/" in href and href not in seen:
            news_links.append(href)
            seen.add(href)
        if len(news_links) >= MAX_ARTICLES:
            break

    articles = []
    for link in news_links:
        driver.get(link)
        sleep(1)
        content_elements = driver.find_elements(By.XPATH, "//div[@class='content']")
        article_text = "\n".join([el.text for el in content_elements if el.text.strip()])
        if article_text.strip():
            articles.append(article_text)

    driver.quit()
    return articles

# === Store results globally for Flask ===
results_data = []

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, data=results_data)

# === Main ===
if __name__ == "__main__":
    print("🔍 Scraping articles...")
    articles = get_articles()

    print(f"⚡ Sending {len(articles)} articles to AI in parallel...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(send_to_groq, art): idx+1 for idx, art in enumerate(articles)}
        for future in as_completed(futures):
            idx = futures[future]
            resp = future.result()
            results_data.append((idx, resp))

    results_data.sort(key=lambda x: x[0])

    print("✅ Data ready! Opening web UI...")
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False, port=5000)
