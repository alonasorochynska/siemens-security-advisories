import os
from urllib.parse import urljoin
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import json

BASE_URL = "https://www.siemens.com"
REPORT_URL = urljoin(BASE_URL, "global/en/products/services/cert.html#SiemensSecurityAdvisories")

current_dir = os.path.dirname(os.path.abspath(__file__))


def get_json_links(soup: BeautifulSoup) -> set:
    json_links = set()
    report_elements = soup.select("tr")
    for element in report_elements:
        json_anchor = element.select_one("a.sups-download.sups-scaf")
        if json_anchor:
            json_links.add(json_anchor["href"])
    return json_links


def save_links(links: set) -> None:
    with open(os.path.join(current_dir, "data", "json_links.txt"), "w") as file:
        for link in links:
            file.write(f"{link}\n")


def collect_and_save_json_data(json_links: set) -> None:
    all_data = []
    for link in json_links:
        response = requests.get(link)
        json_data = response.json()
        json_data["document"]["source_url"] = link
        all_data.append(json_data)

    with open(os.path.join(current_dir, "data", "siemens_reports.json"), "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)


def click_next_button(driver) -> bool:
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)
        return True
    except NoSuchElementException:
        print("Increase time sleep and try again")
        return False


def main():
    driver = webdriver.Chrome()
    driver.get(REPORT_URL)
    time.sleep(3)
    json_links = set()
    click_count = 0

    while click_count < 3:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        json_links.update(get_json_links(soup))

        if not click_next_button(driver):
            break
        click_count += 1

    save_links(json_links)
    collect_and_save_json_data(json_links)

    driver.quit()


if __name__ == "__main__":
    main()
