"""
===============================================================================

Filename: schedule_screenshots.py

Description:
For all groups that are avaiable on https://plan.polsl.pl/, script finds 
up-to-date schedule, takes screenshot and saves as a .png file in a given 
folder. File name is the name of group (‘/’ replaced with ‘$’).

Input parameters:
    - folder path to save screenshots
    - location with up-to-date browser driver

Output:
    - info. about start and finish time, program progress
    - 0 - successful completion
    - error info. string - error

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
import sys

# Debug purposes
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":

    start = datetime.now()

    print('\nStart time:', start)

    # Setup webdriver
    try:       
        s = Service(sys.argv[2])
        op = webdriver.EdgeOptions()

        op.add_argument('headless')

        driver = webdriver.Edge(service=s, options=op)
        driver.set_window_size(2160, 1280)
        driver.maximize_window()

        # Get the webpage
        try:
            driver.get("https://plan.polsl.pl/")

            # Retrieve linked texts of all groups. Linked texts are going to be used to get to every group schedule.
            # Do the screenshot of the schedule. Save screenshot with a name of the group ('/' replaced with '$').
            try:
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

                    # Print progress info.
                    print("Group no.", group_no, "of", groups_quantity)

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
                    filepath = sys.argv[1] + '\\' + group.replace('/', '$') + '.png'

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

                    group_no = group_no + 1

                print(0)                     
            except:
                print("Something went wrong when getting the screenshots.")  
        except:
            print("Something went wrong when getting the schedule webpage.")

        # Quit the driver instance.
        driver.quit()
    except:
        print("Something went wrong when setting up the webdriver.")

finish = datetime.now()

print('Finish time:', finish)

duration = finish - start

print('Duration:', duration)
                    