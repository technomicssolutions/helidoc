from django.db import models

class ship(models.Model):
    owner=models.CharField('owner',max_length=200)
    type=models.CharField('type',max_length=200)
    model=models.CharField('model',max_length=200)
    callsign=models.CharField('callsign',max_length=60)
    serialno=models.CharField('serialno',max_length=200)
    registration=models.CharField('registration',max_length=200)
    engine_id=models.BigIntegerField('engine_id')
    hours=models.DecimalField('hours',max_digits=10,decimal_places=1)
    airframehoursoffset=models.DecimalField('airframehoursoffset',max_digits=10,decimal_places=1)
    cycles=models.SmallIntegerField('cycles')
    lastflight=models.DateField('lastflight')
    lastoverhaul=models.DateField('lastoverhaul',null=True)
    manufactured=models.DateField('manufactured',null=True)
    lastdatcon=models.DecimalField('lastdatcon',max_digits=6,decimal_places=1)
    nextmaintdatcon=models.DecimalField('nextmaindatcon',max_digits=6,decimal_places=1)
    nextmaintdate=models.DateField('nextmaindate',null=False)
    nextmaintreason=models.CharField('Next Maintenance Reason',max_length=200)
    arcdate=models.DateField('ARC Date',null=False)
    owned=models.BooleanField('Ship still owned')
    crs=models.CharField('CRS',max_length=255)
    def __str__(self):
        return '%s %s: %s'%(self.type,self.model,self.registration)



class event(models.Model):
    starttime=models.DateTimeField('Start Time')
    duration=models.IntegerField('Duration',blank=True,null=True)
    ship=models.ForeignKey(ship,verbose_name="Helicopter",blank=True,null=True)
    voucher=models.CharField('Voucher',max_length=200,blank=True,null=True)
    security=models.CharField('Security',max_length=200,blank=True,null=True)
    name=models.CharField('Name',max_length=200)
    seats=models.IntegerField('Seats',default=1,null=False)
    mobile=models.CharField('mobile',max_length=200)
    email=models.CharField('email',max_length=200,blank=True,null=True)
    details=models.CharField('Details',max_length=200,blank=True,null=True)
    captain=models.CharField('Captain',max_length=200,blank=True,null=True)
    notes=models.TextField('Notes',blank=True,null=True)
    cancelled=models.BooleanField('Cancelled')
    completed=models.BooleanField('Completed')
    source=models.CharField('Source',max_length=200,blank=True,null=True)
    def __str__(self):
        return '%s: %s %s %s'%(self.starttime,self.duration,self.name,self.details)


# Create your models here.
