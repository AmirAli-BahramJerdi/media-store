from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "thumb",
        "name",
        "category",
        "price",
        "has_image_badge",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "is_active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active",)
    readonly_fields = ("preview",)

    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": ("name", "slug", "category", "price", "description", "is_active"),
        }),
        ("تصویر محصول", {
            "fields": ("image", "preview"),
            "description": "اگر عکس آپلود نشود، از نماد پیش‌فرض استفاده می‌شود.",
        }),
        ("حالت پیش‌فرض (وقتی عکس خالی است)", {
            "fields": ("image_symbol", "css_class"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="تصویر")
    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:44px;height:44px;object-fit:cover;'
                'border-radius:8px;border:1px solid #333;" />',
                obj.image.url,
            )
        return format_html(
            '<span style="display:inline-grid;place-items:center;'
            'width:44px;height:44px;background:#1a1f28;border-radius:8px;'
            'color:#4ade80;font-size:20px;border:1px solid #333;">{}</span>',
            obj.image_symbol,
        )

    @admin.display(description="دارای عکس؟", boolean=True)
    def has_image_badge(self, obj):
        return obj.has_image

    @admin.display(description="پیش‌نمایش")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:280px;max-height:280px;'
                'border-radius:12px;border:1px solid #333;" />',
                obj.image.url,
            )
        return "—"