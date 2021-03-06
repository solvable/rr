
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, get_object_or_404, redirect, Http404
from .models import *
from .forms import *
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


@login_required(login_url='customers:login')
def get_user_profile(request):
    user = request.user
    username = user.username
    email = user.email
    first_name = user.first_name
    last_name = user.last_name
    password = user.password
    context = {
        "username":username,
        "email":email,
        "first_name":first_name,
        "last_name":last_name,
        "password":password,
    }

    return render(request, "user.html", context)



@login_required(login_url='customers:login')
def index(request):
    #Weather content
    import pyowm
    API_KEY = '0661037c3beedfccf03d405e5ed322e4'
    LOCATION_ID = 5205788
    owm=pyowm.OWM(API_KEY)
    observation = owm.weather_at_id(LOCATION_ID)
    w = observation.get_weather()
    status = w.get_detailed_status()
    weather_icon = w.get_weather_icon_name()
    icon = "http://openweathermap.org/img/w/"+weather_icon+".png"
    temp = w.get_temperature('fahrenheit')
    temp_max = temp["temp_max"]
    temp_min = temp["temp_min"]
    wind = w.get_wind()
    wind_speed = wind["speed"]
    fc = owm.daily_forecast_at_id(LOCATION_ID, limit=5)
    f = fc.get_forecast()
    lst = f.get_weathers()
    #End weather content

    #User assignments
    my_open = Appointment.objects.all().filter(assigned_to =request.user.first_name)




    context = {
        "title":"Home",
        "status": status,
        "icon":icon,
        "wind_speed":wind_speed,
        "temp_max":temp_max,
        "temp_min":temp_min,
        "f":f,
        "lst":lst,
        "my_open":my_open,


    }
    return render(request, "index.html", context)

@login_required(login_url='customers:login')
def calendar(request):
    import calendar
    apps = Appointment.objects.all()
    d = datetime.datetime.today()
    day = d.day
    month =d.month
    year =d.year
    c=calendar.HTMLCalendar(firstweekday=0)
    a = str(c.formatmonth(year,month))
    apptend = ""

    for i in apps:
        apptend = apptend + i.appt +","
        print apptend

    unscheduled = Appointment.objects.all().filter(unscheduled=True).order_by('created')



    context = {
        "calendar":a,
        "unscheduled": unscheduled,
        "apps":apptend,
    }

    return render(request, "calendar.html", context)


@login_required(login_url='customers:login')
def recents(request):
    """
    View for customer list
    :param request:
    :return: list of all customer objects rendered on 'customer_list.html'
    """

    yesterday = datetime.datetime.today()-datetime.timedelta(days=1)

    queryset_list = Customer.objects.all().filter(created__gt=yesterday)

    paginator = Paginator(queryset_list, 25) # show 25 customers per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        queryset = paginator.page(paginator.num_pages)

    # Set context variables
    context = {
            "title":"Customer Browse",
            "object_list": queryset,
            "page_request_var":page_request_var,
        }
    return render(request, "customer_list.html", context)


@login_required(login_url='customers:login')
def customer_browse(request):
    """
    View for customer list
    :param request:
    :return: list of all customer objects rendered on 'customer_list.html'
    """
    queryset_list = Customer.objects.all().order_by('lastName', 'firstName')
    paginator = Paginator(queryset_list, 25) # show 25 customers per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        queryset = paginator.page(paginator.num_pages)

    # Set context variables
    context = {
            "title":"Recent Customers",
            "object_list": queryset,
            "page_request_var":page_request_var,
        }
    return render(request, "customer_list.html", context)

@login_required(login_url='customers:login')
def open_workorders(request):

    queryset_list = Appointment.objects.all().filter(completed=False).order_by('created')

    paginator = Paginator(queryset_list, 25) # show 25 customers per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    ests = queryset_list.filter(title="Estimate")
    servs = queryset_list.filter(title="Service")
    insp = queryset_list.filter(title="Inspection")

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        queryset = paginator.page(paginator.num_pages)


    # Set context variables
    context = {
        "openlead": "Lead",
        "openserv": "Service",
        "openinsp": "Inspection",
        "ests":ests,
        "servs":servs,
        "insp":insp,
        "object_list": queryset,
        #"customers":customers,
        "page_request_var": page_request_var,
    }
    return render(request, "open_workorders.html", context)

