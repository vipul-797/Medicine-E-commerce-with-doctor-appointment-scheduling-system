from django.shortcuts import render, redirect
from .forms import ProfileForm, createUserForm
from .models import Appointment, Profile
from random import choice
from string import ascii_letters
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import numpy as np
import joblib

# Create your views here.
def index(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("phone")

        appointment = Appointment(first_name=first_name, last_name=last_name, email=email, mobile=mobile)
        appointment.save()
        return redirect("/")

    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        username = User.objects.filter(email=email).first()
        if username:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                #login(request, user)
                return redirect("/")
            else:
                messages.error(request,"Incorrect password! Try again.")
                return redirect("/login")

        else:
            messages.error(request,"Email Id doesn\'t exist, Please Register")
            return redirect("/sign-up")


        #return render(request, "login.html")

    return render(request, "login.html")


def sign_up(request):
    user = createUserForm()
    form = ProfileForm()
    if request.method == 'POST':
        user = createUserForm(request.POST)
        form = ProfileForm(request.POST)

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        user = User.objects.filter(email=email).exists()

        username = ''.join([choice(ascii_letters) for i in range(30)])

        if password1 != password2:
            messages.error(request, "Both Password are different")
            return redirect("/sign-up")
        
        elif user:
            messages.error(request, "User with this email id already exists.")
            return redirect("/sign-up")

        else:
            new_user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
            new_user.save()
            
            form = Profile(user=new_user, gender=gender, mobile=mobile, age=age)
            form.save()

            username = User.objects.get(email=email)
            user = authenticate(username=username, password=password1)
            if user is not None:
                auth.login(request, user)
            

        return redirect("/")

    else:
        form = ProfileForm()
        user = createUserForm()

    context = {'form':form, 'user_form': user}
    return render(request, "signup.html", context)


def logout(request):
    logout(request)


def disease_pred(request):
    symp = ['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain','stomach_pain','acidity','ulcers_on_tongue',\
        'muscle_wasting','vomiting','burning_micturition','spotting_ urination','fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings',\
        'weight_loss','restlessness','lethargy','patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',\
        'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes','back_pain','constipation',\
        'abdominal_pain','diarrhoea','mild_fever','yellow_urine','yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach','swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation','redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs','fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool','irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs','swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails','swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips','slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints','movement_stiffness','spinning_movements','loss_of_balance','unsteadiness','weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine','continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)','depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain','abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum','rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion','receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen','history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf','palpitations','painful_walking','pus_filled_pimples','blackheads',\
        'scurring','skin_peeling','silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose','yellow_crust_ooze'
    ]
    model = joblib.load('./models/random_forest.pkl')
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        symptoms = request.POST.getlist('symp')

        list_c = [] #empty list to store symptoms in 0' and 1's
        for x in range (0,len(symp)):
            list_c.append(0)

        for z in range (0,len(symp)):
            for k in symptoms:
                if(k==symp[z]):
                    list_c[z]=1

        test = np.array(list_c)
        test = np.array(test).reshape(1,-1)

        prediction = model.predict(test)
        print(prediction[0])
        messages.success(request, "You might have {}".format(prediction[0]))
        return redirect('disease_pred')


    return render(request, "disease_pred.html", context={"symp": symp})

def drug_pred(request):
    model = joblib.load('./models/medical_nb.pkl')
    diseases = ['Acne', 'Allergy', 'Diabetes', 'Fungal infection',
       'Urinary tract infection', 'Malaria', 'Migraine', 'Hepatitis B',
       'AIDS']

    disease_dict = {'Acne':0, 'Allergy':1, 'Diabetes':2, 'Fungal infection':3,
        'Urinary tract infection':4, 'Malaria':5, 'Migraine':6, 'Hepatitis B':7,
        'AIDS':8}
        
    gender_dict = {
        'Male':1,
        'Female':0,
    }

    if request.method == "POST":
        gender = request.POST["gender"]
        age = request.POST["age"]
        disease = request.POST["disease"]
        gen = gender_dict[gender]
        dis = disease_dict[disease]
        age = int(age)
    
        test = [dis, gen, age]
        test = np.array(test)#List to numpy Array
        test = np.array(test).reshape(1,-1)# Convert 1d to 2d array 

        prediction = model.predict(test)
        messages.success(request, "Predicted Drug: {}".format(prediction[0]))
        return redirect('drug_pred')
    
    return render(request, "drug_pred.html", context={"diseases": diseases})