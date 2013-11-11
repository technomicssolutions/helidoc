# Create your views here.
import datetime
from django.shortcuts import HttpResponse,redirect
from django.shortcuts import render_to_response,get_object_or_404
from helidocs.diary.models import event
from helidocs.diary.models import ship
from helidocs.widgets.ukdate import ukdatetime,ukdate
from calendar import monthrange
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.forms import ModelForm,Textarea,TextInput
from django import forms
from helidocs.widgets.widgets import MyDateWidget,MyDateTimeWidget

class NewGroupOnEventForm(ModelForm):
    starttime=forms.DateTimeField(label="Start Time",input_formats=['%H:%M %d/%m/%Y','%H:%M %d/%m/%y','%H:%M:%S %d/%m/%Y'],widget=MyDateTimeWidget())
    voucher=forms.CharField(label='GroupOn Voucher Number',required=True) #,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    security=forms.CharField(label='GroupOn Security Number',required=True) #,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    voucher2=forms.CharField(label='GroupOn2 Voucher Number',required=False) #,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    security2=forms.CharField(label='GroupOn2 Security Number',required=False) #,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    voucher3=forms.CharField(label='GroupOn3 Voucher Number',required=False) #,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    security3=forms.CharField(label='GroupOn3 Security Number',required=False) #,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    create=forms.BooleanField(label="Create Seat Duplicates",required=False,initial=True)

    class Meta:
        model=event
        widgets = {
            'voucher': TextInput(attrs={'size': 40}),
            'details': TextInput(attrs={'size': 40}),
            'email': TextInput(attrs={'size': 40}),
            'notes': Textarea(attrs={'cols': 40, 'rows': 2}),
            'source': forms.widgets.HiddenInput(),
            }


class NewEventForm(ModelForm):
    starttime=forms.DateTimeField(label="Start Time",input_formats=['%H:%M %d/%m/%Y','%H:%M %d/%m/%y','%H:%M:%S %d/%m/%Y'],widget=MyDateTimeWidget())
    #    exercises=forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    #    comments = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':6, 'cols':60}))
    create=forms.BooleanField(label="Create Seat Duplicates",required=False,initial=True)
    class Meta:
        model=event
        exclude = ('security',)
        widgets = {
            'voucher': TextInput(attrs={'size': 40}),
            'email': TextInput(attrs={'size': 40}),
            'mobile': TextInput(attrs={'size': 40}),
            'details': TextInput(attrs={'size': 40}),
            'notes': Textarea(attrs={'cols': 40, 'rows': 2}),
            'source': forms.widgets.HiddenInput(),

            }

class NewEventEditForm(ModelForm):
    starttime=forms.DateTimeField(label="Start Time",input_formats=['%H:%M %d/%m/%Y','%H:%M %d/%m/%y','%H:%M:%S %d/%m/%Y'],widget=MyDateTimeWidget())
    #    exercises=forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    #    comments = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':6, 'cols':60}))
    security=forms.CharField(label='Groupon Security No.',required=False) #,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    duplicate=forms.BooleanField(label="Duplicate (Don't Edit)",required=False)
    class Meta:
        model=event
        exclude = ('seats',)
        widgets = {
            'email': TextInput(attrs={'size': 40}),
            'voucher': TextInput(attrs={'size': 40}),
            'details': TextInput(attrs={'size': 40}),
            'mobile': TextInput(attrs={'size': 40}),
            'notes': Textarea(attrs={'cols': 40, 'rows': 2}),
            'source': forms.widgets.HiddenInput(),
            }



def subtract_date(date, year=0, month=0):
    year, month = divmod(year*12 + month, 12)
    if date.month <= month:
        year = date.year - year - 1
        month = date.month - month + 12
    else:
        year = date.year - year
        month = date.month - month
    return date.replace(year = year, month = month,day=1)

def add_date(date, month=0):
    if date.month+month>12:
        year = date.year+1
        month = date.month + month -12
    else:
        year = date.year
        month = date.month + month
    return date.replace(year = year, month = month)

