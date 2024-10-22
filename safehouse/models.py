from django.db import models
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, FileExtensionValidator

from django.template.defaultfilters import filesizeformat
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
 
        

def validate_image_size(value):
    limit_mb = 5  
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError('File size must be no more than {}.'.format(filesizeformat(limit_mb * 1024 * 1024)))


class OurSolution(models.Model):
    solution_title = models.CharField("Solution Title", max_length=250)  
    slugs = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    solution_description = models.TextField("Solution Description", max_length=500)
    solution_img = models.ImageField("Solution Image (Optional)",
        upload_to = 'our_solutions/',
        validators = [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png']), validate_image_size ],
        max_length = 250,
        blank = True
    )
    other_solution = models.ImageField( "Other Solution Image",
        upload_to='our_solutions/overview/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']) ],
        max_length=250,
        blank=True 
    )
    home_image = models.ImageField("Home Page Image",
        upload_to='our_solutions/overview/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']) ],
        max_length=250,
        blank=True 
    )
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):        
        self.slugs = slugify(self.solution_title)            
        self.updated_at = timezone.now()
        super().save(*args,**kwargs)
        

    def __str__(self):
        return self.solution_title

    class Meta:
        verbose_name = "OurSolution"
        verbose_name_plural = "Solution"

class DownloadPPT(models.Model):    
    solution_title= models.ForeignKey(OurSolution, on_delete=models.CASCADE, null=True, default=None, verbose_name="Select Solution")
    section_title = models.CharField(max_length=50, blank=True, verbose_name="PPT Title")
    ppt_file = models.FileField(
        "PPT File",
        upload_to="our_solutions/ppt/",
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'ppt', 'pptx']),
            validate_image_size
        ]
    )
    url_title = models.CharField(max_length=50, blank=True, verbose_name="URL Title")
    urls = models.CharField(max_length=250, blank=True, verbose_name="URL")
    # sec_video = models.CharField(max_length=250, blank=True, verbose_name="Video")
    # third_video = models.CharField(max_length=250, blank=True, verbose_name="Video")
    # fourth_video = models.CharField(max_length=250, blank=True, verbose_name="Video")
    # fifth_video = models.CharField(max_length=250, blank=True, verbose_name="Video")

    def __str__(self):
        return self.section_title

    class Meta:
        verbose_name = "DownloadPPT"
        verbose_name_plural = "Download PPT"






class SolutionBrand(models.Model):
    solution = models.ManyToManyField('OurSolution', related_name='solutions', verbose_name="Select Solution")
    # solution = models.ManyToManyField(OurSolution, on_delete=models.CASCADE, null=True, default=None, verbose_name="Select Solution")
    brand_name = models.CharField("Brand Name", max_length=100, blank=True)
    brand_image = models.ImageField(
        "Brand Image", 
        upload_to="our_solutions/brand/",
        validators = [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png']), validate_image_size],
        max_length=250,
        blank = True
    )
    sort = models.IntegerField(default=0)
    status = models.BooleanField("Status", default=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand_name

        

class OurSolutionOverview(models.Model):
    solution_title= models.ForeignKey(OurSolution, on_delete=models.CASCADE, null=True, default=None, verbose_name="Select Solution" )
    title = models.CharField("Overview Title", max_length=250)
    description = models.TextField("Overview Description", max_length=500)
    urls = models.CharField("Video Link", max_length=250, blank=True)
    application_img = models.ImageField("Image",
        upload_to = "our_solutions/overview/",
        validators = [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png']), validate_image_size],
        max_length=250,
        blank = True
    )    
    status = models.BooleanField("Status", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def formatted_html_content(self):
        return mark_safe(self.description)

    class Meta:
        verbose_name = "OurSolutionOverview"
        verbose_name_plural = "Solution Overview" 

class Application(models.Model):
    solution_title= models.ForeignKey(OurSolution, on_delete=models.CASCADE, null=True, default=None, verbose_name="Solution Name")
    title = models.CharField("Application Title", max_length=250)
    description = models.TextField("Application Description",max_length=500)
    application_img = models.ImageField("Applicatin Image",
        upload_to = "our_solutions/applications/",
        validators = [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png']), validate_image_size],
        max_length=250,
        blank = True
    )
    status = models.BooleanField("Status", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def formatted_html_content(self):
        return mark_safe(self.description)
    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Application"   

class Feature(models.Model):
    solution_title= models.ForeignKey(OurSolution, on_delete=models.CASCADE, null=True, default=None, verbose_name="Select Solution" )
    title = models.CharField("Feature Title", max_length=250)
    description = models.TextField("Description", max_length=500)
    feature_img = models.ImageField("Image",
        upload_to = "our_solutions/features/",
        validators = [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png']), validate_image_size],
        max_length=250,
        blank = True
    )
    status = models.BooleanField("Status", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Feature"


class Testimonial(models.Model):
    cust_name = models.CharField("Name",max_length=50)
    cust_designation = models.CharField("Designation", max_length=50,blank=True)
    cust_desc = models.TextField("Description",max_length=500,blank=True)
    cust_profile = models.ImageField("Profile Image",
        upload_to='testimonial/',
        validators = [FileExtensionValidator( allowed_extensions=['jpg','jpeg','png']), validate_image_size],
        max_length = 250,
        blank = True
    )
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args,**kwargs)

    def __str__(self):
        return self.cust_name
    
    
    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonial"


class Page(models.Model):
    page = models.CharField("Page Name",max_length=100)

    def __str__(self):
        return self.page
    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Page"

class Banners(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, default=None, verbose_name="Select Page")
    heading = models.CharField("Banner Heading", max_length=50, blank=True) 
    title = models.CharField("Banner Title", max_length=150, blank=True)
    banner_img = models.ImageField("Banner Desktop Image",
        upload_to='page/banner/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), validate_image_size],
        max_length=250,
        blank=True
    )
    mobile_banner = models.ImageField("Banner Mobile Image",
        upload_to='page/banner/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']) ],
        max_length=250,
        blank=True 
    )       

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Banners"
        verbose_name_plural = "Banner"
      


class PageMeta(models.Model):
    page_name = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, default=None, blank=True, verbose_name="Select Page")
    solution_title= models.ForeignKey(OurSolution, on_delete=models.CASCADE, null=True, default=None, blank=True , verbose_name="Select Solution Page")
    # page_name = models.OneToOneField(Page, on_delete=models.CASCADE, null=True, default=None, blank=True)
    # solution_title = models.OneToOneField(OurSolution, on_delete=models.CASCADE, null=True, default=None, blank=True)
    page_title =models.CharField("Page Title", max_length=150,blank=True)
    page_sub_title =models.CharField("Page Sub Title", max_length=250,blank=False)    
    page_banner = models.ImageField("Page Desktop Banner",
        upload_to='page/banner/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), validate_image_size],
        max_length=250,
        blank=True 
    )
    mobile_banner = models.ImageField("Page Mobile Banner", 
        upload_to='page/banner/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']) ],
        max_length=250,
        blank=True 
    )
    page_description =models.TextField("Page Description", max_length=500,blank=True)
    seo_meta_page_title =models.CharField("SEO Title", max_length=150,blank=True)
    seo_meta_description =models.TextField("SEO Description", max_length=500,blank=True)
    seo_meta_url =models.CharField("SEO URL",max_length=150,blank=True)
    is_banners = models.BooleanField(default=False)

    def __str__(self):
        return self.page_title

    class Meta:
        verbose_name = "PageMeta"        
        verbose_name_plural = "SEO & Banner"
        


