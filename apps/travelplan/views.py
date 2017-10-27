from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

def index(request):
    return render(request, 'travelplan/index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_registration(request.POST)
        if len(errors) > 0:
            for error in errors.itervalues():
                messages.error(request, error)
            return redirect('/')
        else:
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_password)
            messages.error(request, "Successfully Registered")
            return redirect('/travelplan/travels')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for some in result:
            messages.error(request, some)
        return redirect('/')
    else:
        request.session['id'] = result.id
        messages.success(request, 'You have logged in!')
        return redirect('/travelplan/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def travels(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['id']),
        'owntrips' : Trip.objects.filter(tripjoiners=User.objects.get(id=request.session['id'])),
        'othertrips' : Trip.objects.exclude(tripjoiners=User.objects.get(id=request.session['id']))
    }
    return render(request, 'travelplan/travels.html', context)

def travelsadd(request):
    return render(request, 'travelplan/add.html')

def destination(request, trip_id):
    context = {
        'trip' : Trip.objects.get(id=trip_id),
        'tripjoiners' : User.objects.filter(tripsgoingto__id=trip_id).exclude(tripcreated__id=trip_id),
    }
    return render(request, 'travelplan/destination.html', context)

def home(request):
    return redirect('/travelplan/travels')

def addtrip(request):
    result = Trip.objects.validate_trip(request.POST)
    if len(result) > 0:
        for some in result:
            messages.error(request, some)
        return redirect('/travelplan/travels/add')
    Trip.objects.create(
        destination=request.POST['destination'],
        description=request.POST['description'],
        traveldatefrom=request.POST['traveldatefrom'],
        traveldateto=request.POST['traveldateto'],
        tripcreater=User.objects.get(id=request.session['id'])
        )
    Trip.objects.get(
        destination=request.POST['destination'], 
        description=request.POST['description'], 
        traveldatefrom=request.POST['traveldatefrom'],
        traveldateto=request.POST['traveldateto'],
        tripcreater=User.objects.get(id=request.session['id'])
        ).tripjoiners.add(User.objects.get(id=request.session['id']))
    return redirect('/travelplan/travels')

def jointrip(request, trip_id):
    Trip.objects.get(id=trip_id).tripjoiners.add(User.objects.get(id=request.session['id']))
    return redirect('/travelplan/travels')
