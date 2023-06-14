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

"""Handle entering group name on starting page. Save group name in the cookie."""
"""def enter_group(request):
    
    group_name = request.POST['group_name']

    print("req:", group_name)

    # Set the cookie value. Pass it to somehow to view_schedule when you will destingush how you get to view_schedule
    response = HttpResponse('anything')
    response.set_cookie('group_name', group_name)

    view_schedule(request, group_name)

    return HttpResponse("OK")"""

"""def set_cookie(request):
    # Set the cookie value. Pass it to somehow to view_schedule when you will destingush how you get to view_schedule
    response = HttpResponse('anything')
    response.set_cookie('group_name', request.POST['group_name'])
    return response"""

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

        if not os.path.exists(file_path):
            print("file_does_not_exist")
            context = {'file_does_not_exist': True}
            #messages.add_message(request, messages.WARNING, 'Group not found.')
            response.content = render(request, 'app/index.html', context)
 
            return response

        response.set_cookie('group_name', group_name)


    print("in view_schedule. group_name: ", group_name)

    # Create name of a file that contains screenshot of group's schedule.
    schedule_screenshot = 'app/' + group_name + ".png"

    #schedule_screenshot = "C:\Repos\Automated-university-schedule\Automated_university_schedule\\app\schedules\\test.png"

    context = {'schedule_screenshot': schedule_screenshot}

    response.content = render(request, 'app/schedule.html', context)
 
    return response

"""Return image of up-to-date schedule for a group, that is retrived from cookies.
def image(request):
    # Retrive student's group from cookies. 
    group_name = request.COOKIES.get('group_name')
 
    # Create path to a file that contains screenshot of group's schedule.
    schedule_screenshot_path = "\schedules\\" + group_name + ".png"
    
    # Open the image file in binary mode
    with open(schedule_screenshot_path, 'rb') as f:
        image_data = f.read()
    
    # Set the appropriate MIME type for the image
    response = HttpResponse(content_type='image/jpeg')
    
    # Set the content of the response to the image data
    response.write(image_data)
    
    return response"""

"""Handle changing the group. User presses 'Change group' button on schedule page, 
then cookie is deleted and user is redirected to starting page."""
def change_group(request):

    response = HttpResponse()

    # Delete cookie.
    response.delete_cookie('group_name')

    context = {'file_does_not_exist': False}

    response.content = render(request, 'app/index.html', context)
 
    return response

"""
def last_message_id(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        raise Http404("Chat does not exist")
            
    return HttpResponse(chat.message_set.count())

def messages(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        raise Http404("Chat does not exist")
    
    messages = chat.message_set.all()
    messages_html = "<br>"

    for message in reversed(messages):
        messages_html += message.__str__() + "<br>"

    return HttpResponse(messages_html)"""