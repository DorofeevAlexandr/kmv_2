from django.contrib import admin
from .models import Counters, Lines, LinesCurrentParams

@admin.register(Counters)
class CountersAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('time', )
    # Фильтрация в списке
    list_filter = ('time',)
    # Поиск по полям
    search_fields = ('time',)

@admin.register(Lines)
class LinesAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('line_number', 'name', 'pseudonym', 'k')
    # Фильтрация в списке
    list_filter = ('line_number', 'pseudonym',)
    # Поиск по полям
    search_fields = ('line_number', 'pseudonym',)

@admin.register(LinesCurrentParams)
class LinesCurrentParamsAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('id', 'length', 'speed_line',)
    # Фильтрация в списке
    list_filter = ('id',)
    # Поиск по полям
    search_fields = ('id',)
