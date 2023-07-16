from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse


class Catalog(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to="image/catalog", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Каталог"
        verbose_name_plural = "Каталог"
        # ordering = ['id', ]

    def get_absolute_url(self):
        return reverse("category", kwargs={"category": self.slug})


class BaseProduct(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    type = models.ForeignKey("Catalog", on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    info = models.TextField(blank=True)
    composition = models.TextField(blank=True)
    care = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Базовая Вещь"
        verbose_name_plural = "Базовые Вещи"

    def get_absolute_url(self):
        return reverse("product", kwargs={"category": self.type.slug, "name": self.slug})


class Product(models.Model):
    parent = models.ForeignKey("BaseProduct", related_name="products", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image/products")
    image_1 = models.ImageField(upload_to="image/products", blank=True)
    image_2 = models.ImageField(upload_to="image/products", blank=True)
    image_3 = models.ImageField(upload_to="image/products", blank=True)
    image_4 = models.ImageField(upload_to="image/products", blank=True)
    image_5 = models.ImageField(upload_to="image/products", blank=True)
    size = models.ForeignKey("Size", on_delete=models.CASCADE)
    color = models.ForeignKey("Color", on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"
        #unique_together = ('parent', "color", "size")
        constraints = [
            UniqueConstraint(fields=['parent', 'color', "size"], name='unique_product')
        ]


class Tag(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        # ordering = ['id', 'title']

    def get_absolute_url(self):
        return reverse("category", kwargs={"category": self.slug})


class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"
        ordering = ['id']


class Color(models.Model):
    title = models.CharField(max_length=150)
    hex = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"
        ordering = ['id']


