from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import ast
from django.utils import timezone
from datetime import datetime
from urllib.parse import unquote
from urllib.parse import quote
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
#
from django.utils.timezone import make_naive


def movie_list(request):
    search_query=request.GET.get('search')
    if search_query:
        movies=Movie.objects.filter(name__icontains=search_query)
    else:
        movies=Movie.objects.all()
    return render(request,'movies/movie_list.html',{'movies':movies})

def theater_list(request,name):
    movie = get_object_or_404(Movie,name=name)
    theater=Theater.objects.filter(movie=movie)
    print("theater",theater)
    for i in theater:
        if isinstance(i.time, datetime):
        # Convert to 'YYYY-MM-DD-HH:MM:SS+TZ' format
            formatted_timestamp = i.time.strftime('%Y-%m-%d-%H:%M:%S%z')
        else:
        # If i.time is a string, parse it into a datetime object
            timestamp = datetime.strptime(i.time, '%Y-%m-%d %H:%M:%S%z')
            formatted_timestamp = timestamp.strftime('%Y-%m-%d-%H:%M:%S%z')

        i.time = formatted_timestamp  
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theater})



@login_required(login_url='/login/')
def book_seats(request,theater_id,time):
    timestamp = datetime.strptime(time, '%Y-%m-%d-%H:%M:%S%z')
    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S%z')
    theaters=get_object_or_404(Theater,name=theater_id,time=formatted_timestamp)
    print("theaters",theaters)
    seats=Seat.objects.filter(theater=theaters)
    print("seats",seats)
    if request.method=='POST':
        selected_Seats= request.POST.getlist('seats')
        with transaction.atomic():
            error_seats=[]
            if not selected_Seats:
                return render(request,"movies/seat_selection.html",{'theater':theaters,"seats":seats,'error':"No seat selected"})
            for seat_id in selected_Seats:
                print(seat_id)
                seat=get_object_or_404(Seat,id=seat_id,theater=theaters)
                if seat.is_booked or seat.payment:
                    error_seats.append(seat.seat_number)
                    continue
                try:
                # Booking.objects.create(
                #     user=request.user,
                #     seat=seat,
                #     movie=theaters.movie,
                #     theater=theaters
                # )
                    seat.is_booked=True
                    seat.payment=False
                    seat.save()
                except IntegrityError:
                    error_seats.append(seat.seat_number)
        if error_seats:
            #error_message=f"The following seats are already booked:{',',join(error_seats)}"
            return render(request,'movies/seat_selection.html',{'theater':theaters,"seats":seats,'error':"No seat selected"})
        seatss=""
        for i in selected_Seats:
            seatss=seatss+i+"-"
            print("i",i,"type i",type(i),"seatss",seatss)
        return redirect('payment_method', theater_id=theater_id, time=time, seat_no=seatss)

    return render(request,'movies/seat_selection.html',{'theaters':theaters,"seats":seats})







import json

from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
import json

@login_required(login_url='/login/')
def payment_method(request, theater_id, time, seat_no):
    from datetime import datetime, timedelta
    from django.utils import timezone
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    import json

    seat_no = seat_no.split("-")
    seat_no = [item for item in seat_no if item != '']  # Remove empty strings
    int_list = [int(item) for item in seat_no if item.isdigit()]  # Convert to integers

    try:
        timestamp = datetime.strptime(time, '%Y-%m-%d-%H:%M:%S%z')
    except ValueError:
        messages.error(request, 'Invalid time format.')
        return redirect('movies:seat_selection')

    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S%z')
    time_obj = datetime.strptime(time, '%Y-%m-%d-%H:%M:%S%z')
    countdown_end = timezone.now() + timedelta(minutes=5)

    if request.method == 'POST':
        theaters = get_object_or_404(Theater, name=theater_id, time=time_obj)
        seats = Seat.objects.filter(theater=theaters)

        if 'cancel' in request.POST:
            print("cancel",seat_no)
            for seat_id in int_list:
                seat = get_object_or_404(Seat, id=seat_id, theater=theaters)
                seat.is_booked = False
                seat.payment = False
                seat.save()

                #Booking.objects.filter(theater=theaters, seat=seat).delete()

            messages.info(request, 'Payment cancelled.')
            return render(request, "movies/seat_selection.html", {'theater': theaters, "seats": seats, 'error': "No seat selected"})

        elif 'pay' in request.POST:
            for seat_id in int_list:
                seat = get_object_or_404(Seat, id=seat_id, theater=theaters)
                seat.is_booked = True
                seat.payment = True
                seat.save()
                Booking.objects.create(
                     user=request.user,
                     seat=seat,
                     movie=theaters.movie,
                     theater=theaters,
                     booked_at=timezone.now()
                 )

           # Booking.objects.filter(user=request.user, theater=theaters, seat__id__in=int_list).update()

            messages.success(request, 'Payment successful!')
            return redirect('profile')

    return render(request, 'movies/payment_method.html', {
        'countdown_end': countdown_end,
        'theater_id': theater_id,
        'time': time,
        'seat_no': seat_no
    })



