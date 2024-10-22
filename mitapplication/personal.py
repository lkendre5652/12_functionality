from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account
from django.http import JsonResponse
import re, random, datetime, uuid


@login_required(login_url="login")
@csrf_exempt
def _profileSignUpload(request):
    if request.method == "POST":        
        profile_photo = request.FILES["profile_photo"]
        _file_extension = profile_photo.name.split(".")[-1]
        _fileSize = profile_photo.size // 1024        
        file_id = request.POST.get('profile_photo_id')                
        if _file_extension not in  ["jpg", "jpeg", 'png', 'webp']:
            return JsonResponse({'status': 'error', 'message': 'Please upload only JPG, JPEG,PNG,WEBP files', 'resp_id': file_id, 'cls':'text-danger'})
        elif not (25 <= _fileSize <= 200):
            return JsonResponse({'status': 'error', 'message': 'Please upload a JPG, JPEG,PNG,WEBP file between 50KB and 200KB in size','resp_id': file_id, 'cls':'text-danger'})        
        current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = uuid.uuid4().hex[:3]
        filename = f"{current_timestamp}_{unique_id}.{_file_extension}"        
        file_path = f'media/student/profile/{filename}'
        with open(file_path, 'wb') as destination:
            for chunk in profile_photo.chunks():
                destination.write(chunk) 
        file_path_admin = f'student/profile/{filename}'        
        data = {
           file_id : file_path_admin
        } 
        print(data)
        res = Account.objects.filter(email=request.user.email).update(**data)      
        print( res)
        if res:
            img_url = "none"
            if request.user.profile_photo:
                img_url = request.user.profile_photo.url            
            return JsonResponse({'status': 'success', 'message': 'File uploaded and model updated successfully', 'resp_id': file_id, 'cls':'text-success', 'img_url': "/"+file_path})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please upload only JPG, JPEG,PNG,WEBP files', 'resp_id': file_id, 'cls':'text-danger'})
        
    else:
        return HttpResponse(300) 