@login_required(login_url='customers:login')
def customer_create(request):
    '''
    View to create a Customer object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404


    # Load Customer Form
    form = CustomerForm(request.POST or None)
    # Check if form is valid
    if form.is_valid():
        # Save instance
        instance = form.save(commit=False)
        instance.user = request.user
        instance.modified_by = str(request.user)
        instance.save()
        # Message success
        messages.success(request, "Successfully Created")
        # Redirect to detail view
        return HttpResponseRedirect(instance.get_absolute_url())

    # Set context variables
    context = {
        "form":form,
    }
    return render(request, "customer_form.html", context)

@login_required(login_url='customers:login')
def customer_detail(request, id):
    '''
    View for Customer object details including address info and jobsites
    '''
    # set global variables
    instance=get_object_or_404(Customer,id=id)
    queryset_list = instance.jobsite_set.all()
    paginator = Paginator(queryset_list, 15) # show 15 customers per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer deliver first page
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        queryset = paginator.page(paginator.num_pages)

    # Set context variables
    context ={
            "title":"Customer Info:",
            "instance":instance,
            "lat":instance.lat,
            "lng":instance.lng,
            "jobsite":queryset,
            "page_request_var": page_request_var,

    }

    return render(request, "customer_detail.html", context)

@login_required(login_url='customers:login')
def customer_update(request, id=None):
    '''
    View for updating customer object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404


    instance=get_object_or_404(Customer,id=id)
    # Load Customer Form
    form = CustomerForm(request.POST or None, instance=instance)
    # Check if form is valid
    if form.is_valid():
        # Save instance
        instance = form.save(commit=False)
        instance.modified_by=str(request.user)
        instance.save()
        # Message success
        messages.success(request, "Successfully Updated")
        # Redirect to detail view
        return HttpResponseRedirect(instance.get_absolute_url())


    context ={
        "title":"Customer Info:",
        "instance":instance,
        "form":form
        }
    return render(request, "customer_form.html", context)

@login_required(login_url='customers:login')
def customer_delete(request, id=None):
    """
    View for Deleting a Customer object
    :param request:
    :param id:
    :return:
    """

    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404


    instance=get_object_or_404(Customer,id=id)
    instance.delete()
    # Message success
    messages.success(request, "Successfully Deleted")
    return redirect("customers:index")


#################### JOBSITE VIEWS ###################

@login_required(login_url='customers:login')
def jobsite_create(request, id=None):
    '''
    View for creating a work order Object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404


    # Load data from customer
    instance=get_object_or_404(Customer,id=id)

    # Load Work Order Form
    form = JobsiteForm(request.POST or None, request.FILES or None)
    form.fields["customer_id"].initial= instance.id
    form.fields["customer_id"].disabled=True


    form.fields["latlng"].disabled=True
    form.fields["lat"].disabled=True
    form.fields["lng"].disabled=True

    form.fields["latlng"].widget = forms.HiddenInput()
    form.fields["lat"].widget =  forms.HiddenInput()
    form.fields["lng"].widget =  forms.HiddenInput()
    form.fields["customer_id"].widget =  forms.HiddenInput()

    # Check if form is valid
    if form.is_valid():
        # Save instance
        form = form.save(commit=False)
        form.user = request.user

        form.modified_by = str(request.user)
        form.save()
        # Message success
        messages.success(request, "Successfully Created")
        # Redirect to detail view
        return HttpResponseRedirect(instance.get_absolute_url())

    # Set context variables
    context={
        "form":form,
        "instance":instance,
    }
    return render(request, "jobsite_form.html", context)

@login_required(login_url='customers:login')
def jobsite_detail(request, id, jobId):
    '''
    View for Customer object details including address info and jobsite
    '''

    # set global variables
    instance = Customer.objects.get(id=id)
    jobsite=get_object_or_404(Jobsite,jobId=jobId)




    if jobsite.appointment_set.exists():
        appointment = (Appointment.objects.all().filter(jobsite_id = jobsite.jobId))
    else:
        appointment = "None Scheduled"

    # Set context variables
    context ={
            "jobsite_title":"Jobsite Info:",
            "instance":instance,
            "lat":instance.lat,
            "lng":instance.lng,
            "jobsite":jobsite,
            "appointment":appointment,
            }

    return render(request, "jobsite_detail.html", context)

@login_required(login_url='customers:login')
def jobsite_update(request, id=None, jobId=None):

    '''
    View for updating jobsite object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404

    instance = get_object_or_404(Jobsite, customer_id=id, jobId=jobId)

    # Load jobsite Form
    form = JobsiteForm(request.POST or None, request.FILES or None, instance=instance)
    # Check if form is valid
    if form.is_valid():
        # Save instance
        form = form.save(commit=False)
        form.modified_by = str(request.user)
        form.save()
        # Message success
        messages.success(request, "Successfully Updated")
        # Redirect to detail view
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Jobsite Info:",
        "instance": instance,
        "form": form
    }
    return render(request, "jobsite_form.html", context)


