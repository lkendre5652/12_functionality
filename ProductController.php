<?php 
public function GetCategory(Request $request){   
        $catseo = Route::getFacadeRoot()->current()->uri();                  
        $CateogryList = Category::where([['url', '=', $catseo]])->get();
        $context = [];   

        /* POST METHOD START */    
        if ($request->isMethod('post')) {            
            $page = $request->input('page', 1);
            Paginator::currentPageResolver(function () use ($page) {
                return $page;
            });
            $prod_view_items = $request->input('prod_view_items');
            $prod_sort = $request->input('prod_sort');
            $prod_gender = $request->input('prod_gender');
            $prod_sleeve = $request->input('prod_sleeve');
            $prod_brand = $request->input('prod_brand');
            $prod_cats = $request->input('prod_cats');
            $prod_child_cats = $request->input('prod_child_cats');
            $prod_size = $request->input('prod_size');
            $prod_color = $request->input('prod_color');
            $prod_min = (int) $request->input('prod_min', 1);
            $prod_max = (int) $request->input('prod_max', 10000);                   
            $userId = Auth::id() ?? 0;            
            $prod_sortArr = [];
            switch ($prod_sort) {
                case 'newest':
                    $prod_sortArr['is_new'] = 'Yes';
                    break;
                case 'htl':
                    $prod_sortArr['final_price'] = 'desc';
                    break;
                case 'lth':
                    $prod_sortArr['final_price'] = 'asc';
                    break;
                case 'popular':
                    $prod_sortArr['no_of_sales'] = 'desc';
                    break;
                default:
                    $prod_sortArr['created_at'] = 'desc';
            }    

            // Determine categories
            $AllChildCat = !empty($prod_cats) || !empty($prod_child_cats)
                ? array_merge($prod_cats ?? [], $prod_child_cats ?? [])
                : $this->getCategoryTree($CateogryList[0]['id']);        
            $context['AllChildCat'] = $AllChildCat;            
            $query = Product::whereIn('category_id', $context['AllChildCat'])
                ->where('status', 1)
                ->where('stock', '>', 2)
                ->with(['images', 'category','brand','wishlist' => function($query) use ($userId) {
                   $query->where('user_id', $userId);
                }]);
            foreach ($prod_sortArr as $column => $direction) {
                if ($column == 'is_new') {                    
                    $query->latest();
                } else {
                    $query->orderBy($column, $direction);
                }
            }
            if (!empty($prod_gender)) {
                $query->whereIn('gender', $prod_gender);
            }
            if (!empty($prod_sleeve)) {
                $query->whereIn('sleeve', $prod_sleeve);
            }
            if (!empty($prod_brand)) {
                $query->whereIn('brand_id', $prod_brand);
            }
            if (!empty($prod_size)) {
                $query->where(function($q) use ($prod_size) {
                    foreach ($prod_size as $size) {
                        $q->orWhere('search_keywords', 'LIKE', '%' . str_replace('months', 'month', strtolower($size)) . '%');
                    }
                });
            }
            if (!empty($prod_color)) {
                $query->whereIn('family_color', $prod_color);                
            }            

            if (empty($prod_sortArr)) {
                $query->orderBy('created_at', 'desc');
            }
            $query->whereBetween('final_price', [$prod_min, $prod_max]);        

            /* FILTER DATA */
            $filterData = [];
            $familyColors = $query->pluck('family_color')->unique();
            $brandIds = $query->pluck('brand_id')->unique();
            $sleevesProds = $query->pluck('sleeve')->unique();
            $genderProds = $query->pluck('gender')->unique();
            // $AllProductAttributes = $query->pluck('size')->unique();
            $filterData['AllBrands'] = $brandIds;
            // $filterData['AllProductAttributes'] = $AllProductAttributes;
            $filterData['sleevesProds'] = $sleevesProds;
            $filterData['genderProds'] = $genderProds; 
            $filterData['familyColors'] = $familyColors;            
            $preFilterData['ckColor'] = $prod_color;
            /* FILTER DATA */
            
            /* PAGINATIONS */
            $allProducts_pg = $query->paginate($prod_view_items);
            $allProducts_pg->getCollection()->transform(function($product) use ($userId) {
                $product->wishlist = $userId > 0 && $product->wishlist->isNotEmpty();
                return $product;
            });
            /* PAGINATIONS */            
            if ($allProducts_pg->isNotEmpty()) {
                return response()->json(['status' => '200', 'allProducts_pg' => $allProducts_pg, 'current_page' => $page, 'filterData' => $filterData, 'preFilterData' => $preFilterData]);
            } else {
                return response()->json(['status' => '400', 'allProducts_pg' => [],'current_page' => $page,'filterData' => $filterData, 'preFilterData' => $preFilterData]);
            }
            /* POST METHOD END */
        }else{ 

            /* GET METHOD START */            
            $AllChildCat = $this->getCategoryTree($CateogryList[0]['id']);
            $context['AllChildCat'] = $AllChildCat; 
            // if(!empty( $AllChildCat )){
            //     $context['AllChildCat'] = $AllChildCat;
            // }else{
            //     $context['AllChildCat'] = [];
            // }                       
            if( !empty( $context['AllChildCat'] ) ){ 
                $context['AllChildCat'];     
                $allCatFound = Product::whereIn('category_id', $context['AllChildCat'])->where('stock','>',2 )->select('category_id')->pluck('category_id')->unique()->values()->toArray();
                $context['allCatFound'] = $allCatFound;
                $allProducts = Product::whereIn('category_id', $context['AllChildCat'])
                    ->where(
                        [
                            ['status',1],
                            ['stock', '>', 2 ]
                        ])
                        ->with('category','brand')
                    ->get();
                $maxFinalPrice = round($allProducts->max('final_price')) + 100;
                /* PRODUCT LIST WITH PAGINATIONS */
                $allProducts_pg = Product::whereIn('category_id', $context['AllChildCat'])
                    ->where(
                        [
                            ['status',1],
                            ['stock', '>', 2 ]
                        ])
                    ->orderby('created_at', 'desc')->paginate(20);
                    $context['allProducts_pg'] = $allProducts_pg;
                /* PRODUCT LIST WITH PAGINATIONS */
                $brandIds = Product::whereIn('category_id', $context['AllChildCat'])->where(
                        [
                            ['status',1],
                            ['stock', '>', 2 ]
                        ])->pluck('brand_id')->unique();
                $prodIds = Product::whereIn('category_id', $context['AllChildCat'])->where(
                    [
                        ['status',1],
                        ['stock', '>', 2 ]
                    ])->pluck('id')->unique();
                $sleevesProds = Product::whereIn('category_id', $context['AllChildCat'])->where(
                    [
                        ['status',1],
                        ['stock', '>', 2 ]
                    ])->pluck('sleeve')->unique();
                $genderProds = Product::whereIn('category_id', $context['AllChildCat'])->where(
                    [
                        ['status',1],
                        ['stock', '>', 2 ]
                    ])->pluck('gender')->unique();
                $familyColors = Product::whereIn('category_id', $context['AllChildCat'])->where(
                    [
                        ['status',1],
                        ['stock', '>', 2 ]
                    ])->pluck('family_color')->unique();
                $RecursiveCats = $this->getCategoryTree_($CateogryList[0]['id'], $AllChildCat);                
                // return $AllProductAttributes = ProductsAttribute::whereIn('product_id', $prodIds)->pluck('size')->unique();
                $AllProductAttributes = ProductsAttribute::whereIn('product_id', $prodIds)
                    ->pluck('size')
                    ->unique()
                    ->sort(function($a, $b) {
                        return extractAgeValue($a) - extractAgeValue($b);
                    });
                $AllBrands = Brand::whereIn('id', $brandIds)->get();
                $context['allProducts'] = $allProducts;
                $context['AllBrands'] = $AllBrands;
                $context['AllProductAttributes'] = $AllProductAttributes;
                $context['sleevesProds'] = $sleevesProds;
                $context['genderProds'] = $genderProds; 
                $context['familyColors'] = $familyColors;
                $context['RecursiveCats'] = $RecursiveCats;  
                $context['maxFinalPrice'] = $maxFinalPrice;
                return view('front.products.new_product_filter')->with($context);
            }else{
                return 404;
            }            
            /* GET METHOD END */
        }    

    }