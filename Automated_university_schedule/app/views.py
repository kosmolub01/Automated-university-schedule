from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Run
from multiprocessing import Process
import os
import sqlite3
from time import sleep
from .schedule_scraper import *
from django.http import JsonResponse

# Schedule scraper input parameters.
screenshots_folder_path = "C:/Repos/Automated-university-schedule/Automated_university_schedule/app/static/app" 
webdriver_path = "C:/Users/s.dwornicki/Downloads/edgedriver_win64/msedgedriver.exe"
db_filename = "update_runs_history.db"

"""Starting page - if client has a cookie, use it and direct to the schedule page.
If there is no cookie, let the client enter the group name and direct to schedule page."""
def index(request):
    # Check cookies. If cookie with group name is detected, then show schedule of that group. 
    group_name = request.COOKIES.get('group_name')

    print("in index group_name: ", group_name)

    if group_name is None:
        # Cookie is not set - serve the starting page.
        context = {'file_does_not_exist': False,
                   'about_tab_visibility': False}
        return render(request, 'app/index.html', context)

    # Direct to schedule page.
    return redirect("app:view_schedule")

"""Show up-to-date schedule page."""
def view_schedule(request):
    # Retrive student's group from cookies. 
    group_name = request.COOKIES.get('group_name')

    response = HttpResponse()

    if group_name is None:
        # Cookie is not set - use the group name from the request.
        group_name = request.POST['group_name']

        print("group name", group_name)

        # Check whether file of a selected group exists.
        group_name = group_name.replace('/', '$')
        
        file_path = os.getcwd() + '\\app\static\\app\\' + group_name + '.png'

        print('file_path', file_path)

        # Check whether file with a schedule of given group exists. It may not 
        # exist because user provided wrong group name or because for some 
        # reason server does not have that file.
        if not os.path.exists(file_path):
            print("file_does_not_exist")
            context = {'file_does_not_exist': True}

            response.content = render(request, 'app/index.html', context)
 
            return response

        response.set_cookie('group_name', group_name)

    # Cookie is set.
    print("in view_schedule. group_name: ", group_name)

    # Create path to a file that contains screenshot of group's schedule.
    # It will be used in HTML.
    schedule_screenshot = 'app/' + group_name + ".png"

    group_name = group_name.replace('/', '$')
    file_path = os.getcwd() + '\\app\static\\app\\' + group_name + '.png'

    # Make sure file exists. If file does not exist, delete the cookie
    # and redirect to the main page (exacly the same action like for changing the group).
    if not os.path.exists(file_path):
        # Direct to change_group view.
        return redirect("app:change_group")

    context = {'schedule_screenshot': schedule_screenshot}

    response.content = render(request, 'app/schedule.html', context)
 
    return response

"""Handle changing the group. User presses 'Change group' button on schedule page, 
then cookie is deleted and user is redirected to starting page."""
def change_group(request):

    response = HttpResponse()

    # Delete cookie.
    response.delete_cookie('group_name')

    context = {'file_does_not_exist': False}

    response.content = render(request, 'app/index.html', context)
 
    return response

def login_page(request):
    response = HttpResponse()
    response.content = render(request, 'app/login.html')
    return response

def login_user(request):
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        # A backend authenticated the credentials.
        login(request, user)
        response = HttpResponse()
        response.content = render(request, 'app/admin.html')
        return response
    else:
        # No backend authenticated the credentials.
        response = HttpResponse(status=403)
        return response

def logout_user(request):
    response = HttpResponse(status=200)
    logout(request)
    return response

def update_the_schedules(request):
    response = HttpResponse(status=200)
    
    # Start process.
    schedule_scraper = ScheduleScraper(screenshots_folder_path, webdriver_path, db_filename)

    process = Process(target=schedule_scraper.scrap_the_schedules)
    process.start()

    # For the next 30 sec, every 5 sec check the number of updated screenshots.

    # Connect to the database.
    conn = sqlite3.connect(db_filename)

    # Create a cursor.
    cursor = conn.cursor()

    """sleep(1)

    for i in range(1, 6):
        # Execute the SELECT statement.
        cursor.execute("SELECT * FROM run ORDER BY id DESC LIMIT 1")

        # Fetch last row.
        row = cursor.fetchone()

        print(row)
            
        sleep(5)"""

    return response

def check_scraper_progress(request):

    print("checking progress")
    # Connect to the database.
    conn = sqlite3.connect(db_filename)

    # Create a cursor.
    cursor = conn.cursor()

    # Execute the SELECT statement.
    cursor.execute("SELECT updated_screenshots, last_status FROM run ORDER BY id DESC LIMIT 1")

    # Fetch  row.
    row = cursor.fetchone()
    updated_screenshots = row[0]
    last_status = row[1]

    response_data = {'updated_screenshots' : updated_screenshots, 'last_status' : last_status}
    return JsonResponse(response_data, status=200)             
