<?php
namespace App\Http\Controllers\Front;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\StudyDestination;
use App\Models\DestinationStateDetail;
use App\Models\AboutUs;
use App\Models\Location;
use App\Models\Service;
use App\Models\Testimonial;
use App\Models\Blog;
use App\Models\BlogCategory;
use App\Models\NewsEvent;
use App\Models\NewsEventImage;
use App\Models\Banner;
use App\Models\MyPage;
use App\Models\Counselling;
use App\Models\EducationCost;
use App\Models\InnerPageSeo;
use App\Models\WebsiteMeta;	
use Illuminate\Support\Facades\Validator;



class FrontEndController extends Controller
{
	 protected $sortOrder;

    public function __construct()
    {
        $this->sortOrder = env('SORT_ORDER', 'asc');
    }	
		
    /*lists single news events data */
    public function GetSingleNewsEvent(Request $request, $single_newsevent=none){
        // return $blog_slug;
        $singleNewsEvent = NewsEvent::where('is_active', true)
        ->where('slugs','=',$single_newsevent)
        ->orderBy('sort', 'asc')
        ->first();
        $relatedNewsEvent = NewsEvent::where('is_active', true)
        ->Where('slugs','!=',$single_newsevent)
        ->orderBy('sort', 'asc')
        ->get(); 
        $sliderNewsEvent = NewsEventImage::where('is_active', true)
        ->Where('newsevent_id','=',$singleNewsEvent->id)
        ->orderBy('sort', 'asc')
        ->get();
		  $parms = $singleNewsEvent->id;
        $innerPgSeo = InnerPageSeo::where(function($query) use ($parms) {
            $query->where('is_active', true)
            ->where('newsevent_id', $parms);
        })
        ->orderBy('sort', 'asc')
        ->first(); 
        $data = [];    
		$data['innerPgSeo']= $innerPgSeo;
        if($sliderNewsEvent){
            $data['sliderNewsEvent'] = $sliderNewsEvent;
        }              
        if($singleNewsEvent){
            $data['singleNewsEvent'] = $singleNewsEvent;
        }
        if($relatedNewsEvent){
            $data['relatedNewsEvent'] = $relatedNewsEvent;
        }
        return view('front.pages.single_newsevent')->with('data',$data);
    }
    
	/*lists news events data */
    public function GetAllNewsEvent(Request $request){
        $allNewsEvent = NewsEvent::where('is_active', true)        
        ->orderBy('sort', 'asc')
        ->get();
        $data = [];        
		 $Allbanner = Banner::where('is_active', true)
        ->where('page_id','=',6)
        ->orderBy('sort', 'asc')
        ->first();
        $PageData = MyPage::where('is_active', true)
        ->where('id','=',6)
        ->orderBy('sort', 'asc')
        ->first();        
        if($PageData){
            $data['PageData'] = $PageData;
        }
        if($Allbanner){
            $data['Allbanner'] = $Allbanner;
        }
        if($allNewsEvent){
            $data['allNewsEvent'] = $allNewsEvent;
        }        
        return view('front.pages.news_events')->with('data',$data);
    }
    
	/*lists single blogs data */
    public function GetSingleBlog(Request $request, $blog_slug=none){
        // return $blog_slug;
        $singleBlog = Blog::where('is_active', true)
        ->where('slugs', '=',$blog_slug)
        ->orderBy('sort', 'asc')
        ->first();
        $data = [];
		$parms = $singleBlog->id;
        $innerPgSeo = InnerPageSeo::where(function($query) use ($parms) {
            $query->where('is_active', true)
            ->where('blog_id', $parms);
        })
        ->orderBy('sort', 'asc')
        ->first();
        $data['innerPgSeo']= $innerPgSeo;
        if($singleBlog->blog_category_id){
            $relatedBlog = Blog::where('is_active', true)
            ->where("blog_category_id","=",$singleBlog->blog_category_id)
            ->where("slugs","!=",$blog_slug)
            ->orderBy('sort', 'asc')
            ->get();
            $data['relatedBlog'] = $relatedBlog;
        }        
        // return $singleBlog->blog_banner;
        if($singleBlog){
            $data['singleBlog'] = $singleBlog;
        }        
        return view('front.pages.single_blog')->with('data',$data);
    }
    
