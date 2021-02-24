from django.urls import path
from civil import views

urlpatterns = [
    path('civil', views.index, name='index'),
    
    
    path('import_activities/', views.import_activities, name='import_activities'),
    path('read_import_activities/', views.read_import_activities, name='read_import_activities'),
    
    path('activities/', views.activities, name='activities'),
    path('add_activity/', views.add_activity, name='add_activity'),
    path('insert_activity/', views.insert_activity, name='insert_activity'),
    path('delete_activities/', views.delete_activities, name='delete_activities'),

    path('design_elements/', views.design_elements, name='design_elements'),
    path('add_design_elements/', views.add_design_elements, name='add_design_elements'),
    path('insert_design_elements/', views.insert_design_elements, name='insert_design_elements'),
    path('delete_design_elements/', views.delete_design_elements, name='delete_design_elements'),
    
    path('insert_hazard/', views.insert_hazard, name='insert_hazard'),
    path('add_hazards/', views.add_hazards, name='add_hazards'),
    path('add_new_hazard/', views.add_new_hazard, name='add_new_hazard'),
    path('insert_new_hazard/', views.insert_new_hazard, name='insert_new_hazard'),
    path('view_hazard/', views.view_hazard, name='view_hazard'),
    
    path('your_projects/', views.your_projects, name='your_projects'),
    path('add_project/', views.add_project, name='add_project'),
    path('insert_project/', views.insert_project, name='insert_project'),
    path('view_detail_project/', views.view_detail_project, name='view_detail_project'),
    path('delete_project/', views.delete_project, name='delete_project'),
    
    
    path('logout/', views.logout),
    path('signup/', views.signup),
    
    path('insert_signup/', views.insert_signup, name='insert_signup'),
    path('checklogin', views.checklogin),

    path('search_hazards/', views.search_hazards, name='search_hazards'),
    
    path('ajax/load-activities/', views.load_activities, name='ajax_load_activities'), 

]