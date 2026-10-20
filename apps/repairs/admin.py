from django.contrib import admin
from .models import RepairOrder, RepairStatus


@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ("short_id", "customer_name", "phone", "device_model", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "phone", "device_model")
    readonly_fields = ("id", "created_at", "updated_at")
    list_editable = ("status",)
    date_hierarchy = "created_at"
    actions = ["mark_ready_for_delivery"]

    @admin.display(description="شناسه")
    def short_id(self, obj):
        return f"#{str(obj.id)[:8]}"

    @admin.action(description="تغییر وضعیت به «آماده تحویل»")
    def mark_ready_for_delivery(self, request, queryset):
        updated = queryset.update(status=RepairStatus.READY)
        self.message_user(request, f"{updated} سفارش آماده تحویل شد.")
