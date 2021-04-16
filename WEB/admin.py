from django.contrib import admin

from . models import Reto
admin.site.register(Reto)
from . models import Sesion
admin.site.register(Sesion)


from . models import Usuario

from . models import Try
from . models import Day
# Register your models here.


admin.site.register(Usuario)

admin.site.register(Try)
admin.site.register(Day)