	/*Get All blogs Data */
	public function GetAllBlog(Request $request){
        $allBlogCategory = BlogCategory::where('is_active', true)
        ->orderBy('sort', 'asc')
        ->get();

        $allBlog = Blog::where('is_active', true)
        ->orderBy('sort', 'desc')
        ->get();
        $data = [];
        if($allBlog){
            $data['allBlog'] = $allBlog;
        }
        if($allBlogCategory){
            $data['allBlogCategory'] = $allBlogCategory;
        }        
        $Allbanner = Banner::where('is_active', true)
        ->where('page_id','=',6)
        ->orderBy('sort', 'asc')
        ->first();
        $PageData = MyPage::where('is_active', true)
        ->where('id','=',6)
        ->orderBy('sort', 'asc')
        ->first();        
        if($PageData){
            $data['PageData'] = $PageData;
        }
        if($Allbanner){
            $data['Allbanner'] = $Allbanner;
        }

        return view('front.pages.blog')->with('data',$data);
    }  
	
	/* Home Page data managing */
    public function getHome(Request $request){
        $data = [];
        $Allbanner = Banner::where('is_active', true)
        ->where('page_id','=',2)
        ->orderBy('sort', 'asc')
        ->get();

        $allAboutStat = AboutUs::where('is_active', true)
        ->where('is_stats','=',true)
        ->orderBy('created_at', 'desc')
        ->get();

        $allNewsEvent = NewsEvent::where('is_active', true)        
        ->orderBy('sort', 'asc')
        ->get();

        $allDestination = StudyDestination::where('status', 'active')
            ->orderBy('sort', 'asc')
            ->select('name','slug','home_pg_image','home_pg_logo')
            ->get(); 
        $allServices = Service::where('status', 'active')
            ->where('is_home', true)
            ->orderBy('created_at', 'desc')
            ->select('id','service_name','overview','square_img','is_home', 'icon_img')
            ->get(); 
        $allTestimonials = Testimonial::where('status', 'active')        
        ->where('is_home', true)
        ->orderBy('sort', 'asc')
        ->get();
        $allAboutData = AboutUs::where('is_active', true)
            ->where(function ($query) {
                $query->where('is_our_accreditation', true)
                    ->orWhere('is_leadership_team', true);
            })
            ->where('is_home', true)
            ->orderBy('sort', 'asc')
            ->get();
        $allBlog = Blog::where('is_active', true)
            ->orderBy('sort', 'asc')
            ->get();        
        $allTopUniversity = DestinationStateDetail::where('status', 'active')
            ->where('is_popular_university', true)
            ->where('is_home', true)
            ->orderBy('sort', 'asc')
            ->select('icon_img','is_home', 'icon_img')
            ->get();
        //$allNewsEvent,$Allbanner
        if($Allbanner){
            $data['Allbanner'] = $Allbanner;
        }

        if($allAboutStat){
            $data['allAboutStat'] = $allAboutStat;
        }
        if($allNewsEvent){
            $data['allNewsEvent'] = $allNewsEvent;
        }
        if($allDestination){
            $data['allDestination'] = $allDestination;
        }
        if($allServices){
            $data['allServices'] = $allServices;
        }
        if($allTestimonials){
            $data['allTestimonials'] = $allTestimonials;
        } 
        if($allAboutData){
            $data['allAboutData'] = $allAboutData;
        } 
        if($allTopUniversity){
            $data['allTopUniversity'] = $allTopUniversity;
        } 
        if($allBlog){
            $data['allBlog'] = $allBlog;
        }
        return view('front.pages.home')->with('data',$data);

    }
	
