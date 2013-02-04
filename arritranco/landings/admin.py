# coding: utf-8

from django import forms
from django.contrib import admin, messages
from models import LandingType, Product, AvailableProduct, Landing

import logging
logger = logging.getLogger(__name__)

class LandingTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', )

class ProductsInline(admin.TabularInline):
    model = AvailableProduct

class LandingAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'enable', )
    list_filter = ('type', 'enable', )
    inlines = [ProductsInline,]


admin.site.register(Landing, LandingAdmin)
admin.site.register(LandingType, LandingTypeAdmin)
admin.site.register(Product, ProductAdmin)