class ClientCat(models.Model):
    cat_name = models.CharField("Client Category Name", max_length=100)
    clt_cat_img = models.ImageField("Client Category Image",
        upload_to='client/cats/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), validate_image_size],
        max_length=250,
        blank=True
    )
    clt_cat_desc = models.TextField("Description",max_length=500, blank=True)

    def __str__(self):
        return self.cat_name
    class Meta:
        verbose_name = "ClientCat"
        verbose_name_plural = "Client Category"

class Milestone(models.Model):
    year = models.CharField("Year", max_length=10)
    ml_desc = models.TextField("Description")

    def __str__(self):
        return self.year
    class Meta:
        verbose_name = "Milestone"
        verbose_name_plural = "Milestone"
       
class ProjectCategory(models.Model):
    category_name = models.CharField("Project Category Name", max_length=250)
    status = models.BooleanField(default=True)
    sort = models.IntegerField(default=0)
    def __str__(self):
        return self.category_name
    class Meta:
        verbose_name ="Project Category"
        verbose_name_plural = "Project Category"


class Project(models.Model):
    solution_name= models.ForeignKey(OurSolution, on_delete=models.CASCADE,null=True, default=None,blank=True, verbose_name="Solution Type" )
    category_name = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, null=True, default=None, blank=True,  verbose_name="Project Category Type" )
    project_name = models.CharField("Project Name",max_length=250)
    project_location = models.CharField("Project Location", max_length=100)
    project_subtitle = models.CharField("Project Subtitle", max_length=250)
    project_description = models.TextField("Description", max_length=5000)
    project_img = models.ImageField("Project Image",
    upload_to='project/', max_length=250)
    sort = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    is_homePage = models.BooleanField(default=False)
    

    def __str__(self):
        return self.project_name
    def formatted_html_content(self):
        return mark_safe(self.project_description)
    class Meta:
        verbose_name= "Project"
        verbose_name_plural ="Project"

# class ClientCat(models.Model):
#     cat_name = models.CharField(max_length=100)
#     clt_cat_img = models.ImageField(upload_to='client/cats/', max_length=250,blank=True)
#     clt_cat_desc = models.TextField(max_length=500, blank=True)    

#     def __str__(self):
#         return self.cat_name

class Client(models.Model):
    cat_name = models.ForeignKey(ClientCat, on_delete=models.CASCADE, null=True, default=None, verbose_name="Client Category Name")
    client_img = models.ImageField(upload_to='client/', max_length=250, verbose_name="Client Image/ Logo")
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Client's Name")
    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Client"
        

class MyTeam(models.Model):
    name  = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    profile_img = models.ImageField("Profile Image", upload_to='team/', max_length=250, null=True, default=None )

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "MyTeam"
        verbose_name_plural = "Team"


class Blog(models.Model):
    blog_title = models.CharField("Blog Title", max_length=250)
    slug = models.SlugField(max_length=100,unique=True)
    blog_description = models.TextField("Blog Description",max_length=5000, blank=True)
    blog_date =models.DateField("Blog Date", default=now)
    blog_img = models.ImageField("Blog Image", upload_to='uploads/blog/',max_length=250,null=True,default=None)

    def __str__(self):
        return self.blog_title
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blog"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=25)
    product = models.CharField(max_length=100)
    message = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contact Form"
