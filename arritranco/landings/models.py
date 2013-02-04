from django.db import models
from django.utils.translation import ugettext_lazy as _
from inventory.models import Machine


class LandingType(models.Model):
    """
        Landing page type
    """
    name = models.CharField('Landing type name', max_length=255, blank=False, null=False)

    def __unicode__(self):
        return u"%s" % self.name


class Product(models.Model):
    """
        Product
    """
    name = models.CharField('Landing type name', max_length=255, blank=False, null=False)

    def __unicode__(self):
        return u"%s" % self.name

class AvailableProduct(models.Model):
    product = models.ForeignKey(Product)
    landing = models.ForeignKey('Landing')
    enable = models.BooleanField(blank=False, null=False, default=True)

    def __unicode__(self):
        return u"%s" % self.product

class Landing(models.Model):
    """
        Landing page
    """
    name = models.CharField('Landing name', max_length=255, blank=False, null=False, help_text=_(u'File name pattern, you can use regexp and date patterns here.'))
    type = models.ForeignKey(LandingType)
    machine = models.ForeignKey(Machine)
    products = models.ManyToManyField(Product, through=AvailableProduct)
    enable = models.BooleanField(blank=False, null=False, default=True)

    def get_disabled_products(self):
        return self.products.filter(availableproduct__enable = False)

    def __unicode__(self):
        return u"%s" % self.name


