from django.contrib import admin

from .models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ['msisdn','number_sim','puk']
    search_fields = ['msisdn','number_sim','puk']
    list_filter = ['msisdn','number_sim','puk']
admin.site.register(Card,CardAdmin)
# Register your models here.
