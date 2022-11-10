#--------------------import some mould-------------#
from flask import  Flask ,render_template,request,redirect,url_for,flash,session
import  os
import mysql.connector
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1889",
    database="AirPort"
)
#----------StartProject------------#
#listCountry
listCountry=[
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Belarus",
    "Bhutan",
    "Blize",
    "canada",
    "China",
    "colombia",
    "Morocco",
    "Mongolia",
    "Mali",
    "Malisya",
    "palestine",
    "panama",
    "Iran",
    "Iraq",
    "Italya",
    "India",
    "Iceland",
    "Qatar",
    "United Arab Emirates",
    "United States of America",
    "South Korea",
    "Sudan",
    "Saudi Arabia",
    "San Marino",
    "Singapore",
    "Dominica",
    "Denmark"]
#listDay
listDay=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","sunday"]
#ClassPlace
ClassPlace=["FirstClass","EconomyClass","BusinessClass"]
#function DisplayAircraft
def DisplayAircraft():
    
    cur=db.cursor()
    cur.execute('select idAircraft from Aircraft')
    all_aircraft=cur.fetchall()
    all_aircraft=[str(val[0]) for val in all_aircraft]
    return all_aircraft
#function DisplaySector
def DisplaySector():
     
     cur=db.cursor()
     cur.execute("select idSector from Sector")
     all_sector=cur.fetchall()
     all_sector=[str(val[0]) for val in all_sector]
     return all_sector
#function DisplayFlight
def DisplayFlight():
    
     cur=db.cursor()
     cur.execute("select idFlight from Flight")
     all_Flight=cur.fetchall()
     all_Flight=[str(val[0]) for val in all_Flight]
     return all_Flight
#*****************************#  
app=Flask(__name__)
app.secret_key=os.urandom(150)
#------------page principale--------------#
@app.route('/')
def PageUser():
        
        if "Email" in session:
            
            cur=db.cursor()
            cur.execute("select Schedule.FlightDate,Flight.DepartureTime,Flight.ArrivaTime,Flight.PrixFlight,Flight.Seat,Sector.Source,Sector.Destination,Aircraft.NameAirport from  Schedule inner join  Flight on  Schedule.idFlight=Flight.idFlight inner join Sector on Sector.idSector=Flight.idSector inner join Aircraft on Aircraft.idAircraft=Flight.idAircraft  ")
            SearchFlight=cur.fetchall()
            return render_template("PageUser.html",Search=SearchFlight,ClassPlace=ClassPlace)
        return render_template("Contact.html")
#-------------PagSingup--------------#
@app.route('/SingUp')
def SingUp():
    return  render_template("SingUp.html")
@app.route("/AddSingUp",methods=["GET","POST"])
def AddSingUp():
    

    
    if request.method=="POST":
       
        NameUser=request.form.get("NameUser")
        EmailUser=request.form.get("EmailUser")
        PasswordUser= request.form.get("PasswordUser")
        PasswordConfirm=request.form.get("PasswordConfirm")

        if PasswordUser !=PasswordConfirm or NameUser=="" or EmailUser=="" or  PasswordUser=="" or PasswordConfirm=="":
            flash("Full all control or Password not confirm" ,category="Confirm")
        else:
            print("OK")
            cur=db.cursor()
            cur.execute("insert into Passenger(Email,FullName,Password) values(%s,%s,%s)",(EmailUser, NameUser ,PasswordUser))
            db.commit()
            flash("SingUp Successfly",category="successfly")
           
            return render_template("Contact.html")
    return render_template("SingUp.html")
