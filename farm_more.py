import sqlite3
import requests
from datetime import datetime

# 1. Connect to the master chest
# We use the full path just to be safe
DB_PATH = "database.db"

def harvest_books():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Target URL - Limited to 50 to keep it snappy and clean
    url = "https://openlibrary.org/search.json?q=textbook&limit=50"
    
    print("Connecting to the Open Library...")
    
    try:
        response = requests.get(url, headers={'User-Agent': 'CourseAggregator/1.0'}, timeout=15)
        response.raise_for_status() # This will catch connection errors
        data = response.json()
        docs = data.get("docs", [])
        
        count = 0
        for book in docs:
            title = book.get("title", "Unknown Title")
            # Grab first subject if it exists, else 'General'
            subjects = book.get("subject", ["General"])
            subject = subjects[0] if isinstance(subjects, list) else "General"
            
            key = book.get("key", "")
            book_url = f"https://openlibrary.org{key}"
            
            # Save only if the title doesn't already exist
            cursor.execute("""
                INSERT OR IGNORE INTO books (title, subject, url, source, scraped_at)
                VALUES (?, ?, ?, ?, ?)
            """, (title, subject, book_url, "Open Library", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            if cursor.rowcount > 0:
                count += 1
                
        conn.commit()
        print(f"Success! {count} new textbooks were added to the chest.")
        
    except Exception as e:
        print(f"Failed to harvest: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    harvest_books()