def homepage(request):
    c={'user':request.user}
    return render_to_response('diary/homepage.html',c)

def calendar(request,pID='0'):
    c={'user':request.user}
    try:
        y,m=pID.split('-')
        r=datetime.datetime(int(y),int(m),1,0,0,0)
    except:
        r=ukdatetime()

    s=r.replace(day=1,hour=0,minute=0,second=0)
    back=s+datetime.timedelta(days=-2)
    last=monthrange(s.year,s.month)[1]

    c.update({'date':s.strftime('%B %Y')})
    days=[]
    skip=s.weekday()
    count=0
    day=1
    y=r.year
    m=r.month+1
    if m==13:
        y=r.year+1
        m=1

    stx=datetime.datetime(r.year,r.month,1,0,0,0).strftime('%Y-%m-%d')
    etx=datetime.datetime(y,m,1,0,0,0).strftime('%Y-%m-%d')
    c['back']=back.strftime('%Y-%m')
    c['forwards']=etx[:7]
    startfuel=0
    dial=34634
    ev=event.objects.filter(starttime__gte=stx,starttime__lt=etx).order_by("starttime")
    stx=datetime.datetime(r.year,r.month,1,0,0,0)

    for q in range(1,7):
        ee=[]
        for x in range(1,8):
            dday=""
            events=""
            link=""
            etx=stx+datetime.timedelta(days=1)
            if count>=skip and day<=last:
                dday=day
                day+=1
                link=stx.strftime('%Y-%m-%d')
                for r in ev:
                    if r.starttime>=stx and r.starttime<etx:
                        if events:
                            events+='<br>'
                        heli=""
                        if r.ship:
                            heli=" [%s]"%(r.ship.model[:3])
                        else:
                            events+='<font color="red">'
                        if r.cancelled:
                            events+='<strike>'
                        captain=''
                        if r.captain:
                            captain="(%s)"%(r.captain)
                        name='<font color="purple"><b>'+r.voucher+"</b> "+r.name+'</font>'
                        if r.voucher and r.voucher.find('(voucher)')!=-1:
                            name='<font color="purple">'+r.voucher.replace('(voucher)','')+'</font>'
                        if r.security:
                            name='<font color="#CC0066"><b>[GO] '+r.voucher+"</b> "+r.name+'</font>'
                        ttdelta=r.duration
                        if not ttdelta:
                            ttdelta=0
                        if r.completed:
                            events+='<font color="#009933"><b>'
                        events+='''<strong><a href="javascript:void(0)" onClick="OpenNewEvent('/calendaredit/'''+str(r.id)+'''');return false;">'''+'%s-%s:</a></strong> %s[%d] %s %s%s'%(r.starttime.strftime('%H:%M'),(r.starttime+datetime.timedelta(minutes=ttdelta)).strftime('%H:%M'),heli,ttdelta,name,r.details,captain)
                        if not r.ship:
                            events+='</font>'
                        if r.cancelled:
                            events+='</strike>'
                        if r.completed:
                            events+='</b></font>'

                stx=stx+datetime.timedelta(days=1)
            count+=1
            ee.append({'day':dday,'link':link,'event':events})
        days.append(ee)
    c['days']=days
    return render_to_response('diary/calendar.html',c)

