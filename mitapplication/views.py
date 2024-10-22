from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
import random
import hashlib
from student.models import Form2019Payment1
from django.db import models
from django.views.decorators.csrf import csrf_exempt 

def payment_view(request):
    if request.method == 'POST':        
        # Get the last ID and generate a new order ID
        last_id = Form2019Payment1.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
        order_id = random.randint(100000, 999999) * 1000000 + last_id + 1

        # Prepare data to insert
        insert_data = {
            'order_id': order_id,
            'course': 'mca',
            'first_name': 'laxman',
            'middle_name': 'Balaji',
            'last_name': 'Kendre',            
            'email': 'lkendre2525@gmail.com',
            'phone': '8668282906',
            'address': 'pune',
            'city': 'Pune',
            'state': 'Maharashtra',
            'pincode': '411039',            
            'currency': 'INR',
            'amount': 1800
        }        
        # Create the payment object
        form_payment, created = Form2019Payment1.objects.get_or_create(order_id=order_id, defaults=insert_data)
        
        if created:            
            # Prepare data for redirection to BillDesk
            amount = 1800.00
            name = "Laxman" + " " + "Kendre"
            city = "Pune"
            str_data = f"MIT|123456789|NA|1800.00|NA|NA|NA|INR|NA|R|mit|NA|NA|F|8668282906|lkendre2525@gmail.com|NA|NA|NA|NA|NA|http://www.mitbio.edu.in/admission-2019-thank-you/"
            checksum = hashlib.sha256(str_data.encode()).hexdigest().upper() 
            #print(checksum)           
            str1_data = f"{str_data}|{checksum}"
            #print(str1_data)
            # Render the form to submit to BillDesk
            #MIT|123456789|NA|94.00|NA|NA|NA|INR|NA|R|mit|NA|NA|F|8668282906|lkendre2525@gmail.com|NA|NA|NA|NA|NA|http://www.mitbio.edu.in/admission-2019-thank-you/|185C45CAC99CEFAA0934628C0DD54A85398AC887DC52D9AF0C9DC6F070C2CFC5
            #MIT|123456789|NA|94.00|NA|NA|NA|INR|NA|R|mit|NA|NA|F|8668282906|lkendre2525@gmail.com|NA|NA|NA|NA|NA|http://www.mitbio.edu.in/admission-2019-thank-you/|185C45CAC99CEFAA0934628C0DD54A85398AC887DC52D9AF0C9DC6F070C2CFC5
            return render(request, 'student/payment_redirect.html', {'msg': str1_data})
        else:
            return HttpResponse("Error: Order ID already exists")
    return render(request, 'student/pay.html')
@csrf_exempt
def BillTest(request):
    import hashlib
    import requests
    name = "Laxman Kendre"
    city = "Pune"
    amt = 1800
    str_data = f"MIT|202510211|NA|{amt}|NA|NA|NA|INR|NA|R|mit|NA|NA|F|AdditionalInfo1|MBSR|lkendre2525@gmail.com|8668282906|{name}|{city}|AdditionalInfo7|https://www.mitbio.edu.in/admission-2021-thank-you/"
    checksum = hashlib.sha256(str_data.encode()).hexdigest().upper()
    str1_data = f"{str_data}|{checksum}"
    # Make a POST request
    url = "https://pgi.billdesk.com/pgidsk/PGIMerchantPayment"
    payload = {'msg': str1_data}
    # response = requests.post(url, data=payload)

    # print(response.text)
    return redirect("https://mitbio.edu.in/billdesk.php?sutd_id=202510100")
    return JsonResponse({'res': response.text})

def _phpBillGateway(request):
    # <?php 

    # //echo $_GET['sutd_id'];
    # $name = "Laxman Kendre";
    # $city = "Pune";
    # $amt = 1800;
    # //$sutd_id = 'sutd_id'
    # // get all data dyanamic


    # $str = "MIT|".$_GET['sutd_id']."|NA|$amt|NA|NA|NA|INR|NA|R|mit|NA|NA|F|AdditionalInfo1|MBSR|lkendre2525@gmail.com|8668282906|".$name."|".$city."|AdditionalInfo7|https://www.mitbio.edu.in/admission-2021-thank-you/";
    #         $checksum = hash_hmac('sha256',$str,'0A04TJUG348O', false);
    #         $checksum = strtoupper($checksum);
    #         $str1 = "MIT|".$_GET['sutd_id']."|NA|$amt|NA|NA|NA|INR|NA|R|mit|NA|NA|F|AdditionalInfo1|MBSR|lkendre2525@gmail.com|8668282906|".$name."|".$city."|AdditionalInfo7|https://www.mitbio.edu.in/admission-2021-thank-you/|".$checksum; 
    # $msg = $_POST['msg'];
    #         ?>
    #         <form method="post" name="redirect" action="https://pgi.billdesk.com/pgidsk/PGIMerchantPayment"> 
    #         <?php
    #         echo "<input type=hidden name='msg' value='".$str1."'>";
    #         ?>
    #         </form>
    #         <script language='javascript'>document.redirect.submit();</script>
    return HttpResponse(200)


