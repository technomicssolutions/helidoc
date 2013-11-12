from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover() 

urlpatterns = patterns('',
    # Example:

    (r'^findfreeseats/$','helidocs.diary.views.findfreeseats'),
    (r'^findfreeseats/(.*)','helidocs.diary.views.findfreeseats'),

    (r'^get_voucher/','helidocs.diary.views.get_voucher'),
    (r'^get_student/','helidocs.diary.views.get_student'),
    (r'^get_voucher_contacts/(.*)','helidocs.diary.views.get_voucher_contacts'),
    (r'^get_student_contacts/(.*)','helidocs.diary.views.get_student_contacts'),
    (r'^calendar/$','helidocs.diary.views.calendar'),
    (r'^calendar/(.*)','helidocs.diary.views.calendar'),
    (r'^calendaradd/(.*)','helidocs.diary.views.calendaradd'),
    (r'^grouponadd/(.*)','helidocs.diary.views.grouponadd'),
    (r'^calendaredit/(?P<pID>\d+)/$','helidocs.diary.views.calendaredit'),
    (r'^daytoview/$','helidocs.diary.views.daytoview'),
    (r'^daytoview/(.*)','helidocs.diary.views.daytoview'),
    (r'^setcomplete/(.*)','helidocs.diary.views.SetComplete'),

    (r'^grouponbookin/$','helidocs.diary.views.grouponbookin'),
    (r'^grouponbookin/(.*)','helidocs.diary.views.grouponbookin'),
    (r'^home/','helidocs.diary.views.homepage'),
    (r'^$','helidocs.diary.views.homepage'),


    (r'^static/admin/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/home/technomics/venvs/helidocs/lib/python2.7/site-packages/django/contrib/admin/static/admin'}),
    (r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/home/technomics/venvs/helidocs/helidocs/static'}),
    # (r'^helidocs/', include('helidocs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
#    (r'^accounts/', include('registration.urls')),
)
