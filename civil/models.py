from django.db import models

class AddProject(models.Model):
    modifier_id  = models.CharField(max_length=200,null=True,blank=True)
    name  = models.CharField(max_length=255,null=True,blank=True)
    budget  = models.CharField(max_length=200,null=True,blank=True)
    checked_by  = models.CharField(max_length=200,null=True,blank=True)
    date_from  = models.CharField(max_length=200,null=True,blank=True)
    date_to  = models.CharField(max_length=200,null=True,blank=True)
    approval_by  = models.CharField(max_length=200,null=True,blank=True)
    location  = models.CharField(max_length=2000,null=True,blank=True)
    
    class Meta:
        db_table = "projects"
        
        
class AddNewHazard(models.Model):
    hazard_name  = models.CharField(max_length=200)
    hazard_permalink  = models.CharField(max_length=200)
    activity_id  = models.CharField(max_length=200)
    probility  = models.CharField(max_length=200)
    severity  = models.CharField(max_length=200)
    risk  = models.CharField(max_length=200)
    control_measure = models.CharField(max_length=500)
    user_id = models.CharField(max_length=100)
    
    class Meta:
        db_table = "hazards"
#
# class AddHazard(models.Model):
#     hazard_name  = models.CharField(max_length=200)
#     hazard_permalink  = models.CharField(max_length=200)
#     activity_id  = models.CharField(max_length=200)
#     probility  = models.CharField(max_length=200)
#     severity  = models.CharField(max_length=200)
#     risk  = models.CharField(max_length=200)
#     control_measure = models.CharField(max_length=500)
#     user_id = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = "hazards"
        
class AddSignup(models.Model): 
    FIRST_NAME  = models.CharField(max_length=200,null=True,blank=True)
    LAST_NAME  = models.CharField(max_length=200,null=True,blank=True)
    EMAIL  = models.CharField(max_length=400)
    PASSWORD  = models.CharField(max_length=200,null=True,blank=True)
    EXPERIENCE  = models.CharField(max_length=200,null=True,blank=True)
    TYPE  = models.CharField(max_length=200,null=True,blank=True)
    
    class Meta:
        db_table = "modifiers"


class AddDesignElement(models.Model):
    name  = models.CharField(max_length=200)
    
    class Meta:
        db_table = "design_elements"      
        
        
class AddActivity(models.Model):
    design_element_id  = models.CharField(max_length=200)
    activity_name  = models.CharField(max_length=200)
    class Meta:
        db_table = "activities"
        verbose_name  = 'Activitie'
        
        
