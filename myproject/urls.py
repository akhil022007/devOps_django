cat > urls.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
# Press Ctrl+D (or Ctrl+Z then Enter on Windows) here