def calendaradd(request,pID=''):
    c={'user':request.user}
    c.update(csrf(request))
    starttime=ukdatetime()
    heli='0'
    if pID:
        if pID.find('*')!=-1:
            pXX,heli=pID.split('*')
        else:
            pXX=pID
        try:
            starttime=datetime.datetime.strptime(pXX,'%Y-%m-%d:%H:%M')

        except:
            try:
                starttime=datetime.datetime.strptime(pXX,'%Y-%m-%d: 12:00:00')
            except:
                y,m,d=pXX.split('-')
                starttime=datetime.datetime(int(y),int(m),int(d),12,00,00)

    message="Please Correct Error and Resubmit"
    if request.method=="GET":
        newevent=NewEventForm(initial={'starttime': starttime,'ship': str(heli)})#initial={'ship': pID,'datcon':s.lastdatcon,'date':lastflown}
        #maint.fields['ship']=pID
        message='Enter the New Event'
        c.update({'newevent':newevent})
    elif request.method=="POST":
        if request.POST["submit"] == "Submit Event":
            newevent=NewEventForm(request.POST)
            if newevent.is_valid():
                original_event=newevent.save()

                #create entries if there is more than one seat on voucher
                obj=event.objects.get(pk=original_event.id)
                for x in range(1,original_event.seats):
                    obj.id=None
                    obj.save(force_insert=True)

                #now check to see if a voucher was involved
                v=request.POST["voucher"]
                if v and v.find('(voucher)')!=-1:
                    vno=v[:v.find(' ')]
                    #print vno
                    entry = voucher.objects.get(number=vno)
                    #print entry
                    if entry:
                        if request.POST.has_key("cancelled"):
                            entry.bookeddate=None
                        else:
                            dt=datetime.datetime.strptime(request.POST["starttime"],"%H:%M %d/%m/%Y")
                            entry.bookeddate=dt
                        if request.POST.has_key("completed"):
                            dt=datetime.datetime.strptime(request.POST["starttime"],"%H:%M %d/%m/%Y")
                            entry.completeddate=dt
                        else:
                            entry.completeddate=None
                        entry.save()

            else:
                c.update({'newevent':newevent})
    return render_to_response('diary/calendar_add.html',c)

def grouponbookin(request,pID=''):
    c={'user':request.user}
    c.update(csrf(request))
    c.update({'dateformat':pID})

    t=datetime.datetime(2013,03,01,23,00,00)
    enddate=datetime.datetime(2013,12,31,23,00,00)

    times=grouponday.objects.filter(date__gt=t)##datetime.datetime.today())
    events={}

    for e in event.objects.filter(starttime__gt=t,security__isnull=False,cancelled=False,ship=5):
        key=e.starttime.strftime('%Y%m%d%H%M')
        r=events.get(key,0)
        r+=1
        events[key]=r

    dates=[]
    count=0
    pdate=-1
    while t<enddate:
        timeon=0
        for r in times:
            if r.morning_start and t>=datetime.datetime(r.date.year,r.date.month,r.date.day,r.morning_start.hour,r.morning_start.minute) \
                and t<=datetime.datetime(r.date.year,r.date.month,r.date.day,r.morning_end.hour,r.morning_end.minute):
                timeon=1
            elif r.afternoon_start and t>=datetime.datetime(r.date.year,r.date.month,r.date.day,r.afternoon_start.hour,r.afternoon_start.minute) \
                and t<=datetime.datetime(r.date.year,r.date.month,r.date.day,r.afternoon_end.hour,r.afternoon_end.minute):
                timeon=1
            elif r.evening_start and t>=datetime.datetime(r.date.year,r.date.month,r.date.day,r.evening_start.hour,r.evening_start.minute) \
                and t<=datetime.datetime(r.date.year,r.date.month,r.date.day,r.evening_end.hour,r.evening_end.minute):
                timeon=1

        if timeon:
            key=t.strftime('%Y%m%d%H%M')
            seats=3-events.get(key,0)

            if seats:
                dates.append({'pdate':pdate,'date':t,'time':t.strftime('%H:%M'),'seats':seats})
                pdate=t
        t+=datetime.timedelta(minutes=10)
        count+=1

    c.update({'dates':dates})
    return render_to_response('flights/grouponbookin.html',c)


