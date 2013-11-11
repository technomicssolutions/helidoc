"""This middleware takes the session identifier in a POST message and adds it to the cookies instead.

This is necessary because SWFUpload won't send proper cookies back; instead, all the cookies are
added to the form that gets POST-ed back to us.
"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sessions.backends.db import SessionStore

class SWFUploadMiddleware(object):
    def process_request(self, request):
        #print "in"+request.path+"   "+reverse('helidocs.techlogs.views.loadfile')
        if (request.method == 'POST') and (request.path == reverse('helidocs.techlogs.views.loadfile')) :
        #      print request.POST
            if request.POST.has_key(settings.SESSION_COOKIE_NAME):
                request.COOKIES[settings.SESSION_COOKIE_NAME] = request.POST[settings.SESSION_COOKIE_NAME]
                s = SessionStore(session_key=settings.SESSION_COOKIE_NAME)
                print "got sessionid:"+ request.POST[settings.SESSION_COOKIE_NAME]
            if request.POST.has_key('csrftoken'):
                request.COOKIES['csrftoken'] = request.POST['csrftoken']
                print "got token:"+ request.POST['csrftoken']
            if request.POST.has_key('editid'):
                request.COOKIES['editid'] = request.POST['editid']
                print "got token:"+ request.POST['editid']
            if request.POST.has_key('data'):
                request.COOKIES['data'] = request.POST['data']
                print "got data:"+ request.POST['data']
        #print "got out of middleware"

