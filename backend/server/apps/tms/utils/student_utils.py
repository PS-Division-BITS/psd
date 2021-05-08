from server.constants import UserType
from apps.tms.models import ActiveUserProfile
import pandas as pd
import re
 
def validate_contact(value): 
    Pattern = re.compile("(0/91)?[7-9][0-9]{9}")
    return Pattern.match(value) 

def check_supervisor(email):
    supervisor_object = ActiveUserProfile.objects.filter(user_type=UserType.SUPERVISOR.value,email=email)
    if supervisor_object:
        return True
    return False

def hod_data(active_user):
        hod_file = pd.read_csv('apps/tms/hod_list.csv')
        hod_1 = hod_file[(hod_file["Campus"]==active_user.campus) & ((hod_file["Department"]==active_user.username[4:6]) | (hod_file["Department"]==active_user.username[6:8]))]
        hod_email_list = hod_1['Email'].tolist()
        return hod_email_list

def get_branch_from_branch_code(branch_code):
    switcher = {
        'A1': 'B.E. Chemical Engineering',
        'A2': 'B.E. Civil Engineering',
        'A3': 'B.E. Electrical and Electronics Engineering',
        'A4': 'B.E. Mechanical Engineering',
        'A5': 'B. Pharm.',
        'A7': 'B.E. Computer Science Engineering',
        'A8': 'B.E. Electronics and Instrumentation Engineering',
        'A9': 'B.E. Biotechnology',
        'AA': 'B.E. Electronics and Communication Engineering',
        'AB': 'B.E. Manufacturing Engineering',
        'B1': 'M.Sc. Biology + ',
        'B2': 'M.Sc. Chemistry + ',
        'B3': 'M.Sc. Economics + ',
        'B4': 'M.Sc. Mathematics + ',
        'B5': 'M.Sc. Physics + ',
        'C2': 'M.Sc. General Studies + ',
        'C5': 'M.Sc. Engineering Technology + ',
        'C6': 'M.Sc. Information Systems + ',
        'C7': 'M.Sc. Finance + ',
        'D2': 'Humanities and Social Sciences',
        'PS': '',
        'TS': '',
    }
    return switcher.get(branch_code, "Invalid branch code")