#-----------------Pagelogin----------------#
@app.route('/User')
def UserContacte():
    return  render_template("UserContacte.html")
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        Email=request.form["Email"]
        password=request.form["password"]
        
        cur = db.cursor()
       
        cur.execute("select  Password, Email  from Passenger where Password ='"+password +"' and Email='"+Email+"'  ")
        Data=cur.fetchall()
        cur=db.cursor()
        cur.execute("select Schedule.FlightDate,Flight.DepartureTime,Flight.ArrivaTime,Flight.PrixFlight ,Flight.Seat,Sector.Source,Sector.Destination,Aircraft.NameAirport from  Schedule inner join  Flight on  Schedule.idFlight=Flight.idFlight inner join Sector on Sector.idSector=Flight.idSector inner join Aircraft on Aircraft.idAircraft=Flight.idAircraft  ")
        SearchFlight=cur.fetchall()
       
        if len((Data))>0:
            session["loggedinUser"]=True
            session["Email"] = Email
            Email=session["Email"]
            return render_template("PageUser.html",Email=Email,listCountry=listCountry,Search=SearchFlight,ClassPlace=ClassPlace)
            
           
        else:
            if Email=="" and password=="":
                flash("Fill all control", category="Confirm")
            else:
                if ((Email.upper()=="ZORO1889@GMAIL.COM" or Email.lower()=="zoro1889@gmail.com") and (password.upper()=="ADMIN" or password.lower()=="admin")): 
                         session["Email"] = Email
                         Email=session["Email"]
                         return redirect(url_for("PagedAdmin"))
               
            flash("your Password or Email not correct", category="Confirm")
            return render_template("Contact.html")
#------------------logout-------------#
@app.route("/logout")
def logout():
        session.clear()
        return render_template("Contact.html")
#--------------------------------------PageUser----------------------------------------------------------------------------------#
@app.route('/Contact')
def PageContact():
    return  render_template("Contact.html")
@app.route("/Resrvation",methods=["POST","GET"])
def PageResvation():
    if request.method=="POST":
        NumberPlace=request.form.get("NumberPlace")
        DateResrvation=request.form.get("DateResrvation")
        Placeclass=request.form.get("Placeclass")
        cur=db.cursor()
        cur.execute("insert into Reservation(NumberPlace,DateReservation,Class) values(%s,%s,%s)",(NumberPlace,DateResrvation,Placeclass))
        db.commit()
        
        
        return redirect(url_for("PageUser"))
    return render_template("PageUser.html")
#---------------------------------------PageAdmin-------------------------------------------------------------------------------#
@app.route('/Admin')
def PagedAdmin():
    if "Email" in session:
        curAir=db.cursor()
        curAir.execute("select * from Aircraft")
        dataAircraft= curAir.fetchall()

        curSector=db.cursor()
        curSector.execute("select * from Sector")
        dataSector=curSector.fetchall()
        
        
        curFlight=db.cursor()
        curFlight.execute("SELECT idFlight,DepartureTime,ArrivaTime,PrixFlight,Seat,flight from Flight ")
        all_Flight=curFlight.fetchall()
        
        
        
        
        
        curSchedule=db.cursor()
        curSchedule.execute("SELECT idSchedule ,FlightDate,NameAirport,Source,Destination,Sector.FirstClass,Sector.EconomyClass ,Sector.BusinessClass   FROM Schedule INNER JOIN  Flight on Flight.idFlight=Schedule.idFlight INNER join Sector on Sector.idSector=Flight.idFlight INNER JOIN  Aircraft on Aircraft.idAircraft=Flight.idAircraft")
        data_Schedule=curSchedule.fetchall()
        
       
        curUser=db.cursor()
        curUser.execute("SELECT Email,FullName from Passenger")
        data_passanger=curUser.fetchall()
        
        
        curResvation=db.cursor()
        curResvation.execute("select * from  Reservation")
        data_Resvation=curResvation.fetchall()







        return render_template("PageAdmin.html",dataAircraft=dataAircraft,dataSector=dataSector,all_Flight=all_Flight ,data_Schedule=data_Schedule,data_passanger=data_passanger,data_Resvation=data_Resvation)

    return render_template("Contact.html")
@app.route('/DashboardAdmin')
def DashboardAdmin():
    return redirect(url_for('PagedAdmin'))
