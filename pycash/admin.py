from pycash.models import *
from django.contrib import admin

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(PaymentType)
admin.site.register(Tax)
admin.site.register(Expense)
admin.site.register(Debits)
admin.site.register(TokenUsage)
admin.site.register(Person)
admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(SyncRecord)
admin.site.register(Income)

class AuthTokenAdmin(admin.ModelAdmin):
    readonly_fields = ('token', 'token_key')
    
admin.site.register(AuthToken, AuthTokenAdmin)