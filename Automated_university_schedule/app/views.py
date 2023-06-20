from django.http import HttpResponse
from django.shortcuts import render, redirect
import os

"""Starting page - if client has a cookie, use it and direct to the schedule page.
If there is no cookie, let the client enter the group name and direct to schedule page."""
def index(request):
    # Check cookies. If cookie with group name is detected, then show schedule of that group. 
    group_name = request.COOKIES.get('group_name')

    print("in index group_name: ", group_name)

    if group_name is None:
        # Cookie is not set - serve the starting page.
        context = {'file_does_not_exist': False}
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
