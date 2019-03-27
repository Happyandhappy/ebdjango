from django.contrib import admin
from .models import PaymentToken, SubscriptionPlan, Subscription


class PaymentTokenAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(PaymentTokenAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

    date_hierarchy = 'date_created'
    fieldsets = (
        (None, {
            'fields': ( ('token'), ('user'),('email'),('last_4_digits'))
        }),
    )

    list_display = (
        'id', 'date_created', 'last_4_digits', 'user')
    list_display_links = ('last_4_digits',)
    list_filter = ('last_4_digits', 'user')
    search_fields = ('last_4_digits', 'date_created', 'user')


class SubscriptionPlanAdmin(admin.ModelAdmin):
    readonly_fields = ('stripe_plan_id',)
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super(SubscriptionPlanAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ('stripe_subscription_id',)
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save'] = False
        return super(SubscriptionAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

admin.site.register(PaymentToken, PaymentTokenAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
