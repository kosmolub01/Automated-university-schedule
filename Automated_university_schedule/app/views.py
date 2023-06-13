from django.http import HttpResponse
from django.shortcuts import render

#from .models import Chat

"""Starting page - if client has a cookie, use it and direct to the schedule page.
If there is no cookie, let the client enter the group name and direct to schedule page."""
def index(request):
    # Check cookies. If cookie with group name is detected, then show schedule of that group. 
    group_name = request.COOKIES.get('group_name')

    if group_name is None:
        # Cookie is not set - serve the starting page.
        return render(request, 'app/index.html')

    # Direct to schedule page.
    return render(request, 'chat/index.html', context)

def send(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        raise Http404("Chat does not exist")
    
    chat.message_set.create(message_text=request.POST['message'], author=request.POST['nick'])
    return HttpResponse(status=204)

"""Show up-to-date schedule for a group, that is retrived from cookies. """
def view_schedule(request, chat_id):
    # Retrive student's group from cookies. 
    group_name = request.COOKIES.get('group_name')
 
    # Put filepath in the context.
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        raise Http404("Chat does not exist")
    
    messages = chat.message_set.all()
    return render(request, 'chat/conversation.html', {'chat_id': chat_id, 'chat_title': chat.chat_title, 'messages': messages})

"""def send(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        raise Http404("Chat does not exist")
    
    chat.message_set.create(message_text=request.POST['message'], author=request.POST['nick'])
    return HttpResponse(status=204)

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