#------------------------------------------------#
#-----------------PageAircraft----------------#
@app.route('/Aircraft')
def PageAircraft():
    if "Email" in session:
        
        cur = db.cursor()
        cur.execute("select * from Aircraft")
        dataAircraft = cur.fetchall()

        return  render_template("Aircraft.html",dataAircraft=dataAircraft)
    return render_template("Contact.html")
#*********AddAircraft**************************#
@app.route("/AddAircraft",methods=["GET","POST"])
def PageAddAircraft():
   
    if request.method=="POST":
       
        Airport=request.form.get('Airport')
        FirstClass=request.form.get("FirstClass")
        economyClass=request.form.get("economyClass")
        BusinessClass=request.form.get("BusinessClass")
        cur=db.cursor()
        cur.execute("insert into Aircraft(NameAirport,FirstClass ,EconomyClass,BusinessClass) values(%s,%s,%s,%s)",(Airport,FirstClass,economyClass,BusinessClass))
        db.commit()
        flash("Element Add Successfly", category="successfly")
        return redirect(url_for('PageAircraft'))
    return render_template("Aircraft.html")
#*********DeleteAircraft**************************#
@app.route("/DeleteAircraft/<string:id>")
def DeleteAircraft(id):

        
        cur = db.cursor()
        cur.execute("delete  from Aircraft where idAircraft={0}".format(id))
        db.commit()
        flash("Element is Delete Successfly", category="Confirm")
        return redirect(url_for('PageAircraft'))
#*********DeleteAircraft**************************#
@app.route('/EditAircraft/<id>')
def Edit(id):
    
    cur=db.cursor()
    cur.execute("select * from Aircraft where idAircraft={0}".format(id))
    data=cur.fetchall()
    return render_template("EditAircraft.html",data=data[0])
#*********UpdateAircraft**************************#
@app.route("/updateAircraft/<id>",methods=["POST","GET"])
def UpdateAircraft(id):
    
    Airport = request.form.get('Airport')
    FirstClass = request.form.get("FirstClass")
    economyClass = request.form.get("economyClass")
    BusinessClass = request.form.get("BusinessClass")
    if request.method == "POST":

        cur=db.cursor()
        cur.execute("update  Aircraft set  NameAirport=%s, FirstClass=%s,EconomyClass=%s,BusinessClass=%s where idAircraft=%s",(Airport,FirstClass,economyClass,BusinessClass,id))
        db.commit()
        flash("Element Update Successfly", category="successfly")
        return redirect(url_for('PageAircraft'))
#------------------------------------------------#
#-----------------PageSector----------------#
@app.route('/Sector')
def PageSector():
   
    curSector = db.cursor()
    curSector.execute("select * from Sector")
    dataSector = curSector.fetchall()
    if "Email" in session:
        return  render_template("Sector.html",listCountry=listCountry,listDay=listDay,dataSector=dataSector)
    return render_template("Contact.html")
#************AddSector*************#
@app.route('/AddSector',methods=["POST","GET"])
def AddSector():
   
   
    Source=request.form.get("Source")
    Destination=request.form.get("Destination")
    WeekDay=request.form.get("WeekDay")
    FirstClass=request.form.get("FirstClass")
    EconomyClass=request.form.get("EconomyClass")
    BusinessClass=request.form.get("BusinessClass")

    if request.method=="POST":
        cur=db.cursor()
        cur.execute("insert into Sector(Source ,Destination ,WeekDay,FirstClass ,EconomyClass ,BusinessClass ) values(%s,%s,%s,%s,%s,%s)",
                    (Source,Destination,WeekDay,FirstClass,EconomyClass,BusinessClass))
        db.commit()
        flash("Element Add Successfly", category="successfly")
        return  redirect(url_for("PageSector"))
    return render_template("Sector.html")
#************DeleteSector*************#
@app.route('/DeleteSector/<string:idSector>')
def DeleteSector(idSector):
    cur=db.cursor()
    cur.execute("delete from Sector where idSector={0} ".format(idSector))
    db.commit()
    return redirect(url_for("PageSector"))