	/*Career Counselling managing*/
    public function GetAllCarrerCounselling(Request $request){        
        $allAccreditation = AboutUs::where('is_active', true)        
        ->where('is_leadership_team',true)
        ->where('is_counsller',true)
        ->orderBy('sort', 'asc')
        ->get();
		$allCounsellingData = Counselling::where('is_active', true)
        ->orderBy('sort', 'asc')
        ->first();
		$websiteMeta = WebsiteMeta::where('is_active', true)
            ->where('is_contact_page', '=',true)
            ->orderBy('sort', 'asc')            
            ->first();
        $data = [];
		$data['websiteMeta'] = $websiteMeta;
		$Allbanner = Banner::where('is_active', true)
        ->where('page_id','=',9)
        ->orderBy('sort', 'asc')
        ->first();
        $PageData = MyPage::where('is_active', true)
        ->where('id','=',9)
        ->orderBy('sort', 'asc')
        ->first();        
        if($PageData){
            $data['PageData'] = $PageData;
        }else{
            $data['PageData'] = '';
        }
        if($Allbanner){
            $data['Allbanner'] = $Allbanner;
        }else{
            $data['Allbanner'] = '';
        }  
        // banner
        if($allAccreditation){
            $data['allAccreditation'] = $allAccreditation;
        }
		$data['allCounsellingData'] = $allCounsellingData;
        return view('front.pages.career_counselling')->with('data',$data);
    }
	
	/*contact page managing*/
    public function GetAllContact(Request $request){
        $allLocation = Location::where('is_active', true)
        ->orderBy('sort', 'asc')
        ->get();
        $data = [];
		$Allbanner = Banner::where('is_active', true)
        ->where('page_id','=',4)
        ->orderBy('sort', 'asc')
        ->first();
        $PageData = MyPage::where('is_active', true)
        ->where('id','=',4)
        ->orderBy('sort', 'asc')
        ->first();        
        if($PageData){
            $data['PageData'] = $PageData;
        }else{
            $data['PageData'] = '';
        }
        if($Allbanner){
            $data['Allbanner'] = $Allbanner;
        }else{
            $data['Allbanner'] = '';
        }
        if($allLocation){
            $data['allLocation'] = $allLocation;
        }
        return view('front.pages.contact')->with('data',$data);
    }
	
	/*About Page Managing*/
    public function GetAllAboutUsData(Request $request){
		$data = [];  
        $Allbanner = Banner::where('is_active', true)
        ->where('page_id','=',15)
        ->orderBy('sort', 'asc')
        ->first();
        $PageData = MyPage::where('is_active', true)
        ->where('id','=',15)
        ->orderBy('sort', 'asc')
        ->first();        
        if($PageData){
            $data['PageData'] = $PageData;
        }else{
            $data['PageData'] = '';
        }
        if($Allbanner){
            $data['Allbanner'] = $Allbanner;
        }else{
            $data['Allbanner'] = '';
        }  
        // banner
        $allAboutData = AboutUs::where('is_active', true)
        ->orderBy('sort', 'asc')
        ->get();     
        //$data = [];
        if($allAboutData){
            $data['allAboutData'] = $allAboutData;
        }   
        return view('front.pages.about_us')->with('data',$data);
    }
	
