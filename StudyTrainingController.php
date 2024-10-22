<?php
namespace App\Http\Controllers\Admin;
use App\Http\Controllers\Controller;

use App\Models\Training; 
use App\Models\TrainingExceptOnlineFaq;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use App\Models\InnerPageSeo;

class StudyTrainingController extends Controller
{   
	
	/* This modal is used to update the trainig page data */
	
    protected function updateExceptOnlineFaqs(Request $request, $id=none){        
        $singleExceptOnlineFaqs = TrainingExceptOnlineFaq::find($id);
        $trainings = Training::select('id', 'name')->get();
        if( $request->method() == 'POST'){
            $request->validate([
                'training_id' => 'required',
                'name' => 'required|max:500',                
                'overview' => "max:5000",                
                'sort' => 'numeric',
            ]);
            $singleExceptOnlineFaqs->training_id = $request->input('training_id');
            $singleExceptOnlineFaqs->title = $request->input('name');
            $singleExceptOnlineFaqs->overview = $request->input('overview');
            $singleExceptOnlineFaqs->icon_img = $request->input('square_img_name');
            $singleExceptOnlineFaqs->is_except_training = $request->has('is_except_training') ? true : false;
            $singleExceptOnlineFaqs->is_online_training = $request->has('is_online_training') ? true : false;
            $singleExceptOnlineFaqs->is_faqs = $request->has('is_faq') ? true : false;
            $singleExceptOnlineFaqs->status = $request->input('status');
            $singleExceptOnlineFaqs->sort = $request->input('sort');
            $result = $singleExceptOnlineFaqs->save();                    
            if($result){
                $request->session()->flash('training_success', 'Your Exceptions/Online/Faqs has been successfully updated!!');
                return view('admin.module.training.update_exceptonlinefaqs')->with('singleExceptOnlineFaqs', $singleExceptOnlineFaqs)->with('trainings',$trainings);                
            }else{
                $request->session()->flash('training_error', 'Your Exceptions/Online/Faqs has been successfully updated!!');
                return view('admin.module.training.update_exceptonlinefaqs')->with('singleExceptOnlineFaqs', $singleExceptOnlineFaqs)->with('trainings',$trainings);
            }
        }else{            
            // return 1;             
            return view('admin.module.training.update_exceptonlinefaqs')->with('singleExceptOnlineFaqs', $singleExceptOnlineFaqs)->with('trainings',$trainings);
        }
    }
	
	/* This modal is used to lists the trainig page data */
	
    protected function exceptOnlineFaqsLists(Request $request){
     	if($request->isMethod('POST')){
            //search                        
            $search = $request->input('search');
            if($search){                
                $searchTerm = '%'. trim($search).'%';
                $count = TrainingExceptOnlineFaq::where('title', 'LIKE', $searchTerm)
                ->count();
                $allTrainingExolfqs = TrainingExceptOnlineFaq::where('title', 'LIKE', $searchTerm)
                ->orderBy('created_at', env('SORT_ORDER','asc'))
                ->paginate($count);
            }else{
                $allTrainingExolfqs = TrainingExceptOnlineFaq::orderby('created_at', env('SORT_ORDER','asc'))->paginate(10);
            }            
            $data['allTrainingExolfqs'] = $allTrainingExolfqs;        
            return view('admin.module.training.ex_ol_faqslists')->with('allTrainingExolfqs',$allTrainingExolfqs);
            //search
        }else{
            $allTrainingExolfqs = TrainingExceptOnlineFaq::orderby('created_at', env('SORT_ORDER','asc'))->paginate(10);
            $context = array('status' => '200', 'data' => $allTrainingExolfqs);
            $data = ['allTrainingExolfqs' => $allTrainingExolfqs];
            if($allTrainingExolfqs){
                return view('admin.module.training.ex_ol_faqslists')->with('allTrainingExolfqs',$allTrainingExolfqs);
            }
        }      
    } 
	
	/* This modal is used to insert the trainig page data */
	
