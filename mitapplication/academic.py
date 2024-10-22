from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Account
import random, datetime, uuid
from django.views.decorators.csrf import csrf_exempt
import re
## Upload Files ##
@csrf_exempt
def _uploadDocuments(request):
    if request.method == 'POST' and request.FILES.get("tenth_marksheet"):
        tenth_marksheet = request.FILES["tenth_marksheet"] #file_id
        file_id = request.POST["file_id"]
        _fileExtension = tenth_marksheet.name.split('.')[-1].lower()
        _fileSize = tenth_marksheet.size // 1024
        if _fileExtension != "pdf":
            return JsonResponse({'status': 'error', 'message': 'Please upload only PDF files', 'resp_id': file_id, 'cls':'text-danger'})
        elif not (100 <= _fileSize <= 500):
            return JsonResponse({'status': 'error', 'message': 'Please upload a PDF file between 100KB and 500KB in size','resp_id': file_id, 'cls':'text-danger'})        
        current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = uuid.uuid4().hex[:3]
        filename = f"{current_timestamp}_{unique_id}.{_fileExtension}"        
        file_path = f'media/student/document/{filename}'
        with open(file_path, 'wb') as destination:
            for chunk in tenth_marksheet.chunks():
                destination.write(chunk)        
        file_path_admin = f'student/document/{filename}'
        data = {}
        if file_id == "tenth_marksheet":
            data["tenth_marksheet"] = file_path_admin
        elif file_id == "twelth_marksheet":
            data["twelth_marksheet"] = file_path_admin
        elif file_id == "grd_marksheet":
            data["grd_marksheet"] = file_path_admin
        elif file_id == "lc":
            data["lc"] = file_path_admin
        elif file_id == "dob_cert":
            data["dob_cert"] = file_path_admin
        elif file_id == "cast_cert":
            data["cast_cert"] = file_path_admin
        elif file_id == "nonc_cert":
            data["nonc_cert"] = file_path_admin
        elif file_id == "caste_validity":
            data["caste_validity"] = file_path_admin
        elif file_id == "defence_cert":
            data["defence_cert"] = file_path_admin
        elif file_id == "migration":
            data["migration"] = file_path_admin
        elif file_id == "jammu_kashmir_cert":
            data["jammu_kashmir_cert"] = file_path_admin
        elif file_id == "jee_score_cert":
            data["jee_score_cert"] = file_path_admin
        elif file_id == "neet_score_cert":
            data["neet_score_cert"] = file_path_admin
        elif file_id == "mhcet_cert":
            data["mhcet_cert"] = file_path_admin
        elif file_id == "gap_cert":
            data["gap_cert"] = file_path_admin
        # return HttpResponse(file_path)
        res = Account.objects.filter(email=request.user.email).update(**data)
        if res:
            return JsonResponse({'status': 'success', 'message': 'File uploaded and model updated successfully', 'resp_id': file_id, 'cls':'text-success'})
        return JsonResponse({'status': 'error', 'message': 'File is not uploaded', 'resp_id': file_id, 'cls':'text-danger'})

    else:
        return JsonResponse({'status': 'error', 'message': 'No file uploaded', 'resp_id': file_id, 'cls':'text-danger'})