	/*State single page managing*/
    public function getSigleState(Request $request, $state_slug=null){
        if($state_slug !== null ){
            $singleDestination = StudyDestination::where('status', 'active')
            ->where('slug', $state_slug)
            ->orderBy('sort', 'asc')
            ->first();
            $otherDestinations = StudyDestination::where('status', 'active')
            ->where('slug', '!=', $state_slug)
            ->orderBy('sort', 'asc')
            ->select('name','slug','home_pg_image','home_pg_logo','listing_pg_image_2')
            ->get();
			
			$allEducationCost = EducationCost::where('is_active', true)
            ->where('destination_id', '=', $singleDestination->id)
            ->orderBy('created_at', 'desc')
            ->get(); 
			$parms = $singleDestination->id;
            $innerPgSeo = InnerPageSeo::where(function($query) use ($parms) {
                $query->where('is_active', true)
                ->where('destination_id', $parms);
            })
            ->orderBy('sort', 'asc')
            ->first();  
            $data = array(                
                'singleDestination' => $singleDestination,
				'allEducationCost' => $allEducationCost,
				  'innerPgSeo' => $innerPgSeo,
            ); 
            if($otherDestinations){
                $data['otherDestinations'] = $otherDestinations;
            }
            if($singleDestination->id){
                $metaDatas = DestinationStateDetail::where('status', 'active')
                ->where('destination_id', $singleDestination->id)
                ->orderBy('created_at', 'desc')
                ->get();
                $data['metadatas'] = $metaDatas; 
            }            
            return view('front.pages.single_destination')->with('data', $data);;
        }
    }
	
	/*Stady Destination listing */
    public function getStudyDestination(Request $request){
        if($request->method() == "GET"){            
            $allDestination = StudyDestination::where('status', 'active')
            ->orderBy('created_at', env('SORT_ORDER', 'desc'))
            ->get();                              
            $data = array(                
                'allDestination' => $allDestination
            ); 
			$Allbanner = Banner::where('is_active', true)
            ->where('page_id','=',14)
            ->orderBy('sort', 'asc')
            ->first();
            $PageData = MyPage::where('is_active', true)
            ->where('id','=',14)
            ->orderBy('sort', 'asc')
            ->first();        
            if($PageData){
                $data['PageData'] = $PageData;
            }
            if($Allbanner){
                $data['Allbanner'] = $Allbanner;
            }
            return view('front.pages.study_destination')->with('data', $data);
        }
    }
	
	/*Privacy Page management*/
    public function getPrivacy(Request $request){
        $data = [];        
        $Allbanner = Banner::where('is_active', true)
        ->where('page_id','=',12)
        ->orderBy('sort', 'asc')
        ->first();
        $PageData = MyPage::where('is_active', true)
        ->where('id','=',12)
        ->orderBy('sort', 'asc')
        ->first();        
        if($PageData){
            $data['PageData'] = $PageData;
        }else{
            $data['PageData'] = '';
        }
        if($Allbanner){
            $data['Allbanner'] = $Allbanner;
        }else{
            $data['Allbanner'] = '';
        }
        return view('front.pages.privacy_policy')->with('data', $data);
    }
	
	/*Pagement Page management*/
    public function getPayment(Request $request){
        $data = [];        
        $Allbanner = Banner::where('is_active', true)
        ->where('page_id','=',13)
        ->orderBy('sort', 'asc')
        ->first();
        $PageData = MyPage::where('is_active', true)
        ->where('id','=',13)
        ->orderBy('sort', 'asc')
        ->first();        
        if($PageData){
            $data['PageData'] = $PageData;
        }else{
            $data['PageData'] = '';
        }
        if($Allbanner){
            $data['Allbanner'] = $Allbanner;
        }else{
            $data['Allbanner'] = '';
        }
        return view('front.pages.payment_terms')->with('data',$data);
    }
	
	/*Terms management*/
    public function getTerms(Request $request){
        // term-conditions
        $data = [];
        $Allbanner = Banner::where('is_active', true)
        ->where('page_id','=',11)
        ->orderBy('sort', 'asc')
        ->first();
        $PageData = MyPage::where('is_active', true)
        ->where('id','=',11)
        ->orderBy('sort', 'asc')
        ->first();        
        if($PageData){
            $data['PageData'] = $PageData;
        }
        if($Allbanner){
            $data['Allbanner'] = $Allbanner;
        }
        return view('front.pages.term_conditions')->with('data', $data);
    }
	