def grouponadd(request,pID=''):
    c={'user':request.user}
    c.update(csrf(request))
    starttime=ukdatetime()
    heli='0'
    if pID:
        if pID.find('*')!=-1:
            pXX,heli=pID.split('*')
        else:
            pXX=pID
        try:
            starttime=datetime.datetime.strptime(pXX,'%Y-%m-%d:%H:%M')

        except:
            try:
                starttime=datetime.datetime.strptime(pXX,'%Y-%m-%d: 12:00:00')
            except:
                y,m,d=pXX.split('-')
                starttime=datetime.datetime(int(y),int(m),int(d),12,00,00)

    message="Please Correct Error and Resubmit"
    if request.method=="GET":
        newevent=NewGroupOnEventForm(initial={'starttime': starttime,'ship': str(heli),'duration':10,'captain':'Simon Smith','details':'6 Mile Buzz Flight'})#initial={'ship': pID,'datcon':s.lastdatcon,'date':lastflown}
        #maint.fields['ship']=pID
        message='Enter the New Event'
        c.update({'newevent':newevent})
    elif request.method=="POST":
        if request.POST["submit"] == "Submit Event":
            newevent=NewGroupOnEventForm(request.POST)
            if newevent.is_valid():
                original_event=newevent.save()

                #create entries if there is more than one seat on voucher
                obj=event.objects.get(pk=original_event.id)
                count=2
                v1=obj.voucher
                v2=obj.security
                for x in range(1,original_event.seats):
                    obj.id=None
                    obj.voucher=request.POST.get("voucher%d"%(count),v1)
                    obj.security=request.POST.get("security%d"%(count),v2)
                    obj.save(force_insert=True)
                    count+=1

                #now check to see if a voucher was involved
                v=request.POST["voucher"]
                if v and v.find('(voucher)')!=-1:
                    vno=v[:v.find(' ')]
                    #print vno
                    entry = voucher.objects.get(number=vno)
                    #print entry
                    if entry:
                        if request.POST.has_key("cancelled"):
                            entry.bookeddate=None
                        else:
                            dt=datetime.datetime.strptime(request.POST["starttime"],"%H:%M %d/%m/%Y")
                            entry.bookeddate=dt
                        if request.POST.has_key("completed"):
                            dt=datetime.datetime.strptime(request.POST["starttime"],"%H:%M %d/%m/%Y")
                            entry.completeddate=dt
                        else:
                            entry.completeddate=None
                        entry.save()

            else:
                c.update({'newevent':newevent})
    return render_to_response('diary/calendar_add.html',c)



def calendaredit(request,pID=''):
    c={'user':request.user}
    c.update(csrf(request))
    message="Please Correct Error and Resubmit"
    r=get_object_or_404(event,pk=pID)
    if request.method=="GET":
        if pID:
            newevent=NewEventEditForm(instance=r)#initial={'ship': pID,'datcon':s.lastdatcon,'date':lastflown}
        else:
            newevent=NewEventEditForm()#initial={'ship': pID,'datcon':s.lastdatcon,'date':lastflown}
            #maint.fields['ship']=pID
        message='Enter the New Event'
        c.update({'newevent':newevent})
    elif request.method=="POST":
        if request.POST["submit"] == "Submit Event":
            if request.POST.has_key("duplicate"):
                newevent=NewEventEditForm(request.POST)
            else:
                newevent=NewEventEditForm(request.POST,instance=r)
            if newevent.is_valid():
                newevent.save()
                if request.POST["details"]=='Delete':
                    event.objects.filter(id=pID).delete()
                    #now check to see if a voucher was involved
                v=request.POST["voucher"]
                if v and v.find('(voucher)')!=-1:
                    vno=v[:v.find(' ')]
                    #print vno
                    entry = voucher.objects.get(number=vno)
                    #print entry
                    if entry:
                        if request.POST.has_key("cancelled"):
                            entry.bookeddate=None
                        else:
                            dt=datetime.datetime.strptime(request.POST["starttime"],"%H:%M %d/%m/%Y")
                            entry.bookeddate=dt
                        if request.POST.has_key("completed"):
                            dt=datetime.datetime.strptime(request.POST["starttime"],"%H:%M %d/%m/%Y")
                            entry.completeddate=dt
                        else:
                            entry.completeddate=None

                        entry.save()
            else:
                c.update({'newevent':newevent})
    return render_to_response('diary/calendar_add.html',c)

