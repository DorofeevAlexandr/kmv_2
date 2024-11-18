from django.contrib import admin
from .models import Counters, Lines, LinesCurrentParams

@admin.register(Counters)
class CountersAdmin(admin.ModelAdmin):
    pass

@admin.register(Lines)
class LinesAdmin(admin.ModelAdmin):
    pass

@admin.register(LinesCurrentParams)
class LinesCurrentParamsAdmin(admin.ModelAdmin):
    pass
