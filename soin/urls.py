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

def debug_view(request, *args, **kwargs):
    return HttpResponse(f"Args: {args}, Kwargs: {kwargs}")

urlpatterns = [
    path('debug/', debug_view, name='debug-view'),
    path('', include('vet.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls, name='admin-vet'),
    #users sign up
    path('user/signup/vet_officer/', user_views.vet0fficer_signup_view, name='vet-register'),
    path('user/signup/farmer/',user_views.farmer_signup_view,name='farmer-register'),
    path('user/signup/official/',user_views.Official_signup_view,name='official-register'),
    #users login 
    path('vet/login/',user_views.vet_login,name='vet-login'),
    path('farmer/login/',user_views.farmer_login,name='farmer-login'),
    path('official/login/',user_views.official_login,name='official-login'),
    path('logout/', user_views.user_logout, name='logout'),
    #password reset
    path("password-reset", auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="user/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_complete.html"), name="password_reset_complete"),

    #users portals
    path('vet_portal/', portal_views.portal_vet, name='vet-portal'),
    path('vet_list/', portal_views.vet_list, name='vet-list'),
    path('vet_list_vet/', portal_views.vet_list_vet, name='vet-list_vet'),
    path('farmer_portal/', portal_views.portal_farmer, name='farmer-portal'),
    path('official_portal/', portal_views.portal_official, name='official-portal'),

    
   
#################################FARMER  Urls######################################## 
   
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

    path('daily-milk/', portal_views.daily_record, name='daily-record'),
    path('daily-milk/list/', DailyMilkRecordList.as_view(), name='daily-milk-list'),
    path('daily-milk/delete/<int:pk>/', DailyMilkRecordDelete.as_view(), name='daily-delete'),


    #################  VET URLs###############################################
     #vet billing
    path('vet-billing/', portal_views.vetbilling, name='vet-billing'),
    path('vet-billing-view/', portal_views.vetbilling_view, name='vet-billing-view'),
    path('vet-billing/create/', VeterinaryBillingCreate.as_view(), name='vet-billing-create'),
    path('vet-billing/list/', VeterinaryBillingList.as_view(), name='vet-billing-list'),
    path('vet-billing/update/<int:pk>/', VeterinaryBillingUpdate.as_view(), name='vet-billing-update'),
    path('vet-billing/delete/<int:pk>/', VeterinaryBillingDelete.as_view(), name='vet-billing-delete'),

    # Deworming URLs
    path('deworming/', portal_views.deworming, name='deworming'),
    path('deworming-view/', portal_views.deworming_view, name='deworming-view'),
    path('deworming/create/', DewormingCreate.as_view(), name='deworming-create'),
    path('deworming/list/', DewormingList.as_view(), name='deworming-list'),
    path('deworming/update/<int:pk>/', DewormingUpdate.as_view(), name='deworming-update'),
    path('deworming/delete/<int:pk>/', DewormingDelete.as_view(), name='deworming-delete'),

    # Artificial Insemination URLs
    path('ai/', portal_views.artificial, name='ai'),
     path('ai-official/', portal_views.artificial_official_view, name='ai_official'),
    path('ai-view/', portal_views.artificial_view, name='ai-view'),
    path('artificial-insemination/create/', ArtificialInseminationCreate.as_view(), name='ai-create'),
    path('artificial-insemination/list/', ArtificialInseminationList.as_view(), name='ai-list'),
    path('artificial-insemination/update/<int:pk>/', ArtificialInseminationUpdate.as_view(), name='ai-update'),
    path('artificial-insemination/delete/<int:pk>/', ArtificialInseminationDelete.as_view(), name='ai-delete'),

    # Pregnancy Diagnosis URLs
    path('pregnanacy-diag/', portal_views.pregdiagnosis, name='pregnancy-diag'),
    path('pregnanacy-view/', portal_views.pregdiagnosis_view, name='pregnancy-view'),
    path('pregnancy-diagnosis/create/', PregnancyDiagnosisCreate.as_view(), name='pd-create'),
    path('pregnancy-diagnosis/list/', PregnancyDiagnosisList.as_view(), name='pd-list'),
    path('pregnancy-diagnosis/update/<int:pk>/', PregnancyDiagnosisUpdate.as_view(), name='pd-update'),
    path('pregnancy-diagnosis/delete/<int:pk>/', PregnancyDiagnosisDelete.as_view(), name='pd-delete'),

    # Farm Consultation URLs
    path('consultation/', portal_views.consultation, name='consultation'),
    path('consultation-view/', portal_views.consultation_view, name='consultation-view'),
    path('farm-consultation/create/', FarmConsultationCreate.as_view(), name='fc-create'),
    path('farm-consultation/list/', FarmConsultationList.as_view(), name='fc-list'),
    path('farm-consultation/update/<int:pk>/', FarmConsultationUpdate.as_view(), name='fc-update'),
    path('farm-consultation/delete/<int:pk>/', FarmConsultationDelete.as_view(), name='fc-delete'),

    # Referral URLs
    path('referral/',portal_views.referral,name='referral'),
    path('referral-view/',portal_views.referral_view,name='referral-view'),
    path('referral/create/', ReferralCreate.as_view(), name='referral-create'),
    path('referral/list/', ReferralList.as_view(), name='referral-list'),
    path('referral/update/<int:pk>/', ReferralUpdate.as_view(), name='referral-update'),
    path('referral/delete/<int:pk>/', ReferralDelete.as_view(), name='referral-delete'),

     # SampleCollection URLs
    path('collection/', portal_views.sample_collection, name='collection'),
    path('collection-view/', portal_views.sample_collection_view, name='collection-view'),
    path('sample-collection/create/', SampleCollectionCreate.as_view(), name='sample-collection-create'),
    path('sample-collection/list/', SampleCollectionList.as_view(), name='sample-collection-list'),
    path('sample-collection/update/<int:pk>/', SampleCollectionUpdate.as_view(), name='sample-collection-update'),
    path('sample-collection/delete/<int:pk>/', SampleCollectionDelete.as_view(), name='sample-collection-delete'),

    # SampleProcessing URLs
    path('processing/', portal_views.sample_processing, name='processing'),
    path('processing-view/', portal_views.sample_processing_view, name='processing-view'),
    path('sample-processing/create/', SampleProcessingCreate.as_view(), name='sample-processing-create'),
    path('sample-processing/list/', SampleProcessingList.as_view(), name='sample-processing-list'),
    path('sample-processing/update/<int:pk>/', SampleProcessingUpdate.as_view(), name='sample-processing-update'),
    path('sample-processing/delete/<int:pk>/', SampleProcessingDelete.as_view(), name='sample-processing-delete'),


    # LaboratoryRecord URLs
    path('lab-record/', portal_views.lab_record, name='lab-record'),
    path('lab-record-view/', portal_views.lab_record_view, name='lab-record-view'),
    path('laboratory-record/create/', LaboratoryRecordCreate.as_view(), name='laboratory-record-create'),
    path('laboratory-record/list/', LaboratoryRecordList.as_view(), name='laboratory-record-list'),
    path('laboratory-record/update/<int:pk>/', LaboratoryRecordUpdate.as_view(), name='laboratory-record-update'),
    path('laboratory-record/delete/<int:pk>/', LaboratoryRecordDelete.as_view(), name='laboratory-record-delete'),

    path('incident/', portal_views.incidence_record, name='incident'),
    path('incident-view/', portal_views.incidence_view, name='incident-view'),
    path('incidents/create/', LivestockIncidentCreate.as_view(), name='livestock_incident_create'),
    path('incidents/', LivestockIncidentList.as_view(), name='livestock_incident_list'),
    path('incidents/update/<int:pk>/', LivestockIncidentUpdate.as_view(), name='livestock_incident_update'),
    path('incidents/delete/<int:pk>/', LivestockIncidentDelete.as_view(), name='livestock_incident_delete'),

    path('postmortem/', portal_views.post_mortem, name='postmortem'),
    path('postmortem-view/', portal_views.post_mortem_view, name='postmortem-view'),
    path('postmortem/create/', PostMortemRecordCreate.as_view(), name='postmortem-create'),
    path('postmortem/list/', PostMortemRecordList.as_view(), name='postmortem-list'),
    path('postmortem/update/<int:pk>/', PostMortemRecordgUpdate.as_view(), name='postmortem-update'),
    path('postmortem/delete/<int:pk>/', PostMortemRecordDelete.as_view(), name='postmortem-delete'),

    path('vaccination/', portal_views.vaccination, name='vaccination'),
    path('vaccination-view/', portal_views.vaccination_view, name='vaccination-view'),
    path('vaccination_official/', portal_views.vaccination_official_view, name='vaccination-official'),
    path('vaccination-records/', VaccinationRecordList.as_view(), name='vaccination-record-list'),
    path('vaccination-records/create/', VaccinationRecordCreate.as_view(), name='vaccination-record-create'),
    path('vaccination-records/update/<int:pk>/', VaccinationRecordUpdate.as_view(), name='vaccination-record-update'),
    path('vaccination-records/delete/<int:pk>/', VaccinationRecordDelete.as_view(), name='vaccination-record-delete'),

    path('surgery/', portal_views.surgical_record, name='surgery'),  
    path('surgery-view/', portal_views.surgical_view, name='surgery-view'),  
    path('surgical-record/create/', SurgicalRecordCreate.as_view(), name='surgical_record_create'),
    path('surgical-record/list/', SurgicalRecordList.as_view(), name='surgical_record_list'),
    path('surgical-record/update/<int:pk>/', SurgicalRecordUpdate.as_view(), name='surgical_record_update'),
    path('surgical-record/delete/<int:pk>/',SurgicalRecordDelete.as_view(), name='surgical_record_delete'),
    
    path('clinical/', portal_views.clinical, name='clinical'),  
    path('clinical-view/', portal_views.clinical_view, name='clinical-view'), 
    path('clinical-record/create/', ClinicalRecordCreate.as_view(), name='clinical-record-create'),
    path('clinical-record/', ClinicalRecordList.as_view(), name='clinical-record-list'),
    path('clinical-record/update/<int:pk>/', ClinicalRecordUpdate.as_view(), name='clinical-record-update'),
    path('clinical-record/delete/<int:pk>/', ClinicalRecordDelete.as_view(), name='clinical-record-delete'),


    path('client/', portal_views.client, name='client'),
    path('clients/create/', ClientCreate.as_view(), name='client-create'),
    path('clients/', ClientList.as_view(), name='client-list'),
    path('clients/update/<int:pk>/', ClientUpdate.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDelete.as_view(), name='client_delete'),

    path('diary/', portal_views.diary, name='diary'),
    path('diaries/create/', DiaryCreate.as_view(), name='diary-create'),
    path('diaries/', DiaryList.as_view(), name='diary-list'),
    path('diaries/update/<int:pk>/', DiaryUpdate.as_view(), name='diary_update'),
    path('diaries/delete/<int:pk>/', DiaryDelete.as_view(), name='diary_delete'),
    ##############Shop######################
    
    path('shop/', portal_views.shop, name='shop'),
    path('resources/', portal_views.resources, name='resources'),
    
    path('disease-reports/', disease_report, name='disease-report'),
    path('disease-reports/view/', disease_report_view, name='disease-report-view'),
    path('disease-reports/list', DiseaseReportList.as_view(), name='disease-report-list'),
    path('disease-reports/create/', DiseaseReportCreate.as_view(), name='disease-report-create'),
    path('disease-reports/update/<int:pk>/', DiseaseReportUpdate.as_view(), name='disease-report-update'),
    path('disease-reports/delete/<int:pk>/', DiseaseReportDelete.as_view(), name='disease-report-delete'),

    path('slaughterhouse/', slaughterhouse, name='slaughterhouse'),
    path('slaughterhouse_view/', slaughterhouse_view, name='slaughterhouse-view'),
    path('slaughterhouse/create/', SlaughterhouseCreate.as_view(), name='slaughterhouse_create'),
    path('slaughterhouse/list/', SlaughterhouseList.as_view(), name='slaughterhouse_list'),
    path('slaughterhouse/update/<int:pk>/', SlaughterhouseUpdate.as_view(), name='slaughterhouse_update'),
    path('slaughterhouse/delete/<int:pk>/', SlaughterhouseDelete.as_view(), name='slaughterhouse_delete'),
    
    # Employee URLs
    path('employee/', employee, name='employee'),
    path('employee/create/', EmployeeCreate.as_view(), name='employee_create'),
    path('employee/list/', EmployeeList.as_view(), name='employee_list'),
    path('employee/update/<int:pk>/', EmployeeUpdate.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', EmployeeDelete.as_view(), name='employee_delete'),
    
    # Butcher URLs
    path('butcher/', butcher, name='butcher'),
    path('butcher/create/', ButcherCreate.as_view(), name='butcher_create'),
    path('butcher/list/', ButcherList.as_view(), name='butcher_list'),
    path('butcher/update/<int:pk>/', ButcherUpdate.as_view(), name='butcher_update'),
    path('butcher/delete/<int:pk>/', ButcherDelete.as_view(), name='butcher_delete'),
    
    # Invoice URLs
    path('invoice/', invoice, name='invoice'),
    path('invoice-view',invoice_view, name='invoiceview'),
    path('invoice/create/', InvoiceCreate.as_view(), name='invoice_create'),
    path('invoice/list/', InvoiceList.as_view(), name='invoice_list'),
    path('invoice/update/<int:pk>/', InvoiceUpdate.as_view(), name='invoice_update'),
    path('invoice/delete/<int:pk>/', InvoiceDelete.as_view(), name='invoice_delete'),

    # questions
    path('quiz/', quiz, name='quiz'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    #path('submit-answer/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('cpd/', tutorial, name='cpd'),
    path('lessons/', lesson, name='lessons'),
    path('tutorials/create/', TutorialCreate.as_view(), name='tutorial-create'),
    path('tutorials/list/', TutorialList.as_view(), name='tutorial-list'),
    path('tutorials/update/<int:pk>/', TutorialUpdate.as_view(), name='tutorial-update'),
    path('tutorials/delete/<int:pk>/', TutorialDelete.as_view(), name='tutorial-delete'),
    path('questions/create/', QuestionCreateAPIView.as_view(), name='question-create'),
    path('questions/<int:section_id>/', QuizView.as_view(), name='questions-list'),   
    path('questions/submit/<int:section_id>/', QuizSubmit.as_view(), name='questions-submit'),
    path('questions/res/', QuizResultList.as_view(), name='questions-res'),  
    path('download/<int:section_id>/', download_file, name='download_file'),
    path('questions/result/', result, name='questions-result'),
    
    path('sections/<int:lesson_id>/', SectionList.as_view(), name='section-list'),
    path('sections/comments/create/<int:section_id>/', CommentCreateView.as_view(), name='comment-create'),
    path('sections/comments/<int:section_id>/', CommentListView.as_view(), name='comment-list'),
    path('sections/create/', SectionCreate.as_view(), name='section-create'),
    
    path('examination/', livestock_examination, name='livestock-examination'),
    path('livestock-examination/create/', LivestockExaminationCreate.as_view(), name='livestock-examination-create'),
    path('livestock-examination/list/', LivestockExaminationList.as_view(), name='livestock-examination-list'),
    path('livestock-examination/update/<int:pk>/', LivestockExaminationUpdate.as_view(), name='livestock-examination-update'),
    path('livestock-examination/delete/<int:pk>/', LivestockExaminationDelete.as_view(), name='livestock-examination-delete'),

    # Calving Record URLs
    path('calving/', calving_record, name='calving-record'),
    path('calving-record/create/', CalvingRecordCreate.as_view(), name='calving-record-create'),
    path('calving-record/list/', CalvingRecordList.as_view(), name='calving-record-list'),
    path('calving-record/update/<int:pk>/', CalvingRecordUpdate.as_view(), name='calving-record-update'),
    path('calving-record/delete/<int:pk>/', CalvingRecordDelete.as_view(), name='calving-record-delete'),
    
    path('assesment/', assessment_record, name='assesment-record-page'),
    path('assesment_official/', assessment_record_view, name='assesment-view'),
    path('assesment-records/create/', AssessmentRecordCreate.as_view(), name='assesment-record-create'),
    path('assesment-records/list/', AssessmentRecordList.as_view(), name='assesment-record-list'),
    path('assesment-records/update/<int:pk>/', AssessmentRecordUpdate.as_view(), name='assesment-record-update'),
    path('assesment-records/delete/<int:pk>/', AssessmentRecordDelete.as_view(), name='assesment-record-delete'),
    
    path('kills/', daily_kill_report, name='daily-kills'),
    path('kills_view/', daily_kill_report_view, name='daily-kills-view'),
    path('daily-kills/create/', DailyKillCreate.as_view(), name='daily_kill_create'),
    path('daily-kills/list/', DailyKillList.as_view(), name='daily-kills-list'),
    path('daily-kills/update/<int:pk>/', DailyKillUpdate.as_view(), name='daily_kill_update'),
    path('daily-kills/delete/<int:pk>/', DailyKillDelete.as_view(), name='daily_kill_delete'),
    
    path('movement-permit/', movement_permit_report, name='movement-permit-report'),
    path('movement-permit_report/', movement_permit_report_view, name='movement-permit-view'),
    path('movement-permits/create/', MovementPermitCreate.as_view(), name='movement_permit_create'),
    path('movement-permits/', MovementPermitList.as_view(), name='movement-permit-list'),
    path('movement-permits/<int:pk>/update/', MovementPermitUpdate.as_view(), name='movement_permit_update'),
    path('movement-permits/<int:pk>/delete/', MovementPermitDelete.as_view(), name='movement_permit_delete'),

    
    path('no_objections/', no_objection_report, name='no_objection_report'),
    path('no_objections/create/', NoObjectionCreate.as_view(), name='no_objection_create'),
    path('no_objections/list/', NoObjectionList.as_view(), name='no-objection-list'),
    path('no_objections/<int:pk>/update/', NoObjectionUpdate.as_view(), name='no_objection_update'),
    path('no_objections/<int:pk>/delete/',NoObjectionDelete.as_view(), name='no_objection_delete'),

    
    path('monthly-report/', monthly_report, name='monthly_report'),
    path('monthly-reports/create/', MonthlyReportCreate.as_view(), name='monthly_report_create'),
    path('monthly-reports/', MonthlyReportList.as_view(), name='monthly-report-list'),
    path('monthly-reports/<int:pk>/update/', MonthlyReportUpdate.as_view(), name='monthly_report_update'),
    path('monthly-reports/<int:pk>/delete/', MonthlyReportDelete.as_view(), name='monthly_report_delete'),

    path('practitioner/record/', practitioner_record, name='practitioner_record'),
    path('practitioner/record/view/', practitioner_record_view, name='practitioner_record_view'),
    path('practitioner/create/', PractitionerCreate.as_view(), name='practitioner_create'),
    path('practitioner/list/', PractitionerList.as_view(), name='practitioner_list'),
    path('practitioner/update/<int:pk>/', PractitionerUpdate.as_view(), name='practitioner_update'),
    path('practitioner/delete/<int:pk>/', PractitionerDelete.as_view(), name='practitioner_delete'),


    #path('answers/', UserAnswerCreate.as_view(), name='user-answer-create'),

]
if  not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)