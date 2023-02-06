import datetime
from django.urls import resolve
from urllib.parse import urlparse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
from django.views.generic import RedirectView
from operator import itemgetter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from . import models, forms, serializers


class ModelsAPIView(APIView):
    model = None
    modelSerializer = None

    def get(self, request, *args, **kwargs):
        objects = self.model.objects.all()
        serializer = self.modelSerializer(objects, many=True)
        return Response({self.model.__name__: serializer.data})

    def post(self, request, *args, **kwargs):
        object_data = request.data.get(self.model.__name__)
        serializer = self.modelSerializer(data=object_data)

        if serializer.is_valid(raise_exception=True):
            new_object = serializer.save()

        return Response({"Success": f"{self.model.__name__} '{new_object}' created succesfully."})


class ModelDetailsAPIView(APIView):
    model = None
    modelSerializer = None

    def get(self, request, pk, *args, **kwargs):
        object = self.model.objects.get(pk=pk)
        serializer = self.modelSerializer(object)
        return Response({self.model.__name__: serializer.data})

    def delete(self, request, pk, *args, **kwargs):
        object = self.model.objects.get(pk=pk)
        object.delete()
        return Response({"Success": f"{self.model.__name__} '{object}' deleted succesfully."})

    def patch(self, request, pk, *args, **kwargs):
        prev_object = self.model.objects.get(pk=pk)

        object_data = request.data.get(self.model.__name__)
        serializer = self.modelSerializer(
            prev_object, data=object_data, partial=True)

        if serializer.is_valid(raise_exception=True):
            new_object = serializer.save()

        return Response({"Success": f"{self.model.__name__} '{new_object}' updated succesfully."})


class UsersAPIView(ModelsAPIView):
    model = models.User
    modelSerializer = serializers.UserSerializer


class UserDetailsAPIView(ModelDetailsAPIView):
    model = models.User
    modelSerializer = serializers.UserSerializer


class LibrariesAPIView(ModelsAPIView):
    model = models.Library
    modelSerializer = serializers.LibrarySerializer


class LibraryDetailsAPIView(ModelDetailsAPIView):
    model = models.Library
    modelSerializer = serializers.LibrarySerializer


class ReadingRoomsAPIView(ModelsAPIView):
    model = models.ReadingRoom
    modelSerializer = serializers.ReadingRoomSerializer


class ReadingRoomDetailsAPIView(ModelDetailsAPIView):
    model = models.ReadingRoom
    modelSerializer = serializers.ReadingRoomSerializer


class BooksAPIView(ModelsAPIView):
    model = models.Book
    modelSerializer = serializers.BookSerializer


class BookDetailsAPIView(ModelDetailsAPIView):
    model = models.Book
    modelSerializer = serializers.BookSerializer


class ReadingRoomBooksAPIView(ModelsAPIView):
    model = models.ReadingRoomBook
    modelSerializer = serializers.ReadingRoomBookSerializer


class ReadingRoomBookDetailsAPIView(ModelDetailsAPIView):
    model = models.ReadingRoomBook
    modelSerializer = serializers.ReadingRoomBookSerializer


class ReadingRoomBookUsersAPIView(ModelsAPIView):
    model = models.ReadingRoomBookUser
    modelSerializer = serializers.ReadingRoomBookUserSerializer


class ReadingRoomBookUserDetailsAPIView(ModelDetailsAPIView):
    model = models.ReadingRoomBookUser
    modelSerializer = serializers.ReadingRoomBookUserSerializer


# "Какие книги закреплены за заданным читателем?"
class UserBooksAPIView(APIView):
    model = models.User
    modelSerializer = serializers.UserSerializer

    def get(self, request, pk, *args, **kwargs):
        object = self.model.objects.get(pk=pk)
        serializer = self.modelSerializer(object)

        try:
            reading_room_book_user_set = serializer.data['readingroombookuser_set']
            books = []
            for reading_room_book_user in reading_room_book_user_set:
                book = reading_room_book_user['reading_room_book']['book']
                books.append(book)
        except KeyError:
            books = []
        return Response({"Book": books})


# "Кто из читателей взял книгу более месяца тому назад?"
class UsersYoungAPIView(APIView):
    model = models.User
    modelSerializer = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        month_ago = now - datetime.timedelta(days=30)

        objects = self.model.objects.filter(
            readingroombookuser__borrow_date__lte=month_ago, readingroombookuser__returned_date__isnull=True)
        serializer = self.modelSerializer(objects, many=True)

        return Response({self.model.__name__: serializer.data})


# За кем из читателей закреплены книги, количество экземпляров которых в библиотеке не превышает 2?
class UsersBooksRareAPIView(APIView):
    model = models.User
    modelSerializer = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        objects = self.model.objects.filter(
            readingroombookuser__reading_room_book__book__total_stock__lte=2, readingroombookuser__returned_date__isnull=True)
        serializer = self.modelSerializer(objects, many=True)

        return Response({self.model.__name__: serializer.data})