    protected function addExceptOnlineFaqs(Request $request){                
        $trainings = Training::select('id', 'name')
        ->where('status', 'active')
        ->orderBy('sort', 'asc')
        ->get();
        if($request->method() == "POST"){
            // return $request->all();
            $request->validate([
                'training_id' => 'required',
                'name' => 'required|max:500',                
                'overview' => "max:5000",                
                'sort' => 'numeric',
            ]);
            $training_id = $request->input('training_id');
            $title = $request->input('name');
            $overview = $request->input('overview');
            $icon_img = $request->input('square_img_name');
            $is_except_training = $request->has('is_except_training') ? true : false;
            $is_online_training = $request->has('is_online_training') ? true : false;
            $is_faq = $request->has('is_faq') ? true : false;
            $status = $request->input('status');
            $sort = $request->input('sort');
            $data = array(
                'training_id' => $training_id,
                'title' => $title,
                'overview' => $overview,
                'icon_img' => $icon_img,                
                'is_except_training' => $is_except_training,
                'is_online_training' => $is_online_training,
                'is_faqs' => $is_faq,
                'status' => $status,
                'sort' => $sort,
            );
            $resp = TrainingExceptOnlineFaq::create($data);
            if($resp){
                $request->session()->flash('training_success', 'Your Training Metadata has been successfully created!!');
                return view('admin.module.training.create_ex_ol_faqs')->with('trainings',$trainings);
            }else{
                $request->session()->flash('training_error', 'Your Training Metadata has been successfully created!!');
                return view('admin.module.training.create_ex_ol_faqs')->with('trainings',$trainings);
            }            
        }else{
            return view('admin.module.training.create_ex_ol_faqs')->with('trainings',$trainings);
        }

    }
	
	/* This modal is used to update the trainig data */
	
    protected function updateTraining(Request $request, $id=None){ 
        $data = [];        
        $singleTraining = Training::find($id); 
        $singleInnerPageSeo = InnerPageSeo::where('is_active', true)
        ->where('training_id', '=', $id)
        ->orderby('sort', 'asc')
        ->first();     

        $data['singleInnerPageSeo'] = $singleInnerPageSeo;
        $data['singleTraining'] = $singleTraining;

        if( $request->method() == 'POST'){
            // $request->validate([
            //     'name' => 'required|max:500',
            //     'slug' => 'required',
            //     'overview' => "max:5000",                
            //     'sort' => 'numeric',
            // ]);
            $request->validate([
                'name' => 'required|max:500',
                'slug' => [
                    'required',
                    'string',
                    'alpha_dash',
                    Rule::unique('study_destinations', 'slug')->ignore($id),
                ],
                'overview' => 'max:5000',
                'sort' => 'numeric',
            ], [
                'slug.required' => 'The slug field is required.',
                'slug.string' => 'The slug must be a string.',
                'slug.alpha_dash' => 'The slug may only contain letters, numbers, dashes, and underscores.',
                'slug.unique' => 'The slug has already been taken.',
            ]);                                     
            $singleTraining->name = $request->name;            
            $singleTraining->slug = $request->slug;
            $singleTraining->banner_title = $request->banner_title;
            $singleTraining->desktop_banner = $request->square_img_name;
            $singleTraining->mobile_banner = $request->listing_img_name;
            $singleTraining->overview = $request->overview;
            $singleTraining->overview_image = $request->icon_img_name;            
            $singleTraining->is_home = $request->has('is_home') ? true : false;
            $singleTraining->sort = $request->sort;
            $singleTraining->status = $request->status;
            $singleTraining->save();

            $innerPageSeo = InnerPageSeo::firstOrNew(['training_id' => $singleTraining->id]);
            $innerPageSeo->seo_meta_title = $request->input('seo_meta_title');
            $innerPageSeo->seo_meta_description = $request->input('seo_meta_description');
            $innerPageSeo->seo_meta_og_description = $request->input('seo_meta_og_description');
            $innerPageSeo->seo_meta_og_twitter_description = $request->input('seo_meta_og_twitter_description');
            $innerPageSeo->seo_meta_canonical = $request->input('seo_meta_canonical');
            $innerPageSeo->seo_meta_og_locale = $request->input('seo_meta_og_locale');
            $innerPageSeo->seo_meta_og_site_name = $request->input('seo_meta_og_site_name');
            $innerPageSeo->seo_meta_og_type = $request->input('seo_meta_og_type');
            $innerPageSeo->seo_meta_og_url = $request->input('seo_meta_og_url');
            $innerPageSeo->seo_meta_og_secure_url = $request->input('seo_meta_og_secure_url');
            $innerPageSeo->seo_meta_og_twitter_card = $request->input('seo_meta_og_twitter_card');
            $innerPageSeo->seo_meta_og_twitter_title = $request->input('seo_meta_og_twitter_title');
            $innerPageSeo->seo_keyword = $request->input('seo_keyword');
            $innerPageSeo->indexing = $request->input('indexing');
            $innerPageSeo->follow_link = $request->input('follow_link');
            $innerPageSeo->meta_robot = $request->input('meta_robot');
            $innerPageSeo->page_type = $request->input('page_type');
            $innerPageSeo->article_type = $request->input('article_type');
            $innerPageSeo->sort = $request->input('sort');
            $innerPageSeo->is_active = true;            
            $innerPageSeo->save(); 
            
            $singleInnerPageSeo = InnerPageSeo::where('is_active', true)
            ->where('training_id', '=', $id)
            ->orderby('sort', 'asc')
            ->first(); 
            $data['singleInnerPageSeo'] = $singleInnerPageSeo;

            if($singleTraining){
                $request->session()->flash('training_success', 'Your Training has been successfully updated!!');
                return view('admin.module.training.update')->with('data', $data);                
            }else{
                $request->session()->flash('training_error', 'Your Training has been successfully updated!!');
                return view('admin.module.training.update')->with('data', $data);
            }
        }else{                         
            return view('admin.module.training.update')->with('data', $data);
        }        
    }
	
