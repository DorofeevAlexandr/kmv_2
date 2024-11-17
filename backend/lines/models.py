from django.db import models


class Counters(models.Model):
    time = models.DateTimeField()
    lengths = models.TextField(blank=True, null=True)  # This field type is a guess.
    connection_counters = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'counters'



class Lines(models.Model):
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


class LinesCurrentParams(models.Model):
    id = models.ForeignKey(Lines, models.DO_NOTHING, db_column='id', blank=True, null=True)
    no_connection_counter = models.BooleanField(blank=True, null=True)
    indicator_value = models.IntegerField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    speed_line = models.FloatField(blank=True, null=True)
    updated_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lines_current_params'