#************EditSector*************#
@app.route('/EditSector/<idSector>')
def EditSector(idSector):
    cur=db.cursor()
    
    cur.execute("select * from Sector where idSector={0} ".format(idSector))
    data=cur.fetchall()
    return render_template("EditSector.html",data=data[0],listCountry=listCountry,listDay=listDay)
#************UpdateSector*************#
@app.route('/UpdateSector/<idSector>',methods=["POST","GET"])
def updateSector(idSector):
    if request.method=="POST":
       
        Source=request.form.get("Source_")
        Destination=request.form.get("Destination")
        WeekDay=request.form.get("WeekDay")
        FirstClass=request.form.get("FirstClass")
        EconomyClass=request.form.get("EconomyClass")
        BusinessClass=request.form.get("BusinessClass")
       
        cur=db.cursor()
        cur.execute(" update Sector set Source=%s,Destination=%s,WeekDay=%s,FirstClass=%s,EconomyClass=%s,BusinessClass=%s where  idSector=%s",(Source,Destination, WeekDay,FirstClass,EconomyClass,BusinessClass,idSector))
        db.commit()
        flash("Element Update Successfly", category="successfly")
        return redirect(url_for('PageSector'))
    return render_template("Contact.html")
#------------------------------------------------#
#-----------------PageFlights----------------#
@app.route('/Flights')
def PageFlight():
    
    if "Email" in session:
        
        all_air_data=DisplayAircraft()
        all_sector_data=DisplaySector()
        
        cur=db.cursor()
        cur.execute("SELECT idFlight,DepartureTime,ArrivaTime,PrixFlight,Seat,flight from Flight ")
        all_Flight=cur.fetchall()
        return  render_template("Flights.html",all_air=all_air_data,all_sector=all_sector_data,all_Flight=all_Flight)
    return render_template("Contact.html")
#************AddFlights*************# 
@app.route('/AddFlights',methods=["POST","GET"])
def AddFlights():
    if request.method=="POST":
        DepartureTime=request.form.get("DepartureTime")
        ArrivalTime=request.form.get("ArrivalTime")
        PrixFlight=request.form.get("PrixFlight")
        AircraftID=request.form.get("AircraftID")
        SectorID=request.form.get("SectorID")
        
        Seat=request.form.get("Seat")
        Flight=request.form.get("Flight")
        
        cur=db.cursor()
        
        cur.execute("insert into Flight(DepartureTime,ArrivaTime,PrixFlight,idAircraft,idSector,Seat,flight) values(%s,%s,%s,%s,%s,%s,%s)",
                (DepartureTime,ArrivalTime,PrixFlight,AircraftID,SectorID,Seat,Flight))
        flash("Element Add Successfly", category="successfly")
        db.commit()
        return redirect(url_for("PageFlight"))
    return render_template("Contact.html")
#************DeleteFlights*************#
@app.route('/DeleteFlights/<string:idFlights>')
def DeleteFlights(idFlights):
    
    cur=db.cursor()
    cur.execute("delete  from Flight where idFlight={0}".format(idFlights))
    
    db.commit()
    flash("Element Delte Successfly", category="successfly")
    return redirect(url_for("PageFlight"))
#************EditFlights*************#
@app.route('/EditFlights/<idFlights>')
def EditFlights(idFlights):
    all_air_data=DisplayAircraft()
    all_sector_data=DisplaySector()
   
    cur=db.cursor()
    cur.execute("select * from  Flight where idFlight={0}".format(idFlights))
    all_data_Flight=cur.fetchall()
    return render_template("EditFlight.html",all_data_Flight=all_data_Flight[0],all_air_data=all_air_data,all_sector_data=all_sector_data)
