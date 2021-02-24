from django.shortcuts import render, redirect
from django.db import connection, transaction
from django.http import HttpResponse
import cgi
import openpyxl
from urllib.request import urlopen
import re
from .forms import *
from django.db import connection, transaction
from datetime import date
import datetime
# from civil.models import AddHazard
# from civil.forms import AddHazardForm

from civil.models import AddNewHazard
from civil.forms import AddNewHazardForm

from civil.models import AddDesignElement
from civil.forms import AddDesignElementForm

from civil.models import AddActivity
from civil.forms import AddActivityForm

from civil.models import AddProject
from civil.forms import AddProjectForm

from civil.models import AddSignup
from civil.forms import AddSignupForm



def signup(request):
    return render(request, "signup.html")

def insert_signup(request):
    if request.method == 'POST':
        FIRST_NAME = request.POST['FIRST_NAME']
        LAST_NAME = request.POST['LAST_NAME']
        EMAIL = request.POST['EMAIL']
        PASSWORD = request.POST['PASSWORD']
        EXPERIENCE= request.POST['EXPERIENCE']
        TYPE = request.POST['TYPE']
        dictdata = {'FIRST_NAME': FIRST_NAME, 'LAST_NAME': LAST_NAME, 'TYPE': TYPE,'EXPERIENCE': EXPERIENCE, 'EMAIL': EMAIL,'PASSWORD':PASSWORD}
        cursor = connection.cursor()
        sql = "INSERT INTO modifiers (FIRST_NAME, LAST_NAME, TYPE,EXPERIENCE,EMAIL,PASSWORD) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (FIRST_NAME, LAST_NAME, TYPE, EXPERIENCE, EMAIL, PASSWORD)
        cursor.execute(sql, val)
        #menuform = AddSignup(dictdata)
        #menuform.save()

        return redirect('/civil')
    else:
        return redirect('/civil') 
            
def checklogin(request):
    if request.method == 'POST':
        emailcheck = request.POST['EMAIL']
        passwordcheck = request.POST['PASSWORD']
        cursor = connection.cursor()
        query_string = "SELECT * FROM modifiers WHERE EMAIL =%s and PASSWORD =%s;"
        cursor.execute(query_string, (emailcheck, passwordcheck))
        for record in cursor.fetchall():
            id = record[0]
            FIRST_NAME = record[1]
            type = record[5]
        numrow = cursor.rowcount
        if numrow:
            request.session['logged_in'] = True
            request.session['STU'] = True
            request.session['userid'] = id
            request.session['userfname'] =FIRST_NAME
            request.session['username'] = emailcheck
            request.session['usertype'] = type
            return redirect('/civil')
        else:
            return render(request, 'login.html', {})
            