	/* This function is used to list the city for lp pags */
	public function getCity(Request $request,$city){
        $mycity = ['delhi', 'pune'];                
        switch ($city){
            case 'delhi':
                $context['crrCity'] =$city;
                return view('front.pages.city.delhi')->with('context',$context);
                break;
            case 'pune':
                $context['crrCity'] =$city;
                return view('front.pages.city.pune')->with('context',$context);
                break;
            case 'mumbai':
                $context['crrCity'] =$city;
                return view('front.pages.city.mumbai')->with('context',$context);
                break;
            case 'nashik':
                $context['crrCity'] =$city;
                return view('front.pages.city.nashik')->with('context',$context);
                break;
            case 'surat':                
                $context['crrCity'] =$city;
                return view('front.pages.city.surat')->with('context',$context);
                break;                
            default:                
				return redirect(route('home').'/c45445');
        }                                              
    }

    public function formAction(Request $request){
        if ($request->isMethod('post')) {
            // Validate the request data
            $rules = [
                'frm_name' => ['required', 'string', 'regex:/^[a-zA-Z\s\-]+$/', 'max:100'],
                'frm_mobile' => ['required', 'string', 'regex:/^[0-9]{8,15}$/', 'max:15'],
                'frm_email' => ['required', 'string', 'email', 'max:50'],
                'frm_city' => ['required', 'string'],  // Added 'string' to match the validation rule
            ];            
            $messages = [
                'frm_name.regex' => 'The name field format is invalid.',
                'frm_mobile.regex' => 'Please enter a mobile number with a length of 8 to 15 digits.',
                'frm_email.email' => 'The email field format is invalid.',
                'frm_city.required' => 'The city field is required.',  // Changed to 'required' for consistency
            ];                
            // Validate the request data with custom messages
            $validatedData = $request->validate($rules, $messages);    
            // Validation passed, proceed with your logic
            $context = [
                // 'frm_name' => $request->input('frm_name'),
                // 'frm_mobile' => $request->input('frm_mobile'),
                // 'frm_email' => $request->input('frm_email'),
                // 'frm_city' => $request->input('frm_city'),
                // 'frm_query' => $request->input('frm_query'),
                'AuthToken' => config('services.authtoken'),
                'Source' => config('services.source'),
                'FirstName' => $request->input('frm_name'),
                'MobileNumber' => $request->input('frm_mobile'),
                'Email' => $request->input('frm_email'),
                'City' => $request->input('frm_city'),
                'leadChannel' => config('services.leadchannel'),
                'LeadSource' => config('services.leadsource'),
                'leadCampaign' => config('services.leadcampaign'),
                'Course' => config('services.course'),
                'Remarks' =>  $request->input('frm_query'),

            ];

            $jsonData = json_encode($context);

            $curl = curl_init();

            curl_setopt_array($curl, array(
                CURLOPT_URL => config('services.authurl'),
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_ENCODING => '',
                CURLOPT_MAXREDIRS => 10,
                CURLOPT_TIMEOUT => 0,
                CURLOPT_FOLLOWLOCATION => true,
                CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
                CURLOPT_CUSTOMREQUEST => 'POST',
                CURLOPT_POSTFIELDS => $jsonData,
                CURLOPT_HTTPHEADER => array(
                    'Content-Type: application/json',
                ),
            ));
            $response = curl_exec($curl);
            curl_close($curl);            
            if($response == "Success"){
                return response()->json([
                    'status' => 200,
                    'msg' => 'Thank you for filling the form. Our representative will get back to you shortly.',
                    'cls' => 'frm_success'
                ]); 
            }else{
                return response()->json([
                    'status' => 404,
                    'msg' => 'Oops, something went wrong. Please try again later.',
                    'cls' => 'frm_error'
                ]); 
            }
        } else {            
            return response()->json([
                'status' => 404,
                'msg' => 'Oops, something went wrong. Please try again later.',
                'cls' => 'frm_error'
            ]); 
        }      
    }	
}
