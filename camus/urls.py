"""camus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt
from rest_framework.documentation import include_docs_urls
from django.views.static import serve
from camus.settings.base import BASE_MEDIA_CARD_DIR

API_TITLE = 'camus api documentation'
API_DESCRIPTION = 'camus api server for camus'

urlpatterns = [
    url(r'image/(?P<path>.*)$', serve, {'document_root': BASE_MEDIA_CARD_DIR}),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, authentication_classes=[],
                                    permission_classes=[])),
    path('', include('camus.case.urls')),
    path('', include('camus.project.urls')),
    path('', include('camus.camus_auth.urls')),
    path('', include('camus.tool.urls')),
    path('admin/', admin.site.urls),
    path('api/token', jwt.TokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh', jwt.TokenRefreshView.as_view(), name='refresh_token'),
]
