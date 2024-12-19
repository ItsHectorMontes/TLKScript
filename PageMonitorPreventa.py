import requests
from bs4 import BeautifulSoup
import time
import webbrowser

# GRASP Principles Used:
# - Information Expert: Assign responsibilities to the class that has the necessary information.
# - Controller: Create a class that coordinates and controls the flow.
# - High Cohesion & Low Coupling: Each class focuses on a single, well-defined purpose.
# - Creator: Objects that contain or closely use other objects are responsible for their creation.

class PageContentProvider:
    """
    (Information Expert)
    Responsible for fetching the page content from a given URL.
    It knows how to retrieve the HTML and handle errors.
    """
    def __init__(self, url):
        self.url = url

    def get_html(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None


class ButtonChecker:
    """
    (Information Expert)
    Responsible for parsing the HTML content and determining if a specific button is active.
    Returns the link if the button is active; otherwise, returns None.
    """
    def __init__(self, target_button_text, inactive_class):
        self.target_button_text = target_button_text.upper()
        self.inactive_class = inactive_class

    def find_button_link(self, html_content):
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, "html.parser")
        buttons = soup.find_all("a")

        for button in buttons:
            if button.text.strip().upper() == self.target_button_text:
                button_classes = button.get("class", [])
                link = button.get("href")

                if self.inactive_class not in button_classes:
                    return self._build_full_link(link)
        return None

    def _build_full_link(self, link):
        if link and link.startswith("/"):
            return f"https://teleticket.com.pe{link}"
        return link


class BrowserOpener:
    """
    (Information Expert)
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
    (Controller)
    Orchestrates the monitoring process using the other classes.
    It controls the flow: fetch HTML, check button, and open link if active.
    """
    def __init__(self, url, target_button_text, inactive_class, interval=10):
        self.page_content_provider = PageContentProvider(url)
        self.button_checker = ButtonChecker(target_button_text, inactive_class)
        self.browser_opener = BrowserOpener()
        self.interval = interval

    def start_monitoring(self):
        print(f"Starting to monitor the '{self.button_checker.target_button_text}' button...")
        while True:
            html = self.page_content_provider.get_html()
            if html is None:
                print("Could not get HTML. Retrying...")
                time.sleep(self.interval)
                continue

            link = self.button_checker.find_button_link(html)
            if link:
                print(f"The '{self.button_checker.target_button_text}' button is active!")
                self.browser_opener.open_link(link)
                break
            else:
                print(f"'{self.button_checker.target_button_text}' button is still inactive. Checking again...")
                time.sleep(self.interval)


# Usage example
if __name__ == "__main__":
    URL = "https://teleticket.com.pe/system-of-a-down-lima-2025"
    TARGET_BUTTON_TEXT = "PREVENTA INTERBANK"
    INACTIVE_CLASS = "btn_inactive"
    INTERVAL_SECONDS = 10

    monitor = ButtonMonitor(
        url=URL,
        target_button_text=TARGET_BUTTON_TEXT,
        inactive_class=INACTIVE_CLASS,
        interval=INTERVAL_SECONDS
    )
    monitor.start_monitoring()
