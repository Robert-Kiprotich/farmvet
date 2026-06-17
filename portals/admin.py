from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import requests

from .views import get_valid_access_token

from .models import (
    ApprovedDairyFarm,
    Question,
    CpdQuestions,
    Moderator,
    CpdChoices,
    Section,
    Tutorial,
    Attempt,
    UserRetake,
    ZoomMeeting,
    LessonPurchase,
    Payment,
)


# =========================================
# ZOOM MEETING ADMIN
# =========================================

@admin.register(ZoomMeeting)
class ZoomMeetingAdmin(admin.ModelAdmin):

    change_list_template = "admin/zoom_changelist.html"

    list_display = (
        "topic",
        "facilitator",
        "price",
        "start_time",
        "access_enabled",
        "user",
    )

    list_filter = (
        "access_enabled",
        "start_time",
    )
    filter_horizontal = ("blocked_users",)    
    search_fields = (
        "topic",
        "meeting_id",
    )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "schedule/",
                self.admin_site.admin_view(self.schedule_zoom),
                name="schedule_zoom",
            ),
        ]

        return custom_urls + urls

    def schedule_zoom(self, request):

        access_token = get_valid_access_token(request.user)

        if not access_token:
            messages.warning(
                request,
                "Please authenticate with Zoom before scheduling a meeting."
            )
            return redirect("zoom-auth")

        if request.method == "POST":

            topic = request.POST.get("topic")
            start_time = request.POST.get("start_time")
            price = request.POST.get("price")
            facilitator = request.POST.get("facilitator")

            from decimal import Decimal

            try:
                price = Decimal(price)
            except:
                price = Decimal("0.00")

            url = "https://api.zoom.us/v2/users/me/meetings"

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }

            payload = {
                "topic": topic,
                "type": 2,
                "start_time": start_time,
                "duration": 30,
                "timezone": "Africa/Nairobi",
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload
            )

            if response.status_code == 201:

                meeting = response.json()

                ZoomMeeting.objects.create(
                    user=request.user,
                    facilitator=facilitator or request.user.get_full_name(),
                    meeting_id=meeting["id"],
                    topic=meeting["topic"],
                    price=price,
                    start_time=meeting["start_time"],
                    join_url=meeting["join_url"],
                    access_enabled=True,
                )

                messages.success(
                    request,
                    "Zoom meeting created successfully."
                )

                return redirect("/admin/portals/zoommeeting/")

            messages.error(
                request,
                f"Zoom API Error: {response.text}"
            )

            return redirect(request.path)

        return render(
            request,
            "admin/schedule_meeting.html"
        )

    def save_model(self, request, obj, form, change):

        old_obj = None

        if change:
            old_obj = ZoomMeeting.objects.get(pk=obj.pk)

        super().save_model(request, obj, form, change)

        # OPTIONAL LOGGING ONLY (NO PAYMENT UPDATE)
        if old_obj and old_obj.access_enabled and not obj.access_enabled:

            messages.warning(
                request,
                "Meeting access disabled. Blocked users cannot join."
            )
       


# =========================================
# CUSTOM AUTOCOMPLETE
# =========================================

class CustomAutocompleteJsonView(AutocompleteJsonView):

    def __init__(self, model_admin=None, **kwargs):
        self.model_admin = model_admin
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):

        try:
            return super().get(request, *args, **kwargs)

        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=400
            )


# =========================================
# MODERATOR ADMIN
# =========================================

@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):

    list_display = ("name",)

    search_fields = ("name",)

    def save_model(self, request, obj, form, change):

        if Moderator.objects.filter(name=obj.name).exists():

            raise ValidationError(
                f"A moderator with the name '{obj.name}' already exists."
            )

        super().save_model(request, obj, form, change)


