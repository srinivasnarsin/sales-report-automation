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

    # ✅ GitHub Actions needs headless — locally you can comment these 4 lines out
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 30)

    # Today's date formatted exactly as the modal shows it: "27 Mar 2026"
    # %-d gives day without leading zero (Linux/Mac). On Windows use %#d
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

        try:
            log_me_in = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Log me In')]"
            )
            print("   🔄 Found 'Log me In' button, clicking...")
            log_me_in.click()
            print("   ✅ Clicked Log me In")
        except:
            print("   ℹ️ No 'Log me In' button, continuing...")

        time.sleep(5)
        driver.save_screenshot(os.path.join(download_path, "step2_after_login.png"))
        print("   ✅ Login done!")

        # --- Step 3: Click pie chart icon in sidebar ---
        print("📊 Step 3: Clicking pie chart icon...")
        time.sleep(8)

        sidebar_icons = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'tooltip-target')]"
        )
        print(f"   Found {len(sidebar_icons)} sidebar icons")
        driver.execute_script("arguments[0].click();", sidebar_icons[2])
        print("   ✅ Clicked pie chart icon!")

        time.sleep(3)
        driver.save_screenshot(os.path.join(download_path, "step3_after_piechart.png"))

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

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//p[text()='Sales Report']")
        )).click()
        print("   ✅ Clicked Sales Report!")

        time.sleep(5)
        driver.save_screenshot(os.path.join(download_path, "step4_salesreport_loaded.png"))

        # --- Step 5: Select Yesterday date ---
        print("📅 Step 5: Selecting Yesterday date...")
        time.sleep(2)

        date_picker = wait.until(EC.element_to_be_clickable(
            (By.ID, "billDate")
        ))
        driver.execute_script("arguments[0].click();", date_picker)
        print("   ✅ Opened date picker!")

        time.sleep(2)

        yesterday_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Yesterday')]")
        ))
        driver.execute_script("arguments[0].click();", yesterday_btn)
        print("   ✅ Selected Yesterday!")

        time.sleep(2)
        driver.save_screenshot(os.path.join(download_path, "step5_yesterday_selected.png"))

        # --- Step 6: Click Export to Excel ---
        print("📊 Step 6: Clicking Export to Excel...")
        time.sleep(3)

        export_btn = wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "tableExportExcel")
        ))
        driver.execute_script("arguments[0].click();", export_btn)
        print("   ✅ Clicked Export to Excel!")

        time.sleep(3)
        driver.save_screenshot(os.path.join(download_path, "step6_after_export.png"))

        # --- Step 7: Click Download Report button ---
        print("📋 Step 7: Clicking Download Report button...")
        time.sleep(2)

        download_report_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Download Report')]")
        ))
        driver.execute_script("arguments[0].click();", download_report_btn)
        print("   ✅ Clicked Download Report!")

        time.sleep(3)
        driver.save_screenshot(os.path.join(download_path, "step7_after_download_report.png"))

        # --- Step 8: Click Data Export icon ---
        print("📤 Step 8: Clicking Data Export icon...")
        time.sleep(8)

        print(f"   Current URL: {driver.current_url}")
        data_export_btn = driver.find_element(By.ID, "headerDataExport")
        driver.execute_script("arguments[0].click();", data_export_btn)
        print("   ✅ Clicked Data Export!")

        time.sleep(5)
        driver.save_screenshot(os.path.join(download_path, "step8_after_data_export.png"))

        # -----------------------------------------------------------------------
        # Step 9: Find correct row and download
        #
        # Row = <li id="list_component_main_li">
        # Must pass ALL 5 checks:
        #   1. <span class="mdlr-multiple-row">Sales Report</span>
        #   2. <button data-interactive="true"> contains "Filtered"
        #   3. <label class="vsos-approved">COMPLETED</label>
        #   4. Created On span contains today's date  e.g. "27 Mar 2026"
        #   5. Generated On span contains today's date
        # Then click: <button class="p-[7px] rounded-[50%]...">
        # Close btn:  <button class="m-lft-10">
        # -----------------------------------------------------------------------
        print("⬇️ Step 9: Finding Sales Report row in Data Export modal...")

        def close_modal_if_open():
            try:
                close_btn = driver.find_element(
                    By.XPATH, "//button[contains(@class,'m-lft-10')]"
                )
                driver.execute_script("arguments[0].click();", close_btn)
                print("   🔒 Closed modal")
                time.sleep(2)
            except Exception as e:
                print(f"   ⚠️ Could not close modal: {e}")

        def reopen_modal():
            try:
                btn = driver.find_element(By.ID, "headerDataExport")
                driver.execute_script("arguments[0].click();", btn)
                print("   🔄 Reopened Data Export modal")
                time.sleep(8)
            except Exception as e:
                print(f"   ⚠️ Could not reopen modal: {e}")

        def try_find_and_click_download():
            wait.until(EC.presence_of_element_located(
                (By.ID, "list_component_main_li")
            ))
            print("   ✅ Modal rows visible")

            all_rows = driver.find_elements(By.ID, "list_component_main_li")
            print(f"   Found {len(all_rows)} total rows")

            for i, row in enumerate(all_rows):
                try:
                    # ✅ Check 1: Sales Report span
                    sales_spans = row.find_elements(
                        By.XPATH,
                        ".//span[contains(@class,'mdlr-multiple-row') and normalize-space(text())='Sales Report']"
                    )
                    if not sales_spans:
                        continue

                    # ✅ Check 2: Filtered button
                    filtered_btns = row.find_elements(
                        By.XPATH, ".//button[@data-interactive='true']"
                    )
                    has_filtered = any("Filtered" in btn.text for btn in filtered_btns)
                    if not has_filtered:
                        print(f"   ⏭️  Row {i} — no Filtered button")
                        continue

                    # ✅ Check 3: COMPLETED label
                    completed_labels = row.find_elements(
                        By.XPATH,
                        ".//label[contains(@class,'vsos-approved') and normalize-space(text())='COMPLETED']"
                    )
                    if not completed_labels:
                        print(f"   ⏭️  Row {i} — not COMPLETED")
                        continue

                    # ✅ Check 4 & 5: Created On AND Generated On must be today
                    # Row layout (mdlr-col divs in order):
                    #   col 0 → File Type  (has the Sales Report span + Filtered btn)
                    #   col 1 → File Name  (long UUID span)
                    #   col 2 → Created On
                    #   col 3 → Generated On
                    #   col 4 → Status
                    #   col 5 → Download button
                    cols = row.find_elements(
                        By.XPATH, ".//div[contains(@class,'mdlr-col')]"
                    )

                    created_on   = cols[2].text.strip() if len(cols) > 2 else ""
                    generated_on = cols[3].text.strip() if len(cols) > 3 else ""
                    print(f"   Row {i} → Created: '{created_on}' | Generated: '{generated_on}'")

                    if today_str not in created_on:
                        print(f"   ⏭️  Row {i} — Created On doesn't match today")
                        continue
                    if today_str not in generated_on:
                        print(f"   ⏭️  Row {i} — Generated On doesn't match today")
                        continue

                    print(f"   ✅ Row {i} — ALL 5 checks passed!")

                    # ✅ Click the download arrow button
                    download_btn = row.find_element(
                        By.XPATH, ".//button[contains(@class,'rounded-[50%]')]"
                    )
                    driver.execute_script("arguments[0].click();", download_btn)
                    print(f"   ✅ Clicked download on row {i}!")
                    return True

                except Exception as row_err:
                    print(f"   Row {i} error: {row_err}")
                    continue

            print("   ❌ No matching row found in this attempt")
            return False

        # ── Retry loop: up to 3 attempts ────────────────────────────────────────
        MAX_RETRIES = 3
        downloaded = False

        for attempt in range(1, MAX_RETRIES + 1):
            print(f"\n   🔁 Attempt {attempt}/{MAX_RETRIES}...")
            driver.save_screenshot(os.path.join(download_path, f"step9_attempt{attempt}.png"))

            downloaded = try_find_and_click_download()

            if downloaded:
                print(f"   ✅ Download triggered on attempt {attempt}!")
                break
            else:
                print(f"   ❌ Attempt {attempt} failed")
                if attempt < MAX_RETRIES:
                    print("   ⏳ Waiting 15 seconds, closing and reopening modal...")
                    time.sleep(15)
                    close_modal_if_open()
                    reopen_modal()

        if not downloaded:
            driver.save_screenshot(os.path.join(download_path, "step9_all_retries_failed.png"))
            raise Exception(
                f"❌ No Sales Report row matched (Filtered + COMPLETED + Created/Generated = '{today_str}') after 3 attempts"
            )

        # --- Step 10: Wait for download ---
        print("⏳ Step 10: Waiting for file to download...")
        time.sleep(12)
        driver.save_screenshot(os.path.join(download_path, "step10_after_download.png"))

        # --- Step 11: Get downloaded file ---
        print("📂 Step 11: Getting downloaded file...")
        files = [f for f in os.listdir(download_path)
                 if ("SALES" in f.upper() or "ENT" in f.upper())
                 and "cleaned" not in f
                 and (f.endswith(".xlsx") or f.endswith(".csv"))]

        print(f"   Found {len(files)} Sales files:")
        for f in files:
            print(f"   - {f}")

        if not files:
            print("   ⚠️ No Sales file found, using latest file...")
            files = [f for f in os.listdir(download_path)
                     if (f.endswith(".xlsx") or f.endswith(".csv"))
                     and "cleaned" not in f]

        if not files:
            raise Exception("No downloaded file found in output folder!")

        latest = max(files, key=lambda f: os.path.getctime(
            os.path.join(download_path, f)
        ))

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