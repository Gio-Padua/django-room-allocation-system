from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField
from django.db.models import Sum, Count
from django.db.models.functions import ExtractYear

# Create your views here.

@login_required(redirect_field_name='next', login_url='/login/')
def index(request):
    room = Room.objects.count()
    allocation = Allocation.objects.count()
    resident = Resident.objects.count()
    resident_prio = Resident.objects.filter(priority=True).count()
    alloc_1 = Resident.objects.filter(assigned=True).count()
    alloc_0 = Resident.objects.filter(assigned=False).count()
    resident_counts_by_year = Resident.objects.annotate(year=ExtractYear('date')).values('year').annotate(count=Count('id')).order_by('year')


    print(resident_counts_by_year)

    alloc = [alloc_1, alloc_0]
    
    context = {'room': room, 'resident': resident, 'allocation':allocation, 'num_prio': resident_prio, 'assignment':alloc, 'residents_yearly': resident_counts_by_year}
    return render(request, 'index.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def ResidentTable(request):
  residents = Resident.objects.all().order_by('lname')
  context = {'residents': residents, 'success': False}
  return render(request, 'table/residents.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def addResidents(request):
    if request.method == 'POST':
        form = ResidentsForm(request.POST)
        if form.is_valid():
            nlname = form.cleaned_data['lname']
            nfname = form.cleaned_data['fname']
            naddress = form.cleaned_data['address']
            nfamily  = form.cleaned_data['family_size']
           
            numpriority = form.cleaned_data['priority_members']
            catpriority = form.cleaned_data['priority_category']
            npriority = form.cleaned_data['priority']
            nassigned = form.cleaned_data['assigned']

            new_resident = Resident(
                lname = nlname,
                fname = nfname,
                address = naddress,
                family_size  = nfamily,
                priority_members = numpriority,
                priority_category = catpriority,
                priority = npriority,
                assigned = nassigned,
            )
            new_resident.save() 
            messages.success(request, 'Resident added successfuly!')
            return redirect('residents')  # Redirect to residents list view after success
    else:
        form = ResidentsForm()

    context = {'form': form}

    return render(request, 'table/resident_add.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def editResidents(request, id):
    resident = Resident.objects.get(pk=id)

    if request.method == 'POST':
        form = ResidentsForm(request.POST, instance=resident)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resident edited successfuly!')
            return redirect('residents')  # Redirect to the residents list after a successful edit
    else:
        form = ResidentsForm(instance=resident)

    context = {'form': form, 'resident': resident}  # Pass the student object to the template
    return render(request, 'table/resident_edit.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def deleteResident(request, id):
    resident = Resident.objects.get(pk=id)
    if request.method == 'POST':
        resident.delete()
        messages.warning(request, 'Resident deleted successfully!')
        return redirect('residents')  # Assuming you have a 'resident_list' view
    return render(request, 'table/resident_del.html', {'resident': resident})

@login_required(redirect_field_name='next', login_url='/login/')
def roomsTable(request):
  rooms = Room.objects.all().order_by('name')  # Get all rooms
  context = {'rooms': rooms}
  return render(request, 'table/rooms.html', context)


@login_required(redirect_field_name='next', login_url='/login/')
def room_add(request):
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Rooms added successfuly!')
      return redirect('room_list')  # Redirect to room list after saving
  else:
    form = RoomForm()
  context = {'form': form}
  return render(request, 'table/room_add.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def room_edit(request, id):
    room = Room.objects.get(pk=id)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rooms edited successfuly!')
            return redirect('room_list')  # Redirect to the residents list after a successful edit
    else:
        form = RoomForm(instance=room)

    context = {'form': form, 'room': room}  # Pass the student object to the template
    return render(request, 'table/room_edit.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def delete_room(request, id):
    room = Room.objects.get(pk=id)
    if request.method == 'POST':
        room.delete()
        messages.warning(request, 'Rooms deleted successfully!')
        return redirect('room_list')  # Assuming you have a 'resident_list' view
    return render(request, 'table/room_del.html', {'room': room})
#Allocations

@login_required(redirect_field_name='next', login_url='/login/')
def allocationTable(request):
    allocations = Allocation.objects.all()
    context = {'allocations': allocations}
    return render(request, 'table/allocation.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def allocation_add(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, 'Allocation added successfully!')
           return render('allocation_list', {'success' : True})
    else:
        form = AllocationForm()
    context = {'form': form}
    return render(request, 'table/alloc_add.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def allocation_edit(request, id):
    allocation = Allocation.objects.get(pk=id)
    if request.method == 'POST':
        form = AllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Allocation edited successfully!')
            return redirect('allocation_list')
    else:
        form = AllocationForm(instance=allocation)
    context = {'form': form, 'allocation': allocation}
    return render(request, 'table/alloc_edit.html', context)

@login_required(redirect_field_name='next', login_url='/login/')
def allocation_delete(request, id):
    allocation = Allocation.objects.get(pk=id)
    if request.method == 'POST':
        allocation.delete()
        messages.warning(request, 'Allocation deleted successfully!')
        return redirect('allocation_list')
    return render(request, 'table/alloc_del.html', {'allocation': allocation})


from .genetic_allocation import genetic_algorithm

@login_required(redirect_field_name='next', login_url='/login/')
def allocate_all(request):
    residentq = Resident.objects.all()
    for resident in residentq:
        resident.assigned = False
        resident.save()
    Allocation.objects.all().delete()

    rooms = list(Room.objects.all())
    residents = list(Resident.objects.all())

    # Run the genetic algorithm
    best_solution = genetic_algorithm(rooms, residents)
    print(best_solution)
    
    # Apply assignments
    for resident_index, room_index in enumerate(best_solution):
            resident = residents[resident_index]
            room = rooms[room_index]
            resident.assigned = True
            resident.save()

            allocation = Allocation(resident=resident, room=room)
            allocation.save()
            

    print(f"Allocated {len(residents)} residents to {len(rooms)} rooms.")

    messages.success(request, "Allocations Generated successfully!")
    return JsonResponse({'message': 'Allocations updated successfully!'})

#reports

class ResidentReport(ReportView):
    report_model = Resident
    group_by = "lname"
    date_field = "date"
    filters = ["lname"]
  
    columns = [
        "lname",
        
        ComputationField.create(
            Count, "assigned", verbose_name="Room assigned", 
        ),
        ComputationField.create(
            Sum, "family_size", name="family_size", verbose_name="Total num of residents"
        ),
    ]

    chart_settings = [
        Chart(
            "Total assigned $",
            Chart.BAR,
            data_source=["family_size"],
            title_source=["lname"],
        ),
        Chart(
            "Total assigned $ [PIE]",
            Chart.PIE,
            data_source=["family_size"],
            title_source=["lname"],
        ),
    ]