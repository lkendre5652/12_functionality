from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.db.models import Max


class OTPVerify(models.Model):
    otp_my = models.CharField(max_length=7, blank=False, verbose_name="OTP")
    email = models.EmailField(max_length=100, blank=False, verbose_name="E-mail")
    client_ip = models.CharField(max_length=12, blank=True, verbose_name="Client IP Address")
    verify_otp = models.BooleanField(default=False, verbose_name="Verify OTP")    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.otp_my

    class Meta:
        verbose_name = "OTPVerify"
        verbose_name_plural = "OTP Verify"


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, middle_name, last_name, dob, marital_status, username, email, phone_number, admission_type, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')  
        # max_id = Account.objects.aggregate(Max('id'))['id__max']
        # next_id = 20240001 if max_id is None else max_id + 1

        user = self.model(
            # id=next_id,
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob,
            marital_status=marital_status,
            phone_number=phone_number,
            admission_type=admission_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        user.is_student = True
        return user

    
    
    def create_superuser(self, first_name, middle_name,last_name, dob,marital_status,phone_number,admission_type,email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            middle_name="",  # Superuser doesn't have a middle name
            last_name=last_name,
            dob=None,  # Superuser doesn't have a date of birth
            marital_status="",  # Superuser doesn't have a marital status
            phone_number="",  # Superuser doesn't have a phone number
            admission_type="",  # Superuser doesn't have an admission type
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_student = False
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    COURCE_CHOICES_TYPE = (
        ('ug_program', 'UG Program'),
        ('pg_program', 'PG Program'),       
        ('phd_program', 'PhD Program'),
    )
    COURCE_CHOICES = (
        ("ug_program","B.Tech in Bioengineering - 4 Years"),
        ("pg_program","Integrated Masters Program in Bioengineering - 5 Years"),        
        ("pg_program","M.Tech in Environmental Bioengineering - 2 Years"),
        ("pg_program","M.Sc. in Industrial Biotechnology – 2 Years"),
        ("pg_program","M.Sc. in Bioinformatics"),
        ("phd_program","PhD in Bioengineering"),      

    )
    BLOOD_GROUP_CHOICES = (
        ("abpos", "AB+"),
        ("abneg", "AB-"),
        ("apos", "A+"),
        ("aneg", "A-"),
        ("bpos", "B+"),
        ("bneg", "B-"),
        ("opos", "O+"),
        ("oneg", "O-"),
    )
    MARITAL_CHOICES = (
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    CATEGORY_CHOICE = (
        ("general","General"),
        ("obc","OBC"),
        ("vjnt","VJNT"),
        ("ntb","NT-B"),
        ("ntc","NT-C"),
        ("ntd","NT-D"),
        ("sbc","SBC"),
        ("sc","S.C."),
        ("st","S.T.")
    )
    DEGREE_CHOICE = (
        ("b.e. /b.tech. environmental engineering", "B.E. /B.Tech. Environmental Engineering"),
        ("b.e. /b.tech. chemical engineering", "B.E. /B.Tech. Chemical Engineering"),
        ("b.e. /b.tech. ceramic technology", "B.E. /B.Tech. Ceramic Technology"),
        ("b.e. /b.tech. mechanical engineering", "B.E. /B.Tech. Mechanical Engineering"),
        ("b.e. /b.tech. metallurgy engineering", "B.E. /B.Tech. Metallurgy Engineering"),
        ("b.e. /b.tech. civil engineering", "B.E. /B.Tech. Civil Engineering"),
        ("b.e. /b.tech. mining engineering", "B.E. /B.Tech. Mining Engineering"),
        ("b.e. /b.tech. biochemical engineering", "B.E. /B.Tech. Biochemical Engineering"),
        ("b.e. /b.tech. biotechnology", "B.E. /B.Tech. Biotechnology"),
        ("b.sc. biotechnology", "B.Sc. Biotechnology"),
        ("b.sc. microbiology", "B.Sc. Microbiology"),
        ("b.sc. chemistry", "B.Sc. Chemistry"),
        ("b.sc. life sciences", "B.Sc. Life Sciences"),
        ("other allied engineering", "Other allied Engineering"),
        ("other allied science branches", "Other allied Science Branches")
    )
    NATIONALITY_CHOICES = (
        #  ("indian","Indian"),
        #  ("nri","NRI"),
        #  ("piooci","PIO/OCI"),
        #  ("foreign","Foreign"),
        ("country_Indian","Indian"),
        ("country_Afghan","Afghan"),
        ("country_Albanian","Albanian"),
        ("country_Algerian","Algerian"),
        ("country_Ambia","Ambia"),
        ("country_American","American Samoan"),
        ("country_Americans","Americans"),
        ("country_Andorran","Andorran"),
        ("country_Angolan","Angolan"),
        ("country_Anguillan","Anguillan"),
        ("country_Antiguan","Antiguan Barbudan"),
        ("country_Argentinian","Argentinian"),
        ("country_Armenian","Armenian"),
        ("country_Aruban","Aruban"),
        ("country_Australian","Australian"),
        ("country_Austrian","Austrian"),
        ("country_Azerbaijani","Azerbaijani"),
        ("country_Bahamian","Bahamian"),
        ("country_Bahraini","Bahraini"),
        ("country_Bajan","Bajan"),
        ("country_Bangladeshi","Bangladeshi"),
        ("country_Barthélemoise","Barthélemoise"),
        ("country_Belarusian","Belarusian"),
        ("country_Belgian","Belgian"),
        ("country_Belizean","Belizean"),
        ("country_Beninese","Beninese"),
        ("country_Bermudian","Bermudian"),
        ("country_Bhutanese","Bhutanese"),
        ("country_Bissau","Bissau-Guinean"),
        ("country_Bolivian","Bolivian"),
        ("country_Bosnian","Bosnian Herzegovinian"),
        ("country_Bouvet","Bouvet Island"),
        ("country_Brazilian","Brazilian"),
        ("country_British","British"),
        ("country_Bruneian","Bruneian"),
        ("country_Bulgarian","Bulgarian"),
        ("country_Burkinabè","Burkinabè"),
        ("country_Burmese","Burmese"),
        ("country_Burundian","Burundian"),
        ("country_Cambodian","Cambodian"),
        ("country_Cameroonian","Cameroonian"),
        ("country_Canadian","Canadian"),
        ("country_Canarian","Canarian"),
        ("country_Cape","Cape Verdean"),
        ("country_Caymanian","Caymanian"),
        ("country_Central","Central African"),
        ("country_Chadian","Chadian"),
        ("country_Chilean","Chilean"),
        ("country_Chinese","Chinese"),
        ("country_Colombian","Colombian"),
        ("country_Comoran","Comoran"),
        ("country_Congolese","Congolese (Democratic Republic of Congo)"),
        ("country_Congolese","Congolese (Republic of Congo)"),
        ("country_Cook","Cook Islander"),
        ("country_Costa","Costa Rican"),
        ("country_Croatian","Croatian"),
        ("country_Cuban","Cuban"),
        ("country_Curacaoan","Curacaoan"),
        ("country_Cypriot","Cypriot"),
        ("country_Czech","Czech"),
        ("country_Danish","Danish"),
        ("country_Djiboutian","Djiboutian"),
        ("country_Dominican","Dominican (Dominica)"),
        ("country_Dominican","Dominican (Dominican Republic)"),
        ("country_Dutch","Dutch"),
        ("country_East","East Timorese"),
        ("country_Ecuadorean","Ecuadorean"),
        ("country_Egyptian","Egyptian"),
        ("country_El","El Salvadoran"),
        ("country_Equatorial","Equatorial Guinean"),
        ("country_Eritrean","Eritrean"),
        ("country_Estonian","Estonian"),
        ("country_Ethiopian","Ethiopian"),
        ("country_Falkland","Falkland Islander"),
        ("country_Faroese","Faroese"),
        ("country_Fijian","Fijian"),
        ("country_Filipino","Filipino"),
        ("country_Finnish","Finnish"),
        ("country_French","French"),
        ("country_French","French Guyanese"),
        ("country_Gabonese","Gabonese"),
        ("country_Gambian","Gambian"),
        ("country_Georgian","Georgian"),
        ("country_German","German"),
        ("country_Ghanaian","Ghanaian"),
        ("country_Gibraltarian","Gibraltarian"),
        ("country_Greek","Greek"),
        ("country_Greenlandic","Greenlandic"),
        ("country_Grenadian","Grenadian"),
        ("country_Guadeloupean","Guadeloupean"),
        ("country_Guamanian","Guamanian"),
        ("country_Guatemalan","Guatemalan"),
        ("country_Guinean","Guinean"),
        ("country_Guyanese","Guyanese"),
        ("country_Haitian","Haitian"),
        ("country_Honduran","Honduran"),
        ("country_Hongkonger","Hongkonger"),
        ("country_Hungarian","Hungarian"),
        ("country_i","i-Kiribati"),
        ("country_Icelander","Icelander"),
        ("country_Indonesian","Indonesian"),
        ("country_Iranian","Iranian"),
        ("country_Iraqi","Iraqi"),
        ("country_Irish","Irish"),
        ("country_Israeli","Israeli"),
        ("country_Italian","Italian"),
        ("country_Ivorian","Ivorian (Côte D'Ivoire)"),
        ("country_Ivorian","Ivorian (Ivory Coast)"),
        ("country_Jamaican","Jamaican"),
        ("country_Japanese","Japanese"),
        ("country_Jersey","Jersey"),
        ("country_Jordanian","Jordanian"),
        ("country_Kazakh","Kazakh"),
        ("country_Kenyan","Kenyan"),
        ("country_Kosovar","Kosovar"),
        ("country_Kuwaiti","Kuwaiti"),
        ("country_Kyrgyz","Kyrgyz"),
        ("country_Laotian","Laotian"),
        ("country_Latvian","Latvian"),
        ("country_Lebanese","Lebanese"),
        ("country_Liberian","Liberian"),
        ("country_Libyan","Libyan"),
        ("country_Liechtensteiner","Liechtensteiner"),
        ("country_Lithuanian","Lithuanian"),
        ("country_Luxembourger","Luxembourger"),
        ("country_Macanese","Macanese"),
        ("country_Macedonian","Macedonian"),
        ("country_Malagasy","Malagasy"),
        ("country_Malawian","Malawian"),
        ("country_Malaysian","Malaysian"),
        ("country_Maldivian","Maldivian"),
        ("country_Malian","Malian"),
        ("country_Maltese","Maltese"),
        ("country_Manx","Manx"),
        ("country_Marshallese","Marshallese"),
        ("country_Martinique","Martinique"),
        ("country_Mauritanian","Mauritanian"),
        ("country_Mauritian","Mauritian"),
        ("country_Mexican","Mexican"),
        ("country_Moldovan","Moldovan"),
        ("country_Monégasque","Monégasque"),
        ("country_Mongolian","Mongolian"),
        ("country_Montenegrin","Montenegrin"),
        ("country_Montserratian","Montserratian"),
        ("country_Moroccan","Moroccan"),
        ("country_Mosotho","Mosotho"),
        ("country_Motswana","Motswana"),
        ("country_Mozambican","Mozambican"),
        ("country_Namibian","Namibian"),
        ("country_Nauruan","Nauruan"),
        ("country_Nepali","Nepali"),
        ("country_New","New Caledonian"),
        ("country_New","New Zealander"),
        ("country_ni","ni-Vanuatu"),
        ("country_Nicaraguan","Nicaraguan"),
        ("country_Nigerian","Nigerian"),
        ("country_Nigerien","Nigerien"),
        ("country_Niuean","Niuean"),
        ("country_North","North Korean"),
        ("country_Norwegian","Norwegian"),
        ("country_Omani","Omani"),
        ("country_Pakistani","Pakistani"),
        ("country_Palauan","Palauan"),
        ("country_Palestinian","Palestinian"),
        ("country_Panamanian","Panamanian"),
        ("country_Papua","Papua New Guinean"),
        ("country_Paraguayan","Paraguayan"),
        ("country_Peruvian","Peruvian"),
        ("country_Polish","Polish"),
        ("country_Portuguese","Portuguese"),
        ("country_Puerto","Puerto Rican"),
        ("country_Qatari","Qatari"),
        ("country_Reunion","Reunion"),
        ("country_Romanian","Romanian"),
        ("country_Russian","Russian"),
        ("country_Rwandan","Rwandan"),
        ("country_Saint","Saint Helenian"),
        ("country_Saint","Saint Kittian Nevisian"),
        ("country_Saint","Saint Lucian"),
        ("country_Saint","Saint Martiner"),
        ("country_Sammarinese","Sammarinese"),
        ("country_Samoan","Samoan"),
        ("country_Santomean","Santomean"),
        ("country_Sarnian","Sarnian"),
        ("country_Saudi","Saudi Arabian"),
        ("country_Scottish","Scottish"),
        ("country_Senegalese","Senegalese"),
        ("country_Serbian","Serbian"),
        ("country_Seychellois","Seychellois"),
        ("country_Sierra","Sierra Leonean"),
        ("country_Singaporean","Singaporean"),
        ("country_Slovakian","Slovakian"),
        ("country_Slovenian","Slovenian"),
        ("country_Solomon","Solomon Islander"),
        ("country_Somali","Somali"),
        ("country_South","South African"),
        ("country_South","South Korean"),
        ("country_South","South Sudanese"),
        ("country_Spanish","Spanish"),
        ("country_Sri","Sri Lankan"),
        ("country_Sudanese","Sudanese"),
        ("country_Surinamese","Surinamese"),
        ("country_Swazi","Swazi"),
        ("country_Swedish","Swedish"),
        ("country_Swiss","Swiss"),
        ("country_Syrian","Syrian"),
        ("country_Tahitian","Tahitian"),
        ("country_Taiwanese","Taiwanese"),
        ("country_Tajik","Tajik"),
        ("country_Tanzanian","Tanzanian"),
        ("country_Thai","Thai"),
        ("country_Togolese","Togolese"),
        ("country_Tongan","Tongan"),
        ("country_Trinbagonian","Trinbagonian"),
        ("country_Tunisian","Tunisian"),
        ("country_Turkish","Turkish"),
        ("country_Turkmen","Turkmen"),
        ("country_Turks","Turks And Caicos Islander"),
        ("country_Tuvaluan","Tuvaluan"),
        ("country_Ugandan","Ugandan"),
        ("country_Ukrainian","Ukrainian"),
        ("country_United","United Arab Emirati"),
        ("country_Uruguayan","Uruguayan"),
        ("country_Uzbek","Uzbek"),
        ("country_Vatican","Vatican City"),
        ("country_Venezuelan","Venezuelan"),
        ("country_Vietnamese","Vietnamese"),
        ("country_Vincentian","Vincentian"),
        ("country_Virgin","Virgin Islands (British)"),
        ("country_Virgin","Virgin Islands (US)"),
        ("country_Yemeni","Yemeni"),
        ("country_Yugoslavian","Yugoslavian"),
        ("country_Zambian","Zambian"),
        ("country_Zimbabwean","Zimbabwean"),
    )
    PASSPORT_COUNTRY_CHOICE = (
        ("passportCountry_India","India"),
        ("passportCountry_Afghanistan","Afghanistan"),
        ("passportCountry_Albania","Albania"),
        ("passportCountry_Algeria","Algeria"),
        ("passportCountry_Ambia","Ambia"),
        ("passportCountry_American","American Samoa"),
        ("passportCountry_United","United States Of America"),
        ("passportCountry_Andorra","Andorra"),
        ("passportCountry_Angola","Angola"),
        ("passportCountry_Anguilla","Anguilla"),
        ("passportCountry_Antigua","Antigua And Barbuda"),
        ("passportCountry_Argentina","Argentina"),
        ("passportCountry_Armenia","Armenia"),
        ("passportCountry_Aruba","Aruba"),
        ("passportCountry_Australia","Australia"),
        ("passportCountry_Austria","Austria"),
        ("passportCountry_Azerbaijan","Azerbaijan"),
        ("passportCountry_Bahamas","Bahamas"),
        ("passportCountry_Bahrain","Bahrain"),
        ("passportCountry_Barbados","Barbados"),
        ("passportCountry_Bangladesh","Bangladesh"),
        ("passportCountry_Saint","Saint Barthelemy"),
        ("passportCountry_Belarus","Belarus"),
        ("passportCountry_Belgium","Belgium"),
        ("passportCountry_Belize","Belize"),
        ("passportCountry_Benin","Benin"),
        ("passportCountry_Bermuda","Bermuda"),
        ("passportCountry_Bhutan","Bhutan"),
        ("passportCountry_Guinea","Guinea-Bissau"),
        ("passportCountry_Bolivia","Bolivia"),
        ("passportCountry_Bosnia","Bosnia And Herzegovina"),
        ("passportCountry_Bouvet","Bouvet Island"),
        ("passportCountry_Brazil","Brazil"),
        ("passportCountry_United","United Kingdom"),
        ("passportCountry_Brunei","Brunei"),
        ("passportCountry_Bulgaria","Bulgaria"),
        ("passportCountry_Burkina","Burkina Faso"),
        ("passportCountry_Myanmar","Myanmar"),
        ("passportCountry_Burundi","Burundi"),
        ("passportCountry_Cambodia","Cambodia"),
        ("passportCountry_Cameroon","Cameroon"),
        ("passportCountry_Canada","Canada"),
        ("passportCountry_Canary","Canary Island"),
        ("passportCountry_Cape","Cape Verde"),
        ("passportCountry_Cayman","Cayman Islands"),
        ("passportCountry_Central","Central African Republic"),
        ("passportCountry_Chad","Chad"),
        ("passportCountry_Chile","Chile"),
        ("passportCountry_China","China"),
        ("passportCountry_Colombia","Colombia"),
        ("passportCountry_Comoros","Comoros"),
        ("passportCountry_Democratic","Democratic Republic Of Congo"),
        ("passportCountry_Republic","Republic Of Congo"),
        ("passportCountry_Cook","Cook Islands"),
        ("passportCountry_Costa","Costa Rica"),
        ("passportCountry_Croatia","Croatia"),
        ("passportCountry_Cuba","Cuba"),
        ("passportCountry_Curacao","Curacao"),
        ("passportCountry_Cyprus","Cyprus"),
        ("passportCountry_Czech","Czech Republic"),
        ("passportCountry_Denmark","Denmark"),
        ("passportCountry_Djibouti","Djibouti"),
        ("passportCountry_Dominica","Dominica"),
        ("passportCountry_Dominican","Dominican Republic"),
        ("passportCountry_Netherlands","Netherlands"),
        ("passportCountry_East","East Timor"),
        ("passportCountry_Ecuador","Ecuador"),
        ("passportCountry_Egypt","Egypt"),
        ("passportCountry_El","El Salvador"),
        ("passportCountry_Equatorial","Equatorial Guinea"),
        ("passportCountry_Eritrea","Eritrea"),
        ("passportCountry_Estonia","Estonia"),
        ("passportCountry_Ethiopia","Ethiopia"),
        ("passportCountry_Falkland","Falkland Islands"),
        ("passportCountry_Faroe","Faroe Islands"),
        ("passportCountry_Fiji","Fiji"),
        ("passportCountry_Philippines","Philippines"),
        ("passportCountry_Finland","Finland"),
        ("passportCountry_France","France"),
        ("passportCountry_French","French Guiana"),
        ("passportCountry_Gabon","Gabon"),
        ("passportCountry_Gambia","Gambia"),
        ("passportCountry_Georgia","Georgia"),
        ("passportCountry_Germany","Germany"),
        ("passportCountry_Ghana","Ghana"),
        ("passportCountry_Gibraltar","Gibraltar"),
        ("passportCountry_Greece","Greece"),
        ("passportCountry_Greenland","Greenland"),
        ("passportCountry_Grenada","Grenada"),
        ("passportCountry_Guadeloupe","Guadeloupe"),
        ("passportCountry_Guam","Guam"),
        ("passportCountry_Guatemala","Guatemala"),
        ("passportCountry_Guinea","Guinea"),
        ("passportCountry_Guyana","Guyana"),
        ("passportCountry_Haiti","Haiti"),
        ("passportCountry_Honduras","Honduras"),
        ("passportCountry_Hong","Hong Kong"),
        ("passportCountry_Hungary","Hungary"),
        ("passportCountry_Kiribati","Kiribati"),
        ("passportCountry_Iceland","Iceland"),
        ("passportCountry_Indonesia","Indonesia"),
        ("passportCountry_Iran","Iran"),
        ("passportCountry_Iraq","Iraq"),
        ("passportCountry_Ireland","Ireland"),
        ("passportCountry_Israel","Israel"),
        ("passportCountry_Italy","Italy"),
        ("passportCountry_Cote","Cote Dlvoire"),
        ("passportCountry_Ivory","Ivory Coast"),
        ("passportCountry_Jamaica","Jamaica"),
        ("passportCountry_Japan","Japan"),
        ("passportCountry_Jersey","Jersey"),
        ("passportCountry_Jordan","Jordan"),
        ("passportCountry_Kazakhstan","Kazakhstan"),
        ("passportCountry_Kenya","Kenya"),
        ("passportCountry_Kosova","Kosova"),
        ("passportCountry_Kuwait","Kuwait"),
        ("passportCountry_Kyrgyzstan","Kyrgyzstan"),
        ("passportCountry_Laos","Laos"),
        ("passportCountry_Latvia","Latvia"),
        ("passportCountry_Lebanon","Lebanon"),
        ("passportCountry_Liberia","Liberia"),
        ("passportCountry_Libya","Libya"),
        ("passportCountry_Liechtenstein","Liechtenstein"),
        ("passportCountry_Lithuania","Lithuania"),
        ("passportCountry_Luxembourg","Luxembourg"),
        ("passportCountry_Macau","Macau"),
        ("passportCountry_Republic","Republic of North Macedonia"),
        ("passportCountry_Madagascar","Madagascar"),
        ("passportCountry_Malawi","Malawi"),
        ("passportCountry_Malaysia","Malaysia"),
        ("passportCountry_Maldives","Maldives"),
        ("passportCountry_Mali","Mali"),
        ("passportCountry_Malta","Malta"),
        ("passportCountry_Isle","Isle Of Man"),
        ("passportCountry_Marshall","Marshall Island"),
        ("passportCountry_Martinique","Martinique"),
        ("passportCountry_Mauritania","Mauritania"),
        ("passportCountry_Mauritius","Mauritius"),
        ("passportCountry_Mexico","Mexico"),
        ("passportCountry_Moldova","Moldova"),
        ("passportCountry_Monaco","Monaco"),
        ("passportCountry_Mongolia","Mongolia"),
        ("passportCountry_Montenegro","Montenegro"),
        ("passportCountry_Montserrat","Montserrat"),
        ("passportCountry_Morocco","Morocco"),
        ("passportCountry_Lesotho","Lesotho"),
        ("passportCountry_Botswana","Botswana"),
        ("passportCountry_Mozambique","Mozambique"),
        ("passportCountry_Namibia","Namibia"),
        ("passportCountry_Nauru","Nauru"),
        ("passportCountry_Nepal","Nepal"),
        ("passportCountry_New","New Caledonia"),
        ("passportCountry_New","New Zealand"),
        ("passportCountry_Vanuatu","Vanuatu"),
        ("passportCountry_Nicaragua","Nicaragua"),
        ("passportCountry_Nigeria","Nigeria"),
        ("passportCountry_Niger","Niger"),
        ("passportCountry_Niue","Niue"),
        ("passportCountry_North","North Korea"),
        ("passportCountry_Norway","Norway"),
        ("passportCountry_Oman","Oman"),
        ("passportCountry_Pakistan","Pakistan"),
        ("passportCountry_Palau","Palau"),
        ("passportCountry_Palestinian","Palestinian Territory"),
        ("passportCountry_Panama","Panama"),
        ("passportCountry_Papua","Papua New Guinea"),
        ("passportCountry_Paraguay","Paraguay"),
        ("passportCountry_Peru","Peru"),
        ("passportCountry_Poland","Poland"),
        ("passportCountry_Portugal","Portugal"),
        ("passportCountry_Puerto","Puerto Rico"),
        ("passportCountry_Qatar","Qatar"),
        ("passportCountry_Reunion","Reunion"),
        ("passportCountry_Romania","Romania"),
        ("passportCountry_Russia","Russia"),
        ("passportCountry_Rwanda","Rwanda"),
        ("passportCountry_Saint","Saint Helena"),
        ("passportCountry_Saint","Saint Kitts And Nevis"),
        ("passportCountry_Saint","Saint Lucia"),
        ("passportCountry_Saint","Saint Martin"),
        ("passportCountry_San","San Marino"),
        ("passportCountry_Samoa","Samoa"),
        ("passportCountry_Sao","Sao Tome And Principe"),
        ("passportCountry_Guernsey","Guernsey"),
        ("passportCountry_Saudi","Saudi Arabia"),
        ("passportCountry_Scotland","Scotland"),
        ("passportCountry_Senegal","Senegal"),
        ("passportCountry_Serbia","Serbia"),
        ("passportCountry_Seychelles","Seychelles"),
        ("passportCountry_Sierra","Sierra Leone"),
        ("passportCountry_Singapore","Singapore"),
        ("passportCountry_Slovakia","Slovakia"),
        ("passportCountry_Slovenia","Slovenia"),
        ("passportCountry_Solomon","Solomon Islands"),
        ("passportCountry_Somalia","Somalia"),
        ("passportCountry_South","South Africa"),
        ("passportCountry_South","South Korea"),
        ("passportCountry_South","South Sudan"),
        ("passportCountry_Spain","Spain"),
        ("passportCountry_Sri","Sri Lanka"),
        ("passportCountry_Sudan","Sudan"),
        ("passportCountry_Suriname","Suriname"),
        ("passportCountry_Swaziland","Swaziland"),
        ("passportCountry_Sweden","Sweden"),
        ("passportCountry_Switzerland","Switzerland"),
        ("passportCountry_Syria","Syria"),
        ("passportCountry_Tahiti","Tahiti"),
        ("passportCountry_Taiwan","Taiwan"),
        ("passportCountry_Tajikistan","Tajikistan"),
        ("passportCountry_Tanzania","Tanzania"),
        ("passportCountry_Thailand","Thailand"),
        ("passportCountry_Togo","Togo"),
        ("passportCountry_Tonga","Tonga"),
        ("passportCountry_Trinidad","Trinidad And Tobago"),
        ("passportCountry_Tunisia","Tunisia"),
        ("passportCountry_Turkey","Turkey"),
        ("passportCountry_Turkmenistan","Turkmenistan"),
        ("passportCountry_Turks","Turks And Caicos Island"),
        ("passportCountry_Tuvalu","Tuvalu"),
        ("passportCountry_Uganda","Uganda"),
        ("passportCountry_Ukraine","Ukraine"),
        ("passportCountry_United","United Arab Emirates"),
        ("passportCountry_Uruguay","Uruguay"),
        ("passportCountry_Uzbekistan","Uzbekistan"),
        ("passportCountry_Vatican","Vatican City"),
        ("passportCountry_Venezuela","Venezuela"),
        ("passportCountry_Vietnam","Vietnam"),
        ("passportCountry_Saint","Saint Vincent And The Grenadines"),
        ("passportCountry_Virgin","Virgin Islands (British)"),
        ("passportCountry_Virgin","Virgin Islands (Us)"),
        ("passportCountry_Yemen","Yemen"),
        ("passportCountry_Yugoslavia","Yugoslavia"),
        ("passportCountry_Zambia","Zambia"),
        ("passportCountry_Zimbabwe","Zimbabwe"),
    )    
    cource_type = models.CharField(max_length=150, choices=COURCE_CHOICES_TYPE,blank=True,verbose_name="Select Cource Type")
    cource = models.CharField(max_length=150, choices=COURCE_CHOICES, blank=True,verbose_name="Select Cource")
    # student_I generations
    students_id = models.CharField(max_length=50, verbose_name="Student Id", blank=True)
    # student_I generations
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Middle Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    dob = models.DateField(null=True, verbose_name="Date Of Birth")
    blood_group = models.CharField(blank=True, max_length=50, choices=BLOOD_GROUP_CHOICES, verbose_name="Blood Group")
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True, verbose_name="Gender")
    marital_status = models.CharField(max_length=50, choices=MARITAL_CHOICES, blank=True, verbose_name="Marital Status")
    username = models.CharField(max_length=50, unique=True, verbose_name="Username")
    email = models.EmailField(max_length=100, unique=True, verbose_name="E-mail")
    phone_number = models.CharField(max_length=50, verbose_name="Mobile No", blank=True)
    admission_type = models.CharField(max_length=50, blank=True, verbose_name="Admission Type")
    # additional fields
    parent_email = models.CharField(max_length=100, blank=True, verbose_name="Parent/Guardian Email Address")
    father_name = models.CharField(max_length=100, blank=True, verbose_name="Father’s Name")
    mother_name = models.CharField(max_length=100, blank=True, verbose_name="Mother’s Name")
    parent_contact = models.CharField(max_length=100, blank=True, verbose_name="Parent’s Mobile Number")
    permanent_address = models.TextField(blank=True, verbose_name="Permanent Address")
    city = models.CharField(max_length=150, blank=True, verbose_name="City")
    state=models.CharField(max_length=150, blank=True, verbose_name="State")
    country = models.CharField(max_length=150, choices=PASSPORT_COUNTRY_CHOICE, blank=True, verbose_name="Country (As mentioned in passport)")
    pin_code = models.CharField(blank=True, max_length=6, default=0, verbose_name="Pin Code")
    is_preset_address = models.BooleanField(verbose_name="Is Present address different?", default=False)
    present_address1 = models.TextField(blank=True, verbose_name="Present Address1")
    present_address2 = models.TextField(blank=True, verbose_name="Present Address2")
    present_city = models.CharField(max_length=150, blank=True, verbose_name="Present City")
    present_state=models.CharField(max_length=150, blank=True, verbose_name="Present State")
    present_country = models.CharField(max_length=150, choices=PASSPORT_COUNTRY_CHOICE, blank=True, verbose_name="Present Country")
    present_pincode = models.CharField(blank=True, max_length=6,default=0, verbose_name="Present Pincode")
    nationality = models.CharField(max_length=50, choices=NATIONALITY_CHOICES, blank=True, verbose_name="Nationality")
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICE, blank=True)
    cast = models.CharField(max_length=50, blank=True, verbose_name="Cast Name")
    ssc = models.CharField(max_length=5, blank=True, verbose_name="SSC Percentage/CGPA") # NA
    hsc = models.CharField(max_length=5, blank=True, verbose_name="HSC Percentage/CGPA") # NA
    graduation = models.CharField(max_length=5, blank=True, verbose_name="Graduation Percentage/CGPA") # NA
    degree = models.CharField(max_length=100, choices=DEGREE_CHOICE, blank=True,verbose_name="Graduation Degree")    
    neet = models.BooleanField(verbose_name="NEET", default=False)
    jee = models.BooleanField(verbose_name="JEE", default=False)
    mhcet = models.BooleanField(verbose_name="MH-CET", default=False)
    peracet = models.BooleanField(verbose_name="PERA-CET", default=False)
    other = models.BooleanField(verbose_name="NONE", default=False)    
    gate_cet = models.BooleanField(verbose_name="GATE", default=False)
    gateb_cet = models.BooleanField(verbose_name="GATB", default=False)    
    is_hostel = models.BooleanField(default=False, verbose_name="Do you need a hostel?")
    non_creamy_layer = models.BooleanField(default=False, verbose_name="Non-Creamy Layer")
    minority = models.BooleanField(default=False, verbose_name="Whether Minority")
    ex_serviceman = models.BooleanField(default=False, verbose_name="Are your parent from Ex-serviceman")
    physically = models.BooleanField(default=False, verbose_name="Physically Challenged?")
    kashmiri = models.BooleanField(default=False, verbose_name="Whether Kashmiri Migrant")
    area_of_residence = models.BooleanField(default=False, verbose_name="Area of Residence")
    oms = models.BooleanField(default=False, verbose_name="OMS")
    nri_pio_oci = models.BooleanField(default=False, verbose_name="NRI/PIO/OCI")
    abc_id = models.CharField(blank=True,  max_length=150, verbose_name="ABC ID(Academic Bank of Credit)")

    ## Educational Details ##
    ### 10th ###
    tenth_result_status = models.CharField(blank=True, max_length=25, verbose_name="10th Result Status")
    tenth_school = models.CharField(blank=True, max_length=100, verbose_name="10th School/College Name")
    tenth_board = models.CharField(blank=True, max_length=100, verbose_name="10th Board/University Name")
    tenth_seat = models.CharField(blank=True, max_length=25, verbose_name="10th Exam Seat No")
    tenth_year = models.CharField(blank=True, max_length=10, verbose_name="10th Year of Passing")
    tenth_result_pattern = models.CharField(blank=True, max_length=25, verbose_name="10th Result Pattern")
    tenth_percent = models.CharField(blank=True, max_length=5, verbose_name="10th Percentage/CGPA")
    tenth_math = models.CharField(blank=True, max_length=5, verbose_name="10th Math Marks")
    tenth_sci = models.CharField(blank=True, max_length=5, verbose_name="10th Science Marks")
    tenth_en = models.CharField(blank=True, max_length=5, verbose_name="10th English Marks")

    ### 12th ###
    twelth_result_status = models.CharField(blank=True, max_length=25, verbose_name="12th Result Status")
    twelth_college = models.CharField(blank=True, max_length=100, verbose_name="12th School/College Name")
    twelth_board = models.CharField(blank=True, max_length=100, verbose_name="12th Board/University Name")
    twelth_seat = models.CharField(blank=True, max_length=25, verbose_name="12th Exam Seat No")
    twelth_year = models.CharField(blank=True, max_length=10, verbose_name="12th Year of Passing")
    twelth_result_pattern = models.CharField(blank=True, max_length=25, verbose_name="12th Result Pattern")
    twelth_percent = models.CharField(blank=True, max_length=5, verbose_name="12th Percentage/CGPA")
    twelth_bio = models.CharField(blank=True, max_length=5, verbose_name="12th Biology Marks")
    twelth_math = models.CharField(blank=True, max_length=5, verbose_name="12th Maths Marks")
    twelth_sci = models.CharField(blank=True, max_length=5, verbose_name="12th Science Marks")
    twelth_en = models.CharField(blank=True, max_length=5, verbose_name="12th English Marks")

    ### Graduation ###
    ######## 
    graduate_degree = models.CharField(blank=True, choices=DEGREE_CHOICE, max_length=100, verbose_name="Graduation Degree")
    graduate_result_status = models.CharField(blank=True, max_length=25, verbose_name="Graduation Result Status")
    graduate_college = models.CharField(blank=True, max_length=100, verbose_name="Graduation School/College Name")
    graduate_university = models.CharField(blank=True, max_length=100, verbose_name="Graduation Board/University Name")
    graduate_seat = models.CharField(blank=True, max_length=25, verbose_name="Graduation Exam Seat No")
    graduate_year = models.CharField(blank=True, max_length=10, verbose_name="Graduation Year of Passing")
    graduate_result_pattern = models.CharField(blank=True, max_length=25, verbose_name="Graduation Result Pattern")
    graduate_percent = models.CharField(blank=True, max_length=5, verbose_name="Graduation Percentage/CGPA")

    ## entrance Exam ##
    phy_f = models.CharField(max_length=3, blank=True, verbose_name="Physics")
    chm_f = models.CharField(max_length=3, blank=True, verbose_name="Chemistry")
    bio_f = models.CharField(max_length=3, blank=True, verbose_name="Biology")
    math_f = models.CharField(max_length=3, blank=True, verbose_name="Mathematics")
    perc_f = models.CharField(max_length=3, blank=True, verbose_name="Percentile")
    phy_s = models.CharField(max_length=3, blank=True, verbose_name="Physics")
    chm_s = models.CharField(max_length=3, blank=True, verbose_name="Chemistry")
    bio_s = models.CharField(max_length=3, blank=True, verbose_name="Biology")
    math_s = models.CharField(max_length=3, blank=True, verbose_name="Mathematics")
    perc_s = models.CharField(max_length=3, blank=True, verbose_name="Percentile")
    gate = models.CharField(max_length=3, blank=True, verbose_name="GATE - Percentile")
    gatb = models.CharField(max_length=3, blank=True, verbose_name="GATB - Percentile")
    ## Entrance Exam ##   
    # profile and sign ##
    profile_photo = models.FileField(upload_to="media/student/profile/", blank=True,verbose_name="Profile Photo")
    stud_sign_photo = models.FileField(upload_to="media/student/profile/", blank=True,verbose_name="Student Sign")
    stud_profile_sign = models.FileField(upload_to="media/student/profile/", blank=True,verbose_name="Student Sign")
    ## profile and sign ##
    ## Documents Upload ##
    tenth_marksheet = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="10th Marksheet")
    twelth_marksheet = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="12th Marksheet")
    grd_marksheet = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="Graduation Marksheet")
    lc = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="College Leaving Certificate")
    dob_cert = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="Domicile/Nationality/Birth Certificate")
    cast_cert = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="Caste Certificate (if applicable)")
    nonc_cert = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="Non-Creamy Layer Certificate ")
    caste_validity = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="Caste Validity Certificate (if applicable)")
    defence_cert = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="Certificate of Defense Personnel")
    migration = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="Migrant/Displaced Students Form")
    jammu_kashmir_cert = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="Jammu and Kashmir State")
    jee_score_cert = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="JEE Score Card")
    neet_score_cert = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="NEET Score Card")
    mhcet_cert = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="MHT-CET Score Card")
    gap_cert = models.FileField(upload_to="media/student/document/", blank=True,verbose_name="Gap Certificate")
    ## Payment ##
    amount = models.CharField(max_length=250, blank=True, default="1800.00",verbose_name="Fees(rs)")
    txnreferenceno = models.CharField(max_length=250, blank=True, verbose_name="Transaction Reference No")
    bankreferenceno = models.CharField(max_length=250, blank=True, verbose_name="Bank Reference No")
    bankid = models.CharField(max_length=250, blank=True, verbose_name="Bank ID")
    bankmerchantid = models.CharField(max_length=250, blank=True, verbose_name="Bank Merchant ID")
    currencyname = models.CharField(max_length=250, blank=True, verbose_name="Currency Name")
    itemcode = models.CharField(max_length=250, blank=True, verbose_name="Item Code")
    paymentstatus = models.CharField(max_length=50, blank=True, verbose_name="Payment Status")
    payment_request = models.TextField(max_length=500, verbose_name="Payment Request String", blank=True)
    payment_response = models.TextField(max_length=500, verbose_name="Payment Response String",blank=True)
    ## Payment ##
    ## Form Section ##
    personal_frm = models.BooleanField(default=False, verbose_name="Personal Details")
    education_frm = models.BooleanField(default=False, verbose_name="Education Details")
    payment_frm = models.BooleanField(default=False, verbose_name="Payment Details")
    ## Form Section ##
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'dob', 'marital_status','middle_name', 'phone_number', 'admission_type']
    objects = MyAccountManager()
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, add_label):
        return True
    def save(self, *args, **kwargs):        
        self.updated_at = timezone.now()        
        # student_I generations
        max_id = Account.objects.aggregate(max_id=Max('id'))['max_id']                
        current_year = str(timezone.now().year)
        if max_id is not None:
            max_id_new = max_id+1
            # print( max_id)
            if not self.students_id :
                self.students_id = f"{current_year}mitbio{max_id_new}"
        # student_I generations
        super().save(*args, **kwargs)        
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Students"

