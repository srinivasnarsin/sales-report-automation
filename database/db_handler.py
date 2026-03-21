from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

def get_engine():
    return create_engine(os.getenv("DATABASE_URL"))

def create_table():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sales_report (
                id SERIAL PRIMARY KEY,
                division_name VARCHAR(255),
                promo_name VARCHAR(255),
                bill_no VARCHAR(255),
                barcode VARCHAR(255),
                article_name VARCHAR(255),
                section_name VARCHAR(255),
                site_name VARCHAR(255),
                bill_date TIMESTAMP,
                category_name2 VARCHAR(255),
                category_name1 VARCHAR(255),
                category_name4 VARCHAR(255),
                department_name VARCHAR(255),
                mrp NUMERIC,
                hsn_code VARCHAR(255),
                short_name VARCHAR(255),
                qty NUMERIC,
                sale_mrp NUMERIC,
                selling_amt NUMERIC,
                tax_amount NUMERIC,
                tax_percent NUMERIC,
                taxable_amount NUMERIC,
                vendor_name VARCHAR(255),
                sales_type VARCHAR(255),
                partner_name VARCHAR(255),
                city VARCHAR(255),
                discount_amount NUMERIC,
                asm VARCHAR(255),
                site_short_name VARCHAR(255),
                color VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(bill_no, barcode, bill_date)
            )
        """))
        conn.commit()
    print("   ✅ Table ready!")

def insert_data(filepath):
    print(f"📊 Reading file: {filepath}")

    # Read the file
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    print(f"   Found {len(df)} rows, {len(df.columns)} columns")

    # Clean column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Convert bill_date to datetime
    df["bill_date"] = pd.to_datetime(df["bill_date"], errors="coerce")

    # Fill empty values
    df = df.fillna("")

    engine = get_engine()

    # --- Check if data for this date already exists ---
    date = df["bill_date"].dt.date.min()
    print(f"   Checking if data for {date} already exists...")

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*) FROM sales_report
            WHERE DATE(bill_date) = :date
        """), {"date": str(date)})
        count = result.scalar()

    if count > 0:
        print(f"   ⚠️ Data for {date} already exists ({count} rows) — skipping insert!")
        return 0

    # --- Bulk insert ---
    df.to_sql(
        "sales_report",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=100
    )

    print(f"   ✅ Inserted {len(df)} rows for {date}!")
    return len(df)


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Setting up database...")
    print("=" * 50)

    # Step 1: Create table
    create_table()

    # Step 2: Find latest file in output/
    output_dir = "output"
    files = [f for f in os.listdir(output_dir) if f.endswith(".xlsx") or f.endswith(".csv")]

    if not files:
        print("⚠️ No files found in output/ folder!")
        print("Run downloader.py first!")
    else:
        latest = max(files, key=lambda f: os.path.getctime(
            os.path.join(output_dir, f)
        ))
        filepath = os.path.join(output_dir, latest)
        print(f"   📂 Using file: {latest}")
        insert_data(filepath)

    print("=" * 50)
    print("✅ Done!")
    print("=" * 50)