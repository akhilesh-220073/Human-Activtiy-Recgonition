input_phenomenon(motion(_Source,_Location,_Value),event).
input_phenomenon(current(_Source,_Location,_Value),event).
input_phenomenon(light(_Source,_Location, _Value),event).
input_phenomenon(pressure(_Source,_Location, _Value),event).
input_phenomenon(contact(_Source, _Location, _Value),event).
input_phenomenon(humidity(_Source, _Location, _Value),event).
input_phenomenon(temperature(_Source, _Location, _Value),event).

%having_bath
state_phenomenon increasedHumidity(Source, Location):= 
    (humidity(Source, Location, Value1) aand (threshold(humidity, Source, Location, Threshold1), Value1 > Threshold1)) ~> 
    (humidity(Source, Location, Value2) aand (threshold(humidity, Source, Location, Threshold2), Value2 < Threshold2)).

state_phenomenon havingBath(Location):=
    increasedHumidity(ambience, Location) aand member(Location, [bathroom]).

%state_phenomenon longtimehumidity(Source,Location):=
    %filter((humidity(Source,Location)),greater(600000)).

state_phenomenon deviceOn(Source, Location):= 
    (current(Source, Location, Value1) aand (threshold(current, Source, Location, Threshold1), Value1 > Threshold1)) ~> 
    (current(Source, Location, Value2) aand (threshold(current, Source, Location, Threshold2), Value2 < Threshold2)).

%Entering_the_house
event_phenomenon openOrCloseDoor(Location):=
    contact(door, Location, Value) aand (threshold(contact, door, Location, Threshold), Value > Threshold).

state_phenomenon lightIsOn(Source, Location):=
    (light(Source, Location, Value1) aand (threshold(light, Source, Location, Threshold1), Value1 > Threshold1)) ~> 
    (light(Source, Location, Value2) aand (threshold(light, Source, Location, Threshold2), Value2 < Threshold2)).

state_phenomenon lightIsOff(Source, Location):=
    (light(Source, Location, Value1) aand (threshold(light, Source, Location, Threshold1), Value1 < Threshold1)) ~> 
    (light(Source, Location, Value2) aand (threshold(light, Source, Location, Threshold2), Value2 > Threshold2)).

state_phenomenon personOnObject(Object, Location):= 
    (pressure(Object, Location, Value1) aand (threshold(pressure, Object, Location, Threshold1), Value1 > Threshold1)) ~>
    (pressure(Object, Location, Value2) aand (threshold(pressure, Object, Location, Threshold2), Value2 < Threshold2)).


%watching_tv
state_phenomenon watchingTV(AtLocation, FromLocation):=
    lightIsOn(tv, AtLocation) intersection personOnObject(FromLocation, AtLocation).

state_phenomenon personInRoom(Location):=
    (motion(_Source, Location, Value1) aand Value1 > 0.5)  <@ 60000.

state_phenomenon stoveIsOn(Location):=
    (light(stove, Location, Value1) aand (threshold(light, stove, Location, Threshold1), Value1 > Threshold1)) ~>
    (light(stove, Location, Value2) aand (threshold(light, stove, Location, Threshold2), Value2 < Threshold2)).

%Cooking
%state_phenomenon personCooking(AtLocation, FromLocation):=
    %stoveIsOn(stove, AtLocation) intersection personInroom(FromLocation, AtLocation).

%sleeping_pattern
state_phenomenon personSleeping(Location):=
    filter(
        (
            (lightIsOff(_Source, Location) aand member(Location, [bedroom]))
            intersection 
            (personOnObject(bed, Location) aand member(Location, [bedroom]))
        ),
        greater(3600000)).
%filter(((lightIsOff(_Source, bedroom) aand threshold(sleeptime, Value)) intersection personOnObject(bed, bedroom)), greater(Value)).

% state_phenomenon makingSandwich(Location):=
%     (current(sandwichmaker, Location, Value1) aand (threshold(current, sandwichmaker, Location, Threshold1), Value1 > Threshold1)) ~> 
%     (current(sandwichmaker, Location, Value2) aand (threshold(current, sandwichmaker, Location, Threshold2), Value2 < Threshold2)). 

state_phenomenon longTimeSameRoom(Location):=
    filter((personInRoom(Location) complement personSleeping(Location)), greater(10800000)).

state_phenomenon veryLongBath(Location):=
    filter((havingBath(Location)), greater(3600)).

state_phenomenon deviceOnDuringSleep(Location):=
    personSleeping(Location) intersection deviceOn(_Source, _Location).

state_phenomenon tvLeftOpen(PersonLocation, TVLocation):=
    lightIsOn(tv, TVLocation) intersection (personInRoom(PersonLocation) aand (PersonLocation \= TVLocation)).

state_phenomenon deviceOpenInOtherRoom(PLocation, Device, DLocation):=
    personInRoom(PLocation) intersection (deviceOn(Device, DLocation) aand (PLocation \= DLocation)).

dynamic_phenomenon leavingHouse(Location):=
    personInRoom(corridor) before (openOrCloseDoor(Location) aand member(Location, [entrance])).

dynamic_phenomenon leavingWithDeviceOn(Location, DLocation, Device):=
    leavingHouse(Location) contains (current(Device, DLocation, Value) aand (threshold(current,Device, DLocation,Threshold), Value > Threshold)).

dynamic_phenomenon leavingWithWaterOn(Location):=
    leavingHouse(Location) contains increasedHumidity(Location).














  
