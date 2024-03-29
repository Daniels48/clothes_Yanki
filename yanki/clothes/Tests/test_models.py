from django.db import transaction
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from PIL import Image
from io import BytesIO
from clothes.models import *


class Test_Catalog(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.slug1 = "test_slug"
        cls.title1 = "test_title"
        cls.obj_catalog = Catalog.objects.create(title=cls.title1, slug=cls.slug1)

    # def setUp(self):
    #     self.slug1 = "test_slug"
    #     self.title1 = "test_title"
    #     self.obj_catalog = Catalog.objects.create(title=self.title1, slug=self.slug1)

    def test_length_title(self):
        title_false = "a" * 256
        self.assertEqual(Catalog.objects.count(), 1)

        with self.assertRaises(DataError):
            with transaction.atomic():
                Catalog.objects.create(title=title_false, slug="test2")

        self.assertEqual(Catalog.objects.count(), 1)

    def test_unique_slug(self):
        self.assertEqual(self.obj_catalog.slug, self.slug1)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Catalog.objects.create(title=self.title1, slug=self.slug1)

        self.assertEqual(Catalog.objects.count(), 1)

    def test_str(self):
        self.assertEqual(str(self.obj_catalog), self.title1)

    def test_url(self):
        self.assertEqual(self.obj_catalog.get_absolute_url(), f"/catalog/{self.slug1}/")

    def test_image(self):
        pass

    def tearDown(self):
        self.obj_catalog.delete()


# class Test_BaseProduct(BaseModelTest):
#     def test_specific(self):
#         self.common_model_tests(BaseProduct)


    # def create_temporary_image(self):
    #     image = Image.new('RGB', (100, 100), color='red')
    #     image_io = BytesIO()
    #     image.save(image_io, format='JPEG')
    #     image_io.seek(0)
    #     return image_io
    #
    # def test_image_field(self):
    #     image_io = self.create_temporary_image()
    #
    #     # Создаем объект MyClass с изображением для тестирования
    #     my_object = MyClass.objects.create(name="John", image=image_io, slug="john-doe")
    #
    #     # Проверяем, что изображение успешно загружено
    #     self.assertTrue(my_object.image)
    #
    #     # Проверяем, что изображение сохранено по указанному пути
    #     image_path = os.path.join('images', os.path.basename(my_object.image.name))
    #     self.assertTrue(os.path.exists(image_path))