def logout(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html', {})
    else:
        request.session['logged_in'] = False
    return render(request, 'login.html', {})

def index(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        return render(request, "dashboard.html")

def view_hazard(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        activity_id = '0'
        records = []
        sql_select_Query = "SELECT * FROM `design_elements`"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        for record in cursor.fetchall():
            records.append({'id': record[0], 'name': record[1]})
        
        activity_records = []
        sql_select_activity_records_Query = "SELECT a.id,d.name,a.activity_name FROM `activities` as a join design_elements as d on a.`design_element_id` = d.id"
        cursor = connection.cursor()
        cursor.execute(sql_select_activity_records_Query)
        for record in cursor.fetchall():
            activity_records.append({'id': record[0], 'name': record[1], 'activity_name': record[2]})
        
        hazards_records = []
        sql_select_hazards_Query = "SELECT DISTINCT hazard_name FROM hazards WHERE activity_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql_select_hazards_Query,(activity_id))
        for hazard in cursor.fetchall():
            hazard_name = hazard[0]
            sql_select_hazards_records_Query = "SELECT id,hazard_permalink, AVG(probility), AVG(severity), AVG(risk), control_measure from hazards WHERE hazard_name=%s AND activity_id = %s"
            cursor.execute(sql_select_hazards_records_Query,(hazard_name,activity_id))
            for record in cursor.fetchall():
                hazards_records.append({'hazard_name': hazard_name,'activity_id':activity_id, 'id': record[0],'hazard_permalink':record[1], 'probility': record[2],'severity': record[3],'risk': record[4],'control_measure':record[5]})
        #hazards_records.sort(key=lambda x: x.risk.lower())
        return render(request, "view_hazard.html",{'records': records, 'activity_records': activity_records, 'hazards_records': hazards_records})
    
def your_projects(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        modifier_id = request.GET['id']
        records = []
        sql_select_Query = "SELECT * FROM `projects` WHERE modifier_id=%s"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(modifier_id))
        for record in cursor.fetchall():
            records.append({'id': record[0],'name': record[1],'location': record[2] ,'budget': record[3] ,'datafrom': record[4],'dateto': record[5],'approvalby': record[6],'checkedby': record[7],'modifier_id':record[8]})
    
        return render(request, "your_projects.html", {'records': records})
        
def add_project(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        return render(request, "add_project.html", {})
        
def insert_project(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        modifier_id = request.POST['UserId']
        name = request.POST['ProjectName']
        budget = request.POST['Budget']
        checked_by = request.POST['CheckedBy']
        date_from = request.POST['StartDate']
        date_to = request.POST['EndDate']
        approval_by = request.POST['ApprovedBy']
        location = request.POST['ProjectLocation']
        
        dictdata = {'modifier_id': modifier_id, 'name': name, 'budget': budget, 'checked_by': checked_by, 'date_from': date_from, 'date_to': date_to, 'approval_by': approval_by, 'location': location}
        menuform = AddProjectForm(dictdata)
        menuform.save()
        return redirect('/civil')

def view_detail_project(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        modifier_id = request.GET['id']
        
        records = []
        sql_select_Query = "SELECT * FROM `design_elements`"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        for record in cursor.fetchall():
            records.append({'id': record[0], 'name': record[1]})
    
        activity_records = []
        sql_select_activity_records_Query = "SELECT a.id,d.name,a.activity_name FROM `activities` as a join design_elements as d on a.`design_element_id` = d.id"
        cursor = connection.cursor()
        cursor.execute(sql_select_activity_records_Query)
        for record in cursor.fetchall():
            activity_records.append({'id': record[0], 'name': record[1], 'activity_name': record[2]})
    
        hazards_records = []
        sql_select_hazards_Query = "SELECT DISTINCT hazard_name FROM hazards WHERE user_id != %s"
        cursor = connection.cursor()
        cursor.execute(sql_select_hazards_Query,(modifier_id))
        for hazard in cursor.fetchall():
            hazard_name = hazard[0]
            sql_select_hazards_records_Query = "SELECT d.name,a.activity_name,AVG(h.probility), AVG(h.severity), AVG(h.risk), h.control_measure from hazards as h join activities as a join design_elements as d ON h.activity_id=a.id and a.design_element_id = d.id WHERE h.hazard_name=%s AND h.user_id != %s"
            cursor.execute(sql_select_hazards_records_Query,(hazard_name,modifier_id))
            for record in cursor.fetchall():
                hazards_records.append({'hazard_name': hazard_name,'design_element': record[0],'activity_name':record[1], 'probility': record[2],'severity': record[3],'risk': record[4],'control_measure':record[5]})
        #hazards_records.sort(key=lambda x: x.risk.lower())
        return render(request, "view_detail_project.html",{'records': records, 'activity_records': activity_records, 'hazards_records': hazards_records,})

def delete_project(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        cursor = connection.cursor()
        project_id = request.GET['id']
        modifier_id = request.GET['userid']
        sql = "DELETE FROM projects WHERE id = %s AND modifier_id = %s"
        val = (project_id,modifier_id)
        cursor.execute(sql, val)
        return redirect('/your_projects/?id='+modifier_id)
        
def design_elements(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        records = []
        sql_select_Query = "SELECT * FROM `design_elements`"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        for record in cursor.fetchall():
            records.append({'id': record[0],'name': record[1]})
    
        return render(request, "design_elements_dashboard.html", {'records': records})

def import_activities(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        return render(request, "import_activities.html", {})

def read_import_activities(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        excel_raw_data = pd.read_excel(request.FILES.get('excel_data'))
        return render(request, "read_import_activities.html", {})
        
def add_design_elements(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        records = []
        sql_select_Query = "SELECT * FROM `design_elements`"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        for record in cursor.fetchall():
            records.append({'id': record[0],'name': record[1]})
        return render(request, "add_design_elements.html", {'records': records})

def delete_design_elements(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        col_id = request.GET['id']
        cursor = connection.cursor()
        sql = "DELETE FROM design_elements WHERE id = %s"
        val = (col_id)
        cursor.execute(sql, val)
        return redirect('design_elements')

def activities(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        records = []
        sql_select_Query = "SELECT a.id,d.name,a.activity_name FROM `activities` as a join design_elements as d on a.`design_element_id` = d.id"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        for record in cursor.fetchall():
            records.append({'id': record[0],'name': record[1],'activity_name': record[2]})
        return render(request, "activities_dashboard.html", {'records': records})

def add_activity(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        records = []
        sql_select_Query = "SELECT * FROM `design_elements`"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        for record in cursor.fetchall():
            records.append({'id': record[0], 'name': record[1]})
            
        return render(request, "add_activity.html", {'records': records})

def delete_activities(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        col_id = request.GET['id']
        cursor = connection.cursor()
        sql = "DELETE FROM activities WHERE id = %s"
        val = (col_id)
        cursor.execute(sql, val)
        return redirect('/activities')

def add_hazards(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        
        hazard_permalink = request.GET['name']
        activity_id = request.GET['activity_id']
        hazards_records = []
        
        cursor = connection.cursor()
        sql_select_hazards_records_Query = "SELECT id, hazard_name, hazard_permalink, AVG(probility), AVG(severity), AVG(risk), control_measure from hazards WHERE hazard_permalink = %s AND activity_id =%s "
        cursor.execute(sql_select_hazards_records_Query,(hazard_permalink,activity_id))
        for record in cursor.fetchall():
            
            activity_id = activity_id
            hazard_name = record[1]
            hazard_permalink =record[2]
            probility = record[3]
            severity = record[4]
            risk = record[5]
            control_measure = record[6]
     
        return render(request, "add_hazards.html", {'hazard_name': hazard_name,'hazard_permalink':hazard_permalink,'activity_id':activity_id,'probility': probility,'severity': severity,'risk': risk,'control_measure':control_measure})
    
def add_new_hazard(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        records = []
        sql_select_Query = "SELECT * FROM `design_elements`"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        for record in cursor.fetchall():
            records.append({'id': record[0], 'name': record[1]})
    
        activity_records = []
        sql_select_activity_records_Query = "SELECT a.id,d.name,a.activity_name FROM `activities` as a join design_elements as d on a.`design_element_id` = d.id"
        cursor = connection.cursor()
        cursor.execute(sql_select_activity_records_Query)
        for record in cursor.fetchall():
            activity_records.append({'id': record[0], 'name': record[1], 'activity_name': record[2]})
    
        return render(request, "add_new_hazard.html",{'records': records, 'activity_records': activity_records})

def search_hazards(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        Design_Element = request.POST['DesignElement']
        activity_id = request.POST['Activity']
        
        sql_DesignElement_Query = "SELECT name FROM `design_elements` where id=%s"
        cursor = connection.cursor()
        cursor.execute(sql_DesignElement_Query,(Design_Element))
        for record in cursor.fetchall():
            DesignElement = record[0]

        sql_Activity_Query = "SELECT activity_name FROM `activities` where id=%s"
        cursor = connection.cursor()
        cursor.execute(sql_Activity_Query,(activity_id))
        for record in cursor.fetchall():
            Activity = record[0]
            
        records = []
        sql_select_Query = "SELECT * FROM `design_elements`"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        for record in cursor.fetchall():
            records.append({'id': record[0], 'name': record[1]})
    
        activity_records = []
        sql_select_activity_records_Query = "SELECT a.id,d.name,a.activity_name FROM `activities` as a join design_elements as d on a.`design_element_id` = d.id"
        cursor = connection.cursor()
        cursor.execute(sql_select_activity_records_Query)
        for record in cursor.fetchall():
            activity_records.append({'id': record[0], 'name': record[1], 'activity_name': record[2]})
    
        hazards_records = []
        sql_select_hazards_Query = "SELECT DISTINCT hazard_name FROM hazards WHERE activity_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql_select_hazards_Query,(activity_id))
        for hazard in cursor.fetchall():
            hazard_name = hazard[0]
            sql_select_hazards_records_Query = "SELECT id,hazard_permalink, AVG(probility), AVG(severity), AVG(risk), control_measure from hazards WHERE hazard_name=%s AND activity_id = %s"
            cursor.execute(sql_select_hazards_records_Query,(hazard_name,activity_id))
            for record in cursor.fetchall():
                hazards_records.append({'hazard_name': hazard_name,'activity_id':activity_id, 'id': record[0],'hazard_permalink':record[1], 'probility': record[2],'severity': record[3],'risk': record[4],'control_measure':record[5]})
        #hazards_records.sort(key=lambda x: x.risk.lower())
        return render(request, "view_hazard.html",{'records': records, 'activity_records': activity_records, 'hazards_records': hazards_records,'DesignElement':DesignElement,'Activity':Activity})
    
def load_activities(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        DesignElement = request.GET.get('DesignElement')
        activity_records = []
        sql_select_activity_records_Query = "SELECT * FROM activities WHERE design_element_id = %s "
        cursor = connection.cursor()
        cursor.execute(sql_select_activity_records_Query,(DesignElement))
        for record in cursor.fetchall():
            activity_records.append({'id': record[0], 'name': record[1], 'activity_name': record[2]})
        return render(request, 'load_activities.html', {'activity_records': activity_records})
    
def insert_hazard(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        hazard_name = request.POST['HazardName']
        hazard_permalink = hazard_name.replace(" ", "_")
        activity_id = request.POST['Activity']
        probility = request.POST['Probility']
        severity = request.POST['Severity']
        control_measure = request.POST['ControlMeasure']
        risk = int(probility) * int(severity)
        user_id = request.POST['UserId']
        
        dictdata = {'hazard_name': hazard_name, 'hazard_permalink': hazard_permalink, 'activity_id': activity_id,'probility': probility, 'severity': severity,'control_measure':control_measure, 'risk': risk, 'user_id': user_id}
        menuform = AddHazardForm(dictdata)
        menuform.save()
        return redirect('/view_hazard')
    
def insert_new_hazard(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        hazard_name = request.POST['HazardName']
        hazard_permalink = hazard_name.replace(" ", "_")
        activity_id = request.POST['Activity']
        probility = request.POST['Probility']
        severity = request.POST['Severity']
        control_measure = request.POST['ControlMeasure']
        risk = int(probility) * int(severity)
        user_id = request.POST['UserId']
        
        dictdata = {'hazard_name': hazard_name, 'hazard_permalink': hazard_permalink, 'activity_id': activity_id,'probility': probility, 'severity': severity,'control_measure':control_measure, 'risk': risk, 'user_id':user_id}
        menuform = AddNewHazardForm(dictdata)
        menuform.save()
        return redirect('/add_new_hazard')
    
def insert_design_elements(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        DesignElementName = request.POST['DesignElementName']
        dictdata = {'name': DesignElementName}
        menuform = AddDesignElementForm(dictdata)
        menuform.save()
        return redirect('/design_elements')
    
def insert_activity(request):
    if not request.session.get('logged_in'):
        return render(request, 'login.html')
    else:
        DesignElement = request.POST['DesignElement']
        ActivityName = request.POST['ActivityName']
        dictdata = {'design_element_id': DesignElement, 'activity_name': ActivityName}
        menuform = AddActivityForm(dictdata)
        menuform.save()
        return redirect('/activities')


      
   