"""online_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('search_page', views.searchPage, name = 'search'),
    path('promo_page', views.promoPage, name = 'promo'),
    path('favorite_page', views.favPage, name = 'favorit'),
    path('my_account', views.myAccountPage, name = 'account'),
    path('my_cart', views.myCart, name = 'cart'),
    path('detail', views.details, name = 'detail'),
    path('oAuth/',include(('loginSys.urls', 'loginSys'), namespace = 'oAuthLogged')),
    path('oAuthSell/', include(('sellerSide.urls', 'sellerSide'),namespace = 'home_seller')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)