@login_required(login_url='/login/')    
def cancel(request,theater_id,time,seat_no):
    print("cancel function")
    time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S%z')
    print("cancel",seat_no)
    list_of_strings = ast.literal_eval(seat_no)
    int_list = [int(item) for item in list_of_strings]
    theaters=get_object_or_404(Theater,name=theater_id,time=time_obj)
    print("theaters",theaters)
    seats=Seat.objects.filter(theater=theaters)
    for seat_id in int_list:
        seat=get_object_or_404(Seat,id=seat_id,theater=theaters)
        seat.is_booked=False
        seat.payment=False
        seat.save()
                # Example: Deleting seats that are booked in a particular theater
        #Booking.objects.filter(theater=theaters, seat=seat).delete()

    messages.info(request, 'Payment cancelled.')
    return render(request,"movies/seat_selection.html",{'theater':theaters,"seats":seats,'error':"No seat selected"})  # Replace 'previous_page' with your actual previous page URL name
@login_required(login_url='/login/')    
def conform(request,theater_id,time):
    print("pay")







def unique_theater_movies(request):
    # Fetch all theaters and group data
    theaters = Theater.objects.all()

    # Prepare a dictionary to organize theaters, movies, and timings
    theater_data = {}

    for theater in theaters:
        if theater.name not in theater_data:
            # Initialize theater entry with an empty movie dictionary
            theater_data[theater.name] = {
                'image': theater.movie.image.url if theater.movie.image else None,
                'movies': {},  # Movies dictionary for this theater
                'rowspan': 0  # Initialize rowspan for this theater
            }

        if theater.movie.name not in theater_data[theater.name]['movies']:
            # Initialize movie entry with an empty list of timings
            theater_data[theater.name]['movies'][theater.movie.name] = []

        # Add unique show timings
        if theater.time not in theater_data[theater.name]['movies'][theater.movie.name]:
            theater_data[theater.name]['movies'][theater.movie.name].append(theater.time)

        # Increment the rowspan for this theater based on the number of movies
        theater_data[theater.name]['rowspan'] = len(theater_data[theater.name]['movies'])

    return render(request, 'movies/all_theaters.html', {'theater_data': theater_data})

