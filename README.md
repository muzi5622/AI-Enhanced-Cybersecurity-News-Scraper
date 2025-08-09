# 📰 AI-Enhanced Cybersecurity News Scraper

This project scrapes the latest **cybersecurity news** from [CyberNews.com](https://cybernews.com/security/), sends each article to the **Groq AI API** for rewriting and formatting, and displays the AI-enhanced articles in a clean, Bootstrap-powered web interface.

---

## 🚀 Features
- **Web scraping** using Selenium (Chrome UI visible).
- **Parallel AI processing** for multiple articles (fast results).
- AI-enhanced output with:
  - Easy-to-read language
  - Headings
  - Bullet points
  - Numbered lists
- Responsive web UI with Bootstrap.
- Opens automatically in your browser.

---

## 📦 Requirements
- Python 3.8+
- Google Chrome installed
- ChromeDriver (matching your Chrome version)
- Groq API Key

Install dependencies:
```bash
pip install -r requirements.txt
````

---

## 🔑 Setup

1. **Clone this repository**:

```bash
git clone https://github.com/muzi5622/AI-Enhanced-Cybersecurity-News-Scraper/
cd AI-Enhanced-Cybersecurity-News-Scraper
```

2. **Set your Groq API key**
   Open the Python file and replace:

```python
API_KEY = "your_groq_api_key_here"
```

3. **Run the script**:

```bash
python main.py
```

---

## 🖥️ Usage

When you run the script:

1. Chrome will open and scrape the latest **Cybersecurity** articles.
2. Each article is **rewritten by Groq AI**.
3. The results are shown in a clean web interface.
4. Your browser will automatically open to `http://127.0.0.1:5000`.

---

## 📷 Screenshot

<img width="888" height="962" alt="image" src="https://github.com/user-attachments/assets/0ae70cf6-defe-4bc2-9c7f-082dc36d70c9" />


---

## ⚠️ Notes

- This project uses a **visible Chrome browser** for scraping (not headless).  
- AI requests are handled in **parallel** to speed up processing.  
- A **valid Groq API key** is required for AI enhancements.  
- I created this project after completing my **Python Selenium** learning — the Selenium scraping part was built by me, while the rest of the features were implemented with the help of AI.  



