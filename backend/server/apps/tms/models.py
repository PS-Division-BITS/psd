from django.db import models
from server.constants import CampusType, TransferType, UserType, ApplicationsStatus, ThesisLocaleType

class ActiveUserProfile(models.Model):        #model used for filling the database with inital values
    """
    Profile model for each User in the app.
    Keep fields nullable to create a corresponding
    UserProfile model isntance automatically once a User
    model instance is created.
    """
    username = models.CharField(max_length=13)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_choices = [
        (UserType.STUDENT.value, 'Student'),
        (UserType.SUPERVISOR.value, 'Supervisor'),
        (UserType.HOD.value, 'Head of Department'),
        (UserType.AD.value, 'Associate Dean'),
        (UserType.PSD.value, 'PS-Division'),
    ]
    campus_choices = [
        (CampusType.GOA.value, 'Goa'),
        (CampusType.HYD.value, 'Hyderabad'),
        (CampusType.PILANI.value, 'Pilani'),
    ]
    email = models.EmailField()
    campus = models.IntegerField(choices=campus_choices, blank=True,
        null=True)
    contact = models.CharField(
        blank=True, null=True, max_length=20,
        help_text="Enter 10 digit contact number"
    )
    user_type = models.IntegerField(choices=user_choices, blank=True,
        null=True)
    cgpa = models.CharField(max_length=6, default="NA")

    is_active_tms = models.BooleanField(default=False)


    def __str__(self):
        return str(self.email+str(self.user_type))


class PS2TSTransfer(models.Model):
    """
    Model to store the information for
    PS --> TS transfer related queries
    """
    sub_type_choices = [
        (TransferType.PS2TS.value, 'PS to TS (Single Degree)'),
        (TransferType.PSPS2PSTS.value, 'PS-PS to PS-TS (Dual Degree)'),
        (TransferType.PSPS2TSPS.value, 'PS-PS to TS-PS (Dual Degree)'),
        (TransferType.TSPS2TSTS.value, 'TS-PS to TS-TS (Dual Degree)'),
    ]

    thesis_locale_choices = [
        (ThesisLocaleType.ON_CAMPUS.value, 'On Campus'),
        (ThesisLocaleType.OFF_CAMPUS_INDIA.value, 'Off Campus (India)'),
        (ThesisLocaleType.OFF_CAMPUS_ABROAD.value, 'Off Campus (Abroad)'),
        (ThesisLocaleType.OFF_CAMPUS_INDUSTRY.value, 'Off Campus (Industry)'),
    ]
    status_choices = [
        (ApplicationsStatus.PENDING.value, 'Pending'),
        (ApplicationsStatus.APPROVED.value, 'Approved'),
        (ApplicationsStatus.REJECTED.value, 'Rejected'),
    ]
    # linking the application with its applicant
    applicant = models.OneToOneField(ActiveUserProfile, primary_key=True,
        on_delete=models.CASCADE)
    # corresponding on-campus supervisor
    supervisor_email = models.EmailField()
    # corresponding hod
    hod_email = models.EmailField()
    # sub-type for application; see choices above
    sub_type = models.IntegerField(choices=sub_type_choices)
    # other details required for the form
    cgpa = models.DecimalField(max_digits=6, decimal_places=2)
    thesis_locale = models.IntegerField(choices=thesis_locale_choices)
    thesis_subject = models.CharField(max_length=150,
        help_text='Broad area/Title of Thesis')
    name_of_org = models.CharField(max_length=100,
        help_text='Name of BITS Campus or Organization where thesis will be carried')
    expected_deliverables = models.TextField(help_text='Expected outcome of thesis')
    # fields to note the status of the application
    is_supervisor_approved = models.IntegerField(
        default=ApplicationsStatus.PENDING.value,
        choices=status_choices
    )
    is_hod_approved = models.IntegerField(
        default=ApplicationsStatus.PENDING.value,
        choices=status_choices
    )
    is_ad_approved = models.IntegerField(
        default=ApplicationsStatus.PENDING.value,
        choices=status_choices
    )
    # comments from authorities
    comments_from_supervisor = models.TextField(null=True, blank=True)
    comments_from_hod = models.TextField(null=True, blank=True)
    comments_from_ad = models.TextField(null=True, blank=True)
    # date-time-stamp
    application_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'PS to TS Application'
        verbose_name_plural = 'PS to TS Applications'


class TS2PSTransfer(models.Model):
    """
    Model to store the information for
    TS --> PS transfer related queries
    """
    # TS2PS = 0
    # PSTS2PSPS = 1
    # TSTS2TSPS = 2
    sub_type_choices = [
        (TransferType.TS2PS, 'TS to PS (Single Degree)'),
        (TransferType.PSTS2PSPS, 'PS-TS to PS-PS (Dual Degree)'),
        (TransferType.TSTS2TSPS, 'TS-TS to TS-PS (Dual Degree)'),
        ]
    status_choices = [
        (ApplicationsStatus.PENDING.value, 'Pending'),
        (ApplicationsStatus.APPROVED.value, 'Approved'),
        (ApplicationsStatus.REJECTED.value, 'Rejected'),
    ]
    # linking application with its applicant
    applicant = models.OneToOneField(ActiveUserProfile, primary_key=True,
        on_delete=models.CASCADE)
    # corresponding hod
    hod_email = models.EmailField()
    # sub-type for application; see choices above
    sub_type = models.IntegerField(choices=sub_type_choices)
    # other details required for the form
    cgpa = models.DecimalField(max_digits=6, decimal_places=2)
    reason_for_transfer = models.TextField()
    name_of_org = models.CharField(max_length=100,
            help_text='Name of BITS Campus or Organization where thesis was being carried')
    # field to note the status of the application
    is_hod_approved = models.IntegerField(
        default=ApplicationsStatus.PENDING.value,
        choices=status_choices
    )
    is_ad_approved = models.IntegerField(
        default=ApplicationsStatus.PENDING.value,
        choices=status_choices
    )
    # comments from authorities
    comments_from_hod = models.TextField(null=True, blank=True)
    comments_from_ad = models.TextField(null=True, blank=True)
    # date-time-stamp
    application_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'TS to PS Application'
        verbose_name_plural = 'TS to PS Applications'

class DeadlineModel(models.Model):
 
    deadline_PS2TS = models.DateTimeField(null = True, blank = True)
    deadline_TS2PS = models.DateTimeField(null = True, blank = True)
    is_active_PS2TS = models.BooleanField(default=False)
    is_active_TS2PS = models.BooleanField(default=False)
    message = models.TextField(null=True,blank=True)

# Create your models here.
