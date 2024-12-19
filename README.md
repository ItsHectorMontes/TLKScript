# Button Monitor Script

This Python script automates the process of monitoring a specific button on a webpage. It fetches the webpage content, checks if the target button is active, and opens the link in the default web browser if the button becomes active. The script demonstrates adherence to GRASP principles, making it modular, maintainable, and cohesive.

---

## Features

- Monitors a specific button on a webpage by its text.
- Checks if the button is active or inactive based on its CSS class.
- Automatically opens the associated link in the browser when the button is active.
- Includes robust error handling for network requests.
- Highly modular design using GRASP principles:
  - **Information Expert**: Assigns responsibilities to classes with the relevant information.
  - **Controller**: Orchestrates the workflow using separate components.
  - **High Cohesion & Low Coupling**: Ensures each class has a single, well-defined responsibility.
  - **Creator**: Manages object creation within the appropriate context.

---

## Dependencies

The script requires the following Python libraries:

- `requests`: For fetching webpage content.
- `beautifulsoup4`: For parsing HTML content.
- `time`: For periodic monitoring.
- `webbrowser`: For opening links in the default browser.

Install dependencies using pip:

```bash
pip install requests beautifulsoup4
```

---

## How It Works

1. **PageContentProvider**
   - Fetches the HTML content of the given webpage.
   - Handles network errors gracefully.

2. **ButtonChecker**
   - Parses the HTML to find the target button by its text.
   - Checks if the button is active based on the presence or absence of a specific CSS class.
   - Returns the full URL if the button is active.

3. **BrowserOpener**
   - Opens the link in the default web browser if the button is active.

4. **ButtonMonitor**
   - Orchestrates the process by periodically fetching the page, checking the button, and opening the link when active.

---

## Usage

### Example Scenario

Monitor the "PREVENTA INTERBANK" button on the [Teleticket website](https://teleticket.com.pe) for the "System of a Down Lima 2025" event.

### Steps:

1. Update the following variables in the script:
   - `URL`: The webpage to monitor.
   - `TARGET_BUTTON_TEXT`: The text of the button to monitor.
   - `INACTIVE_CLASS`: The CSS class indicating the button is inactive.
   - `INTERVAL_SECONDS`: The interval (in seconds) between checks.

Example:

```python
URL = "https://teleticket.com.pe/system-of-a-down-lima-2025"
TARGET_BUTTON_TEXT = "PREVENTA INTERBANK"
INACTIVE_CLASS = "btn_inactive"
INTERVAL_SECONDS = 10
```

2. Run the script:

```bash
python script_name.py
```

3. The script will:
   - Continuously fetch the page and check the button's status.
   - Print updates to the console about the button's status.
   - Open the button's link in the default browser once it becomes active.

---

## Example Output

```
Starting to monitor the 'PREVENTA INTERBANK' button...
'PREVENTA INTERBANK' button is still inactive. Checking again...
'PREVENTA INTERBANK' button is still inactive. Checking again...
The 'PREVENTA INTERBANK' button is active!
Opening link: https://teleticket.com.pe/system-of-a-down-lima-2025/preventa
```

---

## Customization

You can customize the script for different use cases by modifying the following:

- **URL**: Point to a different webpage.
- **TARGET_BUTTON_TEXT**: Set the text of the button you want to monitor.
- **INACTIVE_CLASS**: Update the CSS class that indicates the button is inactive.
- **INTERVAL_SECONDS**: Adjust the frequency of checks.

---

## Limitations

- The script assumes the button is an `<a>` tag. If the button uses a different tag, minor adjustments to the `ButtonChecker` class may be required.
- Ensure the webpage structure remains consistent for the script to work reliably.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.
