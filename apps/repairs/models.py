from django.db import models
from apps.core.models import TimeStampedUUIDModel


class RepairStatus(models.TextChoices):
    RECEIVED = "received", "دریافت شده"
    INSPECTING = "inspecting", "در حال بررسی"
    REPAIRING = "repairing", "در حال تعمیر"
    READY = "ready", "آماده تحویل"
    DELIVERED = "delivered", "تحویل داده شده"


class RepairOrder(TimeStampedUUIDModel):
    customer_name = models.CharField(max_length=120, verbose_name="نام مشتری")
    phone = models.CharField(max_length=15, db_index=True, verbose_name="شماره موبایل")
    device_model = models.CharField(max_length=120, blank=True, verbose_name="مدل دستگاه")
    status = models.CharField(
        max_length=20,
        choices=RepairStatus.choices,
        default=RepairStatus.RECEIVED,
        db_index=True,
        verbose_name="وضعیت",
    )
    estimated_delivery = models.DateTimeField(null=True, blank=True, verbose_name="تحویل تقریبی")
    notes = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "سفارش تعمیر"
        verbose_name_plural = "سفارش‌های تعمیر"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["phone", "-created_at"])]

    def __str__(self):
        return f"#{str(self.id)[:8]} - {self.customer_name}"

    @property
    def status_index(self):
        order = [c[0] for c in RepairStatus.choices]
        return order.index(self.status)

    @property
    def progress_percent(self):
        return int((self.status_index + 1) / len(RepairStatus.choices) * 100)
