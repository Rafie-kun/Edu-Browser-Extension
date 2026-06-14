import sqlite3
import requests  # We are using requests instead of urllib
from datetime import datetime

# Connect to database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

url = "https://openlibrary.org/search.json?q=textbook&limit=200"

print("Traveling to Open Library (via requests)...")

try:
    # Adding a timeout so it doesn't hang forever
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    data = response.json()
    docs = data.get("docs", [])
    
    count = 0
    for book in docs:
        title = book.get("title", "Unknown Title")
        subjects = book.get("subject", ["General"])
        subject = subjects[0] if subjects else "General"
        key = book.get("key", "")
        book_url = f"https://openlibrary.org{key}"
        
        cursor.execute("""
            INSERT OR IGNORE INTO books (title, subject, url, source, scraped_at)
            VALUES (?, ?, ?, ?, ?)
        """, (title, subject, book_url, "Open Library", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        count += 1
        
    conn.commit()
    print(f"Boom! Successfully harvested {count} new textbooks.")

except Exception as e:
    print(f"Still hitting a snag: {e}")
    print("Tip: Are you on a VPN or a restricted network?")

conn.close()