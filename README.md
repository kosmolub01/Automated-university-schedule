# Automated-university-schedule
Web app that makes checking the schedule at Silesian University of Technology easier. It replaces several clicks with just one. In order to view up-to-date schedule, user doesn't have to manually select group and current date. During the first usage, the user enters a group name and later that information is stored in cookies. To see schedule, only opening the webpage is required.

## Overview of the app

https://youtu.be/AsO_iFg4Bfc

## Screenshots
**Initial page** - here you provide group name:

![image](https://github.com/kosmolub01/Automated-university-schedule/assets/72302279/d813425d-69bb-4415-80e0-5ccdfd240b6f)

**Result for "INFKat IV/1" group** - this page will be shown to you with an up-to-date schedule for the group you provided every time you access the app. You can also change the group:

![image](https://github.com/kosmolub01/Automated-university-schedule/assets/72302279/3175848f-b2de-4889-a7c0-b1883b6c9589)

**Admin page login:**

![image](https://github.com/kosmolub01/Automated-university-schedule/assets/72302279/5dbfb0bd-d77b-4f2d-9aa5-6ab63c41a54d)

**Admin page** - here admin can run the script to update the schedules:

![image](https://github.com/kosmolub01/Automated-university-schedule/assets/72302279/fc1147e9-a415-488b-9187-f3195d31d174)

## Additional Information
Screenshots of schedules are taken by scraper script schedule_scraper.py. They are saved on the server. The logs of script execution are saved in SQLite DB.

The script is started by admin, by clicking "Update" button on admin page.

**Video of how the schedule_scraper.py works:**

https://youtu.be/iu4LDIGPQI8

## Technologies Used To Implement Core Features
- Django
- Selenium
- SQLite

## Project Status
Project is: _in progress_.

## TODO
- Finish admin page (setting automatic scraper runs)
