from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO as IO
import datetime
import pandas as pd
import re
import xlsxwriter 

from apps.tms.models import ActiveUserProfile, PS2TSTransfer as psts, TS2PSTransfer as tsps

count=1
final=pd.DataFrame(columns=['Sr.No', 'Name', 'Stream'])
flag=0

def getFileHod(request, choice):
    #encodeed all the types in a map
    objectCode={'01':psts.objects.filter(sub_type=0),
    '10':tsps.objects.filter(sub_type=0),
    '0100':tsps.objects.filter(sub_type=1) ,
    '1110':tsps.objects.filter(sub_type= 2), 
    'xx11':psts.objects.filter(sub_type=1)}
    global count
    global final    
    if choice==1:
        filename="PS To TS"
        final=pd.DataFrame(columns=['Sr.No', 'Name', 'Transfer Type','CGPA','Thesis Locale', 'Thesis Subject', 'Organization Name', 'Expected Outcome'])
        makeFile(objectCode['01'],1)
        makeFile(objectCode['xx11'],1)
    elif choice==2:
        filename="TS To PS"
        final=pd.DataFrame(columns=['Sr.No', 'Name', 'Transfer Type','CGPA', 'Reason for Transfer','Organization Name'])
        makeFile(objectCode['10'],2)
        makeFile(objectCode['1110'],2)
        makeFile(objectCode['0100'],2)
    response=download(final,filename)
    #reset global vars
    count=1
    if choice==1:
        final=pd.DataFrame(columns=['Sr.No', 'Name', 'Transfer Type','CGPA','Thesis Locale', 'Thesis Subject', 'Organization Name', 'Expected Outcome'])
    elif choice==2:
        final=pd.DataFrame(columns=['Sr.No', 'Name', 'Transfer Type', 'Reason for Transfer','Organization Name'])
    return response

    
def download(final,filename):
    #final is the dataframe that contains all the details of the students approved by the hod
    excel_file=IO() #create a io memory stream
    xlwriter=pd.ExcelWriter(excel_file,engine='xlsxwriter') #xlsxwriter is a requirement
    final.to_excel(xlwriter, f'{filename}', index=False) #chosen the sheetname to be the same as filename
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0) #place the pointer at the start of the file
    response=HttpResponse(excel_file.read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition']=f'attachment; filename={filename}.xlsx' #makes an http file response of the excel
    print(final) #for debugging
    
    return response

def makeFile(x,choice):
    for data in x:
            da=datetime.datetime(2020,9,18)
            db=datetime.datetime.now()
            thisDate = data.application_date
            if(not (thisDate<=db and thisDate>=da)):
                continue
            global count
            global final
            global flag
            temp={}
            if choice==0: #for psd folks
                Name=data.applicant.user.first_name
                ID=data.applicant.user.username
                Campus=data.applicant.get_campus_display()
                Contact=data.applicant.contact
                hodEmail=data.hod_email
                orgName=data.name_of_org
                supApproved="NA"
                supEmail="NA"
                supName="NA"
                supApproved="NA"
                thesisLocale="NA"

                if flag:
                    supEmail=data.supervisor_email
                    sup=User.objects.filter(email= supEmail)[0]
                    supName=sup.first_name + " " + sup.last_name
                    supApproved=data.get_is_supervisor_approved_display()
                    thesisLocale=data.get_thesis_locale_display()

                hod=User.objects.filter(email=hodEmail)[0]
                hodName=hod.first_name+" "+hod.last_name
                hodApproved=data.get_is_hod_approved_display()
                adApproved=data.get_is_ad_approved_display()
                temp={'Sr.No':count , 'ID':ID,'Name':Name,'Campus':Campus,'Contact':Contact,'Supervisor Name':supName,'Supervisor Email':supEmail,'HoD Name':hodName, 'HoD Email':hodEmail, 'Application Type':data.get_sub_type_display(),'Supervisor Approval':supApproved, 'HoD Approval':hodApproved, 'AD Approval':adApproved, 'Thesis Locale':thesisLocale,'Organization Name': orgName}

            elif choice==2: #ts-ps for hod
                if data.is_hod_approved==1:
                    temp={'Sr.No':count, 'Name':data.applicant.user.first_name+' '+ data.applicant.user.last_name, 'Transfer Type':data.get_sub_type_display(), 'CGPA':str(data.cgpa),'Reason for Transfer':data.reason_for_transfer,'Organization Name':data.name_of_org  } #for hod: tsps
            else: #ps-ts for hod
                if data.is_hod_approved==1:
                    temp={'Sr.No':count, 'Name':data.applicant.user.first_name+' '+ data.applicant.user.last_name, 'Transfer Type':data.get_sub_type_display(), 'CGPA':str(data.cgpa),'Thesis Locale':data.get_thesis_locale_display(), 'Thesis Subject': data.thesis_subject,'Organization Name': data.name_of_org, 'Expected Outcome': data.expected_deliverables }
            final=final.append(temp,ignore_index=True) 
            if not flag:
                final=final.drop(columns=['Supervisor Name', 'Supervisor Email', 'Supervisor Approval','Thesis Locale'])
            count=count+1
