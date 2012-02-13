'''
Created on 13/05/2011

@author: Agustin
'''
from django.db import models
from location.models import Building
from hardware.models import RackPlace, NetworkedDevice, NetworkPort
from django.utils.translation import ugettext_lazy as _
from hardware.managementutils import sftpGet 

SWITCH_LEVEL = (
    (10, _(u'Access')),
    (20, _(u'CPD')),
    (30, _(u'Distribution')),
    (40, _(u'Core')),
)

BACKUP_METHOD_NULL = 0
BACKUP_METHOD_SFTP = 1

SWITCH_BACKUP_METHOD = (
    (BACKUP_METHOD_NULL, _(u'No backup/Manual')),
    (BACKUP_METHOD_SFTP, _(u'SFTP')),
)

SWITCH_LEVEL_SNMP = {
    10 : 'PejeVerde7',
    20 : '--',
    30 : '--',
    40 : '--',
}

                      
SWITCH_LEVEL_BACKUP_INFO = {
    10 : (BACKUP_METHOD_SFTP, 'manager', 'ACogerFulas7'),
    20 : (BACKUP_METHOD_NULL, '', ''),
    30 : (BACKUP_METHOD_NULL, '', ''),
    40 : (BACKUP_METHOD_NULL, '', ''),
}

#class NetworkBaseModel(RackableModel):
#    recommended_version = models.CharField(max_length = 255)
#    ports = models.PositiveIntegerField(_(u'Default port number for this model'))
#    backupmethod = models.IntegerField(choices = SWITCH_BACKUP_METHOD)
#    backupusername = models.CharField(_(u'Backup username'), max_length = 255,
#            help_text = _(u'Backup username (credentials used in the backup process)')
#            )
#    backuppassword = models.CharField(_(u'Backup password'), max_length = 255,
#            help_text = _(u'Backup password (credentials used in the backup process)')
#            )
#    backupconfigfile = models.CharField(_(u'Backup configuration file'), max_length = 255,
#            help_text = _(u'Configuration file to backup ("path/file")')
#            )
#    template = models.TextField()
#    oid = models.CharField(max_length = 255,
#            help_text = _(u'The string returned by this kind of hw when snmp queried about model')
#            )

class ManagementInfo(models.Model):
    name = models.CharField(max_length = 255, help_text = _(u'Descriptive name of the management info (I.e. "Procurve switch, basic credentials"'))
    defaultports = models.PositiveIntegerField(_(u'Default number of ports for this type of device'))
    backupmethod = models.IntegerField(choices = SWITCH_BACKUP_METHOD)
    backupusername = models.CharField(_(u'Backup username'), max_length = 255,
            help_text = _(u'Backup username (credentials used in the backup process)')
            )
    backuppassword = models.CharField(_(u'Backup password'), max_length = 255,
            help_text = _(u'Backup password (credentials used in the backup process)')
            )
    backupconfigfile = models.CharField(_(u'Backup configuration file'), max_length = 255,
            help_text = _(u'Configuration file to backup ("path/file")')
            )
    recommended_version = models.CharField(max_length = 255)
    configtemplate = models.TextField(_(u'Configuration template'))
    oid = models.CharField(max_length = 255,
            help_text = _(u'The string returned by this kind of hw when snmp queried about model')
            )
    
    def __unicode__(self):
        return u'%s' % self.name  

class Switch(RackPlace, NetworkedDevice):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    ports = models.PositiveIntegerField()
    level = models.IntegerField(choices = SWITCH_LEVEL)
    managementinfo = models.ForeignKey(ManagementInfo) 

    def __unicode__(self):
        return u'%s' % self.name        

    #Backups switch configuration to the specified file 
    #Returns 
    #  False, "" : if no backup method defined for this switch     
    #  True, None : If backup succeeded    
    #  True, ErrorDescription : If backup failed  
    def backup_config_to_file(self, destinationfile):
        mgt = self.managementinfo
        if mgt.backupmethod == BACKUP_METHOD_SFTP :
            errorDesc = sftpGet(hostname = self.main_ip, username = mgt.backupusername, password = mgt.backuppassword, \
                                 sourcefile = mgt.backupconfigfile, destfile = destinationfile)
            return True, errorDesc  
        return False, None
       
class MACsHistory(models.Model):
    port = models.ManyToManyField(NetworkPort)
    captured = models.DateTimeField()
    mac = models.CharField(max_length=12) 
  
class RoutingZone(models.Model):
    """
        A model to represent a zone or group of buildings with common routing characteristics
    """
    prefix = models.CharField(max_length=6)
    name = models.CharField(max_length=255)
    bluevlan_prefix = models.IntegerField()
    public_nets = models.CharField(max_length=255,
      help_text = _(u"A list of public networks"))
    cajacanarias_nets = models.CharField(max_length=255,
      help_text = _(u"A list of CajaCanarias networks"))  
    slug = models.SlugField()

    def __unicode__(self):
        return u'[%04d] %s - %s' % (int(self.bluevlan_prefix), self.prefix, self.name)    
    
class NetworkedBuilding(Building):
    """
        A model to represent a Building with networking (with a routing zone) 
    """
    routingzone = models.ForeignKey(RoutingZone)
    
    
    
    
