<?php
namespace App\Http\Controllers\Admin;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\CurrentOpening;
use App\Models\CareerModule;
use App\Models\Counselling;


class CareerController extends Controller
{
	/* This function is updating the career counselling module data */
	
	protected function updateCounselling(Request $request, $id=None){        
        $singleCounselling = Counselling::find($id);
        $data = [];
        $data['singleCounselling'] = $singleCounselling;
        if( $request->method() == 'POST'){
            $request->validate([                              
                'sort' => 'numeric',
            ]);                        
            $singleCounselling->choose_us = $request->choose_us;            
            $singleCounselling->packages = $request->packages;
            $singleCounselling->counselling = $request->counselling;
            $singleCounselling->transform = $request->transform;            
            $singleCounselling->sort = $request->sort;
            $singleCounselling->is_active = $request->has('is_active') ? true : false;            
            $singleCounselling->save();
            if($singleCounselling){
                $request->session()->flash('career_success', 'Your Counselling has been successfully updated!!');
                return view('admin.module.career.counselling.update')->with('data', $data);                
            }else{
                $request->session()->flash('career_error', 'Your Counselling has been successfully updated!!');
                return view('admin.module.career.counselling.update')->with('data', $data);
            }
        }else{                         
            return view('admin.module.career.counselling.update')->with('data', $data);
        }        
    }
	
	/* This function listing the career counselling module data */
	
    protected function CareerCounselling(Request $request){                
        $data = [];        
        if($request->isMethod('POST')){
            //search
            $search = $request->input('search');
            if($search){                
                $searchTerm = '%'. trim($search).'%';
                $count = Counselling::where('choose_us', 'LIKE', $searchTerm)
                ->count();
                $allCounselling = Counselling::where('choose_us', 'LIKE', $searchTerm)
                ->orderBy('created_at', 'desc')
                ->paginate($count);
            }else{
                $allCounselling = Counselling::orderby('created_at', 'desc')->paginate(10);
            }
            //search
            $data['allCounselling'] = $allCounselling;        
            return view('admin.module.career.counselling.counsellinglists')->with('data',$data);                
        }else{
            $allCounselling = Counselling::orderby('created_at', 'desc')->paginate(10);
            $data['allCounselling'] = $allCounselling;        
            return view('admin.module.career.counselling.counsellinglists')->with('data',$data);                
        }
        
    }
	
	/* This function inserting the career counselling module data */
	
    protected function createCounselling(Request $request){
        if($request->method() == "POST"){            
            $request->validate([                               
                'sort' => 'numeric',                
            ]);            
            $data = array(
                'choose_us' => $request->input('choose_us'),
                'packages' => $request->input('packages'),
                'counselling' => $request->input('counselling'), 
                'transform' => $request->input('transform'),                
                'sort' => $request->sort, 
                'is_active' => $request->has('is_active') ? true : false,
            );            
            $resp = Counselling::create($data);
            if($resp){
                $request->session()->flash('career_success', 'Your Counselling been successfully created!!');
                return view('admin.module.career.counselling.create');
            }else{
                $request->session()->flash('career_error', 'Your Counselling been successfully created!!');
                return view('admin.module.career.counselling.create');
            }            
        }else{
            return view('admin.module.career.counselling.create');
        }

    }
    
	/* This function is used to update career page data */
	
    protected function updateCareerData(Request $request, $id=None){        
        $singleCareerModule = CareerModule::find($id);
        $data = [];
        $data['singleCareerModule'] = $singleCareerModule;
        if( $request->method() == 'POST'){
            $request->validate([    
                'name' => 'required|max:500',
                'overview' => "max:5000",                
                'sort' => 'numeric',
            ]);                        
            $singleCareerModule->name = $request->name;            
            $singleCareerModule->overview = $request->overview;
            $singleCareerModule->image = $request->square_img_name;
            $singleCareerModule->is_life_slider = $request->has('is_life_slider') ? true : false;
            $singleCareerModule->sort = $request->sort;
            $singleCareerModule->is_active = $request->has('is_active') ? true : false;            
            $singleCareerModule->save();
            if($singleCareerModule){
                $request->session()->flash('career_success', 'Your Careed Data has been successfully updated!!');
                return view('admin.module.career.career_module.update')->with('data', $data);                
            }else{
                $request->session()->flash('career_error', 'Your Careed Data has been successfully updated!!');
                return view('admin.module.career.career_module.update')->with('data', $data);
            }
        }else{                         
            return view('admin.module.career.career_module.update')->with('data', $data);
        }        
    }
	
	/* This function is used to list the career page data */
	
