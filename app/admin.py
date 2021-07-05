from django.contrib import admin


from .models import Usina, Bloco, NrVolCoeff, NrXcgCoeff, BlocoData


@admin.register(Usina)
class UsinaAdmin(admin.ModelAdmin):
    pass


class NrVolCoeffInline(admin.TabularInline):
    model = NrVolCoeff
    # garantir que o modelo requeira nr_coeff antes de ser salvo
    extra = 1
    min_num = 1
    max_num = 1
    can_delete = False


class NrXcgCoeffInline(admin.TabularInline):
    model = NrXcgCoeff
    # garantir que o modelo requeira xcg_coeff antes de ser salvo
    extra = 1
    min_num = 1
    max_num = 1
    can_delete = False


@admin.register(Bloco)
class BlocoAdmin(admin.ModelAdmin):
    inlines = [NrVolCoeffInline, NrXcgCoeffInline]
    exclude = ('nr_vol_coeff', 'nr_xcg_coeff')


@admin.register(BlocoData)
class BlocoDataAdmin(admin.ModelAdmin):
    list_display = ('nome_display', 'data', 'nr', 'pzm', 'pzj', 'pzi')

    @admin.display(description='Nome')
    def nome_display(self, obj):
        return obj.__str__()
