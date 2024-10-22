from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail,BadHeaderError,send_mass_mail
from smtplib import SMTPAuthenticationError
from .models import Contact, OurSolution,Feature, Application, Client,ClientCat,OurSolutionOverview,PageMeta,Page, Project, SolutionBrand, DownloadPPT
from email.utils import formataddr

def custom_404(request, exception=None):    
    return render(request, 'common/404.html', status=404)

def getSolution(request):
    page_id = get_object_or_404(Page, id=3)
    pageMetaData = PageMeta.objects.filter(page_name=page_id)
    ourSolutionData = OurSolution.objects.filter(status = True)
    # return HttpResponse(pageMetaData)
    context = {
        'pageMetaData':pageMetaData,
        'ourSolutionData':ourSolutionData,
    }
    return render(request, 'our_solution/our_solution.html',context)

def getSolutionDetails(request, slug=None):    
    sltn_page_id = get_object_or_404(OurSolution, slugs=slug)        
    pageMetaData = PageMeta.objects.filter(solution_title=sltn_page_id)
    latestProject = Project.objects.filter(solution_name=sltn_page_id).order_by('sort')[:6]     
    client_data = Client.objects.all().order_by('-id') 
    client_cat_data = ClientCat.objects.all().order_by('-id')
    other_solutions = OurSolution.objects.all().exclude( slugs = slug )
    ourSolutionDatas = OurSolution.objects.filter(slugs = slug )    
    ourSolutionData = OurSolution.objects.filter(status=True)    
    our_solution = get_object_or_404(OurSolution, slugs=slug)
    # Retrieve all SolutionBrand instances associated with the specific OurSolution
    solution_brands = sltn_page_id.solutions.order_by('sort').filter(status = True)
    pptData = DownloadPPT.objects.filter(solution_title=sltn_page_id)
    # for items in pptData:
    #     print(items.ppt_file)
    # return HttpResponse( pptData )
    context = {}
    if slug:
        our_solution = get_object_or_404(OurSolution, slugs=slug)        
        overView_data = OurSolutionOverview.objects.filter(solution_title=our_solution)
        features_data = Feature.objects.filter(solution_title=our_solution)
        application_data = Application.objects.filter(solution_title=our_solution)        
        context['overView_data'] = overView_data
        context['features_data'] = features_data
        context['application_data'] = application_data
        # return HttpResponse( context['features_data'] )
    context['latest_project'] = latestProject
    context['ourSolutionData'] = ourSolutionData
    context['ourSolutionDatas'] = ourSolutionDatas         
    context['other_solutions'] = other_solutions
    context['client_data'] = client_data
    context['client_cat_data'] = client_cat_data
    context['pageMetaData'] = pageMetaData
    context['solution_brands'] = solution_brands
    context['pptData'] = pptData
    return render(request,'our_solution/solution_detail.html',context)


@csrf_exempt
def contactAction(request):    
    if request.method == 'POST':                   
        name  = request.POST.get('your_name')
        email  = request.POST.get('your_email')
        mobile  = request.POST.get('contact_num')
        product  = request.POST.get('product')
        message  = request.POST.get('your_message')
        if len( name ) > 1 and len( email ) > 1 and len( mobile ) > 1 and len( product ) > 1:
            idata = {
                'name': name,
                'email': email,
                'contact': mobile,
                'product' : product,
                'message': message,
            }
            res = Contact.objects.create(**idata)
            if res:

                # subject line
                subject = 'Enquiry Form Submission For - Safehouse'

                # admin reply
                
                admin_msg = ""
                admin_msg += "Dear Team, \n\n"
                admin_msg += "We have received below details from Safehouse website Enquiry Form submitted today.\n\n"
                admin_msg += "Name : "+ name
                admin_msg += "\nEmail : "+email
                admin_msg += "\nContact : "+mobile
                admin_msg += "\nProduct : "+product
                admin_msg += "\nMessage : "+message                
                admin_msg += "\n\n\nThanks & Regards,\n"
                admin_msg += name.title()
                admin_email = [ 'laxman.kendre@ikf.co.in', 'lkendre2525@gmail.com' ]
                try:
                    #send_mail(subject, admin_msg,email,admin_email, fail_silently=False)
                    my_message = (subject, admin_msg,email,admin_email)
                    send_mass_mail((my_message,),fail_silently=False)
                except BadHeaderError:
                    pass
                except SMTPAuthenticationError  as e:
                    pass
                

                #user reply
                user_msg = ""
                user_msg += "Dear "+name.title()+"\n\n"
                user_msg += "Thank you so much for filling up the enquiry form. We will get back to you as soon as we can.\n\n\n"
                user_msg += "Thanks & Regards,\n"
                user_msg += "Safehouse\n"                
                # from_email = 'Safehouse<laxman.kendre@ikf.co.in>'
                recipient_list = [ email]  
                from_email = formataddr(('Safehouse', 'laxman.kendre@ikf.co.in'))
                # resp = send_mail(subject, user_msg, from_email, recipient_list)
                try:
                    resp = send_mail(subject, user_msg, from_email, recipient_list)
                except BadHeaderError:
                    pass
                except SMTPAuthenticationError  as e:
                    respData = {'status': 404, 'msg': "There was an error while trying to send your enquiry. To send us an email at test@test.com",'cls':'text-warning'}
                    return JsonResponse( respData )
                if resp:                
                    respData = {'status': 200, 'msg': "Thank you for filling out the details. We\'ll reach out to you real soon!",'cls':'text-success'}
                    return JsonResponse( respData )
                    # return HttpResponse('sent')
                    return JsonResponse({'status': 200, 'msg': "Thank you for filling out the details. We\'ll reach out to you real soon!", 'cls':'success'})
                else:
                    respData = {'status': 404, 'msg': "There was an error while trying to send your enquiry. To send us an email at test@test.com",'cls':'text-warning'}
                    return JsonResponse( respData )
                    # return HttpResponse('not sent')
                    return JsonResponse({'status': 404, 'msg': "Have you entered all the information correctly? Please check and try again.", 'cls':'text-warning'})
            else:
                return HttpResponse('not saved')            
        return redirect('contact-us/')