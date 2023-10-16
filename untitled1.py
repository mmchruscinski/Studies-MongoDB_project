import tkinter as tk
from tkcalendar import Calendar
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['Tickets']


sel_date = "5/29/23"
RoutesList = []
CoursesList = []
RoutesListNew = []
LenList = []
st1_sel = "Kraków"
st2_sel = "Kielce"
col_routes = db['Routes']
col_courses = db['Courses']
    
data_courses = col_courses.aggregate([{"$lookup": {"from": "Routes", "localField": "Route_id", "foreignField": "_id", "as": "Route" } }, {"$match": {"$and": [{"Date" : sel_date }, {"Route.Route" : st1_sel}, {"Route.Route" : st2_sel} ] } } ])
#data_routes = data_courses['Route']

   
for document in data_courses:
    CoursesList.append(document["Route"][0]["Route"])
    print(document["Route"][0]["Route"])

'''        
print("\n\n\n")
        
for item in CoursesList:
    print(item["Name"])
'''