# =========================================
# QUESTION ADMIN
# =========================================

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "text",
        "moderator",
        "correct_answer"
    )

    list_filter = (
        "correct_answer",
        "moderator"
    )

    search_fields = (
        "text",
        "moderator__name"
    )

    autocomplete_fields = ("moderator",)

    fieldsets = (
        (
            "Question Details",
            {
                "fields": (
                    "moderator",
                    "text",
                )
            }
        ),
        (
            "Options",
            {
                "fields": (
                    "option_a",
                    "option_b",
                    "option_c",
                    "option_d",
                    "correct_answer",
                )
            }
        ),
    )


# =========================================
# USER RETAKE ADMIN
# =========================================

@admin.register(UserRetake)
class UserRetakeAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "retakes_left"
    )

    actions = ["reset_retakes"]

    def reset_retakes(self, request, queryset):

        for user_retake in queryset:
            user_retake.reset_retakes()

        self.message_user(
            request,
            "Retakes reset successfully."
        )


# =========================================
# CPD ADMIN
# =========================================

class CpdAnswersAdmin(admin.StackedInline):

    model = CpdChoices


@admin.register(CpdQuestions)
class CpdQuestionsAdmin(admin.ModelAdmin):

    inlines = [CpdAnswersAdmin]


# =========================================
# TUTORIAL ADMIN
# =========================================

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):

    list_display = (
        "lesson",
        "user",
        "unit_price",
        "start",
        "stop",
        "points",
        "created_at",
    )

    list_filter = ("created_at",)

    search_fields = (
        "lesson",
        "user__username",
        "cpd_number",
    )


# =========================================
# PAYMENT PROXY MODELS
# =========================================

class ZoomPayment(Payment):

    class Meta:
        proxy = True
        verbose_name = "Zoom Payment"
        verbose_name_plural = "Zoom Payments"


class LessonPayment(Payment):

    class Meta:
        proxy = True
        verbose_name = "Lesson Payment"
        verbose_name_plural = "Lesson Payments"


# =========================================
# BASE PAYMENT ADMIN
# =========================================

class BasePaymentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "zoom_meeting",
        "lesson",
        "amount",
        "status",
        "user_access_enabled",
        "mpesa_receipt",
        "created_at",
    )

    list_filter = (
        "status",
        "user_access_enabled",
        "created_at",
    )

    search_fields = (
        "user__username",
        "mpesa_receipt",
        "checkout_request_id",
    )

    actions = [
        "mark_completed",
        "mark_failed",
        "enable_user_access",
        "disable_user_access",
    ]

    # =========================================
    # ACTIONS
    # =========================================

    def mark_completed(self, request, queryset):
        queryset.update(status="Completed")

    def mark_failed(self, request, queryset):
        queryset.update(status="Failed")

    def enable_user_access(self, request, queryset):
        queryset.update(user_access_enabled=True)

    def disable_user_access(self, request, queryset):
        queryset.update(user_access_enabled=False)

# =========================================
# MAIN PAYMENT ADMIN
# =========================================

@admin.register(Payment)
class MainPaymentAdmin(BasePaymentAdmin):

    pass


# =========================================
# ZOOM PAYMENT ADMIN
# =========================================

@admin.register(ZoomPayment)
class ZoomPaymentAdmin(BasePaymentAdmin):

    list_display = (
        "user",
        "zoom_meeting",
        "amount",
        "status",
        "mpesa_receipt",
        "created_at",
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        return qs.filter(
            zoom_meeting__isnull=False
        )


# =========================================
# LESSON PAYMENT ADMIN
# =========================================

@admin.register(LessonPayment)
class LessonPaymentAdmin(BasePaymentAdmin):

    list_display = (
        "user",
        "lesson",
        "amount",
        "status",
        "mpesa_receipt",
        "created_at",
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        return qs.filter(
            lesson__isnull=False
        )

# =========================================
# LESSON PURCHASE ADMIN
# =========================================

@admin.register(LessonPurchase)
class LessonPurchaseAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "lesson",
        "payment",
        "purchased_at",
    )


# =========================================
# SECTION ADMIN
# =========================================

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "lesson",
        "created_at",
    )


# =========================================
# OTHER MODELS
# =========================================

admin.site.register(Attempt)
admin.site.register(CpdChoices)
admin.site.register(ApprovedDairyFarm)