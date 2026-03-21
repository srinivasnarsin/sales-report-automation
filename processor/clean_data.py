import pandas as pd
import os

def clean_data(filepath):
    print(f"🧹 Cleaning data: {filepath}")

    # Read file
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    print(f"   Rows before cleaning: {len(df)}")

    # --- Remove NSM rows from Division Name ---
    df = df[df["Division Name"].str.strip() != "NSM"]
    print(f"   Rows after removing NSM: {len(df)}")

    # Save cleaned file
    cleaned_path = filepath.replace(".csv", "_cleaned.csv").replace(".xlsx", "_cleaned.xlsx")
    df.to_csv(cleaned_path, index=False)
    print(f"   ✅ Cleaned file saved: {cleaned_path}")

    return cleaned_path


if __name__ == "__main__":
    # Test with latest file in output/
    output_dir = "output"
    files = [f for f in os.listdir(output_dir) if 
             (f.endswith(".xlsx") or f.endswith(".csv")) 
             and "cleaned" not in f]

    if not files:
        print("⚠️ No files found in output/!")
    else:
        latest = max(files, key=lambda f: os.path.getctime(
            os.path.join(output_dir, f)
        ))
        clean_data(os.path.join(output_dir, latest))