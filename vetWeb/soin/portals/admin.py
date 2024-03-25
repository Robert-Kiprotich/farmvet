from django.contrib import admin

from .models import Vet_Forms, Sick_Approach_Form, Death_Approach_Form, Surgical_Approach_Form, Deworming_Form, Vaccination_Form, Artificial_Insemination_Form, Calf_Registration_Form, Livestock_Inventory_Form, Pregnancy_Diagnosis_Form,Farm_Consultation

admin.site.register(Vet_Forms)
admin.site.register(Sick_Approach_Form)
admin.site.register(Death_Approach_Form)
admin.site.register(Surgical_Approach_Form)
admin.site.register(Deworming_Form)
admin.site.register(Vaccination_Form)
admin.site.register(Artificial_Insemination_Form)
admin.site.register(Calf_Registration_Form)
admin.site.register(Livestock_Inventory_Form)
admin.site.register(Pregnancy_Diagnosis_Form)
admin.site.register(Farm_Consultation)