@csrf_exempt
def _academicDetails(request):
    if request.user.personal_frm == True:
        if request.method == "POST":
            ## doc ##
            # _tenthMarkSheet = request.FILES.get("tenth_marksheet")
            # if not _tenthMarkSheet:
            #     return HttpResponse("No file uploaded")
            # _fileExtension = _tenthMarkSheet.name.split('.')[-1].lower()
            # _fileSize = _tenthMarkSheet.size // 1024
            # if _fileExtension != "pdf":
            #     return HttpResponse("Please upload only PDF files")
            # elif not (100 <= _fileSize <= 500):
            #     return HttpResponse("Please upload a PDF file between 100KB and 500KB in size")        
            # current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # unique_id = uuid.uuid4().hex[:3]
            # filename = f"{current_timestamp}_{unique_id}.{_fileExtension}"        
            # file_path = f'student/document/{filename}'
            # with open(f'media/{file_path}', 'wb') as destination:
            #     for chunk in _tenthMarkSheet.chunks():
            #         destination.write(chunk)        
            # data = {"tenth_marksheet": file_path}
            # res = Account.objects.filter(email=request.user.email).update(**data)
            # return HttpResponse("File uploaded and model updated successfully")
            
                
                
            ## 10th ##        
            context = {}
            tenth_result_status = request.POST.get('tenth_result_status')        
            if not tenth_result_status:
                context['id'] = "tenth_rs_sErr"
                context['msg'] = "Please select an option."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)
            tenth_school = request.POST.get('tenth_school')        
            if not tenth_school:
                context['id'] = "tenth_schoolErr"
                context['msg'] = "Please enter an input."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)

            tenth_board = request.POST.get('tenth_board')
            if not tenth_board:
                context['id'] = "tenth_boardErr"
                context['msg'] = "Please enter an input."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)

            tenth_seat = request.POST.get('tenth_seat')
            _yearPatter =  r'^[0-9]{4}$'
            tenth_year = request.POST.get('tenth_year')
            if not tenth_year or not re.match(_yearPatter, tenth_year.strip()) or tenth_year == "0000" or tenth_year == "000":
                context['id'] = "tenth_pass_yErr"
                context['msg'] = "Please enter an input."
                context['status'] = 404
                context['cls'] = "text-danger" 
                return JsonResponse(context)

            tenth_result_pattern = request.POST.get('tenth_result_pattern')
            if not tenth_result_pattern:
                context['id'] = "tenth_res_pErr"
                context['msg'] = "Please select an option."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)
            
            _perPatter =  r'^[0-9]{1,3}$'  
            _cgpaPattern = r'^(?:[5-9](?:\.\d+)?|10(?:\.0)?)$'#r'^[5-9][\.]*[\d]?|[A-D][+-]?$' #r'^[5-9](?:\.\d+)?[A-D]?[+-]?$'#r'^[5-9](?:\.\d+)?[A-D]*[+-]?$'
            tenth_percent = request.POST.get('tenth_percent')
            if tenth_result_pattern == "cgpa":
                if not tenth_percent:
                    context['id'] = "tenth_perErr"
                    context['msg'] = "Please enter an input.dd"
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)
                elif not re.match(_cgpaPattern,tenth_percent):
                    context['id'] = "tenth_perErr"
                    context['msg'] = "Please enter valid an input."
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)

            else:
                if not tenth_percent:
                    context['id'] = "tenth_perErr"
                    context['msg'] = "Please enter an input.dd"
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)
                elif not re.match(_perPatter,tenth_percent) or int(tenth_percent) > 100 or int(tenth_percent) < 1:
                    context['id'] = "tenth_perErr"
                    context['msg'] = "Please enter valid an input.sd"
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)

            # return HttpResponse(200)
            tenth_math = request.POST.get('tenth_math')
            # if not tenth_math:
            #     context['id'] = "tenth_perErr"
            #     context['msg'] = "Please select an option."
            #     context['status'] = 404
            #     context['cls'] = "text-danger"
            #     return JsonResponse(context)
            tenth_sci = request.POST.get('tenth_sci')
            tenth_en = request.POST.get('tenth_en')

            ## 12th ## twelth_res_p
            twelth_result_status = request.POST.get('twelth_result_status')
            if not twelth_result_status:
                context['id'] = "twelth_res_sErr"
                context['msg'] = "Please select an option."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)
            
            twelth_college = request.POST.get('twelth_college')
            if not twelth_college:
                context['id'] = "twelth_collegeErr"
                context['msg'] = "Please select an option."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)
            twelth_board = request.POST.get('twelth_board')
            if not twelth_board:
                context['id'] = "twelth_boardErr"
                context['msg'] = "Please select an option."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)

            twelth_seat = request.POST.get('twelth_seat')                
            twelth_year = request.POST.get('twelth_year')
            if not twelth_year or not re.match(_yearPatter, twelth_year.strip()) or twelth_year == "0000" or twelth_year == "000":
                context['id'] = "twelth_pas_yErr"
                context['msg'] = "Please select an option."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)
            twelth_result_pattern = request.POST.get('twelth_result_pattern')
            if not twelth_result_pattern:
                context['id'] = "twelth_res_pErr"
                context['msg'] = "Please select an option."
                context['status'] = 404
                context['cls'] = "text-danger"
                return JsonResponse(context)
            twelth_percent = request.POST.get('twelth_percent')
            if tenth_result_pattern == "cgpa":
                if not twelth_percent:
                    context['id'] = "twelth_perErr"
                    context['msg'] = "Please enter valid inputs.df"
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)
                elif not re.match(_cgpaPattern,twelth_percent):
                    context['id'] = "twelth_perErr"
                    context['msg'] = "Please enter valid inputs.0"
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)
            else:
                if not twelth_percent:
                    context['id'] = "twelth_perErr"
                    context['msg'] = "Please enter valid inputs.df"
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)
                elif not re.match(_perPatter,twelth_percent) or int(twelth_percent) > 100 or int(twelth_percent) < 1:
                    context['id'] = "twelth_perErr"
                    context['msg'] = "Please enter valid inputs.0"
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)        
        
            twelth_bio = request.POST.get('twelth_bio')
            twelth_math = request.POST.get('twelth_math')
            twelth_sci = request.POST.get('twelth_sci')
            twelth_en = request.POST.get('twelth_en')

            ## Graduate ##
            graduate_degree = request.POST.get('graduate_degree')
            graduate_result_status = request.POST.get('graduate_result_status')
            graduate_college = request.POST.get('graduate_college')
            graduate_university = request.POST.get('graduate_university')
            graduate_seat = request.POST.get('graduate_seat')        
            graduate_year = request.POST.get('graduate_year')
            graduate_result_pattern = request.POST.get('graduate_result_pattern')
            graduate_percent = request.POST.get('graduate_percent')
            if graduate_result_pattern == "cgpa":
                if not re.match(_cgpaPattern,graduate_percent):
                    context['id'] = "grd_perErr"
                    context['msg'] = "Please enter valid inputs.0"
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)
            else:
                if not re.match(_perPatter,twelth_percent) or int(twelth_percent) > 100 or int(twelth_percent) < 1:
                    context['id'] = "grd_perErr"
                    context['msg'] = "Please enter valid inputs.0"
                    context['status'] = 404
                    context['cls'] = "text-danger"
                    return JsonResponse(context)
            

            # entrance
            phy_f = request.POST.get('_phy_f')
            chm_f = request.POST.get('_chm_f')
            bio_f = request.POST.get('_bio_f')
            math_f = request.POST.get('_math_f')
            perc_f = request.POST.get('_perc_f')
            phy_s = request.POST.get('_phy_s')
            chm_s = request.POST.get('_chm_s')
            bio_s = request.POST.get('_bio_s')
            math_s = request.POST.get('_math_s')
            perc_s = request.POST.get('_perc_s')
            gate = request.POST.get('gate')
            gatb = request.POST.get('gatb')

            # entrance
            gate_percentile = request.POST.get('gate_percentile').title()        
            gatb_percentile = request.POST.get('gatb_percentile').title()
            neet = request.POST.get('neet').title()
            iit_jee1 = request.POST.get('iit_jee1').title()
            mhcet = request.POST.get('mhcet').title()
            peracet = request.POST.get('peracet').title()
            none_ = request.POST.get('none_').title()
            # neet = True if request.POST.get('neet') is not None and request.POST.get('neet') == "on" else False
            # iit_jee1 = True if request.POST.get('iit_jee1') is not None and request.POST.get('iit_jee1') == "on" else False
            # mhcet = True if request.POST.get('mhcet') is not None and request.POST.get('mhcet') == "on" else False
            # peracet = True if request.POST.get('peracet') is not None and request.POST.get('peracet') == "on" else False
            # none_ = True if request.POST.get('none_') is not None and request.POST.get('none_') == "on" else False
            
            

            # return HttpResponse( neet )
            context = {
                "tenth_result_status" : tenth_result_status,
                "tenth_school" : tenth_school,
                "tenth_board" : tenth_board,
                "tenth_seat" : tenth_seat,
                "tenth_year" : tenth_year,
                "tenth_result_pattern" : tenth_result_pattern,
                "tenth_percent" : tenth_percent,
                "tenth_math" : tenth_math,
                "tenth_sci" : tenth_sci,
                "tenth_en" : tenth_en,
                "twelth_result_status" : twelth_result_status,
                "twelth_college" : twelth_college,
                "twelth_board" : twelth_board,
                "twelth_seat" : twelth_seat,
                "twelth_year" : twelth_year,
                "twelth_result_pattern" : twelth_result_pattern,
                "twelth_percent" : twelth_percent,
                "twelth_bio": twelth_bio,
                "twelth_math" : twelth_math,
                "twelth_sci" : twelth_sci,
                "twelth_en" : twelth_en,
                "graduate_degree" : graduate_degree,
                "graduate_result_status" : graduate_result_status,
                "graduate_college" : graduate_college,
                "graduate_university" : graduate_university,
                "graduate_seat" : graduate_seat,
                "graduate_year" : graduate_year,
                "graduate_result_pattern" : graduate_result_pattern,
                "graduate_percent" : graduate_percent,

                #entrance
                "phy_f" : phy_f if phy_f is not None else "",
                "chm_f" : chm_f if chm_f is not None else "",
                "bio_f" : bio_f if bio_f is not None else "",
                "math_f" : math_f if math_f is not None else "",
                "perc_f" : perc_f if perc_f is not None else "",
                "phy_s" : phy_s if phy_s is not None else "",
                "chm_s" : chm_s if chm_s is not None else "",
                "bio_s" : bio_s if bio_s is not None else "",
                "math_s" : math_s if math_s is not None else "",
                "perc_s" : perc_s if perc_s is not None else "",
                "gate" : gate if gate is not None else "",
                "gatb" : gatb if gatb is not None else "",
                "gate_cet": gate_percentile,
                "gateb_cet": gatb_percentile,
                "neet": neet,
                "jee": iit_jee1,
                "mhcet": mhcet,
                "peracet": peracet,
                "other": none_,
                ## education form status ##
                "education_frm" : True,

            }   
            context['neet'] = neet
            # context['iit_jee1'] = iit_jee1
            context['mhcet'] = mhcet
            context['peracet'] = peracet
            # context['none_'] = none_
            print( context )
            # return HttpResponse(context)
            resp = Account.objects.filter(email=request.user.email).update(**context)
            if resp:
                resp = {
                    'status': 200,
                    'msg' : 'Your data has been saved successfully!!',
                    'cls': 'text-success',
                    "id": ''
                }            
            else:
                resp = {
                    'status': 404,
                    'msg' : 'Your data is not saved, please try after sometime!!',
                    'cls': 'text-danger',
                    "id": '',
                }
            return JsonResponse(resp)        
        _degree = Account.DEGREE_CHOICE    
        context = {
            'degree': _degree,
        }
        return render(request, 'student/academic.html',context)
    else:        
        return redirect('dashboard')