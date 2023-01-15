from django.http import Http404, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render

from .models import Car, CarOwner, Ownership, DriverLicense


def car_owner_detail(request, car_owner_pk):
    try:
        car_owner = CarOwner.objects.get(pk=car_owner_pk)
    except CarOwner.DoesNotExist:
        raise Http404("Car does not exist")

    return render(request, 'car_owner_detail.html', {'car_owner': car_owner, 'title': "Car Owner Details"})


def car_owner_list(request):
    car_owners = CarOwner.objects.all()

    return render(request, 'car_owner_list.html', {'car_owners': car_owners, 'title': "Car Owners"})


def ownership_detail(request, ownership_pk):
    try:
        ownership = Ownership.objects.get(pk=ownership_pk)
    except Ownership.DoesNotExist:
        raise Http404("Ownership does not exist")

    return render(request, 'ownership_detail.html', {'ownership': ownership, 'title': "Ownership Details"})


def ownership_list(request):
    ownerships = Ownership.objects.all()

    return render(request, 'ownership_list.html', {'ownerships': ownerships, 'title': "Ownerships"})


# def car_detail(request, car_pk):
#     try:
#         car = Car.objects.get(pk=car_pk)
#     except Car.DoesNotExist:
#         raise Http404("Car does not exist")

#     return render(request, 'car_detail.html', {'car': car, 'title': "Car Details"})
class CarDetail(DetailView):
    model = Car
    pk_url_kwarg = 'car_pk'
    template_name = 'car_detail.html'

# def car_list(request):
#     cars = Car.objects.all()

#     return render(request, 'car_list.html', {'cars': cars, 'title': "Cars"})


class CarList(ListView):
    model = Car
    template_name = 'car_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['cars'] = self.model.objects.all()
        context['title'] = "Cars"
        return context


def driver_license_detail(request, driver_license_pk):
    try:
        driver_license = DriverLicense.objects.get(pk=driver_license_pk)
    except DriverLicense.DoesNotExist:
        raise Http404("Driver License does not exist")

    return render(request, 'driver_license_detail.html', {'driver_license': driver_license, 'title': "Driver License Details"})


def driver_license_list(request):
    driver_licenses = DriverLicense.objects.all()

    return render(request, 'driver_license_list.html', {'driver_licenses': driver_licenses, 'title': "Driver Licenses"})
