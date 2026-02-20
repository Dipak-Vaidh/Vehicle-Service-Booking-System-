from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm

from .forms import BookingForm
from .models import Booking , CarModel
from django.http import JsonResponse


from django.shortcuts import get_object_or_404

from django.views.decorators.http import require_POST

from django.template.loader import render_to_string

# pagination
from django.core.paginator import Paginator



# ---------------------------
# Signup View
# ---------------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, 'bookings/signup.html', {'form': form})


# ---------------------------
# Login View
# ---------------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'bookings/login.html', {'form': form})


# ---------------------------
# Dashboard View
# ---------------------------

# ============ >>>> 1.
# @login_required
# def dashboard_view(request):
#     return render(request, 'bookings/dashboard.html')

# =========== >>>> 2. 
# @login_required
# def dashboard_view(request):
#     form = BookingForm()

#     bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

#     return render(request, 'bookings/dashboard.html', {
#         'form': form,
#         'bookings': bookings
#     })

# ==================== >>> 3.
# @login_required
# def dashboard_view(request):

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user   # link booking to logged in user
#             booking.save()
#             return redirect('dashboard')
#     else:
#         form = BookingForm()

#     bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

#     return render(request, 'bookings/dashboard.html', {
#         'form': form,
#         'bookings': bookings
#     })

# with ajax
from django.core.paginator import Paginator

@login_required
def dashboard_view(request):

    # CREATE (POST)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': booking.id,
                    'brand': booking.car_brand.name,
                    'model': booking.car_model.name,
                    'fuel': booking.fuel_type,
                    'service': booking.service_type,
                    'date': booking.service_date,
                    'status': booking.status,
                })

    # FILTER
    status_filter = request.GET.get('status')

    bookings = Booking.objects.filter(user=request.user)

    if status_filter and status_filter != "All":
        bookings = bookings.filter(status=status_filter)

    bookings = bookings.order_by('-created_at')

    # 🔥 PAGINATION (6 per page)
    paginator = Paginator(bookings, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 🔥 THIS IS WHERE YOU PUT IT
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'bookings/partials/booking_table.html', {
            'page_obj': page_obj
        })

    # NORMAL PAGE LOAD
    form = BookingForm()

    return render(request, 'bookings/dashboard.html', {
        'form': form,
        'page_obj': page_obj
    })

# @login_required
# def dashboard_view(request):

#     # ---------- CREATE BOOKING (AJAX) ----------
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.save()

#             # AJAX create response
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({
#                     'id': booking.id,
#                     'brand': booking.car_brand.name,
#                     'model': booking.car_model.name,
#                     'fuel': booking.fuel_type,
#                     'service': booking.service_type,
#                     'date': booking.service_date,
#                     'status': booking.status,
#                 })

#             return redirect('dashboard')

#         return JsonResponse({'errors': form.errors}, status=400)

#     # ---------- FILTER LOGIC ----------
#     status_filter = request.GET.get('status')

#     bookings = Booking.objects.filter(user=request.user)

#     if status_filter and status_filter != "All":
#         bookings = bookings.filter(status=status_filter)

#     bookings = bookings.order_by('-created_at')

#     # AJAX filter response
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'bookings/partials/booking_table.html', {
#             'bookings': bookings
#         })

#     form = BookingForm()

#     return render(request, 'bookings/dashboard.html', {
#         'form': form,
#         'bookings': bookings
#     })


# ---------------------------
# Logout View
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect('login')

# Create Ajax View 
def load_models(request):
    brand_id = request.GET.get('brand_id')
    models = CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse(list(models), safe=False)

# # delete view
# @login_required
# def delete_booking(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id, user=request.user)

#     if request.method == "POST":
#         booking.delete()
#         return redirect('dashboard')

#     return redirect('dashboard')

@require_POST
def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)
    booking.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('dashboard')

# Update 
# @login_required
# def update_booking(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id, user=request.user)

#     if request.method == "POST":
#         form = BookingForm(request.POST, instance=booking)
#         if form.is_valid():
#             updated_booking = form.save(commit=False)
#             updated_booking.user = request.user
#             updated_booking.save()
#             return redirect('dashboard')
#     else:
#         form = BookingForm(instance=booking)

#     return render(request, 'bookings/update_booking.html', {
#         'form': form
#     })

# new update booking with ajax
# @login_required
# def update_booking(request, booking_id):
#     booking = Booking.objects.get(id=booking_id, user=request.user)

#     if request.method == "POST":
#         form = BookingForm(request.POST, instance=booking)
#         if form.is_valid():
#             booking = form.save()

#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({
#                     'id': booking.id,
#                     'brand': booking.car_brand.name,
#                     'model': booking.car_model.name,
#                     'fuel': booking.fuel_type,
#                     'service': booking.service_type,
#                     'date': booking.service_date,
#                     'status': booking.status,
#                 })

#     return JsonResponse({'error': 'Invalid request'}, status=400) 
    

@login_required
def update_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save()

            return JsonResponse({
                'id': booking.id,
                'brand': booking.car_brand.name,
                'model': booking.car_model.name,
                'fuel': booking.fuel_type,
                'service': booking.service_type,
                'date': booking.service_date.strftime("%Y-%m-%d"),
                'status': booking.status,
            })

        return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)    

    
@login_required
def edit_booking_modal(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)
    form = BookingForm(instance=booking)

    html = render_to_string(
        'bookings/partials/edit_form.html',
        {'form': form, 'booking': booking},
        request=request
    )

    return JsonResponse({'html': html})    
