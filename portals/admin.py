from django.contrib import admin

from .models import (
    VeterinaryBilling,
    Deworming,
    ArtificialInsemination,
    PregnancyDiagnosis,
    FarmConsultation,
    Referral,
    Question,
    Choice,
)
class AnswerAdmin(admin.StackedInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(VeterinaryBilling)
admin.site.register(Deworming)
admin.site.register(ArtificialInsemination)
admin.site.register(PregnancyDiagnosis)
admin.site.register(FarmConsultation)
admin.site.register(Referral)