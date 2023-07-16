from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from yanki import settings
from clothes.utilits.authenticate.authenticate import AuthenticateMixin
from .forms import get_cities
from .set_session_data.Others import Set_local_data
from .set_session_data.currency import Currency
from .set_session_data.like import Like
from .utilits.GlobalSearch import ClothesSearch
from .views import *


urlpatterns = [
                  path("", ClothesHome.as_view(), name="home"),
                  path("catalog/", ClothesCatalog.as_view(), name="catalog"),
                  path("catalog/<slug:category>/", ClothesCatalog.as_view(), name="category"),
                  path("catalog/<slug:category>/<slug:name>/", ClothesProduct.as_view(), name="product"),
                  path("profile/history/", ClothesHistory.as_view(), name="history"),
                  path("profile/info/", ClothesInfo.as_view(), name="info"),
                  path("favorite/", ClothesFavorite.as_view(), name="favorite"),
                  path("logout/", LogoutView.as_view(), name="logout"),
                  path("cart/", ClothesCart.as_view(), name="cart"),
                  path("session/", Set_local_data.as_view(), name="session"),
                  path("authenticate/", AuthenticateMixin.as_view(), name="authenticate"),
                  path("search/", ClothesSearch.as_view(), name="search"),
                  path("currency/", Currency.as_view(), name="authenticate"),
                  path("like/", Like.as_view(), name="like"),
                  path("about_info/", ClothesAbout.as_view(), name="about"),
                path("cities/", get_cities, name="cities")


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
