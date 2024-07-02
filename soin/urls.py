from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from portals import views as portal_views  
from portals.views import *
from portals.monitoring import *



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
    path('gallerypdf/', portal_views.display_images, name='display-images'),
    ##calf
    path('calf', portal_views.calf, name='calf'),
    path('calves-list', CalfList.as_view(), name='calves-list'),
    path('calves/create/',CalfCreate.as_view(), name='add_calf'),
    path('calves/update/<int:pk>/',CalfUpdate.as_view(), name='edit_calf'),
    path('calves/delete/<int:pk>/', CalfDelete.as_view(), name='remove_calf'),

# dead animal
    path('dead_animal/', portal_views.dead_animal, name='dead_animal'),
    path('dead-animal-list/', DeadAnimalList.as_view(), name='dead-animal-list'),
    path('dead-animal/create/', DeadAnimalCreate.as_view(), name='add-dead-animal'),
    path('dead-animal/update/<int:pk>/', DeadAnimalUpdate.as_view(), name='update_dead_animal'),
    path('dead-animal/delete/<int:pk>/', DeadAnimalDelete.as_view(), name='delete_dead_animal'),

# Culling
    path('culling/', portal_views.culling, name='culling'),
    path('culling-list/', CullingList.as_view(), name='culling-list'),
    path('culling/create/',  CullingCreate.as_view(), name='create_culling'),
    path('culling/update/<int:pk>/', CullingUpdate.as_view(), name='update_culling'),
    path('culling/delete/<int:pk>/', CullingDelete.as_view(), name='delete_culling'),
#  new animal
    path('new_animal/', portal_views.new_animal, name='new_animal'),
    path('new-animal-list/', NewAnimalList.as_view(), name='new-animal-list'),
    path('new-animal/create/', NewAnimalCreate.as_view(), name='add-new-animal'),
    path('new-animal/update/<int:pk>/',  NewAnimalUpdate.as_view(), name='edit-new-animal'),
    path('new-animal/delete/<int:pk>/', NewAnimalDelete.as_view(), name='remove-new-animal'),

# livestock inventory
    path('livestock/', portal_views.livestock, name='livestock'),
    path('livestock-list/',LivestockList.as_view(), name='livestock-list'),
    path('livestock/create/', LivestockCreate.as_view(), name='add-livestock'),
    path('livestock/update/<int:pk>/', LivestockUpdate.as_view(), name='edit-livestock'),
    path('livestock/delete/<int:pk>/', LivestockDelete.as_view(), name='remove-livestock'),

