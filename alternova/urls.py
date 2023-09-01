from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Alternova API",
      default_version='v1',
      description="This API was created with the purpose of responding to the requirements requested for the development of the technical test of Alternova, an API that simulates a streaming platform",
      contact=openapi.Contact(email="mapg012000@hotmail.com"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/movies/',  include('movies.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
