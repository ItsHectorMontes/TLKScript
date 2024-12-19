import requests
from bs4 import BeautifulSoup
import time
import webbrowser

class PageFetcher:
    """
    Responsible for fetching the content of a given URL and returning the HTML.
    """
    def __init__(self, url):
        self.url = url

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None


class ButtonChecker:
    """
    Responsible for parsing the HTML to determine if a specific button is active,
    and returning the appropriate link if found.
    """
    def __init__(self, target_button_text, inactive_class):
        self.target_button_text = target_button_text.upper()
        self.inactive_class = inactive_class

    def check_button(self, html_content):
        if not html_content:
            return None
        soup = BeautifulSoup(html_content, "html.parser")
        buttons = soup.find_all("a")

        for button in buttons:
            if button.text.strip().upper() == self.target_button_text:
                button_classes = button.get("class", [])
                link = button.get("href")

                # Check that the button does NOT have the 'inactive_class'
                if self.inactive_class not in button_classes:
                    return self._build_full_link(link)
        return None

    def _build_full_link(self, link):
        # Construct the full URL if needed
        if link and link.startswith("/"):
            return f"https://teleticket.com.pe{link}"
        return link


class LinkOpener:
    """
    Responsible for opening a given link in the default web browser.
    """
    def open_link(self, link):
        if link:
            print(f"Opening link: {link}")
            webbrowser.open(link)
        else:
            print("No valid link to open.")


class ButtonMonitor:
    """
    Orchestrates the process of monitoring the target button until it is active.
    Uses PageFetcher to get HTML, ButtonChecker to detect the button, 
    and LinkOpener to open the link.
    """
    def __init__(self, url, target_button_text, inactive_class, interval=10):
        self.page_fetcher = PageFetcher(url)
        self.button_checker = ButtonChecker(target_button_text, inactive_class)
        self.link_opener = LinkOpener()
        self.interval = interval

    def start_monitoring(self):
        print(f"Starting to monitor the '{self.button_checker.target_button_text}' button...")
        while True:
            html = self.page_fetcher.fetch_html()
            if html is None:
                print("Could not fetch HTML. Will try again.")
                time.sleep(self.interval)
                continue

            link = self.button_checker.check_button(html)
            if link:
                print(f"The '{self.button_checker.target_button_text}' button is active!")
                self.link_opener.open_link(link)
                break
            else:
                print(f"'{self.button_checker.target_button_text}' button is still inactive. Checking again...")
                time.sleep(self.interval)


# Usage
if __name__ == "__main__":
    # Adjust parameters if needed
    URL = "https://teleticket.com.pe/system-of-a-down-lima-2025"
    TARGET_BUTTON_TEXT = "PREVENTA FANS"
    INACTIVE_CLASS = "btn_inactive"
    INTERVAL_SECONDS = 10

    monitor = ButtonMonitor(url=URL, target_button_text=TARGET_BUTTON_TEXT, 
                            inactive_class=INACTIVE_CLASS, interval=INTERVAL_SECONDS)
    monitor.start_monitoring()
