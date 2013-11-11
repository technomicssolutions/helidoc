__author__ = 'bhj'
from django import forms
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe
import datetime
from helidocs.widgets.ukdate import ukdate,ukdatetime

#custom widget for airport code

class AirInWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        if value==None: value=""
        elif type(value)!=type(u'unicode'):
            value=value.strftime('%H:%M %d/%m/%Y')
#        if value[4]=="-":
#            value="%s:%s %s/%s/%s"%(value[12:14],value[15:17],value[9:11],value[6:8],value[:4])
        v = smart_unicode(value)
        #return mark_safe(u'<SCRIPT LANGUAGE="JavaScript">FSfncWriteFieldHTML("form","%s_0","%s",100,"/static/images/FSdateSelector/","EN",false,false,null,null,null,null)</SCRIPT>'%(name,v))
        qq=u'''<input type="text" id="id__name" name="_name" value="_value"/>
    <img border="0" onClick="copyairport();" src="/static/paste.png"/>'''
        qq=qq.replace(u'_name',name).replace(u'_value',v)
        return mark_safe(qq)

class MyDateTimeWidgetwithCopy(forms.DateTimeInput):
    def __init__(self, attrs={}, format=None):
        super(MyDateTimeWidgetwithCopy, self).__init__(attrs={'is_hidden':False,'class': 'vDateField', 'size': '20'}, format=format)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        if value==None: value=""
        elif type(value)!=type(u'unicode'):
            value=value.strftime('%H:%M %d/%m/%Y')
#        if value[4]=="-":
#            value="%s:%s %s/%s/%s"%(value[12:14],value[15:17],value[9:11],value[6:8],value[:4])
        v = smart_unicode(value)
        #return mark_safe(u'<SCRIPT LANGUAGE="JavaScript">FSfncWriteFieldHTML("form","%s_0","%s",100,"/static/images/FSdateSelector/","EN",false,false,null,null,null,null)</SCRIPT>'%(name,v))
        qq=u'''<input type="text" id="id__name" name="_name" value="_value"/>
    <button id="trig_name"><img border="0" src="/static/fsdatepicker/cal.gif"/></button>
    <script type="text/javascript">//<![CDATA[
      Zapatec.Calendar.setup({
        firstDay          : 1,
        weekNumbers       : false,
        showOthers        : true,
        electric          : false,
        inputField        : "id__name",
        button            : "trig_name",
        ifFormat          : "%H:%M %d/%m/%Y",
        showsTime         :     true,
        daFormat          : "%Y/%m/%d"
      });
    //]]></script><img border="0" onClick="copycompleted();" src="/static/paste.png"/>'''
        qq=qq.replace(u'_name',name).replace(u'_value',v)
        return mark_safe(qq)

    class Media:
        css = {
            'all': ('/css/pretty.css',),
            }
        js = ('animations.js', 'http://othersite.com/actions.js')


class MyDateTimeWidget(forms.DateTimeInput):
    def __init__(self, attrs={}, format=None):
        super(MyDateTimeWidget, self).__init__(attrs={'is_hidden':False,'class': 'vDateField', 'size': '20'}, format=format)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        if value==None: value=""
        elif type(value)!=type(u'unicode'):
            value=value.strftime('%H:%M %d/%m/%Y')
#        if value[4]=="-":
#            value="%s:%s %s/%s/%s"%(value[12:14],value[15:17],value[9:11],value[6:8],value[:4])
        v = smart_unicode(value)
        #return mark_safe(u'<SCRIPT LANGUAGE="JavaScript">FSfncWriteFieldHTML("form","%s_0","%s",100,"/static/images/FSdateSelector/","EN",false,false,null,null,null,null)</SCRIPT>'%(name,v))
        qq=u'''<input type="text" id="id__name" name="_name" value="_value"/>
    <button id="trig_name"><img border="0" src="/static/fsdatepicker/cal.gif"/></button>
    <script type="text/javascript">//<![CDATA[
      Zapatec.Calendar.setup({
        firstDay          : 1,
        weekNumbers       : false,
        showOthers        : true,
        electric          : false,
        inputField        : "id__name",
        button            : "trig_name",
        ifFormat          : "%H:%M %d/%m/%Y",
        showsTime         :     true,
        daFormat          : "%Y/%m/%d"
      });
    //]]></script>'''
        qq=qq.replace(u'_name',name).replace(u'_value',v)
        return mark_safe(qq)

    class Media:
        css = {
            'all': ('/css/pretty.css',),
            }
        js = ('animations.js', 'http://othersite.com/actions.js')

