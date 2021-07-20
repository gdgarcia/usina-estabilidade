from django.contrib import admin

from .models import SensorData, BundleData


class SensorDataInline(admin.TabularInline):
    model = SensorData


@admin.register(BundleData)
class BundleDataAdmin(admin.ModelAdmin):
    inlines = [SensorDataInline]
