"""
===============================================================================

Filename: schedule_screenshots.py

Description:
For all groups that are avaiable on https://plan.polsl.pl/, ScheduleScraper 
object can find up-to-date schedule, takes screenshot and saves as a .png file 
in a given folder. Filename of a screenshot is the name of group 
(‘/’ replaced with ‘$’). Logs are saved in DB.

===============================================================================

"""
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from datetime import datetime, date
from selenium.webdriver.chrome.options import Options
import sys
import sqlite3

# Name of DB file.
db_file = "update_runs_history.db"

class DbSetUpException(Exception):
   def __init__(self):
      pass

   def __str__(self):
      message = "Schedule Scraper could not set up the DB."
      return message
   
class DbUpdateException(Exception):
   def __init__(self):
      pass

   def __str__(self):
      message = "Schedule Scraper could not update the DB."
      return message

class ScheduleScraper:
    """
    ScheduleScraper class.

    TBD:
    Attributes
    ----------
    name : str
        first name of the person

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """
    def __init__(self, screenshots_folder_path, webdriver_path):
        self.screenshots_folder_path = screenshots_folder_path
        self.webdriver_path = webdriver_path
        self._set_up_the_db()
    
    # In case there is no DB or table, it creates them.
    def _set_up_the_db(self):
        
        # Connect to the database.
        conn = sqlite3.connect(db_file)

        # Create a cursor.
        cursor = conn.cursor()

        # Create run table.
        sql_create_table = """ CREATE TABLE IF NOT EXISTS run (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        updated_screenshots integer,
                                        last_status text,
                                        start_time DATE,
                                        finish_time DATE
                                    ); """

        cursor.execute(sql_create_table)

        """sql_drop_table = " DROP TABLE run; "

        cursor.execute(sql_drop_table)"""

        # Close the cursor and the database connection.
        cursor.close()
        conn.close()

    def scrap_the_schedules(self):
        
        start = datetime.now()

        # Connect to the database.
        conn = sqlite3.connect(db_file)

        # Create a cursor.
        cursor = conn.cursor()

        sql_insert = """INSERT INTO run (start_time, last_status) VALUES (?, ?)"""
        cursor.execute(sql_insert, [start, 'Running'])

        # Setup webdriver
        try:       
            print("Setup webdriver")
            s = Service(webdriver_path)
            op = webdriver.EdgeOptions()

            op.add_argument('headless')

            driver = webdriver.Edge(service=s, options=op)
            driver.set_window_size(2160, 1280)
            driver.maximize_window()

            # Get the webpage
            try:
                print("Get the webpage")
                driver.get("https://plan.polsl.pl/")

                # Retrieve linked texts of all groups. Linked texts are going to be used to get to every group schedule.
                # Do the screenshot of the schedule. Save screenshot with a name of the group ('/' replaced with '$').
                try:
                    print("Retrieve linked texts of all groups")
                    driver.switch_to.frame("page_content")

                    # Uncheck "Teacher". 
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                        By.XPATH, "/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/input[2]")))
                    element.click()

                    # Click "Search". 
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                        By.XPATH, "/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr[3]/td/center/input")))
                    element.click()

                    # Get HTML content of the page.
                    html = driver.page_source

                    soup = BeautifulSoup(html, features="html.parser")

                    # Extract demanded part of the HTML content (link texts).
                    link_texts = soup.find("div", {"id": "result_plan"}).find_all("a")

                    # Needed for progress info.
                    group_no = 0
                    groups_quantity = len(link_texts)

                    for link_text in link_texts:

                        # Click the result link. 
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                            By.LINK_TEXT, link_text.string)))
                        element.click()

                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                            By.ID, "wBWeek")))
                        element = Select(element)

                        # Select current week.
                        current_day = date.today().day
                        current_month = date.today().month

                        weeks = element.options[1:]

                        for week in weeks:

                            if(int(week.text[3:5]) == current_month and int(week.text[0:2]) <= current_day and 
                            int(week.text[6:8]) >= current_day):
                                week.click()
                                break

                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                            By.ID, "wBButton")))
                        element.click()

                        # Do the screenshot.

                        # Retrive group name.
                        group = link_text.string

                        # Create filepath (folder path provided as a argument + '\' + 
                        # + group name retrived from the webpage ('/' replaced with '$') + '.png').
                        filepath = screenshots_folder_path + '\\' + group.replace('/', '$') + '.png'

                        # Do the screenshot.
                        driver.save_screenshot(filepath)

                        # Get back to page with all groups.
                        driver.get("https://plan.polsl.pl/")

                        driver.switch_to.frame("page_content")

                        # Uncheck "Teacher". 
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                            By.XPATH, "/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/input[2]")))
                        element.click()

                        # Click "Search". 
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                            By.XPATH, "/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table[2]/tbody/tr[3]/td/center/input")))
                        element.click()

                        sql_update_table = """UPDATE run SET updated_screenshots=? WHERE start_time=?"""
                        # Execute the update statement.
                        cursor.execute(sql_update_table, [group_no + 1, start])
                        print("DB write")

                        group_no = group_no + 1                    
                except:
                    print("Except - retrieve linked texts of all groups")
                    sql_update_table = """UPDATE run SET last_status=? WHERE start_time=?"""
                    # Execute the update statement.
                    cursor.execute(sql_update_table, ['Error - something went wrong when getting the screenshots', start])
            except:
                print("Except - Get the webpage")
                sql_update_table = """UPDATE run SET last_status=? WHERE start_time=?"""
                # Execute the update statement.
                cursor.execute(sql_update_table, ['Error - something went wrong when getting the schedule webpage', start])

            # Quit the driver instance.
            driver.quit()
        except:
            print("Except - Setup webdriver")
            sql_update_table = """UPDATE run SET last_status=? WHERE start_time=?"""
            # Execute the update statement.
            cursor.execute(sql_update_table, ['Error - something went wrong when setting up the webdriver', start])

        finally:
            print("Finally")
            finish = datetime.now()

            sql_update_table = """UPDATE run SET finish_time=? WHERE start_time=?"""
            # Execute the update statement.
            cursor.execute(sql_update_table, [finish, start])

            conn.commit()

            # Close the cursor and the database connection.
            cursor.close()
            conn.close()

if __name__ == "__main__":
    try:
        screenshots_folder_path = sys.argv[1]
        webdriver_path = sys.argv[2]

        scraper = ScheduleScraper(screenshots_folder_path, webdriver_path)
        scraper.scrap_the_schedules()

    except(IndexError):
        print("\nPlease, provide all parameters.\n\nschedule_screenshots.py <screenshots_folder_path> <webdriver_path>")
