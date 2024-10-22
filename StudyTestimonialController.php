<?php

namespace App\Http\Controllers\Admin;
use App\Http\Controllers\Controller;
use App\Models\Testimonial;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class StudyTestimonialController extends Controller
{
    /* This modal is used to update the testimonials */
	
    protected function updateTestimonial(Request $request, $id=None){        
        $singletestimonial = Testimonial::find($id);   
        if( $request->method() == 'POST'){
            $request->validate([    
                'name' => 'required|max:500',
                'message' => "max:5000",                
                'sort' => 'numeric',
            ]);                        
            $singletestimonial->name = $request->name;            
            $singletestimonial->university = $request->university;
            $singletestimonial->message = $request->message;
            $singletestimonial->is_video = $request->has('is_video') ? true : false;
            $singletestimonial->is_home = $request->has('is_home') ? true : false;
            $singletestimonial->video_link = $request->video_link;
            $singletestimonial->sort = $request->sort;
            $singletestimonial->status = $request->status;
            $singletestimonial->profile = $request->square_img_name;
            $singletestimonial->save();
            if($singletestimonial){
                $request->session()->flash('testimonial_success', 'Your Testimonial has been successfully updated!!');
                return view('admin.module.testimonial.update')->with('singletestimonial', $singletestimonial);                
            }else{
                $request->session()->flash('testimonial_error', 'Your Testimonial has been successfully updated!!');
                return view('admin.module.testimonial.update')->with('singletestimonial', $singletestimonial);
            }
        }else{                         
            return view('admin.module.testimonial.update')->with('singletestimonial', $singletestimonial);
        }        
    }   
	
	/* This modal is used to lists the testimonials */
	
    protected function testimonialLists(Request $request){
       if($request->isMethod('POST')){
            //search                        
            $search = $request->input('search');
            if($search){                
                $searchTerm = '%'. trim($search).'%';
                $count = Testimonial::where('name', 'LIKE', $searchTerm)
                ->count();
                $allTestimonial = Testimonial::where('name', 'LIKE', $searchTerm)
                ->orderBy('created_at', env('SORT_ORDER','asc'))
                ->paginate($count);
            }else{
                $allTestimonial = Testimonial::orderby('created_at', env('SORT_ORDER','asc'))->paginate(10);
            }            
            $data['allTestimonial'] = $allTestimonial;        
            return view('admin.module.testimonial.testimoniallists')->with('allTestimonial',$allTestimonial);
            //search
        }else{
            $allTestimonial = Testimonial::orderby('created_at', env('SORT_ORDER','asc'))->paginate(10);
            $context = array('status' => '200', 'data' => $allTestimonial);
            $data = ['allTestimonial' => $allTestimonial];
            if($allTestimonial){
                return view('admin.module.testimonial.testimoniallists')->with('allTestimonial',$allTestimonial);
            }
        }      
    }
	
	/* This modal is used to insert the testimonials */
	
    protected function createTestimonial(Request $request){
        if($request->method() == "POST"){
            $request->validate([
                'name' => 'required|max:500',
                'message' => "max:5000",                
                'sort' => 'numeric',
            ]);                        
            $name = $request->input('name');
            $university = $request->input('university');
            $message = $request->input('message');
            $square_img_name = $request->input('square_img_name');
            $is_video = $request->has('is_video') ? true : false;
            $video_link = $request->input('video_link');                        
            $is_home = $request->has('is_home') ? true : false;
            $status = $request->input('status');
            $sort = $request->input('sort');                       
            $data = array(
                'name' => $name,
                'university' => $university,
                'message' => $message,
                'profile' => $square_img_name,
                'is_video' => $is_video,
                'video_link' => $video_link,
                'is_home' => $is_home,
                'status' => $status,
                'sort' => $sort,
            );
            $resp = Testimonial::create($data);
            if($resp){
                $request->session()->flash('testimonial_success', 'Your Job has been successfully created!!');
                return view('admin.module.testimonial.create');
            }else{
                $request->session()->flash('testimonial_error', 'Your Job has been successfully created!!');
                return view('admin.module.testimonial.create');
            }            
        }else{
            return view('admin.module.testimonial.create');
        }

    }
}
