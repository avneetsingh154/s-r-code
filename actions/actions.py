from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import selenium.webdriver as webdriver
from time import sleep

class ActionPerformWebAutomation(Action):
    def name(self) -> Text:
        return "action_perform_web_automation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/120.0.0.0'
        driver_path = r"C:\Users\offic\OneDrive\Desktop\msedgedriver.exe"
        edge_service = EdgeService(driver_path)
        edge_options = EdgeOptions()

        # If you don't want to showcase the automation on the webpage
        edge_options.add_argument('--headless')

        edge_options.add_argument(f'user-agent={user_agent}')

        url = "https://bhuvan-app3.nrsc.gov.in/aadhaar/"

        # Create an Edge WebDriver instance with specified options
        browser = webdriver.Edge(service=edge_service, options=edge_options)

        try:
            search_query = 'Chandigarh'
            # Open the URL in the browser
            browser.get(url)

            # Wait for the search field to be present
            search_field = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.ID, "Val"))
            )

            # Clear the search field (optional, depending on your use case)
            search_field.clear()

            # Enter the search query into the search field
            search_field.send_keys(search_query)

            # Wait for the table to update (you may adjust the wait time)
            sleep(2)

            # Assuming the table has an ID, locate the table element
            table_element = WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.ID, "ga"))
            )

            # Extract information from the table (adjust based on your table structure)
            rows = table_element.find_elements(By.TAG_NAME, "tr")

            # Extract row data and respond back to the user
            table_data = []
            for i, row in enumerate(rows, start=1):
                columns = row.find_elements(By.TAG_NAME, "td")
                row_data = [column.text for column in columns]
                formatted_row = f"{i}. {', '.join(row_data)}"
                table_data.append(formatted_row)

            # Send the formatted list as a response to the user
            dispatcher.utter_message(text="\n".join(table_data))



        finally:
            browser.quit()

        return []