@login_required(login_url='login')
@csrf_exempt
def _personalAction(request):
    if request.method == "POST":
        context = {}        
        _gender = request.POST.get('_gender')        
        if not _gender or _gender.lower() not in ["male", "female", "other"]:
            context['id'] = "genderErr"
            context['msg'] = "Please select an option."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)    
        _emailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'            
        _parntemail = request.POST.get('_parntemail')        
        if not _parntemail or not re.match(_emailPattern, _parntemail):
            context['id'] = "parntemailErr"
            context['msg'] = "Please enter a valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)       

        _nationality = request.POST.get('_nationality')        
        if not _nationality or _nationality not in dict(Account.NATIONALITY_CHOICES).keys():
            context['id'] = "nationalityErr"
            context['msg'] = "Please select a valid option."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)        
        
        _category = request.POST.get('_category')
        if not _category or _category not in dict(Account.CATEGORY_CHOICE).keys():
            context['id'] = "categoryErr"
            context['msg'] = "Please select a valid option."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)
        
        _cast = request.POST.get('_cast')
        if not _cast:
            context['id'] = "casteErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)
        
        _blood_group = request.POST.get('_blood_group')
        if not _blood_group or _blood_group not in dict(Account.BLOOD_GROUP_CHOICES).keys():
            context['id'] = "blood_groupErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)

        _course_details = request.POST.get('_course_details')
        ## error pending ##
        # if not _course_details or _course_details not in Account.COURCE_CHOICES:
        #     context['id'] = "blood_groupErr"
        #     context['msg'] = "Please enter valid input."
        #     context['status'] = 404
        #     context['cls'] = "text-danger"
        #     return JsonResponse(context)

        _permanent_address = request.POST.get('_permanent_address')
        if not _permanent_address:
            context['id'] = "permanent_addressErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)


        _city = request.POST.get('_city')
        if not _city:
            context['id'] = "cityErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)

        _state = request.POST.get('_state')
        if not _state:
            context['id'] = "stateErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)

        _country = request.POST.get('_country')
        # return HttpResponse( _country )
        if not _country or _country not in dict(Account.PASSPORT_COUNTRY_CHOICE).keys():
            context['id'] = "countryErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)

        _pincode = request.POST.get('_pincode')
        _pinPattern = r'^[0-9]{6}$'
        if not _pincode or not re.match(_pinPattern,_pincode):
            context['id'] = "pincodeErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)        

        _is_preset_address = True if request.POST.get('_is_preset_address') == "on" else False
        _present_address1 = request.POST.get('_present_address1')
        if _is_preset_address == True and ( not _present_address1):
            context['id'] = "present_address1Err"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context) 

        _present_address2 = request.POST.get('_present_address2')
        if _is_preset_address == True and (not _present_address2):
            context['id'] = "present_address2Err"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)

        _present_city = request.POST.get('_present_city')
        if _is_preset_address == True and not _present_city:
            context['id'] = "present_cityErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)


        _present_state = request.POST.get('_present_state')
        if _is_preset_address == True and not _present_state:
            context['id'] = "present_stateErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)
        _present_country = request.POST.get('_present_country')
        
        if _is_preset_address == True and _present_country not in dict(Account.PASSPORT_COUNTRY_CHOICE).keys():
            context['id'] = "present_countryErr"
            context['msg'] = "Please enter valid input."
            context['status'] = 404
            context['cls'] = "text-danger"
            return JsonResponse(context)
        
        _present_pincode = request.POST.get('_present_pincode')

        if _is_preset_address == True:
            if not _present_pincode or not re.match(_pinPattern,_present_pincode):
                context['id'] = "pincodeErr"
                context['msg'] = "Please enter valid input."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)

        
        if _is_preset_address == True:
            if not _present_pincode or not re.match(_pinPattern,_present_pincode):
                context['id'] = "present_pincodeErr"
                context['msg'] = "Please enter valid input."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)        
        _father_name = request.POST.get('_father_name')
        _mother_name = request.POST.get('_mother_name')
        _parent_mobile = request.POST.get('_parent_mobile')
        _noncreamy = True if request.POST.get('_noncreamy') == "yes" else False
        _minority = True if request.POST.get('_minority') == "yes" else False
        _exserviceman = True if request.POST.get('_exserviceman') == "yes" else False
        _physically = True if request.POST.get('_physically') == "yes" else False
        _kashmiri = True if request.POST.get('_kashmiri') == "yes" else False
        _residence = True if request.POST.get('_residence') == "yes" else False
        _oms = True if request.POST.get('_oms') == "yes" else False
        _nri = True if request.POST.get('_nri') == "yes" else False
        _abc_id = request.POST.get('_abc_id')

        context = {
            "gender" : _gender,
            "parent_email" : _parntemail,
            "nationality" : _nationality,
            "category" : _category,
            "cast" : _cast,
            "blood_group" : _blood_group,
            "cource" : _course_details,
            "permanent_address" : _permanent_address,
            "city" : _city,
            "state" : _state,
            "country" : _country,
            "pin_code" : _pincode,
            "is_preset_address" : _is_preset_address,
            "present_address1" : _present_address1,
            "present_address2" : _present_address2,
            "present_city" : _present_city,
            "present_state" : _present_state,
            "present_country" : _present_country,
            "present_pincode" : _present_pincode,
            "father_name" : _father_name,
            "mother_name" : _mother_name,
            "parent_contact" : _parent_mobile,
            "non_creamy_layer" : _noncreamy,
            "minority" : _minority,
            "ex_serviceman" : _exserviceman,
            "physically" : _physically,
            "kashmiri" : _kashmiri,
            "area_of_residence" : _residence,
            "oms" : _oms,
            "nri_pio_oci" : _nri,
            "abc_id" : _abc_id,
            "is_admin": False,
            "is_staff": False,            
            "is_superuser": False,
            ## education form status ##
            "personal_frm" : True,
        }        
        resp = Account.objects.filter(email=request.user.email).update(**context)
        if resp:
            resp = {
                'status': 200,
                'msg' : 'Your data has been saved successfully!!',
                'cls': 'text-success',
                "id": 'comm_msg'
            }            
        else:
            resp = {
                'status': 404,
                'msg' : 'Your data is not saved, please try after sometime!!',
                'cls': 'text-danger',
                "id": 'comm_msg',
            }
        return JsonResponse(resp)        