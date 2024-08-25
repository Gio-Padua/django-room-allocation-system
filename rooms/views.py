from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import  redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField
from django.db.models import Sum, Count

# Create your views here.
def TableView(request):
    return render(request, 'table/tables.html')

def ResidentTable(request):
  residents = Resident.objects.all().order_by('name')
  context = {'residents': residents}
  return render(request, 'table/residents.html', context)

def addResidents(request):
    if request.method == 'POST':
        form = ResidentsForm(request.POST)
        if form.is_valid():
            nname = form.cleaned_data['name']
            naddress = form.cleaned_data['address']
            nfamily  = form.cleaned_data['family_size']
            npriority = form.cleaned_data['priority']
            nassigned = form.cleaned_data['assigned']

            new_resident = Resident(
                name = nname,
                address = naddress,
                family_size  = nfamily,
                priority = npriority,
                assigned = nassigned,
            )
            new_resident.save()  # Save the form directly
            return redirect('residents')  # Redirect to residents list view after success
    else:
        form = ResidentsForm()

    context = {'form': form}

    return render(request, 'table/resident_add.html', context)

def editResidents(request, id):
    resident = Resident.objects.get(pk=id)

    if request.method == 'POST':
        form = ResidentsForm(request.POST, instance=resident)
        if form.is_valid():
            form.save()
            return redirect('residents')  # Redirect to the residents list after a successful edit
    else:
        form = ResidentsForm(instance=resident)

    context = {'form': form, 'resident': resident}  # Pass the student object to the template
    return render(request, 'table/resident_edit.html', context)

def deleteResident(request, id):
    resident = Resident.objects.get(pk=id)
    if request.method == 'POST':
        resident.delete()
        messages.success(request, 'Resident deleted successfully!')
        return redirect('residents')  # Assuming you have a 'resident_list' view
    return render(request, 'table/resident_del.html', {'resident': resident})

#rooms
def roomsTable(request):
  rooms = Room.objects.all().order_by('name')  # Get all rooms
  context = {'rooms': rooms}
  return render(request, 'table/rooms.html', context)

def room_add(request):
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('room_list')  # Redirect to room list after saving
  else:
    form = RoomForm()
  context = {'form': form}
  return render(request, 'table/room_add.html', context)


def room_edit(request, id):
    room = Room.objects.get(pk=id)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')  # Redirect to the residents list after a successful edit
    else:
        form = RoomForm(instance=room)

    context = {'form': form, 'room': room}  # Pass the student object to the template
    return render(request, 'table/room_edit.html', context)

def delete_room(request, id):
    room = Room.objects.get(pk=id)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Resident deleted successfully!')
        return redirect('room_list')  # Assuming you have a 'resident_list' view
    return render(request, 'table/room_del.html', {'room': room})
#Allocations

def allocationTable(request):
    allocations = Allocation.objects.all()
    context = {'allocations': allocations}
    return render(request, 'table/allocation.html', context)

def allocation_add(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, 'Allocation created successfully!')
           return redirect('allocation_list')
    else:
        form = AllocationForm()
    context = {'form': form}
    return render(request, 'table/alloc_add.html', context)

def allocation_edit(request, id):
    allocation = Allocation.objects.get(pk=id)
    if request.method == 'POST':
        form = AllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Allocation updated successfully!')
            return redirect('allocation_list')
    else:
        form = AllocationForm(instance=allocation)
    context = {'form': form, 'allocation': allocation}
    return render(request, 'table/alloc_edit.html', context)

def allocation_delete(request, id):
    allocation = Allocation.objects.get(pk=id)
    if request.method == 'POST':
        allocation.delete()
        messages.success(request, 'Allocation deleted successfully!')
        return redirect('allocation_list')
    return render(request, 'table/alloc_del.html', {'allocation': allocation})


from .genetic_allocation import genetic_algorithm

def allocate_all(request):
    residentq = Resident.objects.all()
    for resident in residentq:
        resident.assigned = False
        resident.save()
    Allocation.objects.all().delete()

    # Get rooms and residents
    rooms = list(Room.objects.all())
    residents = list(Resident.objects.all())

    # Run the genetic algorithm
    best_solution = genetic_algorithm(rooms, residents)  # Ignore distribution
    print(f"Length of best_solution: {len(best_solution)}")
    print(f"Length of rooms: {len(rooms)}")
    # Update resident assignments and save
    for resident, room_index in zip(residents, best_solution):
        resident.assigned = True
        resident.save()
        allocation = Allocation(resident=resident, room=rooms[room_index])
        allocation.save()
    

    messages.success(request, "Allocations updated successfully!")
    return JsonResponse({'message': 'Allocations updated successfully!'})

#reports

class RoomsReport(ReportView):
    report_model = Allocation
    date_field = "date"
    group_by = "resident"
    columns = [
        "name",
        ComputationField.create(
            Count, "resident.assigned", verbose_name="Room assigned", 
        ),
        ComputationField.create(
            Sum, "resident.family_size", name="sum__value", verbose_name="Total Value sold $"
        ),
    ]

    chart_settings = [
        Chart(
            "Total assigned $",
            Chart.BAR,
            data_source=["sum__value"],
            title_source=["name"],
        ),
        Chart(
            "Total assigned $ [PIE]",
            Chart.PIE,
            data_source=["sum__value"],
            title_source=["name"],
        ),
    ]