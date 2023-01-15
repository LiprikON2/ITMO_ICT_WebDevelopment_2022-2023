from django.urls import path

from . import views

urlpatterns = [
    path('car-owner/<int:car_owner_pk>',
         views.car_owner_detail, name='car-owner-detail'),
    path('car-owner/',
         views.car_owner_list, name='car-owner-list'),

    path('ownership/<int:ownership_pk>',
         views.ownership_detail, name='ownership-detail'),
    path('ownership/',
         views.ownership_list, name='ownership-list'),

    # path('car/<int:car_pk>',
    #      views.car_detail, name='car-detail'),
    path('car/<int:car_pk>',
         views.CarDetail.as_view(), name='car-detail'),
    # path('car/',
    #      views.car_list, name='car-list'),
    path('car/',
         views.CarList.as_view(), name='car-list'),

    path('driver-license/<int:driver_license_pk>',
         views.driver_license_detail, name='driver-license-detail'),
    path('driver-license/',
         views.driver_license_list, name='driver-license-list'),
]
