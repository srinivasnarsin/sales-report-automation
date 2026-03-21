from scraper.downloader import download_file
from processor.clean_data import clean_data
from database.db_handler import create_table, insert_data
from datetime import datetime

def main():
    print("=" * 50)
    print(f"🚀 Daily Sales Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    # --- Step 1: Download file ---
    print("\n📥 STEP 1: Downloading sales data...")
    filepath = download_file()
    print(f"   ✅ File downloaded: {filepath}")

    # --- Step 2: Clean data ---
    print("\n🧹 STEP 2: Cleaning data...")
    cleaned_path = clean_data(filepath)
    print(f"   ✅ Cleaned file: {cleaned_path}")

    # --- Step 3: Insert into database ---
    print("\n💾 STEP 3: Inserting into database...")
    create_table()
    rows = insert_data(cleaned_path)
    print(f"   ✅ {rows} rows inserted into database!")

    print("\n" + "=" * 50)
    print("✅ All done!")
    print("=" * 50)

if __name__ == "__main__":
    main()