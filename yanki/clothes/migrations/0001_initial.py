# Generated by Django 4.1.3 on 2023-03-05 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('info', models.TextField(blank=True)),
                ('composition', models.TextField(blank=True)),
                ('care', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Базовая Вещь',
                'verbose_name_plural': 'Базовые Вещи',
            },
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='image/catalog')),
            ],
            options={
                'verbose_name': 'Каталог',
                'verbose_name_plural': 'Каталог',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('hex', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image/products')),
                ('image_1', models.ImageField(blank=True, upload_to='image/products')),
                ('image_2', models.ImageField(blank=True, upload_to='image/products')),
                ('image_3', models.ImageField(blank=True, upload_to='image/products')),
                ('image_4', models.ImageField(blank=True, upload_to='image/products')),
                ('image_5', models.ImageField(blank=True, upload_to='image/products')),
                ('count', models.PositiveIntegerField(default=1)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothes.color')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='clothes.baseproduct')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothes.size')),
            ],
            options={
                'verbose_name': 'Вещь',
                'verbose_name_plural': 'Вещи',
            },
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='tags',
            field=models.ManyToManyField(blank=True, to='clothes.tag'),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothes.catalog'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('parent', 'color', 'size'), name='unique_product'),
        ),
    ]