def daytoview(request,pID=''):
    c={'user':request.user}
    c.update(csrf(request))
    c.update({'dateformat':pID})

    try:
        y,m,d=pID.split('-')
        r=datetime.datetime(int(y),int(m),int(d),0,0,0)
    except:
        r=ukdatetime()

    s=r
    back=s+datetime.timedelta(days=-1)
    forwards=s+datetime.timedelta(days=+1)
    last=r #monthrange(s.year,s.month)[1]

    c.update({'date':s.strftime('%A %d %B %Y')})
    days=[]
    skip=s.weekday()
    count=0
    day=1
    y=r.year
    m=r.month+1
    if m==13:
        y=r.year+1
        m=1

    stx=datetime.datetime(r.year,r.month,r.day,0,0,0).strftime('%Y-%m-%d %H:%M:%S')
    etx=datetime.datetime(r.year,r.month,r.day,23,59,59).strftime('%Y-%m-%d %H:%M:%S')
    c['back']=back.strftime('%Y-%m-%d')
    c['forwards']=forwards.strftime('%Y-%m-%d')
    #print stx,etx
    ev=event.objects.filter(starttime__gte=stx,starttime__lt=etx).order_by("starttime")
    stx=datetime.datetime(r.year,r.month,1,0,0,0)

    days=[]
    cols=[]
    times=[]

    ot=datetime.datetime(1899,1,1,0,0,0)
    for x in ev:
        if x.starttime!=ot:
            times.append(x.starttime)
            ot=x.starttime

    for x in times:
        cols=[]
        eventlist={1:'',2:'',0:'',5:'',4:''}
        link=x.strftime('%Y-%m-%d:%H:%M')
        id=x.strftime('%Y%m%d%H%M')
        for r in ev:
            if not r.ship:
                ship=0
            else:
                ship=r.ship.id
            if eventlist.has_key(ship):
                events=eventlist[ship]
            else:
                events=""
            if r.starttime==x:
                if events:
                    events+='<br>'
                heli=""
                if r.ship:
                    heli=" [%s]"%(r.ship.model[:3])
                else:
                    events+='<font color="red">'
                if r.cancelled:
                    events+='<strike>'
                captain=''
                if r.captain:
                    captain="(%s)"%(r.captain)
                name='<font color="purple"><b>'+r.voucher+"</b> "+r.name+'</font>'
                if r.voucher and r.voucher.find('(voucher)')!=-1:
                    name='''<a href="javascript:void(0)" onClick="OpenNewVoucherEvent('/editvoucher/'''+str(r.voucher[:r.voucher.find(' ')])+'''');return false;"><font color="purple">'''+r.voucher.replace('(voucher)','')+'</font></a>'
                if r.security:
                    name='<font color="#CC0066"><b>[GO] '+r.voucher+"</b> "+r.name+'</font>'
                ttdelta=r.duration
                if not ttdelta:
                    ttdelta=0
                if r.completed:
                    events+='<font color="#009933"><b>'
                events+='''<strong><a href="javascript:void(0)" onClick="OpenNewEvent('/calendaredit/'''+str(r.id)+'''');return false;">'''+'%s-%s:</a></strong> %s[%d]%s %s%s'%(r.starttime.strftime('%H:%M'),(r.starttime+datetime.timedelta(minutes=ttdelta)).strftime('%H:%M'),heli,ttdelta,name,r.details,captain)
                if not r.ship:
                    events+='</font>'
                if r.cancelled:
                    events+='</strike>'
                if r.completed:
                    events+='</b></font>'
                eventlist[ship]=events
        cols.append({'id':id+"X",'link':link,'event':x.strftime('%H:%M')})
        cols.append({'id':id+"0",'link':link,'event':eventlist[0],'day':x.strftime('%H:%M')})
        cols.append({'id':id+"1",'link':link+"*1",'ship':1,'event':eventlist[1],'day':x.strftime('%H:%M')})
        cols.append({'id':id+"4",'link':link+"*4",'ship':4,'event':eventlist[4],'day':x.strftime('%H:%M')})
        cols.append({'id':id+"5",'link':link+"*5",'event':eventlist[5],'day':x.strftime('%H:%M')})
        cols.append({'id':id+"6",'link':link,'event':eventlist[2],'day':x.strftime('%H:%M')})

        days.append(cols)

    c['days']=days
    return render_to_response('diary/daytoview.html',c)

