from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from .models import (
   ApprovedDairyFarm, Question, CpdQuestions, Moderator, CpdChoices,
    Section, Tutorial, Attempt, UserRetake
)
class CustomAutocompleteJsonView(AutocompleteJsonView):
    def __init__(self, model_admin=None, **kwargs):
        self.model_admin = model_admin
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        # Check if a moderator with the same name already exists
        if Moderator.objects.filter(name=obj.name).exists():
            raise ValidationError(f"A moderator with the name '{obj.name}' already exists.")
        super().save_model(request, obj, form, change)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'moderator', 'correct_answer')
    list_filter = ('correct_answer', 'moderator')
    search_fields = ('text', 'moderator__name')
    fieldsets = (
        ('Question Details', {
            'fields': ('moderator', 'text')
        }),
        ('Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')
        }),
    )
    autocomplete_fields = ('moderator',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('autocomplete/', self.admin_site.admin_view(CustomAutocompleteJsonView.as_view(model_admin=self)), name='your_app_name_question_autocomplete'),
        ]
        return custom_urls + urls

@admin.register(UserRetake)
class UserRetakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'retakes_left')
    actions = ['reset_retakes']

    def reset_retakes(self, request, queryset):
        for user_retake in queryset:
            user_retake.reset_retakes()
        self.message_user(request, "Retakes have been reset to 3 for selected users.")

    reset_retakes.short_description = "Reset retakes to 3"

class CpdAnswersAdmin(admin.StackedInline):
    model = CpdChoices


class CpdQuestionsAdmin(admin.ModelAdmin):
    inlines = [CpdAnswersAdmin]




class TutorialAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('lesson', 'user__username', 'kvb_number')
    actions = ['activate_tutorials', 'deactivate_tutorials']

    def activate_tutorials(self, request, queryset):
        queryset.update(is_paid=True)
        self.message_user(request, f"{queryset.count()} tutorial(s) activated successfully.")

    def deactivate_tutorials(self, request, queryset):
        queryset.update(is_paid=False)
        self.message_user(request, f"{queryset.count()} tutorial(s) deactivated successfully.")



class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'file', 'content')
    search_fields = ('title',)
    list_filter = ('lesson',)
    fields = ('lesson', 'title', 'content', 'file')
    autocomplete_fields = ('lesson',)

    def get_urls(self):
        """
        Override get_urls to use the custom autocomplete view for the 'lesson' field.
        """
        urls = super().get_urls()
        custom_urls = [
            path('autocomplete/', self.admin_site.admin_view(CustomAutocompleteJsonView.as_view(model_admin=self)), name='your_app_name_section_autocomplete'),
        ]
        return custom_urls + urls
# Register other models
admin.site.register(Attempt)
admin.site.register(Question)
admin.site.register(Moderator)
admin.site.register(CpdChoices)
admin.site.register(ApprovedDairyFarm)
#admin.site.register(Deworming)
#admin.site.register(ArtificialInsemination)
#admin.site.register(PregnancyDiagnosis)
#admin.site.register(FarmConsultation)
#admin.site.register(Referral)
admin.site.register(Tutorial)
admin.site.register(Section)
admin.site.register(CpdQuestions)
