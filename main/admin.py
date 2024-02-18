from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(GameSession)

class FactoryCardAdmin(admin.ModelAdmin):
    list_display = ('card_code', 'cost', 'production_capacity','maximum_production','factory_type')

class LabourCardAdmin(admin.ModelAdmin):
    list_display = ('card_code', 'cost', 'labour')

class WellCardAdmin(admin.ModelAdmin):
    list_display = ('card_code', 'cost', 'capacity')
class AutomationCardAdmin(admin.ModelAdmin):
    list_display = ('card_code', 'cost', 'capacity')

class PayoutCardAdmin(admin.ModelAdmin):
    list_display = ('card_code', 'free_flow_payout_type','iodized_payout_type','crude_payout_type','free_flow_payout','iodized_payout','crude_payout')



admin.site.register(FactoryCard,FactoryCardAdmin)
admin.site.register(LabourCard,LabourCardAdmin)
admin.site.register(WellCard,WellCardAdmin)
admin.site.register(AutomationCard,AutomationCardAdmin)
admin.site.register(PayOutCard,PayoutCardAdmin)
admin.site.register(GamePlayer)
admin.site.register(PlayerFactory)
admin.site.register(Player)




