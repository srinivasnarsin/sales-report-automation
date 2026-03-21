from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import time

load_dotenv()

def download_file():

    print("🔧 Setting up Chrome...")
    options = webdriver.ChromeOptions()

    download_path = os.path.abspath("output")
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)

    # Uncomment when deploying to GitHub Actions
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 15)

    try:
        # --- Step 1: Open website ---
        print("🌐 Step 1: Opening website...")
        driver.get(os.getenv("SOURCE_URL"))
        time.sleep(3)
        print(f"   ✅ Page title: {driver.title}")

        # --- Step 2: Login ---
        print("🔐 Step 2: Logging in...")
        wait.until(EC.presence_of_element_located(
            (By.ID, "username")
        )).send_keys(os.getenv("SOURCE_USERNAME"))
        print("   ✅ Entered username")

        driver.find_element(
            By.ID, "passwordGenericInput"
        ).send_keys(os.getenv("SOURCE_PASSWORD"))
        print("   ✅ Entered password")

        driver.find_element(
            By.XPATH, "//button[contains(text(), 'Log In')]"
        ).click()
        print("   ✅ Clicked Log In")

        time.sleep(3)

        # --- Step 2b: Handle second login button ---
        try:
            log_me_in = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Log me In')]"
            )
            print("   🔄 Found 'Log me In' button, clicking...")
            log_me_in.click()
        except:
            print("   ℹ️ No 'Log me In' button, continuing...")

        time.sleep(5)
        driver.save_screenshot("output/step2_after_login.png")
        print("   ✅ Login done!")

        # --- Step 3: Click pie chart icon in sidebar ---
        print("📊 Step 3: Clicking pie chart icon...")
        time.sleep(3)

        sidebar_icons = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'tooltip-target')]"
        )
        print(f"   Found {len(sidebar_icons)} sidebar icons")
        driver.execute_script("arguments[0].click();", sidebar_icons[2])
        print("   ✅ Clicked pie chart!")

        time.sleep(3)
        driver.save_screenshot("output/step3_after_piechart.png")

        # --- Step 4: Search and click Sales Report ---
        print("🔍 Step 4: Searching for Sales Report...")

        search_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Type To Search']")
        ))
        driver.execute_script("arguments[0].click();", search_box)
        time.sleep(1)
        search_box.send_keys("Sales Report")
        print("   ✅ Typed 'Sales Report'")

        time.sleep(2)
        driver.save_screenshot("output/step4_after_search.png")

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//p[text()='Sales Report']")
        )).click()
        print("   ✅ Clicked Sales Report!")

        time.sleep(5)
        driver.save_screenshot("output/step4_salesreport_loaded.png")

        # --- Step 5: Select Yesterday date ---
        print("📅 Step 5: Selecting Yesterday date...")
        time.sleep(2)

        date_picker = wait.until(EC.element_to_be_clickable(
            (By.ID, "billDate")
        ))
        driver.execute_script("arguments[0].click();", date_picker)
        print("   ✅ Opened date picker!")

        time.sleep(2)
        driver.save_screenshot("output/step5_datepicker_open.png")

        yesterday_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Yesterday')]")
        ))
        driver.execute_script("arguments[0].click();", yesterday_btn)
        print("   ✅ Selected Yesterday!")

        time.sleep(2)
        driver.save_screenshot("output/step5_yesterday_selected.png")

# --- Step 6: Click Export to Excel (tableExportExcel) ---
        print("📊 Step 6: Clicking Export to Excel...")
        time.sleep(3)

        export_btn = wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "tableExportExcel")
        ))
        driver.execute_script("arguments[0].click();", export_btn)
        print("   ✅ Clicked Export to Excel!")

        time.sleep(3)
        driver.save_screenshot("output/step6_after_export_excel.png")

        # --- Step 7: Click Download Report button ---
        print("📋 Step 7: Clicking Download Report button...")
        time.sleep(2)

        download_report_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Download Report')]")
        ))
        driver.execute_script("arguments[0].click();", download_report_btn)
        print("   ✅ Clicked Download Report!")

        time.sleep(3)
        driver.save_screenshot("output/step7_after_download_report.png")

        # --- Step 8: Click Data Export icon ---
        print("📤 Step 8: Clicking Data Export icon...")
        time.sleep(2)

        data_export_btn = wait.until(EC.element_to_be_clickable(
            (By.ID, "headerDataExport")
        ))
        driver.execute_script("arguments[0].click();", data_export_btn)
        print("   ✅ Clicked Data Export!")

        time.sleep(3)
        driver.save_screenshot("output/step8_after_data_export.png")

# --- Step 9: Wait for table to load then click download arrow ---
        print("⬇️ Step 9: Clicking download arrow...")
        time.sleep(5)  # wait for table to fully load
        driver.save_screenshot("output/step9_modal_loaded.png")

        # Find all download arrow buttons in the modal and click the first one
        download_arrows = driver.find_elements(
            By.XPATH, "//button[.//path[contains(@class, 'tilcb-fill')]]"
        )
        print(f"   Found {len(download_arrows)} download arrows")

        if not download_arrows:
            # Try alternative - find by the SVG fill color
            download_arrows = driver.find_elements(
                By.XPATH, "//button[contains(@class, 'rounded-[50%]')]"
            )
            print(f"   Found {len(download_arrows)} round buttons")

        if not download_arrows:
            driver.save_screenshot("output/error_no_arrow.png")
            raise Exception("No download arrow found!")

        driver.execute_script("arguments[0].click();", download_arrows[0])
        print("   ✅ Clicked download arrow!")

        # --- Step 10: Wait for download ---
        print("⏳ Step 10: Waiting for file to download...")
        time.sleep(5)
        driver.save_screenshot("output/step10_after_download.png")

        # --- Step 11: Get downloaded file ---
        print("📂 Step 11: Getting downloaded file...")
        files = [f for f in os.listdir(download_path) if f.endswith(".xlsx")]
        if not files:
            files = [f for f in os.listdir(download_path) if f.endswith(".csv")]
        
        print(f"   Found {len(files)} files:")
        for f in files:
            print(f"   - {f}")

        if not files:
            raise Exception("No downloaded file found in output folder!")

        latest = max(files, key=lambda f: os.path.getctime(
            os.path.join(download_path, f)
        ))

        print(f"   ✅ Downloaded: {latest}")
        return os.path.join(download_path, latest)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        driver.save_screenshot("output/error_screenshot.png")
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