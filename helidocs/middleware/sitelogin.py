from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
class SiteLogin:
    #"This middleware requires a login for every view"
    def process_request(self, request):
        if request.path != '/django.fcgi/loginuser/' and request.path != '/loginuser/' and request.path!='/loadfile/' and request.path.find('/AViczT3bgmiJqNWx/')==-1 \
            and request.path.find('/logbook/')==-1 and request.path.find('/fuelentry/')==-1 and request.path.find('/whoami/')==-1 and request.path.find('/setwhoiam/')==-1 and request.path.find('/timesheet/')==-1 \
            and request.path.find('/getcurrentweathercharts/')==-1 and request.user.is_anonymous():
            if request.POST:
                return login(request)
            else:
                return HttpResponseRedirect('/loginuser/?next=%s' % request.path)