	/* This modal is used to lists the trainig data */
	
    protected function trainingLists(Request $request){
        if($request->isMethod('POST')){
            //search                        
            $search = $request->input('search');
            if($search){                
                $searchTerm = '%'. trim($search).'%';
                $count = Training::where('name', 'LIKE', $searchTerm)
                ->count();
                $allTraining = Training::where('name', 'LIKE', $searchTerm)
                ->orderBy('created_at', env('SORT_ORDER','asc'))
                ->paginate($count);
            }else{
                $allTraining = Training::orderby('created_at', env('SORT_ORDER','asc'))->paginate(10);
            }            
            $data['allTraining'] = $allTraining;        
            return view('admin.module.training.traininglists')->with('allTraining',$allTraining);
            //search
        }else{
            $allTraining = Training::orderby('created_at', env('SORT_ORDER','asc'))->paginate(10);
            $context = array('status' => '200', 'data' => $allTraining);
            $data = ['allTraining' => $allTraining];
            if($allTraining){
                return view('admin.module.training.traininglists')->with('allTraining',$allTraining);
            }
        }     
    }
	
	/* This modal is used to insert the trainig data */
	
    protected function createTraining(Request $request){
        if($request->method() == "POST"){
            // return $request->all();
            $request->validate([
                'name' => 'required|max:500',
                'slug' => 'required|unique:trainings,slug,',
                'overview' => "max:5000",                
                'sort' => 'numeric',
            ]);      
            $name = $request->input('name');
            $slug = $request->input('slug');
            $banner_title = $request->input('banner_title');
            $desktop_banner = $request->input('square_img_name');
            $mobile_banner = $request->input('listing_img_name');
            $overview = $request->input('overview');
            $overview_image = $request->input('icon_img_name');
            $is_home = $request->has('is_home') ? true : false;
            $status = $request->input('status');
            $sort = $request->input('sort');

            $data = array(
                'name' => $name,
                'slug' => $slug,
                'banner_title' => $banner_title,
                'desktop_banner' => $desktop_banner,
                'mobile_banner' => $mobile_banner,
                'overview' => $overview,
                'is_home' => $is_home,
                'status' => $status,
                'sort' => $sort,
            );
            $resp = Training::create($data);

            //seo meta
			$innerPageSeo = new InnerPageSeo();
            $innerPageSeo->training_id = $resp->id;
            $innerPageSeo->seo_meta_title = $request->input('seo_meta_title');
            $innerPageSeo->seo_meta_description = $request->seo_meta_description;
            $innerPageSeo->seo_meta_og_description = $request->seo_meta_og_description;
            $innerPageSeo->seo_meta_og_twitter_description = $request->seo_meta_og_twitter_description;
            $innerPageSeo->seo_meta_canonical = $request->seo_meta_canonical;
            $innerPageSeo->seo_meta_og_locale = $request->seo_meta_og_locale;
            $innerPageSeo->seo_meta_og_site_name = $request->seo_meta_og_site_name;
            $innerPageSeo->seo_meta_og_type = $request->seo_meta_og_type;
            $innerPageSeo->seo_meta_og_url = $request->seo_meta_og_url;
            $innerPageSeo->seo_meta_og_secure_url = $request->seo_meta_og_secure_url;
            $innerPageSeo->seo_meta_og_twitter_card = $request->seo_meta_og_twitter_card;
            $innerPageSeo->seo_meta_og_twitter_title = $request->seo_meta_og_twitter_title;
            $innerPageSeo->seo_keyword = $request->seo_keyword;
            $innerPageSeo->indexing = $request->indexing;
            $innerPageSeo->follow_link = $request->follow_link;
            $innerPageSeo->meta_robot = $request->meta_robot;
            $innerPageSeo->page_type = $request->page_type;
            $innerPageSeo->article_type = $request->article_type;
            $innerPageSeo->sort = $request->sort;
            $innerPageSeo->is_active = true;            
            $innerPageSeo->save();
			//seo meta

            if($resp){
                $request->session()->flash('training_success', 'Your Job has been successfully created!!');
                return view('admin.module.training.create');
            }else{
                $request->session()->flash('training_error', 'Your Job has been successfully created!!');
                return view('admin.module.training.create');
            }            
        }else{            
            return view('admin.module.training.create');
        }

    }    
}
