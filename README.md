# 🧠 LinkedIn Job Scraper GUI

A beginner-friendly, GUI-based LinkedIn job scraper built using **Python**, **Tkinter**, and **Selenium**.

This app allows **non-coders** to scrape job listings from LinkedIn based on:
- Job Title  
- Location  
- Page Range (e.g., 2–5)  

📝 The scraped results are automatically saved as an Excel file to your **Downloads** folder.

---

## 🔍 Features

- ✅ No coding knowledge required – just fill in inputs and click "Start"
- ✅ Built-in GUI using Tkinter
- ✅ Scrolls through job listings and paginates like a real user
- ✅ Smart handling of missing or limited page ranges
- ✅ Export results to `.xlsx` with dynamic filename like:  
  `Python_Developer_2025-05-16_22-48.xlsx`

---

## 📦 Requirements

| Tool | Version |
|------|---------|
| Python | 3.10+ recommended |
| Chrome | Latest |
| ChromeDriver | Auto-managed via `webdriver_manager` |

---

## ⚙️ Setup (Developer Mode)

```bash
# 1. Clone the repo
git clone https://github.com/rupankar-1733/linkedin-job-scraper-gui.git
cd linkedin-job-scraper-gui

# 2. Create & activate a virtual environment
python -m venv scraper_env
scraper_env\Scripts\activate   # for Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python gui.py
```

---


## 🛠️ Build to .exe (Optional)

If you want to share the tool as a standalone `.exe`:

```bash
pyinstaller --onefile --noconsole --icon=linkedin_scraper.ico gui.py
```

The final `.exe` will appear in the `dist/` folder.

---

## 🧾 Project Structure

```
linkedin_scraper_app/
├── gui.py                # Tkinter GUI code
├── scrape_jobs.py        # Core scraping logic
├── linkedin_scraper.ico  # App icon (used for .exe)
├── requirements.txt
├── README.md
├── .gitignore
```

---

## 🤝 Author

Built with ❤️ by **Rupankar Mondal**  
🔗 GitHub: [@rupankar-1733](https://github.com/rupankar-1733)

---

## 📄 License

This project is licensed under the MIT License.
