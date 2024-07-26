from django.contrib import admin
from django.utils.html import format_html
from membre.models import UserWithFlotte

from .forms import UserWithFlotteUserAdminForm

class UserWithFlotteAdmin(admin.ModelAdmin):
    list_display = [ 'user_link','card_link','type_de_ligne','custcode','plan_tarifaire','localisation']
    list_display_links = ['type_de_ligne']
    search_fields = ['custcode','plan_tarifaire','type_de_ligne','localisation']
    list_filter = ['custcode','plan_tarifaire','type_de_ligne','localisation']
    # list_editable = ['custcode','plan_tarifaire']
    form = UserWithFlotteUserAdminForm
    def user_link(self, obj):
        if obj.user:
            return format_html('<a href="{}">{}</a>', obj.user.get_admin_url(), obj.user)
        return '-'
    user_link.short_description = 'Membre'
    
    def card_link(self, obj):
        if obj.card:
            return format_html('<a href="{}">{}</a>', obj.card.get_admin_url(), obj.card)
        return '-'
    card_link.short_description = 'Carte'
admin.site.register(UserWithFlotte , UserWithFlotteAdmin)
# Register your models here.