class MyDateWidget(forms.DateTimeInput):
    def __init__(self, attrs={}, format=None):
        super(MyDateWidget, self).__init__(attrs={'is_hidden':False,'class': 'vDateField', 'size': '20'}, format=format)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        if value==None: value=""
        elif type(value)!=type(u'unicode'):
            value=value.strftime('%d/%m/%Y')
#        if value[4]=="-":
#            value="%s:%s %s/%s/%s"%(value[12:14],value[15:17],value[9:11],value[6:8],value[:4])
        v = smart_unicode(value)
        #return mark_safe(u'<SCRIPT LANGUAGE="JavaScript">FSfncWriteFieldHTML("form","%s_0","%s",100,"/static/images/FSdateSelector/","EN",false,false,null,null,null,null)</SCRIPT>'%(name,v))
        qq=u'''<input type="text" id="id__name" name="_name" value="_value"/>
    <button id="trig_name"><img border="0" src="/static/fsdatepicker/cal.gif"/></button>
    <script type="text/javascript">//<![CDATA[
      Zapatec.Calendar.setup({
        firstDay          : 1,
        weekNumbers       : false,
        showOthers        : true,
        electric          : false,
        inputField        : "id__name",
        button            : "trig_name",
        ifFormat          : "%d/%m/%Y",
        daFormat          : "%d/%m/%Y"
      });
    //]]></script>'''
        qq=qq.replace(u'_name',name).replace(u'_value',v)
        return mark_safe(qq)

    class Media:
        css = {
            'all': ('/css/pretty.css',),
            }
        js = ('animations.js', 'http://othersite.com/actions.js')


# Create your views here.
class CalendarWidget(forms.DateInput):
    def __init__(self, attrs={}, format=None):
        super(CalendarWidget, self).__init__(attrs={'is_hidden':False,'class': 'vDateField', 'size': '10'}, format=format)

    def render(self, name, value, attrs=None):
        if value is None: value = ukdate().strftime('%d/%m/%Y')
        value = smart_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)
        v=value
        if value[4]=="-":
            t=value.split('-')
            v='%s/%s/%s'%(t[2],t[1],t[0])
        return mark_safe(u'<SCRIPT LANGUAGE="JavaScript">FSfncWriteFieldHTML("form","%s","%s",100,"/static/images/FSdateSelector/","EN",true,false,null,null,null,null)</SCRIPT>'%(name,v))

    class Media:
        css = {
            'all': ('/css/pretty.css',),
            }
        js = ('animations.js', 'http://othersite.com/actions.js')

class CalendarNoneWidget(forms.DateInput):
    def __init__(self, attrs={}, format=None):
        super(CalendarNoneWidget, self).__init__(attrs={'is_hidden':False,'class': 'vDateField', 'size': '10'}, format=format)

    def render(self, name, value, attrs=None):
        if value is None: value = "None"
        value = smart_unicode(value)
        final_attrs = self.build_attrs(attrs, name=name)
        v=value
        if value[4]=="-":
            t=value.split('-')
            v='%s/%s/%s'%(t[2],t[1],t[0])
        return mark_safe(u'<SCRIPT LANGUAGE="JavaScript">FSfncWriteFieldHTML("form","%s","%s",100,"/static/images/FSdateSelector/","EN",false,false,null,null,null,null)</SCRIPT>'%(name,v))

    class Media:
        css = {
            'all': ('/css/pretty.css',),
            }
        js = ('animations.js', 'http://othersite.com/actions.js')
