create database AirPort
use AirPort
create table if not exists Aircraft(idAircraft int primary key auto_increment,NameAirport text,FirstClass int,EconomyClass int,BusinessClass int);
create table if not exists Sector(idSector  int primary key auto_increment,Source text,Destination text,WeekDay text,FirstClass int,EconomyClass int,BusinessClass int);
create table if not exists Flight(idFlight int primary key auto_increment,DepartureTime text,ArrivaTime text,PrixFlight text,idAircraft int,idSector  int,
foreign key (idAircraft) references Aircraft(idAircraft) on delete cascade on update cascade ,foreign key (idSector) references  Sector(idSector) on delete cascade on update cascade );
create table if not exists Schedule(idSchedule int primary key auto_increment ,FlightDate date,idFlight int, foreign key (idFlight) references Flight(idFlight) on delete cascade on update cascade);

create table if not exists Passenger(idPassenger int primary key auto_increment,Email text,FullName text,Password text);
create table if not exists Reservation(idReservation int primary key auto_increment,DateReservation date ,Class text);
select * from Flight;
SELECT idSchedule ,FlightDate,NameAirport,Source,Destination,Sector.FirstClass,Sector.EconomyClass ,Sector.BusinessClass   FROM Schedule INNER JOIN  Flight on Flight.idFlight=Schedule.idFlight INNER join Sector on Sector.idSector=Flight.idFlight INNER JOIN  Aircraft on Aircraft.idAircraft=Flight.idAircraft




insert into Passenger(Email ,FullName,Password) values("abbih1998@gmail.com","AbbihZakariyae","1998");
select * from Passenger;