def get_voucher(request,pID=''):
    if 1:#request.is_ajax():
        vt=vouchertype.objects.values("id","type").all()
        vtype={}
        for v in vt:
            vtype[v['id']]=''.join( [ lett[0] for lett in v['type'].split() ] ).upper()


#        r=voucher.objects.values("number","name","vouchertype","duration","recptname").filter(completeddate__isnull=True)
        r=voucher.objects.values("number","name","vouchertype","duration","recptname").all()#filter(completeddate__isnull=True)
        vou=""
        for x in r:
            if x['recptname']:
                name=x['recptname']
            else:
                name=x['name']
            vtx="UnKnown"
            if vtype.has_key(x['vouchertype']):
                vtx=vtype[x['vouchertype']]
            if vou:
                vou+="|%s %s[%s] %s (voucher)"%(x['number'],vtx,x['duration'],name)
            else:
                vou+="%s %s[%s] %s (voucher)"%(x['number'],vtx,x['duration'],name)
        return HttpResponse(vou)
    else:
        vou="Brian|Was|Here"
        return HttpResponse(vou)

def get_student(request,pID=''):
    if 1:#request.is_ajax():
        r=student.objects.values("first","last").all().order_by("first")#filter(completeddate__isnull=True)
        vou=""
        for x in r:
            if vou:
                vou+="|%s %s"%(x['first'],x['last'])
            else:
                vou+="%s %s"%(x['first'],x['last'])
        return HttpResponse(vou)
    else:
        vou="Brian|Was|Here"
        return HttpResponse(vou)


@csrf_exempt
def get_voucher_contacts(request,pID=''):
#    import sys
#    sys.stdout.write('\a')
#    sys.stdout.flush()

    vnumber=pID.split(' ')[0]
    #vnumber='9226'
    vt={}
    for vti in vouchertype.objects.all():
        vt[vti.id]=vti.type
    r=voucher.objects.values("number","name","mobile","landline","seats","vouchertype","duration","recptname").filter(number__startswith=vnumber)
    vou="Not Known|Not Known|1|Not Known"
    if r:
        r=r[0]
        nums=""
        if r['mobile']:
            nums=r['mobile']
        if r['landline']:
            if nums:
                nums+=':'+r['landline']
            else:
                nums=r['landline']

        desc='%d Mins %s %s Seat'%(r['duration'],vt[r['vouchertype']],r['seats'])
        if r['seats']>1: desc+='s'
        nameofflier=r['recptname']
        if nameofflier:
            nameofflier+=' book by %s'%(r['name'])
        else:
            nameofflier=r['name']

        vou="%s|%s|%s|%s"%(nums,nameofflier,r['seats'],desc)
    return HttpResponse(vou)

def get_student_contacts(request,pID=''):
    t=pID.split(' ')
    r=''
    if len(t)>1:
        r=student.objects.values("email","mobile","home","office").filter(first=pID.split(' ')[0],last=pID.split(' ')[1])[:1]
    vou=""
    if r:
        r=r[0]
        cont=''
        if r['mobile']:
            cont+='M:%s'%(r['mobile'])
        if r['home']:
            cont+=',H:%s'%(r['home'])
        if r['office']:
            cont+=',W:%s'%(r['office'])
        if cont.startswith(','):
            cont=cont[1:]
        vou="%s|%s"%(r['email'],cont)
    return HttpResponse(vou)



def addMonth(date, n=1):
    OneDay =datetime.timedelta(days=1)
    # add n+1 months to date then subtract 1 day
    # to get eom, last day of target month
    q,r = divmod(date.month+n, 12)
    eom = datetime.date(date.year+q, r+1, 1) - OneDay
    if date.month != (date+OneDay).month or date.day >= eom.day:
        return eom
    return eom.replace(day=date.day)

