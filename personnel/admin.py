from unfold.admin import ModelAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin import register
from personnel.models import Projet, Candidature, Affectation, Poste
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm


from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
 
 
@register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email_link', 'is_staff', 'is_active')

    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    email_link.short_description = 'Email'

# Register your models here.

@register(Projet)
class AdminProjet(ModelAdmin, ImportExportModelAdmin):
    list_display=('nom','description','objectif')
    # filter_horizontal = ("candidature",)
    import_form_class = ImportForm
    export_form_class = ExportForm
# admin.site.register(Projet,AdminProjet)


@register(Candidature)
class AdminCandidature(ModelAdmin,ImportExportModelAdmin):
    list_display=('nom','prenom','email_link','telephone','localisation','statut')
    list_per_page = 10
    fieldsets = [
        ("Information personnel", {"fields": ["photo",'nom','prenom','email','localisation']}),
        ("Media", {"fields": ["cv",'lettre_motivation']}),
        (None, {"fields": ["statut"]}),]
    search_fields = ["nom"]
    list_filter = ["statut"]
    # filter_horizontal = ("projet",)
    def email_link(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    email_link.short_description = 'Email'
    import_form_class = ImportForm
    export_form_class = ExportForm
# admin.site.register(Candidature,AdminCandidature)


@register(Affectation)
class AdminAffectation(ModelAdmin):
    list_display=('projet','poste')
    list_per_page = 10
    filter_horizontal = ("candidature",)
    list_filter = ("projet","poste")
# admin.site.register(Affectation,AdminAffectation)
    
@register(Poste)
class AdminPoste(ModelAdmin):
    list_display=('nom','description')
    # filter_horizontal = ("candidature",)
# admin.site.register(Poste,AdminPoste)
