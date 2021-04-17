from django.contrib import admin

from . models import Sesion
from . models import Usuario
from . models import Try
from . models import Day


admin.site.register(Usuario)
admin.site.register(Sesion)
admin.site.register(Try)
admin.site.register(Day)