def findfreeseats(request,pID='0'):
    c={'user':request.user}
    ships=ship.objects.filter(id__lt=99).exclude(owned=0)
    t=ukdate()
    tdelta=0
    showmonth=0
    if pID:
        try:
            t=datetime.datetime.strptime(pID,'%m%y')
            showmonth=1
        except:
            try:
                t=datetime.datetime.strptime(pID,'%m%y')
                showmonth=1
            except:
                try:
                    t=datetime.datetime.strptime(pID,'%d%m%y')
                except:
                    try:
                        t=datetime.datetime.strptime(pID,'%Y-%m')
                        showmonth=1
                    except:
                        try:
                            t=datetime.datetime.strptime(pID,'%d%m%Y')
                        except:
                            try:
                                t=datetime.datetime.now()
                                showmonth=1
                            except:
                                try:
                                    tdelta=int(pID)
                                except:
                                    pass
    reportdate=t.strftime('%B %Y')
    c['back']=addMonth(t,-1).strftime('%m%y')
    c['forwards']=addMonth(t,1).strftime('%m%y')

    if not showmonth:
        t=(t+datetime.timedelta(days=tdelta))
        reportdate=t.strftime('%A %d %B %Y')
        c['back']=(t+datetime.timedelta(days=-1)).strftime('%d%m%Y')
        c['forwards']=(t+datetime.timedelta(days=+1)).strftime('%d%m%Y')
        t=t.strftime('%Y-%m-%d')
        te=t
    else:
        reportdate=t.strftime('%B %Y')
        c['back']=addMonth(t,-1).strftime('%m%y')
        c['forwards']=addMonth(t,1).strftime('%m%y')

        last=monthrange(t.year,t.month)[1]
        te=datetime.datetime(t.year,t.month,last).strftime('%Y-%m-%d')
        if t<datetime.datetime.now():
            t=ukdate()
        t=t.strftime("%Y-%m-%d")

    qs=("%s 00:00:00"%(t),"%s 23:59:59"%(te))
    events=event.objects.filter(starttime__range=qs,ship=5,duration__lt=121).order_by('starttime')


    evnts=[]

    otherseats=''
    voucher=''
    if events:
        timezero=events[0].starttime
        pre=events[0]
        otherseats+=events[0].details
        voucher+=events[0].voucher

    taken=0
    for x in events:
        if x.starttime==timezero:
            taken+=1
            pre=x
            if otherseats:
                otherseats+=','+x.details
            else:
                otherseats=x.details
            voucher+=x.voucher
        else:
            avail=''
            if voucher.find('TL[')==-1 and otherseats.lower().find('trial lesson')==-1 and otherseats.lower().find('bespoke')==-1:
                if 3-taken:
                    avail=3-taken
            else:
                avail=''
            link=pre.starttime.strftime('%Y-%m-%d:%H:%M')+"*"+str(pre.ship_id)
            evnts.append({'otherseats':otherseats,'link':link,'starttime':pre.starttime,'ship':pre.ship,'duration':pre.duration,'taken':taken,'available':avail})
            taken=1
            timezero=x.starttime
            pre=x
            otherseats=x.details
            voucher=x.voucher

    c.update({'events':evnts,'date':reportdate})

    template='diary/findfreeslots.html'
    return render_to_response(template,c)


def SetComplete(request,pID=''):
    starttime=datetime.datetime.strptime(pID[:-1],'%Y%m%d%H%M')
    shipid=pID[-1:]
    if shipid=='0':
        shipid=None
    clist=event.objects.filter(starttime=starttime,ship=shipid)
    for x in clist:
        x.completed=True
        x.save()
        if x.voucher.find('(voucher)')!=-1:
            vno=x.voucher[:x.voucher.find(' ')]
            #print vno
            entry = voucher.objects.get(number=vno)
            #print entry
            if entry:
                entry.completeddate=starttime
                entry.save()
    return HttpResponse('Done')