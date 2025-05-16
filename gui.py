import tkinter as tk
from tkinter import messagebox
from scrape_jobs import scrape_jobs

def start_scraping():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    job_title = title_entry.get().strip()
    location = location_entry.get().strip()
    page_range = page_range_entry.get().strip()

    if not all([username, password, job_title, location, page_range]):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        status_label.config(text="⏳ Scraping in progress...")
        root.update()

        scrape_jobs(
            username=username,
            password=password,
            job_title=job_title,
            location=location,
            page_range_str=page_range
        )

        messagebox.showinfo("Success", "✅ Scraping complete!\nFile saved in your Downloads folder.")
        status_label.config(text="✅ Done")

    except ValueError as ve:
        messagebox.showwarning("No Pages", str(ve))
        status_label.config(text="⚠️ No pages found in range")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
        status_label.config(text="❌ Failed")


# GUI Layout
root = tk.Tk()
root.title("LinkedIn Job Scraper")
root.geometry("400x350")
root.resizable(False, False)

tk.Label(root, text="LinkedIn Username (Email):").pack(pady=(10, 0))
username_entry = tk.Entry(root, width=40)
username_entry.pack()

tk.Label(root, text="LinkedIn Password:").pack(pady=(10, 0))
password_entry = tk.Entry(root, show="*", width=40)
password_entry.pack()

tk.Label(root, text="Job Title:").pack(pady=(10, 0))
title_entry = tk.Entry(root, width=40)
title_entry.pack()

tk.Label(root, text="Location:").pack(pady=(10, 0))
location_entry = tk.Entry(root, width=40)
location_entry.pack()

tk.Label(root, text="Page Range (e.g., 3-7):").pack(pady=(10, 0))
page_range_entry = tk.Entry(root, width=40)
page_range_entry.pack()

tk.Button(root, text="Start Scraping", command=start_scraping, bg="#0072b1", fg="white", padx=10, pady=5).pack(pady=15)

status_label = tk.Label(root, text="", fg="green")
status_label.pack()

root.mainloop()
