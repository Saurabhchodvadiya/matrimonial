"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("profiles/", include(("profiles.urls", "profiles"), namespace="profiles")),
    path("matching/", include(("matching.urls", "matching"), namespace="matching")),
    path("interests/", include(("interests.urls", "interests"), namespace="interests")),
    path("shortlists/", include(("shortlists.urls", "shortlists"), namespace="shortlists")),
    path("search/", include(("search.urls", "search"), namespace="search")),
    path("reports/", include(("reports.urls", "reports"), namespace="reports")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
