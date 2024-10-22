from django.shortcuts import render, HttpResponse, redirect
import hashlib
from django.contrib.auth.decorators import login_required
from .models import Account 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required(login_url='login')
def hostelConfirm(request):
    if request.method == "POST" and  request.user.paymentstatus != 'paid':
        hostel = request.POST.get('hostel_required')        
        hostelinc = [True if hostel == '1' else False ]
        # context = {
        #     'is_hostel' : hostelinc
        # }
        resp = Account.objects.filter(email=request.user.email).update(is_hostel=hostel)
        return HttpResponse(resp)



@login_required(login_url='login')
def _paymentDetails(request):
    if request.user.education_frm == True:    
        return render(request, 'student/payment.html')
    elif request.user.personal_frm == True:
        return redirect('academicform')
    else:
        return redirect('dashboard')

@login_required(login_url='login')
def _paymentDetails0(request):
    if request.method == 'GET':
        amount = 1500
        name = "Laxman Kendre"
        city = "Pune"
        order_id = "212154mit"
        email =  "laxman.kendre@ikf.co.in"
        phone =  8668282906        
        str_data = f"MIT|{order_id}|NA|{amount}|NA|NA|NA|INR|NA|TypeField1|mit|NA|NA|TypeField2|AdditionalInfo1|MBSR|{email}|{phone}|{name}|{city}|AdditionalInfo7|http://www.mitbio.edu.in/admission-2019-thank-you/"
        checksum = hashlib.sha256(str_data.encode()).hexdigest().upper()
        str1_data = f"{str_data}|{checksum}"
        
        return render(request, 'student/payment_form.html', {'msg': str1_data})
    else:
        return render(request, 'error.html', {'message': 'Error in data insert'})

@login_required(login_url='login')
def getMyPrint(request):    
    if request.method == "GET" and request.user.is_student == True and request.user.personal_frm == True and request.user.education_frm == True and request.user.payment_frm == True:
        if request.user.paymentstatus == "paid":
            _studId = request.user.id        
            if _studId: 
                _studData = Account.objects.filter(id=_studId)
                context = {
                    'studData': _studData
                }
            return render(request, 'student/student_detials.html',context)
    return redirect('login')
        