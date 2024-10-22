from django.contrib import admin
from .models import Contact, Blog,MyTeam, ClientCat, Client, Project,Milestone,PageMeta,Page,Banners,Testimonial,OurSolution,Feature
from .models import Application,OurSolutionOverview,ProjectCategory, SolutionBrand, DownloadPPT

class DownloadPPTAdmin(admin.ModelAdmin):
    list_display = ['id', 'section_title', 'url_title']
    list_display_links = ['id', 'section_title', 'url_title']
    list_per_page = 20

admin.site.register(DownloadPPT,DownloadPPTAdmin)

class SolutionBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand_name', 'sort', 'status']
    list_display_links = ['id', 'brand_name', 'sort', 'status']
    search_fields = ['brand_name']
    list_filter = ['brand_name']
    list_per_page = 20

admin.site.register(SolutionBrand,SolutionBrandAdmin)


class OurSolutionOverviewAdmin(admin.ModelAdmin):
    list_display = ['id','title','status','created_at','updated_at']
    list_display_links = ['id','title','status','created_at','updated_at']
    search_fields = ['title']
    list_filter = ['title','status']
    list_per_page = 20

admin.site.register(OurSolutionOverview,OurSolutionOverviewAdmin)



class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id','title','status','created_at','updated_at']
    list_display_links = ['id','title','status','created_at','updated_at']
    search_fields = ['title']
    list_filter = ['title','status']
    list_per_page = 20

admin.site.register(Application,ApplicationAdmin)


class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id','title','status','created_at','updated_at']
    list_display_links = ['id','title','status','created_at','updated_at']
    search_fields = ['title']
    list_filter = ['title','status']
    list_per_page = 20

admin.site.register(Feature,FeatureAdmin)

class OurSolutionAdmin(admin.ModelAdmin):
    list_display = ['id','solution_title','slugs','status','created_at','updated_at']
    list_display_links = ['id','solution_title','status','created_at','updated_at']
    search_fields = ['id','solution_title','status']
    list_filter = ['solution_title','status']
    list_per_page = 20

admin.site.register(OurSolution,OurSolutionAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['id','cust_name','status']
    list_display_links = ['id','cust_name','status']
    search_fields = ['id','cust_name','status']
    list_filter = ['cust_name','status']

admin.site.register(Testimonial,TestimonialAdmin)

class BannersAdmin(admin.ModelAdmin):
    list_display = ['id','page','heading']
    list_display_links = ['id','page','heading']
    search_fields = ['id','page']
    list_filter = ['page']

admin.site.register(Banners,BannersAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ['id','page']
    list_display_links = ['id','page']
    search_fields = ['id','page']
    list_filter = ['page']

admin.site.register(Page,PageAdmin)

    
class PageMetaAdmin(admin.ModelAdmin):
    list_display = ['id','page_name','page_title','seo_meta_page_title']
    list_display_links = ['id','page_name','page_title','seo_meta_page_title']
    search_fields = ['id','page_name','page_title','seo_meta_page_title']
    list_filter = ['page_name','page_title','seo_meta_page_title']

admin.site.register(PageMeta, PageMetaAdmin)

class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['id','year','ml_desc']
    list_display_links = ['id','year','ml_desc']
    search_fields = ['id','year']
    list_filter = ['year']
admin.site.register(Milestone, MilestoneAdmin)

class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'sort','status']
    list_display_links = ['category_name']
    search_fields = ['category_name']
    list_filter = ['category_name']

admin.site.register(ProjectCategory, ProjectCategoryAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','project_name','project_location', 'sort']
    list_display_links = ['id','project_name','project_location']
    search_fields = ['id','project_name','project_location']    
    list_filter = ['project_name'] 

admin.site.register(Project, ProjectAdmin)

class ClientCatAdmin(admin.ModelAdmin):
    list_display = ['id','cat_name']
    list_display_links = ['id','cat_name']
    search_fields = ['id','cat_name']
    list_filter = ['cat_name']    

class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'cat_name', 'client_name']

admin.site.register(ClientCat, ClientCatAdmin)
admin.site.register(Client, ClientAdmin)


class MyTeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'designation']

admin.site.register(MyTeam, MyTeamAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'contact']

admin.site.register(Contact, ContactAdmin)

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('blog_title', )}
    list_display = ['id', 'blog_title', 'blog_date']

admin.site.register(Blog, BlogAdmin)
