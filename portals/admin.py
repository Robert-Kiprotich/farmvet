from django.contrib import admin

from .models import (
    VeterinaryBilling,
    Deworming,
    ArtificialInsemination,
    PregnancyDiagnosis,
    FarmConsultation,
    Referral,
    Question,
    CpdQuestions,
    Choice,
    CpdChoices,
    Section,
    Tutorial,
)
class AnswerAdmin(admin.StackedInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]
    
class CpdAnswersAdmin(admin.StackedInline):
    model = CpdChoices

class CpdQuestionsAdmin(admin.ModelAdmin):
    inlines = [CpdAnswersAdmin]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(CpdQuestions, CpdQuestionsAdmin)
admin.site.register(CpdChoices)
admin.site.register(VeterinaryBilling)
admin.site.register(Deworming)
admin.site.register(ArtificialInsemination)
admin.site.register(PregnancyDiagnosis)
admin.site.register(FarmConsultation)
admin.site.register(Referral)
admin.site.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('lesson', 'user__username', 'kvb_number')
    actions = ['activate_tutorials', 'deactivate_tutorials']

def activate_tutorials(modeladmin, request, queryset):
    queryset.update(is_active=True)
    modeladmin.message_user(request, f"{queryset.count()} tutorial(s) activated successfully.")

def deactivate_tutorials(modeladmin, request, queryset):
    queryset.update(is_active=False)
    modeladmin.message_user(request, f"{queryset.count()} tutorial(s) deactivated successfully.")

# Register the actions globally for the Tutorial model
admin.site.add_action(activate_tutorials, "Activate selected tutorials")
admin.site.add_action(deactivate_tutorials, "Deactivate selected tutorials")
 
admin.site.   register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'file', 'content')
    search_fields = ('title',)  # This can stay or be adjusted as needed
    list_filter = ('lesson',)
    fields = ('lesson', 'title', 'content', 'file')
    autocomplete_fields = ('lesson',)  # Works with search_fields in TutorialAdmin