# Сколько в библиотеке читателей младше 20 лет?
class UsersYoungAPIView(APIView):
    model = models.User
    modelSerializer = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        twenty_years_ago = now - datetime.timedelta(days=20 * 365)

        objects = self.model.objects.filter(
            date_of_birth__lte=twenty_years_ago)
        serializer = self.modelSerializer(objects, many=True)

        return Response({self.model.__name__: serializer.data})


# Сколько читателей в процентном отношении имеют начальное образование, среднее, высшее, ученую степень?
class UsersGroupedByDegreeAPIView(APIView):
    model = models.User
    modelSerializer = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        degrees_dict = self.model.group_by_degree()

        degree_data = {}
        for degree, user in degrees_dict.items():
            serializer = self.modelSerializer(user, many=True)
            degree_data[degree] = serializer.data

        return Response({"Degree": degree_data})


# Необходимо предусмотреть возможность выдачи отчета о работе библиотеки в течение месяца.
# Отчет должен включать в себя следующую информацию:
# - количество книг читателей на каждый день в каждом из залов и в библиотеке в целом
# - количество читателей, записавшихся в библиотеку в каждый зал и в библиотеку за отчетный месяц.
class LibraryMonthlyReportAPIView(APIView):
    model = models.Library
    modelSerializer = serializers.LibrarySerializer
    userSerializer = serializers.UserSerializer
    readingRoomSerializer = serializers.ReadingRoomSerializer

    def get(self, request, pk, *args, **kwargs):
        library = self.model.objects.get(pk=pk)
        grouped_library = library.group_new_users_by_day()
        grouped_rooms = library.group_new_users_by_day_per_room()

        grouped_library_data = {
            "library": {},
            "dates": {}
        }
        for date, users in grouped_library['dates'].items():
            serializer = self.userSerializer(users, many=True)
            grouped_library_data['dates'][date] = serializer.data

        serializer = self.modelSerializer(grouped_library['library'])
        grouped_library_data['library'] = serializer.data

        grouped_rooms_data = []
        for grouped_room in grouped_rooms:
            grouped_room_data = {
                "reading_room": {},
                "dates": {}
            }
            for date, users in grouped_room['dates'].items():
                serializer = self.userSerializer(users, many=True)
                grouped_room_data['dates'][date] = serializer.data
            grouped_rooms_data.append(grouped_room_data)

            serializer = self.readingRoomSerializer(
                grouped_room['reading_room'])
            grouped_room_data['reading_room'] = serializer.data

        report_data = {
            "NewUsersLibrary": grouped_library_data,
            "NewUsersReadingRooms": grouped_rooms_data,
        }
        return Response({"MonthlyReport": report_data})


class Home(TemplateView):
    template_name = 'home.html'


class SignUp(CreateView):
    model = models.User
    form_class = forms.UserSignUpForm
    template_name = 'sign_up.html'

    def get_success_url(self):
        return reverse("home")

    # Auto login after signing up
    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return


class LogIn(LoginView):
    template_name = 'log_in.html'


class LogOut(RedirectView):
    query_string = True
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(LogOut, self).get_redirect_url(*args, **kwargs)


# class Flights(LoginRequiredMixin, ListView):
#     model = models.Flight
#     template_name = 'flights.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         api_key = self.request.user.api_key
#         api_url = self.request.user.api_url
#         iata_codes = self.model.get_iata_codes()

#         # Getting city names based on iata airport codes
#         cities_result = utils.get_city_by_iata_code(
#             api_key, api_url, iata_codes)
#         iata_codes_dict, error = itemgetter(
#             'iata_codes_dict', 'error')(cities_result)

#         # Setting city names from dict
#         date_dict = self.model.group_by_day()
#         for date, flights in date_dict.items():
#             for flight in flights:
#                 flight.source = iata_codes_dict[flight.source_airport_code]
#                 flight.destination = iata_codes_dict[flight.destination_airport_code]

#         context['dates'] = date_dict
#         context['error'] = error
#         return context


# class FlightDetails(DetailView):
#     model = models.Flight
#     template_name = 'flight_details.html'

#     def get_context_data(self, **kwargs):
#         context = super(FlightDetails, self).get_context_data(**kwargs)
#         try:
#             flight = self.model.objects.get(pk=self.kwargs.get('pk'))
#         except self.model.DoesNotExist:
#             return go_back(
#                 self.request,
#                 error_message="This flight does not exist"
#             )

#         api_key = self.request.user.api_key
#         api_url = self.request.user.api_url
#         iata_codes = flight.get_iata_code()

#         # Getting city names based on iata airport codes
#         cities_result = utils.get_city_by_iata_code(
#             api_key, api_url, iata_codes)
#         iata_codes_dict, error = itemgetter(
#             'iata_codes_dict', 'error')(cities_result)
#         try:
#             flight.source = iata_codes_dict[flight.source_airport_code]
#             flight.destination = iata_codes_dict[flight.destination_airport_code]
#         except KeyError:
#             error = "Cached request is incorrect"

