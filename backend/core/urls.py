from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

API_VERSION = "^api/v1/"


urlpatterns = [
    url(
        f"{API_VERSION}token/$", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    url(
        f"{API_VERSION}token/refresh/$",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    url(
        f"{API_VERSION}accounts/",
        include(("accounts.urls", "accounts"), namespace="accounts"),
    ),
    url(f"{API_VERSION}getdata/", include(("base.urls", "base"), namespace="base")),
    url(r"admin/", admin.site.urls),
    url(r"health", include("health_check.urls")),
]