@login_required(login_url='customers:login')
def jobsite_delete(request, id=None, jobId=None):
    """
     View for Deleting a jobsite Object
    :param request: httpRequest
    :param id: Customer.id
    :param jobId: jobsite.jobId
    :return:
    """
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404

    customer = Customer.objects.get(id = id)
    instance=get_object_or_404(Jobsite, customer_id=id, jobId=jobId)
    instance.delete()
    # Message success
    messages.success(request, "Successfully Deleted")
    return HttpResponseRedirect(customer.get_absolute_url())

@login_required(login_url='customers:login')
def confirm_delete(request):
    jobsite_delete(request, id=None, jobId=None)


    ###############################################

@login_required(login_url='customers:login')
def appointment_create(request, id=None, jobId=None):
    '''
    View for creating a work order Object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404

    # Load data from Jobsite
    instance = get_object_or_404(Customer, id=id)
    jobsite = Jobsite.objects.get(jobId=jobId)


    # Load Appointment Form
    form = AppointmentForm(request.POST or None, request.FILES or None)
    form.fields["jobsite_id"].initial = jobId
    form.fields["jobsite_id"].disabled = True
    form.fields["title"].label = "Call Type"
    form.fields["customer_id"].initial =id
    form.fields["customer_id"].disabled=True


    # Check if form is valid
    if form.is_valid():
        # Save instance
        form = form.save(commit=False)
        form.user = request.user
        form.modified_by = str(request.user)
        form.save()

        # Message success
        messages.success(request, "Successfully Created")
        # Redirect to detail view

        return HttpResponseRedirect(jobsite.get_absolute_url())

    # Set context variables
    context = {
        "form": form,
        "instance": instance,
    }
    return render(request, "appointment_form.html", context)


@login_required(login_url='customers:login')
def appointment_detail(request, id, jobId, appId):
    '''
    View for Appointment object details including address info and jobsite
    '''

    # set global variables
    instance = Customer.objects.get(id=id)
    jobsite = Jobsite.objects.get(jobId=jobId)
    appointment=get_object_or_404(Appointment,appId=appId)


    # Set context variables
    context = {
        "appointment":appointment,
        "appointment_title": "Appointment Info:",
        "instance": instance,
        "jobsite": jobsite,
        "appointment":appointment,

    }

    return render(request, "appointment_detail.html", context)


@login_required(login_url='customers:login')
def appointment_update(request, id=None, jobId=None, appId=None):

    '''
    View for updating appointment object
    '''
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    instance = get_object_or_404(Appointment, appId=appId)
    jobId = jobId
    id = str(id)

    # Load appointment Form
    form = AppointmentForm(request.POST or None, request.FILES or None, instance=instance)
    # Check if form is valid
    if form.is_valid():
        # Save instance
        instance = form.save(commit=False)
        instance.modified_by = str(request.user)
        instance.save()
        # Message success
        messages.success(request, "Successfully Updated")
        # Redirect to detail view
        id = str(id)
        jobId = str(jobId)
        appId = str(appId)
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "Appointment Info:",
        "instance": instance,
        "form": form
    }
    return render(request, "appointment_form.html", context)

@login_required(login_url='customers:login')
def appointment_delete(request, id=None, jobId=None, appId = None):
    """
     View for Deleting a jobsite Object
    :param request: httpRequest
    :param id: Customer.id
    :param jobId: wordorder.jobId
    :return:
    """
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    instance = get_object_or_404(Customer, id=id)
    jobsite = Jobsite.objects.get(jobId=jobId)
    appointment = Appointment.objects.get(appId=appId)

    appointment.delete()
    # Message success
    messages.success(request, "Successfully Deleted")
    return HttpResponseRedirect(jobsite.get_absolute_url())

@login_required(login_url='customers:login')
def confirm_delete(request):
    appointment_delete(request, id=None, jobId=None, appId=None)