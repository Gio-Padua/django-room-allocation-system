from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('table', views.TableView, name='table'),
    path('residents', views.ResidentTable, name='residents'),
    path('residents/add', views.addResidents, name='residents_add'),
    path('residents/edit/<int:id>', views.editResidents, name='residents_edit'),
    path('residents/delete/<int:id>/', views.deleteResident, name='resident_delete'),

    path('rooms/', views.roomsTable, name='room_list'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/edit/<int:id>/', views.room_edit, name='room_edit'),
    path('rooms/delete/<int:id>/', views.delete_room, name='room_delete'),

    path('allocations/', views.allocationTable, name='allocation_list'),
    path('allocations/create/', views.allocation_add, name='allocation_add'),
    path('allocations/update/<int:id>/', views.allocation_edit, name='allocation_edit'),
    path('allocations/delete/<int:id>/', views.allocation_delete, name='allocation_delete'),
    path('allocations/allocate-all/', views.allocate_all, name='allocate_all'),

    path('report/', views.RoomsReport.as_view(), name='room_report')



]