#************UpdateFlights*************#
@app.route('/UpdateFlights/<all_data_Flight>',methods=['POST','GET'])
def updateFlights(all_data_Flight):
    if request.method=="POST":
        DepartureTime=request.form.get("DepartureTime")
        ArrivalTime=request.form.get("ArrivalTime")
        PrixFlight=request.form.get("PrixFlight")
        AircraftID=request.form.get("AircraftID")
        SectorID=request.form.get("SectorID")
        
        Seat=request.form.get("Seat")
        Flight=request.form.get("Flight")
       
        cur=db.cursor()
        cur.execute("update Flight set DepartureTime=%s,ArrivaTime=%s,prixFlight=%s,idAircraft=%s,idSector=%s,Seat=%s,flight=%s where idFlight=%s",(DepartureTime,ArrivalTime,PrixFlight,AircraftID,SectorID,Seat,Flight,all_data_Flight))
        db.commit()
        return redirect(url_for("PageFlight"))
    return render_template("Contact.html")
#---------------------PageSchedule-------------------------------#
@app.route('/Schedule')
def PageSchedule():
    if "Email" in session:
        data_Flight=DisplayFlight()
        
        cur=db.cursor()
        cur.execute("SELECT idSchedule ,FlightDate,FirstClass,EconomyClass ,BusinessClass FROM Schedule INNER JOIN  Flight on Flight.idFlight=Schedule.idFlight INNER join Sector on Sector.idSector=Flight.idSector ")
        data_Schedule=cur.fetchall()
        return  render_template("Schedule.html",data_Flight=data_Flight,data_Schedule=data_Schedule)
    return render_template("Contact.html")
#************AddSchedule*************#
@app.route('/AddSchedule',methods=['POST',"GET"])
def AddSchedule():
    if request.method=="POST":
       
        FlightDate=request.form.get('FlightDate')
        idFlight=request.form.get("idFlight")
        
        
        cur=db.cursor()
        cur.execute("insert into Schedule(FlightDate,idFlight) values(%s,%s)",(FlightDate,idFlight))
        db.commit()
        flash("Element Add Successfly", category="successfly")
        return redirect(url_for("PageSchedule"))
    return render_template("Contact.html")
#************DeleteSchedule*************#
@app.route('/DeleteSchedule/<string:idSchedule>')
def DeleteSchedule(idSchedule):
   
    cur=db.cursor()
    cur.execute("delete from Schedule where idSchedule={0}".format(idSchedule))
    db.commit()
    return redirect(url_for("PageSchedule"))
#************EditSchedule*************#
@app.route('/EditSchedule/<idSchedule>')
def EditSchedule(idSchedule):
    data_Flight=DisplayFlight()
    
    cur=db.cursor()
    cur.execute("select * from Schedule where idSchedule={0}".format(idSchedule))
    dataSchedule=cur.fetchall()
    return render_template("EditSchedule.html",dataSchedule=dataSchedule[0],data_Flight=data_Flight)
#************UpdateSchedule*************#
@app.route('/UpdateSchedule/<idSchedule>',methods=["POST","GET"])
def UpdateSchedule(idSchedule):
    if request.method=="POST":
        FlightDate=request.form.get('FlightDate')
        idFlight=request.form.get("idFlight")
        
        
        cur=db.cursor()
        cur.execute("update Schedule set   FlightDate=%s,idFlight=%s  where idSchedule=%s",(FlightDate,idFlight,idSchedule))
        db.commit()
        return redirect(url_for("PageSchedule"))
    return render_template("Contact.html")
#***************UserConnect****************#
@app.route('/UserConnect')
def UserConnect():
    if "Email" in session:
       
        cur=db.cursor()
        cur.execute("select idPassenger,Email,FullName from Passenger")
        data_passanger=cur.fetchall()
        return render_template("UserContacte.html",data_passanger=data_passanger)
    return render_template("Contact.html")
#***************DelteUserConnect****************#fff
@app.route('/DeleteUserConnect/<string:idUser>')
def UserDeleteConnect(idUser):
   
    cur=db.cursor()
    cur.execute("delete from Passenger where idPassenger={0}".format(idUser))
    db.commit()
    return redirect(url_for("UserConnect"))
if __name__=="__main__":
    app.run(debug=True)
#-----------------endproject----------------#

