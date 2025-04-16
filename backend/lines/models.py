import uuid
from django.db import models
from django.urls import reverse


class Counters(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    time = models.DateTimeField()
    lengths = models.TextField(blank=True, null=True)  # This field type is a guess.
    connection_counters = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'counters'
        verbose_name = 'Счетчик'
        verbose_name_plural = 'Счетчики'

    def __str__(self):
        return str(self.time)


class LinesStatistics(models.Model):
    # id = models.IntegerField(primary_key=True, editable=False)
    date = models.DateTimeField()
    made_kabel = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lines_statistics'
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'

    def __str__(self):
        return str(self.date)


class Lines(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    line_number = models.IntegerField(unique=True)
    name = models.CharField(unique=True, max_length=1)
    pseudonym = models.CharField(unique=True, max_length=1)
    port = models.CharField(max_length=1)
    modbus_adr = models.IntegerField()
    department = models.IntegerField()
    number_of_display = models.IntegerField()
    cable_number = models.IntegerField()
    cable_connection_number = models.IntegerField()
    k = models.FloatField()
    created_dt = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lines'
        verbose_name = 'Линия'
        verbose_name_plural = 'Линии'

    def __str__(self):
        return f'{self.id} - {self.name} - {self.pseudonym}'

    def get_absolute_url(self):
        return reverse('line', kwargs={'line_number': self.line_number})


class LinesCurrentParams(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    line_number = models.IntegerField(blank=True, null=True, unique=True)
    connection_counter = models.BooleanField(blank=True, null=True)
    indicator_value = models.IntegerField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    speed_line = models.FloatField(blank=True, null=True)
    updated_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lines_current_params'
        verbose_name = 'Текущий параметр'
        verbose_name_plural = 'Текущие параметры'

    def __str__(self):
        return f'{self.id}'