#sales of stock

    path('animal_sales/', portal_views.animal_sales, name='animal_sales'),
    path('animal-sales-list/', AnimalSaleList.as_view(), name='animal-sales-list'),
    path('animal-sales/create/', AnimalSaleCreate.as_view(), name='add-animal-sale'),
    path('animal-sales/update/<int:pk>/', AnimalSaleUpdate.as_view(), name='edit-animal-sale'),
    path('animal-sales/delete/<int:pk>/', AnimalSaleDelete.as_view(), name='delete-animal-sale'),
   
    path('heat-sign-monitoring/', portal_views.heat_sign_monitoring, name='heat_sign_monitoring'),
    path('heat-sign-monitoring-list/', HeatSignMonitoringList.as_view(), name='heat-sign-monitoring-list'),
    path('heat-sign-monitoring/create/', HeatSignMonitoringCreate.as_view(), name='add-heat-sign-monitoring'),
    path('heat-sign-monitoring/update/<int:pk>/', HeatSignMonitoringUpdate.as_view(), name='edit-heat-sign-monitoring'),
    path('heat-sign-monitoring/delete/<int:pk>/', HeatSignMonitoringDelete.as_view(), name='remove-heat-signmonitoring'),

    path('pregnancy-monitoring/', portal_views.pregnancy_monitoring, name='pregnancy_monitoring'),
    path('pregnancy-monitoring-list/', PregnancyMonitoringList.as_view(), name='pregnancy-monitoring-list'),
    path('pregnancy-monitoring/create/', PregnancyMonitoringCreate.as_view(), name='pregnancy-monitoring-create'),
    # path('pregnancy-monitoring/<int:pk>/', PregnancyMonitoringDetail.as_view(), name='pregnancy-monitoring-detail'),
    path('pregnancy-monitoring/update/<int:pk>/', PregnancyMonitoringUpdate.as_view(), name='pregnancy-monitoring-update'),
    path('pregnancy-monitoring/delete/<int:pk>/', PregnancyMonitoringDelete.as_view(), name='pregnancy-monitoring-delete'),


    #FEEDS
    path('feeds/', portal_views.feeds, name='feeds'),
    path('feeds-list/', FeedsList.as_view(), name='feeds-list'),
    path('feeds/create/', FeedsCreate.as_view(), name='feeds-create'),
    # path('pregnancy-monitoring/<int:pk>/', PregnancyMonitoringDetail.as_view(), name='pregnancy-monitoring-detail'),
    path('feeds/update/<int:pk>/',FeedsUpdate.as_view(), name='feeds-update'),
    path('feeds/delete/<int:pk>/', FeedsDelete.as_view(), name='feeds-delete'),

    path('equipment/', portal_views.equipment, name='dairy_equipment'),
    path('dairy-equipment/create/', DairyEquipmentCreate.as_view(), name='dairy_equipment_create'),
    path('dairy-equipment-list/', DairyEquipmentList.as_view(), name='dairy-equipment-list'),
    path('dairy-equipment/update/<int:pk>/', DairyEquipmentUpdate.as_view(), name='dairy_equipment_update'),
    path('dairy-equipment/delete/<int:pk>/', DairyEquipmentDelete.as_view(), name='dairy_equipment_delete'),

    # DairyHygiene URLs
    path('hygiene/', portal_views.hygiene, name='hygiene'),
    path('dairy-hygiene/create/', DairyHygieneCreate.as_view(), name='dairy_hygiene_create'),
    path('dairy-hygiene-list/', DairyHygieneList.as_view(), name='dairy-hygiene-list'),
    path('dairy-hygiene/update/<int:pk>/', DairyHygieneUpdate.as_view(), name='dairy_hygiene_update'),
    path('dairy-hygiene/delete/<int:pk>/', DairyHygieneDelete.as_view(), name='dairy_hygiene_delete'),

    # Salaries URLs
    path('salaries/', portal_views.salaries, name='salaries'),
    path('salaries/create/', SalariesCreate.as_view(), name='salaries_create'),
    path('salaries-list/', SalariesList.as_view(), name='salaries-list'),
    path('salaries/update/<int:pk>/', SalariesUpdate.as_view(), name='salaries_update'),
    path('salaries/delete/<int:pk>/', SalariesDelete.as_view(), name='salaries_delete'),

    # LivestockInsurance URLs
    path('insurance/', portal_views.insurance, name='insurance'),
    path('livestock-insurance/create/', LivestockInsuranceCreate.as_view(), name='livestock_insurance_create'),
    path('livestock-insurance-list/', LivestockInsuranceList.as_view(), name='livestock-insurance-list'),
    path('livestock-insurance/update/<int:pk>/', LivestockInsuranceUpdate.as_view(), name='livestock_insurance_update'),
    path('livestock-insurance/delete/<int:pk>/', LivestockInsuranceDelete.as_view(), name='livestock_insurance_delete'),

    # VeterinaryDrugs URLs
    path('drugs/', portal_views.drugs, name='drugs'),
    path('veterinary-drugs/create/', VeterinaryDrugsCreate.as_view(), name='veterinary_drugs_create'),
    path('veterinary-drugs-list/', VeterinaryDrugsList.as_view(), name='veterinary-drugs-list'),
    path('veterinary-drugs/update/<int:pk>/', VeterinaryDrugsUpdate.as_view(), name='veterinary_drugs_update'),
    path('veterinary-drugs/delete/<int:pk>/', VeterinaryDrugsDelete.as_view(), name='veterinary_drugs_delete'),


     # Archaricides URLs
    path('archaricides/', portal_views.archaricides, name='archaricides'),
    path('archaricides/create/', ArcharicidesCreate.as_view(), name='archaricides_create'),
    path('archaricides-list/', ArcharicidesList.as_view(), name='archaricides-list'),
    path('archaricides/update/<int:pk>/', ArcharicidesUpdate.as_view(), name='archaricides_update'),
    path('archaricides/delete/<int:pk>/', ArcharicidesDelete.as_view(), name='archaricides_delete'),

    path('minerals/', portal_views.minerals, name='minerals'),
    path('minerals/create/', MineralsCreate.as_view(), name='minerals_create'),
    path('minerals-list/', MineralsList.as_view(), name='minerals-list'),
    path('minerals/update/<int:pk>/', MineralsUpdate.as_view(), name='minerals_update'),
    path('minerals/delete/<int:pk>', MineralsDelete.as_view(), name='minerals_delete'),


     # VeterinaryBills URLs
    path('bills/', portal_views.vet_bills, name='bills'),
    path('veterinary-bills/create/', VeterinaryBillsCreate.as_view(), name='veterinary_bills_create'),
    path('veterinary-bills/', VeterinaryBillsList.as_view(), name='veterinary-bills-list'),
    path('veterinary-bills/update/<int:pk>/', VeterinaryBillsUpdate.as_view(), name='veterinary_bills_update'),
    path('veterinary-bills/delete/<int:pk>/', VeterinaryBillsDelete.as_view(), name='veterinary_bills_delete'),

    path('add-gestation/', portal_views.add_gestation, name='add_gestation'),
    path('gestation-detail/', portal_views.gestation_detail, name='gestation_detail'),
    path('gestation/', portal_views.gestation, name='gestation'),

    # pdf notes
    path('notes/', portal_views.pdf_notes, name='notes'),


     path('employees/', portal_views.employees, name='employees'),
    path('employees/create/', EmployeesCreate.as_view(), name='employees_create'),
    path('employees-list/', EmployeesList.as_view(), name='employees-list'),
    path('employees/update/<int:pk>/', EmployeesUpdate.as_view(), name='employees_update'),
    path('employees/delete/<int:pk>/', EmployeesDelete.as_view(), name='employees_delete'),

    path('lactation/', portal_views.lactation, name='lactation'),
    path('lactating-cows/create/', LactatingCowCreate.as_view(), name='lactatingcow-create'),
    path('lactating-cows/', LactatingCowList.as_view(), name='lactatingcow-list'),
    path('lactating-cows/update/<int:pk>/', LactatingCowUpdate.as_view(), name='lactatingcow-update'),
    path('lactating-cows/delete/<int:pk>/', LactatingCowDelete.as_view(), name='lactatingcow-delete'),


    path('milk-record/', portal_views.milk_record, name='milk-record'),
    path('milk-records/create/', MilkRecordCreate.as_view(), name='milkrecord-create'),
    path('milk-records/', MilkRecordList.as_view(), name='milkrecord-list'),
    path('milk-records/update/<int:pk>/', MilkRecordUpdate.as_view(), name='milkrecord-update'),
    path('milk-records/delete/<int:pk>/', MilkRecordDelete.as_view(), name='milkrecord-delete'),

    path('weekly-record/', portal_views.weekly_record, name='weekly-record'),
    path('weekly-milk-records/', WeeklyMilkRecordListView.as_view(), name='weekly-milk-record-list'),
    path('monthly-record/', portal_views.monthly_record, name='monthly-record'),
    path('monthly-milk-records/', MonthlyMilkRecordListView.as_view(), name='monthly-milk-record-list'),
    path('weekly-milk-records/delete/<int:pk>/', WeeklyMilkRecordDelete.as_view(), name='weeklymilkrecord-update'),
    path('monthly-milk-records/delete/<int:pk>/', MonthlyMilkRecordDelete.as_view(), name='monthlymilkrecord-delete'),

    path('sales-of-milk/', portal_views.sales_of_milk, name='sales_of_milk'),
    path('sales-of-milk/create/', SalesOfMilkCreate.as_view(), name='sales_of_milk_create'),
    path('sales-of-milk/list/', SalesOfMilkList.as_view(), name='sales_of_milk_list'),
    path('sales-of-milk/update/<int:pk>/', SalesOfMilkUpdate.as_view(), name='sales_of_milk_update'),
    path('sales-of-milk/delete/<int:pk>/', SalesOfMilkDelete.as_view(), name='sales_of_milk_delete'),


]   



 
if  not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)