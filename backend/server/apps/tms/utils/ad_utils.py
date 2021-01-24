from server.constants import UserType, TransferType, ThesisLocaleType, ApplicationsStatus
from apps.tms.models import PS2TSTransfer, TS2PSTransfer, DeadlineModel
from apps.accounts.models import User

def fetch_ps2ts_list():
    # fetching PS2TS data
    ps2ts_approved_qs = PS2TSTransfer.objects.filter(
        is_ad_approved__lt=ApplicationsStatus.REJECTED.value
        ).values(
        # 'applicant__user__username',
        # 'applicant__user__first_name', 'applicant__user__last_name',
        'applicant__email',
        'sub_type', 'is_supervisor_approved',
        'is_hod_approved', 'cgpa', 'thesis_locale', 'supervisor_email',
            'thesis_subject', 'name_of_org', 'expected_deliverables', 'application_date'
    ).order_by(
        '-thesis_locale', 'is_hod_approved', 
    )
    ps2ts_rejected_qs = PS2TSTransfer.objects.filter(
        is_ad_approved=ApplicationsStatus.REJECTED.value
        ).values(
        # 'applicant__user__username',
        # 'applicant__user__first_name', 'applicant__user__last_name',
        'applicant__email',
        'sub_type', 'is_supervisor_approved',
        'is_hod_approved', 'cgpa', 'thesis_locale', 'supervisor_email',
            'thesis_subject', 'name_of_org', 'expected_deliverables', 'application_date'
    ).order_by(
        '-thesis_locale', 'is_hod_approved', 
    )
    # converting QuerySet --> List
    ps2ts_approved_list = list(ps2ts_approved_qs)
    ps2ts_rejected_list = list(ps2ts_rejected_qs)

    for entries in ps2ts_approved_list:
        entries['first_name'] = User.objects.get(email=entries['applicant__email']).first_name
        entries['last_name'] = User.objects.get(email=entries['applicant__email']).last_name

    for entries in ps2ts_rejected_list:
        entries['first_name'] = User.objects.get(email=entries['applicant__email']).first_name
        entries['last_name'] = User.objects.get(email=entries['applicant__email']).last_name

    print(ps2ts_approved_list)
    return [ps2ts_approved_list, ps2ts_rejected_list]

def fetch_ts2ps_list():
    # fetching TS2PS data
    ts2ps_approved_qs = TS2PSTransfer.objects.filter(
        is_ad_approved__lt=ApplicationsStatus.REJECTED.value
        ).values(
            # 'applicant__user__username',
            # 'applicant__user__first_name', 'applicant__user__last_name',
            'applicant__email',
            'sub_type', 'is_hod_approved', 'cgpa', 
            'reason_for_transfer', 'name_of_org', 'application_date'
        ).order_by(
            'is_hod_approved'
        )
    ts2ps_rejected_qs = TS2PSTransfer.objects.filter(
        is_ad_approved=ApplicationsStatus.REJECTED.value
        ).values(
            # 'applicant__user__username',
            # 'applicant__user__first_name', 'applicant__user__last_name',
            'applicant__email',
            'sub_type', 'is_hod_approved', 'cgpa', 
            'reason_for_transfer', 'name_of_org', 'application_date'
    ).order_by(
            'is_hod_approved'
        )
    # converting QuerySet --> List
    ts2ps_approved_list = list(ts2ps_approved_qs)
    ts2ps_rejected_list = list(ts2ps_rejected_qs)

    for entries in ts2ps_approved_list:
        entries['first_name'] = User.objects.get(email=entries['applicant__email']).first_name
        entries['last_name'] = User.objects.get(email=entries['applicant__email']).last_name

    for entries in ts2ps_rejected_list:
        entries['first_name'] = User.objects.get(email=entries['applicant__email']).first_name
        entries['last_name'] = User.objects.get(email=entries['applicant__email']).last_name

    return [ts2ps_approved_list, ts2ps_rejected_list]


