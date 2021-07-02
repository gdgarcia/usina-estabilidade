from django.contrib import admin


from .models import Usina, Bloco, NrVolCoeff, NrXcgCoeff, BlocoData


@admin.register(Usina)
class UsinaAdmin(admin.ModelAdmin):
    pass


class NrVolCoeffInline(admin.TabularInline):
    model = NrVolCoeff
    extra = 0


class NrXcgCoeffInline(admin.TabularInline):
    model = NrXcgCoeff
    extra = 0


@admin.register(Bloco)
class BlocoAdmin(admin.ModelAdmin):
    inlines = [NrVolCoeffInline, NrXcgCoeffInline]


@admin.register(BlocoData)
class BlocoDataAdmin(admin.ModelAdmin):
    list_display = ('nome_display', 'data', 'nr', 'pzm', 'pzj', 'pzi')

    @admin.display(description='Nome')
    def nome_display(self, obj):
        return obj.__str__()
