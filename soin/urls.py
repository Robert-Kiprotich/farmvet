from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from portals import views as portal_views


from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.contrib.auth import views as auth_views
app_name = 'portals'

urlpatterns = [
    path('', include('vet.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls, name='admin-vet'),
    #users sign up
    path('user/signup/vet_officer/', user_views.vet0fficer_signup_view, name='vet-register'),
    path('user/signup/farmer/',user_views.farmer_signup_view,name='farmer-register'),
    # path('user/signup/student/',user_views.student_signup_view,name='student-register'),
    #users login 
    path('vet/login/',user_views.vet_login,name='vet-login'),
    path('farmer/login/',user_views.farmer_login,name='farmer-login'),
    # path('student/login/',user_views.student_login,name='student-login'),
    path('logout/', user_views.user_logout, name='logout'),
    #password reset
    path("password-reset", auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="user/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_complete.html"), name="password_reset_complete"),

    #users portals
    path('vet_portal/', portal_views.portal_vet, name='vet-portal'),
    path('vet_list/', portal_views.vet_list, name='vet-list'),
    path('farmer_portal/', portal_views.portal_farmer, name='farmer-portal'),
    path('student_portal/', portal_views.portal_student, name='student-portal'),
    path('sickformview/',portal_views.sick_form_view,name='sickformview'),
    path('editsickform/<int:pk>/',portal_views.edit_sick_form,name='sickform-edit'),
    path('deathformview/',portal_views.dead_form_view,name='deadformview'),
    path('editdeadform/<int:pk>/',portal_views.edit_dead_form,name='deadform-edit'),
    path('surgicalformview/',portal_views.surgical_form_view,name='surgicalformview'),
    path('editsurgicalform/<int:pk>/',portal_views.edit_surgical_form,name='surgicalform-edit'),
    path('dewormingformview/',portal_views.deworming_form_view,name='dewormingformview'),
    path('editdewormingform/<int:pk>/',portal_views.edit_deworming_form,name='dewormingform-edit'),
    path('vaccinationformview/',portal_views.vaccination_form_view,name='vaccinationformview'),
    path('editvaccinationform/<int:pk>/',portal_views.edit_vaccination_form,name='vaccinationform-edit'),
    path('artificialformview/',portal_views.artificial_form_view,name='artificialformview'),
    path('editartificialform/<int:pk>/',portal_views.edit_artificial_form,name='artificialform-edit'),
    path('pregnancyformview/',portal_views.pregnancy_form_view,name='pregnancyformview'),
    path('editpregnancyform/<int:pk>/',portal_views.edit_pregnancy_form,name='pregnancyform-edit'),
    #vet forms
    path('clinical_approach/',portal_views.clinical_approach,name='clinical-approach'),
    path('sick_approach', portal_views.sick_approach, name='sick-approach'),
    path('dead_approach', portal_views.dead_approach, name='dead-approach'),
    path('surgical_approach',portal_views.surgical_approach, name='surgical-approach'),
    path('deworming',portal_views.deworming,name='deworming'),
    path('vaccination',portal_views.vaccination,name='vaccination'),
    path('breeding_record/',portal_views.breeding_record,name='breeding_record'),
    path('artificial_insemination', portal_views.artificial_insemination, name='artificial-insemination'),
    path('pregnancy_diagnosis',portal_views.pregnancy_diagnosis,name='pregnancy_diagnosis'),
    path('calf_registration', portal_views.calf_registration, name='calf-registration'),
    path('calfformview/',portal_views.calf_form_view,name='calfformview'),
    path('editcalfform/<int:pk>/',portal_views.edit_calf_registration,name='calfform-edit'),   
    path('livestock_inventory', portal_views.livestock_inventory, name='livestock-inventory'),
    path('livestockformview/',portal_views.livestock_inventory_view,name='livestockformview'),
    path('editlivestockform/<int:pk>/',portal_views.edit_livestock_inventory,name='livestockform-edit'),
    path('consultation',portal_views.consultation,name='consultation'),
    path('consultationformview/',portal_views.consultation_form_view,name='consultationformview'),
    path('editconsultationform/<int:pk>/',portal_views.edit_consultation_form,name='consultation-edit'),
    path('vetbilling',portal_views.vet_billing,name='vetbilling'),
    path('vetbillingformview/',portal_views.vet_billing_form_view,name='vetbillformview'),
    path('editvetbillingform/<int:pk>/',portal_views.edit_vet_billing_form,name='vetbill-edit'),
    path('laboratory',portal_views.lab,name='lab'),
    path('labformview/',portal_views.lab_form_view,name='labformview'),
    path('editlabform/<int:pk>/',portal_views.edit_lab_form,name='lab-edit'),  
    path('referral',portal_views.referral_form,name='referral'),
    path('referralformview/',portal_views.referral_form_view,name='referralformview'),
    path('editreferralform/<int:pk>/',portal_views.edit_referral_form,name='referral-edit'), 

    #reports
    path('artificial-report/', portal_views.artificial_report, name='artificial-report'), 
    path('artificial-report-data/', portal_views.artificial_report_data, name='artificial_report_data'),
    path('deworming-report/', portal_views.deworming_report, name='deworming-report'),
    path('deworming-report-data/', portal_views.deworming_report_data, name='deworming_report_data'),
    path('sick-report/', portal_views.sick_report, name='sick-report'),
    path('sick-report-data/', portal_views.sick_report_data, name='sick_approach_data'),
    path('death-report/',portal_views.death_report, name='death-report'),
    path('death-report-data/',portal_views.death_report_data, name='death_report_data'),
    path('vaccination-report/', portal_views.vaccination_report, name='vaccination-report'),
    path('vaccination-report-data/', portal_views.vaccination_report_data, name='vaccination_report_data'),
    path('pregnancy-report/', portal_views.pregnancy_diagnosis_report, name='pregnancy-report'),
    path('pregnancy-report-data/', portal_views.pregnancy_diagnosis_report_data, name='pregnancy_diagnosis_report_data'),
    path('farm-consultation/', portal_views.farm_consultation_report, name='farm-consultation'),
    path('farm-consultation-data/', portal_views.farm_consultation_report_data, name='farm_consultation_data'),
    path('veterinary-billing-report/', portal_views.veterinary_billing_report, name='veterinary-billing-report'),
    path('veterinary-billing-report-data/', portal_views.veterinary_billing_report_data, name='veterinary_billing_report_data'),
    path('laboratory-report/', portal_views.laboratory_report, name='laboratory-report'),
    path('laboratory-report-data/', portal_views.laboratory_report_data, name='laboratory_report_data'),
    path('referral-report/', portal_views.referral_report, name='referral-report'),
    path('referral-report-data/', portal_views.referral_report_data, name='referral_report_data'),
    path('livestock-inventory-report/', portal_views.livestock_inventory_report, name='livestock-inventory-report'),
    path('livestock-inventory-report-data/', portal_views.livestock_inventory_report_data, name='livestock_inventory_report_data'),
    path('surgical-report/', portal_views.surgical_report, name='surgical-report'),
    path('surgical-report-data/', portal_views.surgical_report_data, name='surgical-report-data'),
   
          
    
    #Farmer fetching forms pdf
    path('sickformpdf/', login_required(portal_views.sick_form_pdf), name='sickformpdf'),
    path('sickformvetpdf/', login_required(portal_views.Sick_Form_Pdf_Vet.as_view()), name='sickformvetpdf'),
    path('deadpdf/', login_required(portal_views.dead_form_pdf), name='deadformpdf'),
    path('deadformvetpdf/', login_required(portal_views.Dead_Form_Pdf_Vet.as_view()), name='deadformvetpdf'),
    path('surgicalformpdf/', login_required(portal_views.Surgical_Form_Pdf.as_view()), name='surgicalformpdf'),
    path('dewormingformpdf/', login_required(portal_views.Deworming_Form_Pdf.as_view()), name='dewormingformpdf'),
    path('artificialformpdf/', login_required(portal_views.Artificial_Insemination_Form_Pdf.as_view()), name='artificialformpdf'),
    path('vaccinationformpdf/', login_required(portal_views.Vaccination_Form_Pdf.as_view()), name='vaccinationformpdf'),
    #path('deadformpdf/', login_required(portal_views.Dead_Form_Pdf.as_view()), name='deadformpdf'),
    path('surgicalformpdf/', login_required(portal_views.Surgical_Form_Pdf.as_view()), name='surgicalformpdf'),
    path('dewormingformpdf/', login_required(portal_views.Deworming_Form_Pdf.as_view()), name='dewormingformpdf'),
    path('artificialformpdf/', login_required(portal_views.Artificial_Insemination_Form_Pdf.as_view()), name='artificialformpdf'),
    path('vaccinationpdf/', login_required(portal_views.Vaccination_Form_Pdf.as_view()), name='vaccinationformpdf'),
    path('consultationformpdf/', login_required(portal_views.Farm_Consultation_Form_Pdf.as_view()), name='consultationformpdf'),
    path('pregnancyformpdf/', login_required(portal_views.Pregnancy_Diagnosis_Form_Pdf.as_view()), name='pregnancyformpdf'),
    path('calfregformpdf/', login_required(portal_views.Calf_Registration_Form_Pdf.as_view()), name='calfregformpdf'),
    path('inventorypdf/', login_required(portal_views.Livestock_Form_Pdf.as_view()), name='inventoryformpdf'),
    path('referralpdf/', login_required(portal_views.referral_Form_Pdf.as_view()), name='referralformpdf'),
    path('gallerypdf/', portal_views.display_images, name='display-images')

]

if  not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)