#         context['flight'] = flight
#         context['error'] = error

#         return context


# class FlightPassengers(DetailView):
#     model = models.FlightUser
#     template_name = 'flight_passengers.html'

#     def get_context_data(self, **kwargs):
#         context = super(FlightPassengers, self).get_context_data(**kwargs)
#         try:
#             flight_tickets = self.model.objects.filter(
#                 flight__pk=self.kwargs.get('pk'))
#         except self.model.DoesNotExist:
#             return go_back(
#                 self.request,
#                 error_message="This flight does not exist"
#             )

#         context['flight_tickets'] = flight_tickets
#         return context


# class FlightReviews(DetailView):
#     model = models.Flight
#     template_name = 'flight_reviews.html'

#     def get_context_data(self, **kwargs):
#         context = super(FlightReviews, self).get_context_data(**kwargs)
#         flight = self.object
#         flight.avg_rating = flight.get_avg_rating()

#         reviews = flight.get_reviews()

#         context['flight'] = flight
#         context['reviews'] = reviews
#         return context


# class FlightReviewCreate(LoginRequiredMixin, CreateView):
#     model = models.Review
#     form_class = forms.FlightReviewForm
#     template_name = 'flight_review_create.html'

#     def get_success_url(self):
#         return go_back(self.request, url="flight_reviews", to_redirect=False, ignore_provided_kwargs=True)

#     def form_valid(self, form):
#         try:
#             flight = models.Flight.objects.get(pk=self.kwargs['pk'])
#         except models.Flight.DoesNotExist:
#             return go_back(
#                 self.request,
#                 error_message="This flight does not exist"
#             )

#         user = self.request.user
#         review = flight.get_user_review(user)
#         if review:
#             review.delete()

#         form.instance.flight = flight
#         form.instance.user = user

#         return super().form_valid(form)


# class Profile(LoginRequiredMixin, TemplateView):
#     model = models.User
#     template_name = 'profile.html'

#     login_url = 'log_in'

#     def get_context_data(self, **kwargs):
#         context = super(Profile, self).get_context_data(**kwargs)

#         api_key = self.request.user.api_key
#         api_url = self.request.user.api_url
#         iata_codes = models.Flight.get_iata_codes()

#         # Getting city names based on iata airport codes
#         cities_result = utils.get_city_by_iata_code(
#             api_key, api_url, iata_codes)
#         iata_codes_dict, error = itemgetter(
#             'iata_codes_dict', 'error')(cities_result)

#         # Setting city names from dict
#         date_dict = models.Flight.group_by_day(
#             reservators__in=[self.request.user])
#         for date, flights in date_dict.items():
#             for flight in flights:
#                 flight_ticket = models.FlightUser.objects.filter(
#                     user=self.request.user, flight=flight).first()

#                 flight.ticket_number = flight_ticket.ticket_number
#                 flight.source = iata_codes_dict[flight.source_airport_code]
#                 flight.destination = iata_codes_dict[flight.destination_airport_code]

#         context['dates'] = date_dict
#         context['error'] = error
#         context.update({'user': self.request.user})
#         return context


# @login_required
# def toggle_reserve(request, pk):
#     model = models.Flight

#     try:
#         flight = model.objects.get(pk=pk)
#     except model.DoesNotExist:
#         return go_back(
#             request,
#             error_message="This flight does not exist"
#         )

#     is_reserved = request.user in flight.reservators.filter(pk=request.user.pk)

#     if not is_reserved:
#         reservators_count = flight.reservators.count()
#         max_reservations = flight.max_reservations

#         if reservators_count >= max_reservations:
#             return go_back(
#                 request=request,
#                 error_message="All seats have already been reserved."
#             )

#         flight.reservators.add(request.user)

#         # Generation random ticket number
#         flight_ticket = models.FlightUser.objects.filter(
#             user=request.user, flight=flight).first()
#         flight_ticket.ticket_number = flight_ticket.get_random_ticket_number()
#         flight_ticket.save()

#     else:
#         flight.reservators.remove(request.user)

#     return go_back(request)


# def go_back(request, to_redirect=True, ignore_provided_kwargs=True, url="", kwargs={}, error_message=""):
#     curr_url = request.path
#     prev_url = urlparse(request.META.get('HTTP_REFERER')).path
#     prev_url_name = resolve(prev_url).url_name
#     prev_url_kwargs = resolve(prev_url).kwargs

#     if not url:
#         url = prev_url_name
#     if ignore_provided_kwargs:
#         kwargs = prev_url_kwargs

#     # Prevent getting stuck in redirecting
#     if curr_url == url:
#         url = "home"
#         kwargs = {}

#     if error_message:
#         messages.error(request, error_message)
#     if to_redirect:
#         return redirect(reverse_lazy(url, kwargs=kwargs))
#     else:
#         return reverse_lazy(url, kwargs=kwargs)
