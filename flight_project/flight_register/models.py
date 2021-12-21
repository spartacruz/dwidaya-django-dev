from django.db import models
from django.db.models.deletion import CASCADE
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import datetime

# Create your models here.
class Flight(models.Model):
    flight_code = models.CharField(max_length=4)
    flight_location = models.CharField(max_length=50)

    def __str__(self):
        text = self.flight_code + " - " + self.flight_location
        return text

class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=50)

    flightfrom = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='+')
    flightto = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='+')
    departuredate = models.CharField(max_length=10)
    returndate = models.CharField(max_length=10)

def validation_data(datanya):
    error_message = None

    #flight validation
    if datanya['flightfrom'] == datanya['flightto']:
        error_message = "Flight from and Flight To cannot be same destination"
        return error_message
    
    #date validation:
    if len(datanya['departuredate']) < 10:
        error_message = "Invalid date format. Should be dd-mm-yyyy (e.g 01-12-2021)"
        return error_message

    elif datanya['departuredate'][2] != '-' or datanya['departuredate'][5] != '-':
        error_message = "Invalid Departure or Return date format. Should be dd-mm-yyyy (e.g 01-12-2021)"
        return error_message

    elif datanya['returndate'][2] != '-' or datanya['returndate'][5] != '-':
        error_message = "Invalid Departure or Return date format. Should be dd-mm-yyyy (e.g 01-12-2021)"
        return error_message

    elif not 1 <= int(datanya['departuredate'][0:2]) < 32:
        error_message = "Invalid Departure or Return date day. Should be from 01 - 31 (e.g dd-mm-yyyy)"
        return error_message
    
    elif not 1 <= int(datanya['departuredate'][3:5]) < 13:
        error_message = "Invalid Departure or Return date month. Should be from 01 - 12 (e.g dd-mm-yyyy)"
        return error_message
    
    elif not 1 <= int(datanya['returndate'][0:2]) < 32:
        error_message = "Invalid Departure or Return date day. Should be from 01 - 31 (e.g dd-mm-yyyy)"
        return error_message
    
    elif not 1 <= int(datanya['returndate'][3:5]) < 13:
        error_message = "Invalid Departure or Return date month. Should be from 01 - 12 (e.g dd-mm-yyyy)"
        return error_message

    elif not 2021 <= int(datanya['departuredate'][6:]) < 2023:
        error_message = "Invalid Departure or Return date year. Should be from 2021 - 2022"
        return error_message
    
    elif not 2021 <= int(datanya['returndate'][6:]) < 2023:
        error_message = "Invalid Departure or Return date year. Should be from 2021 - 2022"
        return error_message
    
    # current_time = datetime.now().date()
    depart = datetime.strptime(datanya['departuredate'], "%d-%m-%Y").date()
    returndate = datetime.strptime(datanya['returndate'], "%d-%m-%Y").date()

    # time_check_departure = depart < current_time
    # time_check_return = returndate < current_time
    time_diff = depart > returndate

    # if time_check_departure == True:
    #     error_message = "Departure date cannot be earlier than current date : " + str(current_time)
    #     return error_message

    # if time_check_return == True:
    #     error_message = "Return date cannot be earlier than current date : " + str(current_time)
    #     return error_message

    if time_diff == True:
        error_message = "Return date cannot be earlier than Departure date"
        return error_message
    

    #name validation
    first_name_check = datanya['firstname'].replace(" ", "")
    last_name_check = datanya['lastname'].replace(" ", "")

    if first_name_check.isalpha() != True or last_name_check.isalpha() != True:
        error_message = "First name and Last name should be alphabet characters only (e.g Yuri Iskandia)"
        return error_message

    elif len(datanya['firstname']) < 2 or len(datanya['lastname']) < 2:
        error_message = "First name and Last name cannot be less than 2 characters"
        return error_message    


    #email validation
    try:
        validate_email(datanya['email'])
    except ValidationError as e:
        error_message = "Please Enter a valid email address (e.g yuri.barru@gmail.com)"
        return error_message
    else:
        pass


    #mobile phone validation
    if datanya['mobile'].isdigit() != True:
        error_message = "Please Input a valid mobile phone number (e.g 081288690xxx)"
        return error_message
    
    elif len(datanya['mobile']) < 10:
        error_message = "Mobile number cannot be less than 10 digits"
        return error_message

    elif len(datanya['mobile']) > 13:
        error_message = "Mobile number cannot be more than 13 digits"
        return error_message

    elif datanya['mobile'][0] != '0' or datanya['mobile'][1] != '8':
        error_message = "Mobile Phone Number must be start with 08...."
        return error_message