    protected function CareerModuleLists(Request $request){                
        $data = [];
        
        if($request->isMethod('POST')){
            //search                        
            $search = $request->input('search');
            if($search){                
                $searchTerm = '%'. trim($search).'%';
                $count = CareerModule::where('name', 'LIKE', $searchTerm)
                ->count();
                $allCareerModule = CareerModule::where('name', 'LIKE', $searchTerm)
                ->orderBy('created_at', 'desc')
                ->paginate($count);
            }else{
                $allCareerModule = CareerModule::orderby('created_at', 'desc')->paginate(10);
            }
            //search
            $data['allCareerModule'] = $allCareerModule;        
            return view('admin.module.career.career_module.careermodulelists')->with('data',$data);                
        }else{
            $allCareerModule = CareerModule::orderby('created_at', 'desc')->paginate(10);
            $data['allCareerModule'] = $allCareerModule;        
            return view('admin.module.career.career_module.careermodulelists')->with('data',$data);                
        }
        
    }
	
	/* This function is used to insert the career page data */
	
    protected function createCareerModule(Request $request){
        if($request->method() == "POST"){
            
            $request->validate([
                'name' => 'required|max:500',
                'overview' => "max:5000",                
                'sort' => 'numeric',                
            ],[
                'name.required' => 'The Tilte field is required.'
            ]);            
            $data = array(
                'name' => $request->input('name'),
                'overview' => $request->input('overview'),
                'image' => $request->input('square_img_name'),                
                'is_life_slider' => $request->has('is_life_slider') ? true : false, 
                'sort' => $request->sort, 
                'is_active' => $request->has('status') ? true : false,
            );
            $resp = CareerModule::create($data);
            if($resp){
                $request->session()->flash('career_success', 'Your Careed Data been successfully created!!');
                return view('admin.module.career.career_module.create');
            }else{
                $request->session()->flash('career_error', 'Your Careed Data been successfully created!!');
                return view('admin.module.career.career_module.create');
            }            
        }else{
            return view('admin.module.career.career_module.create');
        }

    }

    /* This function is used to update the career page jobs data */
	
    public function updateJob(Request $request, $id=None){
        $singleJob = CurrentOpening::find($id);   
        if( $request->method() == 'POST'){
            $request->validate([    
                'job_title' => 'required|max:500',
                'overview' => "max:5000",
                'responsibility' => "max:5000",
                'qualification' => "max:5000",            
                'sort' => 'numeric',
            ]);
            $singleJob->job_title = $request->job_title;
            $singleJob->overview = $request->overview;
            $singleJob->responsibility = $request->responsibility;
            $singleJob->qualification = $request->qualification;
            $singleJob->sort = $request->sort;
            $singleJob->status = $request->status;
            $singleJob->save();
            if($singleJob){
                $request->session()->flash('career_success', 'Your Job has been successfully updated!!');
                return view('admin.module.career.update')->with('singleJob', $singleJob);
            }else{
                $request->session()->flash('career_error', 'Your Job has been successfully updated!!');
                return view('admin.module.career.update')->with('singleJob', $singleJob);
            }
        }else{
            // return $id;                     
            return view('admin.module.career.update')->with('singleJob', $singleJob);
        }        
    }
	
	/* This function is used to list the career page jobs data */
	
    public function jobLists(Request $request){
       if($request->isMethod("POST")){
            //search                        
            $search = $request->input('search');
            if($search){                
                $searchTerm = '%'. trim($search).'%';
                $count = CurrentOpening::where('job_title', 'LIKE', $searchTerm)
                ->count();
                $allJobs = CurrentOpening::where('job_title', 'LIKE', $searchTerm)
                ->orderBy('created_at', env('SORT_ORDER','asc'))
                ->paginate($count);
            }else{
                $allJobs = CurrentOpening::orderby('created_at', env('SORT_ORDER','asc'))->paginate(10);
            }            
            $data['allJobs'] = $allJobs;        
            return view('admin.module.career.joblists')->with('allJobs',$allJobs);
            //search

        }else{
            $allJobs = CurrentOpening::orderby('sort', env('SORT_ORDER','asc'))->paginate(10);
            $context = array('status' => '200', 'data' => $allJobs);
            $data = ['allJobs' => $allJobs];
            if($allJobs){
                return view('admin.module.career.joblists')->with('allJobs',$allJobs);
            }
        }
    }
	
	/* This function is used to insert the career page jobs data */
	
    function createJob(Request $request){    
        if($request->method() == "POST"){
            $request->validate([    
                'job_title' => 'required|max:500',
                'overview' => "max:5000",
                'responsibility' => "max:5000",
                'qualification' => "max:5000",
                // 'form_status' => 'boolean',
                'sort' => 'numeric',
            ]);                        
            $resp = CurrentOpening::create($request->all());
            if($resp){
                $request->session()->flash('career_success', 'Your Job has been successfully created!!');
                return view('admin.module.career.create');
            }else{
                $request->session()->flash('career_error', 'Your Job has been successfully created!!');
                return view('admin.module.career.create');
            }
        }else{
            return view('admin.module.career.create');
        }        
   }   
}
