from django.db import models
from apps.core.models import TimeStampedUUIDModel


class Category(models.TextChoices):
    PROTECTION = "protection", "محافظ صفحه"
    ACCESSORY = "accessory", "لوازم جانبی"
    AUDIO = "audio", "صوتی"


class Product(TimeStampedUUIDModel):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="اسلاگ")
    category = models.CharField(max_length=20, choices=Category.choices, verbose_name="دسته‌بندی")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="قیمت (تومان)")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    image_symbol = models.CharField(max_length=10, default="◈", verbose_name="نماد تصویری")
    css_class = models.CharField(max_length=40, default="product-glass", verbose_name="کلاس CSS تصویر")
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="عکس محصول",
        help_text="اگر خالی باشد، نماد پیش‌فرض نمایش داده می‌شود.",
    )
    image_symbol = models.CharField(max_length=10, default="◈", verbose_name="نماد پیش‌فرض")
    css_class = models.CharField(
        max_length=40, default="product-glass", verbose_name="کلاس CSS پس‌زمینه پیش‌فرض"
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["category", "is_active"])]

    def __str__(self):
        return self.name

    @property
    def has_image(self) -> bool:
        return bool(self.image and hasattr(self.image, "url"))