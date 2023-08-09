from .models import *
from users.models import *
from modeltranslation.translator import register, TranslationOptions


@register(Catalog)
class CatalogTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(BaseProduct)
class BaseProductTranslationOptions(TranslationOptions):
    fields = ("title", "info", "composition", "care")


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("title", )


@register(Size)
class TagTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Color)
class TagTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(User)
class TagTranslationOptions(TranslationOptions):
    fields = ("first_name", "last_name", "city", "post_office")


