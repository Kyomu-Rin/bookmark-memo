from django.contrib  import admin
from django.urls     import path, include

urlpatterns = [
    path('admin_noname0326/',    admin.site.urls),
    path('',                     include('myapp.urls')),
]