"""

from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import ast
from django.utils import timezone
from datetime import datetime
from urllib.parse import unquote, quote
from django.db import transaction
from django.contrib import messages

def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movies = Movie.objects.filter(name__icontains=search_query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def theater_list(request, name):
    movie = get_object_or_404(Movie, name=name)
    theaters = Theater.objects.filter(movie=movie)
    print("theater", theaters)
    for theater in theaters:
        if isinstance(theater.time, str):
            try:
                theater.time = datetime.strptime(theater.time, '%Y-%m-%d %H:%M:%S%z')
            except ValueError:
                theater.time = datetime.strptime(theater.time, '%Y-%m-%d %H:%M:%S')

        if timezone.is_naive(theater.time):
            theater.time = timezone.make_aware(theater.time)

        local_time = timezone.localtime(theater.time)
        theater.time = local_time.strftime('%d/%m/%Y %H:%M:%S')

    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})

@login_required(login_url='/login/')
def book_seats(request, theater_id, time):
    timestamp = datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
    theaters = get_object_or_404(Theater, name=theater_id, time=timestamp)
    print("theaters", theaters)
    seats = Seat.objects.filter(theater=theaters)
    print("seats", seats)
    if request.method == 'POST':
        selected_Seats = request.POST.getlist('seats')
        with transaction.atomic():
            error_seats = []
            if not selected_Seats:
                return render(request, "movies/seat_selection.html", {'theater': theaters, "seats": seats, 'error': "No seat selected"})
            for seat_id in selected_Seats:
                print(seat_id)
                seat = get_object_or_404(Seat, id=seat_id, theater=theaters)
                if seat.is_booked or seat.payment:
                    error_seats.append(seat.seat_number)
                    continue
                try:
                    seat.is_booked = True
                    seat.payment = False
                    seat.save()
                except IntegrityError:
                    error_seats.append(seat.seat_number)
        if error_seats:
            return render(request, 'movies/seat_selection.html', {'theater': theaters, "seats": seats, 'error': "No seat selected"})
        seatss = ""
        for i in selected_Seats:
            seatss = seatss + i + "-"
            print("i", i, "type i", type(i), "seatss", seatss)
        return redirect('payment_method', theater_id=theater_id, time=time, seat_no=seatss)

    return render(request, 'movies/seat_selection.html', {'theaters': theaters, "seats": seats})

@login_required(login_url='/login/')
def payment_method(request, theater_id, time, seat_no):
    seat_no = seat_no.split("-")
    seat_no = [item for item in seat_no if item != '']  # Remove empty strings
    int_list = [int(item) for item in seat_no if item.isdigit()]  # Convert to integers

    try:
        timestamp = datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
    except ValueError:
        messages.error(request, 'Invalid time format.')
        return redirect('movies:seat_selection')

    countdown_end = timezone.now() + timedelta(minutes=5)

    if request.method == 'POST':
        theaters = get_object_or_404(Theater, name=theater_id, time=timestamp)
        seats = Seat.objects.filter(theater=theaters)

        if 'cancel' in request.POST:
            print("cancel", seat_no)
            for seat_id in int_list:
                seat = get_object_or_404(Seat, id=seat_id, theater=theaters)
                seat.is_booked = False
                seat.payment = False
                seat.save()

            messages.info(request, 'Payment cancelled.')
            return render(request, "movies/seat_selection.html", {'theater': theaters, "seats": seats, 'error': "No seat selected"})

        elif 'pay' in request.POST:
            for seat_id in int_list:
                seat = get_object_or_404(Seat, id=seat_id, theater=theaters)
                seat.is_booked = True
                seat.payment = True
                seat.save()
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters,
                    booked_at=timezone.now()
                )

            messages.success(request, 'Payment successful!')
            return redirect('profile')

    return render(request, 'movies/payment_method.html', {
        'countdown_end': countdown_end,
        'theater_id': theater_id,
        'time': time,
        'seat_no': seat_no
    })

@login_required(login_url='/login/')
def cancel(request, theater_id, time, seat_no):
    print("cancel function")
    time_obj = datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
    print("cancel", seat_no)
    list_of_strings = ast.literal_eval(seat_no)
    int_list = [int(item) for item in list_of_strings]
    theaters = get_object_or_404(Theater, name=theater_id, time=time_obj)
    print("theaters", theaters)
    seats = Seat.objects.filter(theater=theaters)
    for seat_id in int_list:
        seat = get_object_or_404(Seat, id=seat_id, theater=theaters)
        seat.is_booked = False
        seat.payment = False
        seat.save()

    messages.info(request, 'Payment cancelled.')
    return render(request, "movies/seat_selection.html", {'theater': theaters, "seats": seats, 'error': "No seat selected"}) 

@login_required(login_url='/login/')
def conform(request, theater_id, time):
    print("pay")

def unique_theater_movies(request):
    theaters = Theater.objects.all()
    theater_data = {}

    for theater in theaters:
        if theater.name not in theater_data:
            theater_data[theater.name] = {
                'image': theater.movie.image.url if theater.movie.image else None,
                'movies': {},
                'rowspan': 0
            }

        if theater.movie.name not in theater_data[theater.name]['movies']:
            theater_data[theater.name]['movies'][theater.movie.name] = []

        if theater.time not in theater_data[theater.name]['movies'][theater.movie.name]:
            theater_data[theater.name]['movies'][theater.movie.name].append(theater.time)

        theater_data[theater.name]['rowspan'] = len(theater_data[theater.name]['movies'])

    return render(request, 'movies/all_theaters.html', {'theater_data': theater_data})
    """
