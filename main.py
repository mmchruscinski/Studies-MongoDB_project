import tkinter as tk
from tkcalendar import Calendar
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['Tickets']

# downloading the data
StationsList = []


col_stations = db['Stations']
data_stations = col_stations.find()
#data_stations = col_stations.find({"Name" : "Kraków"})

for document in data_stations:
    StationsList.append(document["Name"])



# root definition
root = tk.Tk()
root.title('PKP Intercity')
root.geometry('680x480')

r = tk.IntVar()
r.set(1)


    

# labels definition
label1 = tk.Label(root, text='System rezerwacji biletów', font=(25))
label2 = tk.Label(root, text='Stacja początkowa:')
label3 = tk.Label(root, text='Stacja końcowa:')
label4 = tk.Label(root, text='Data:')
label1.pack()

# functions
def ButtonSearch():
    sel_date = cal.get_date()
    RoutesList = []
    CoursesList = []
    RoutesListNew = []
    LenList = []
    idList = []
    st1_sel = st1.get()
    st2_sel = st2.get()
    col_routes = db['Routes']
    col_courses = db['Courses']
    
    data_courses = col_courses.aggregate([{"$lookup": {"from": "Routes", "localField": "Route_id", "foreignField": "_id", "as": "Route" } }, {"$match": {"$and": [{"Date" : sel_date }, {"Route.Route" : st1_sel}, {"Route.Route" : st2_sel} ] } } ])
    
    for document in data_courses:
        CoursesList.append(document["Route"][0])
        RoutesList.append([document["Route"][0]["Route"], document["_id"]])
        
    for item in RoutesList:
        if item[0].index(st1_sel) < item[0].index(st2_sel):
            
            RoutesListNew.append(item[0])
            #LenList.append(item[1])
            idList.append(item[1])
            
            print(item)
    counter = len(RoutesListNew)
    
    found = tk.Toplevel(root)
    found.title('Lista połączeń')
    found.geometry('450x450')
    
    labelFound = tk.Label(found, text=('Znalezionych połączeń w terminie ' + sel_date + ': ' + str(counter)))
    #r = tk.IntVar()
    #r.set(0)
     
    labelFound.pack()
    
    counters = []
    for i in range(counter):
        counters.append(i)
    print(counters)
    
    for i in counters:
        tk.Radiobutton(found, text=("Opcja " + str(i+1) ), variable=r, value=i).pack()
        
        labelRoute = tk.Label(found, text=RoutesListNew[i])
        labelRoute.pack()
    
    lab_mail = tk.Label(found, text = "Podaj email")
    lab_mail.pack()
    email = tk.Entry(found, width = 60)
    email.pack()
    
    buy_button = tk.Button(found, text =  'Kup bilet', command = lambda: ButtonBuy(r.get(), idList, email.get()), padx=30, pady=15)
    buy_button.pack()


def ButtonBuy(val, list, email):

    col = db["Courses"]
    users = db["Users"]
    
    filter = {"_id" : list[val]}
    seatsTaken = [col.find_one(filter)["SeatsTaken"], col.find_one(filter)["Seats"]]
    print(seatsTaken)
    if (seatsTaken[0] == seatsTaken[1]):
        seatsOcc()
    else:
        update = {"$set" : {"SeatsTaken" : seatsTaken[0]+1}}
        result = col.update_one(filter, update)
        
        filter = {"email" : email}
        result = users.update_one(filter, {"$push": {"tickets": list[val]}}, upsert=True)
        
        dialog()
        
    print("Matched Documents:", result.matched_count)
    print("Modified Documents:", result.modified_count)
    
    
    
def dialog():
    tk.messagebox.showinfo("Bilet", "Zakupiono bilet")
    
def seatsOcc():
    tk.messagebox.showinfo("Bilet", "Nie miejsc na wybrany kurs!")
    
def grad_date():
    tk.date.config(text = "Selected Date is: " + cal.get_date())

# buttons
search_button = tk.Button(root, text = 'Szukaj połączenia', command = ButtonSearch, padx=30, pady=15)

# input fields
label2.pack()
st1 = tk.StringVar(root)
drop1 = tk.OptionMenu(root, st1, *StationsList)
drop1.config(width=50)
drop1.pack()

label3.pack()
st2 = tk.StringVar(root)
drop2 = tk.OptionMenu(root, st2, *StationsList)
drop2.config(width=50)
drop2.pack()


# calendar
label4.pack()
cal = Calendar(root, selectmode = 'day')
cal.pack()


 
tk.date = tk.Label(root, text = "")
tk.date.pack()
    

search_button.pack()

root.mainloop()

client.close()