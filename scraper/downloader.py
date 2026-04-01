from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import time
from datetime import datetime

load_dotenv()

def download_file():

    print("🔧 Setting up Chrome...")
    options = webdriver.ChromeOptions()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    download_path = os.path.join(base_dir, "output")
    os.makedirs(download_path, exist_ok=True)

    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)

    # ============================================================
    # ✅ REQUIRED FIX FOR GITHUB ACTIONS
    # ============================================================
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-zygote")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 30)

    today_str = str(datetime.now().day) + datetime.now().strftime(" %b %Y")
    print(f"   📅 Checking for today's date: '{today_str}'")

    try:
        # --- Clean output folder ---
        print("🧹 Cleaning output folder...")
        for f in os.listdir(download_path):
            if (f.endswith(".csv") or f.endswith(".xlsx")) and "cleaned" not in f:
                os.remove(os.path.join(download_path, f))
                print(f"   Deleted: {f}")

        # --- Step 1: Open website ---
        print("🌐 Step 1: Opening website...")
        driver.get(os.getenv("SOURCE_URL"))
        time.sleep(3)
        print(f"   ✅ Page title: {driver.title}")

        # --- Step 2: Login ---
        print("🔐 Step 2: Logging in...")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(os.getenv("SOURCE_USERNAME"))
        print("   ✅ Entered username")

        driver.find_element(By.ID, "passwordGenericInput").send_keys(os.getenv("SOURCE_PASSWORD"))
        print("   ✅ Entered password")

        driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]").click()
        print("   ✅ Clicked Log In")

        time.sleep(3)

        try:
            log_me_in = driver.find_element(By.XPATH, "//button[contains(text(), 'Log me In')]")
            print("   🔄 Found 'Log me In' button, clicking...")
            log_me_in.click()
            print("   ✅ Clicked Log me In")
        except:
            print("   ℹ️ No 'Log me In' button, continuing...")

        time.sleep(5)
        driver.save_screenshot(os.path.join(download_path, "step2_after_login.png"))
        print("   ✅ Login done!")

        # --- Step 3: Pie chart ---
        print("📊 Step 3: Clicking pie chart icon...")

        sidebar_icons = []
        for attempt in range(30):
            sidebar_icons = driver.find_elements(By.XPATH, "//div[contains(@class, 'tooltip-target')]")
            if len(sidebar_icons) >= 3:
                break
            print(f"   ⏳ Waiting for sidebar... attempt {attempt+1} ({len(sidebar_icons)} icons found)")
            time.sleep(2)

        print(f"   Found {len(sidebar_icons)} sidebar icons")
        if len(sidebar_icons) < 3:
            raise Exception(f"Sidebar not loaded! Only found {len(sidebar_icons)} icons after 30 attempts")

        driver.execute_script("arguments[0].click();", sidebar_icons[2])
        print("   ✅ Clicked pie chart icon!")

        time.sleep(3)
        driver.save_screenshot(os.path.join(download_path, "step3_after_piechart.png"))

        # --- Step 4: Sales Report ---
        print("🔍 Step 4: Searching for Sales Report...")

        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type To Search']")))
        driver.execute_script("arguments[0].click();", search_box)
        time.sleep(1)
        search_box.send_keys("Sales Report")
        print("   ✅ Typed 'Sales Report'")

        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Sales Report']"))).click()
        print("   ✅ Clicked Sales Report!")

        time.sleep(5)
        driver.save_screenshot(os.path.join(download_path, "step4_salesreport_loaded.png"))

        # --- Step 5: Select Yesterday ---
        print("📅 Step 5: Selecting Yesterday date...")
        time.sleep(2)

        date_picker = wait.until(EC.element_to_be_clickable((By.ID, "billDate")))
        driver.execute_script("arguments[0].click();", date_picker)
        print("   ✅ Opened date picker!")

        time.sleep(2)

        yesterday_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Yesterday')]")))
        driver.execute_script("arguments[0].click();", yesterday_btn)
        print("   ✅ Selected Yesterday!")

        time.sleep(2)
        driver.save_screenshot(os.path.join(download_path, "step5_yesterday_selected.png"))

        # --- Step 6: Export ---
        print("📊 Step 6: Clicking Export to Excel...")
        time.sleep(3)

        export_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tableExportExcel")))
        driver.execute_script("arguments[0].click();", export_btn)
        print("   ✅ Clicked Export to Excel!")

        time.sleep(3)
        driver.save_screenshot(os.path.join(download_path, "step6_after_export.png"))

        # --- Step 7: Download Report ---
        print("📋 Step 7: Clicking Download Report button...")
        time.sleep(2)

        download_report_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download Report')]")))
        driver.execute_script("arguments[0].click();", download_report_btn)
        print("   ✅ Clicked Download Report!")

        time.sleep(3)
        driver.save_screenshot(os.path.join(download_path, "step7_after_download_report.png"))

        # --- Step 8: Data Export ---
        print("📤 Step 8: Clicking Data Export icon...")
        time.sleep(8)

        print(f"   Current URL: {driver.current_url}")
        data_export_btn = driver.find_element(By.ID, "headerDataExport")
        driver.execute_script("arguments[0].click();", data_export_btn)
        print("   ✅ Clicked Data Export!")

        time.sleep(5)
        driver.save_screenshot(os.path.join(download_path, "step8_after_data_export.png"))

        # ============================================================
        # 🔥 STEP 9 — FIRST DATA ROW (index 1), debugging added
        # ============================================================

        print("⬇️ Step 9: Finding Sales Report row in Data Export modal...")

        def close_modal_if_open():
            try:
                close_btn = driver.find_element(By.XPATH, "//button[contains(@class,'m-lft-10')]")
                driver.execute_script("arguments[0].click();", close_btn)
                print("   🔒 Closed modal")
                time.sleep(2)
            except:
                pass

        def reopen_modal():
            try:
                btn = driver.find_element(By.ID, "headerDataExport")
                driver.execute_script("arguments[0].click();", btn)
                print("   🔄 Reopened Data Export modal")
                time.sleep(8)
            except:
                pass

        def try_find_and_click_download():
            wait.until(EC.presence_of_element_located((By.ID, "list_component_main_li")))
            print("   ✅ Modal rows visible")

            all_rows = driver.find_elements(By.ID, "list_component_main_li")
            print(f"   Found {len(all_rows)} total rows")

            if not all_rows:
                print("   ❌ No rows found!")
                return False

            # 🔥 FIRST DATA ROW (skip header)
            row = all_rows[1] if len(all_rows) > 1 else all_rows[0]

            print(f"   Row 1 full text: '{row.text[:200]}'")

            all_elements = row.find_elements(By.XPATH, ".//*[normalize-space(text())]")
            for el in all_elements[:10]:
                print(f"     tag={el.tag_name} class='{el.get_attribute('class')[:40]}' text='{el.text[:50]}'")

            completed_labels = row.find_elements(
                By.XPATH, ".//*[normalize-space(text())='COMPLETED']"
            )

            if not completed_labels:
                print("   ⏭️ Row 1 — not COMPLETED yet")
                return False

            print("   ✅ Row 1 — COMPLETED!")

            download_btn = row.find_element(By.XPATH, ".//button[contains(@class,'rounded-[50%]')]")
            driver.execute_script("arguments[0].click();", download_btn)
            print("   ✅ Clicked download on row 1!")
            return True

        MAX_RETRIES = 3
        downloaded = False

        for attempt in range(1, MAX_RETRIES + 1):
            print(f"\n   🔁 Attempt {attempt}/{MAX_RETRIES}...")
            driver.save_screenshot(os.path.join(download_path, f"step9_attempt{attempt}.png"))

            downloaded = try_find_and_click_download()

            if downloaded:
                print(f"   ✅ Download triggered on attempt {attempt}!")
                break

            print("   ❌ Attempt failed, retrying...")
            time.sleep(15)
            close_modal_if_open()
            reopen_modal()

        if not downloaded:
            driver.save_screenshot(os.path.join(download_path, "step9_all_retries_failed.png"))
            raise Exception("❌ First DATA row not COMPLETED after 3 attempts!")

        # --- Step 10: Wait for file to download ---
        print("⏳ Step 10: Waiting for file to download...")
        time.sleep(12)
        driver.save_screenshot(os.path.join(download_path, "step10_after_download.png"))

        # --- Step 11: Locate downloaded file ---
        print("📂 Step 11: Getting downloaded file...")
        files = [
            f for f in os.listdir(download_path)
            if ("SALES" in f.upper() or "ENT" in f.upper())
            and "cleaned" not in f
            and (f.endswith(".xlsx") or f.endswith(".csv"))
        ]

        print(f"   Found {len(files)} Sales files:")
        for f in files:
            print(f"   - {f}")

        if not files:
            print("   ⚠️ No Sales file found, checking all downloads...")
            files = [
                f for f in os.listdir(download_path)
                if (f.endswith(".xlsx") or f.endswith(".csv"))
                and "cleaned" not in f
            ]

        if not files:
            raise Exception("No downloaded file found in output folder!")

        latest = max(files, key=lambda f: os.path.getctime(os.path.join(download_path, f)))

        print(f"   ✅ Downloaded: {latest}")
        return os.path.join(download_path, latest)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        driver.save_screenshot(os.path.join(download_path, "error_screenshot.png"))
        print("   📸 Error screenshot saved!")
        raise

    finally:
        driver.quit()
        print("🔒 Browser closed")


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting Sales Report Downloader")
    print("=" * 50)
    path = download_file()
    print("=" * 50)
    print(f"✅ Done! File saved at: {path}")
    print("=" * 50)