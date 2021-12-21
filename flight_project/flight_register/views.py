from django.core.checks.messages import Error
from django.shortcuts import redirect, render
from .forms import FlightForm
from .models import Customer
from .models import Flight
from .models import validation_data
from .create_table_fpdf2 import PDF
import zipfile
from django.http import FileResponse
from pgpy import PGPKey, PGPMessage
import os

# Create your views here.
def flight_list(request):
    context = {'customer_list': Customer.objects.all()}
    return render(request, "flight_register/flight_list.html", context)

def flight_form(request, id = 0):
    if request.method == "GET":
        if id == 0:
            form = FlightForm()
        else:
            customer = Customer.objects.get(pk = id)
            form = FlightForm(instance = customer)

        return render(request, "flight_register/flight_form.html", {'form': form})
    
    else:
        if id == 0:

            form = FlightForm(request.POST) #create new user
        else:
            customer = Customer.objects.get(pk = id) #updating user
            form = FlightForm(request.POST, instance = customer)

        #validation
        validasi = {
            'flightfrom': request.POST.get("flightfrom"),
            'flightto': request.POST.get("flightto"),
            'firstname': request.POST.get("firstname"),
            'lastname': request.POST.get("lastname"),
            'email': request.POST.get("email"),
            'mobile': request.POST.get("mobile"),
            'departuredate': request.POST.get("departuredate"),
            'returndate': request.POST.get("returndate"),
        }
        print(validasi)

        error_message = validation_data(validasi)

        if error_message:
            error_message = "Failed to submit data: " + error_message
            return render(request, "flight_register/flight_form.html", {'form': form, 'error':error_message})

        else:
            error_message = None

        if form.is_valid():
            form.save()
        
        return redirect('/flight/list')

def flight_delete(request, id):
    customer = Customer.objects.get(pk = id)
    customer.delete()
    return redirect('/flight/list')

def flight_export(request):

    template_dict = {
        'First Name':list(Customer.objects.all().values_list('firstname', flat=True)),
        'Last Name': list(Customer.objects.all().values_list('lastname', flat=True)),
        'Mobile': list(Customer.objects.all().values_list('mobile', flat=True)),
        'Email': list(Customer.objects.all().values_list('email', flat=True)),
        # 'Flight From': list(Customer.objects.all().values_list('flightfrom', flat=True)),
        # 'Flight To': list(Customer.objects.all().values_list('flightto', flat=True)),
        'Flight From': '',
        'Flight To': '',
        'Departure Date': list(Customer.objects.all().values_list('departuredate', flat=True)),
        'Return Date': list(Customer.objects.all().values_list('returndate', flat=True))
    }

    #iterate value from foreign key flight code
    key_flight_to = list(Customer.objects.all().values_list('flightto', flat=True))

    listku = []
    for i in key_flight_to:
        sample_test = Flight.objects.get(pk = i)
        valuenya = sample_test.flight_code
        listku.append(valuenya)
        
    template_dict['Flight To'] = listku

    key_flight_from = list(Customer.objects.all().values_list('flightfrom', flat=True))
    listku = []
    for i in key_flight_from:
        sample_test = Flight.objects.get(pk = i)
        valuenya = sample_test.flight_code

        listku.append(valuenya)
        
    #append with template dict
    template_dict['Flight From'] = listku

    #creating PDF file
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=10)
    pdf.create_table(table_data = template_dict, title='Dwidaya Passanger List', cell_width='even')
    pdf.ln()
    pdf.output('Report Passanger List.pdf')

    #zipping a file
    zipfile.ZipFile('Report Passanger List.zip', mode='w').write("Report Passanger List.pdf")
    cwd = os.getcwd()
    # path_zip = cwd + "\\" + 'Report Passanger List.zip'

    # zip_file = open(path_zip, 'rb')

    #encryptfile
    encryptFile(cwd)
    path_enc = cwd + "\\" + 'Report Passanger List.zip.encrypted'
    encrypted_file = open(path_enc, 'rb')
    
    return FileResponse(encrypted_file, as_attachment=True)

    #return redirect('/flight/list')

def encryptFile(cwd):
    pubkey, _ = PGPKey.from_file( cwd + "\\" + "testpublickey.key")
    pubkey._require_usage_flags = False

    direc = cwd + "\\" + "Report Passanger List.zip"

    message_from_file = PGPMessage.new(direc, file=True)
    encrypted_message = pubkey.encrypt(message_from_file)
    msgbytes = bytes(encrypted_message)

    with open('Report Passanger List.zip.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(msgbytes)
    
    #decryptFile(cwd)
    #testing()
