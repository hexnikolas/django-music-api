import re
import json
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import CharField, TextField
from django.db.models import  Q
from datetime import datetime
from dateutil.relativedelta import relativedelta
from music.serializers import UserSerializer
from music.models import User, Track, Album, Artist



@csrf_exempt
def index(request):
    return JsonResponse({"message":"API works! Try the other pages (/subscription, /track/track_id/listen, /search) also!"})

@csrf_exempt
def subscription(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Please use POST method, since it is safer to use with sensitive data, such as card details."})
    elif request.method == 'POST':
        # parsing the request data to json
        request_data = JSONParser().parse(request)

        # checking user id is present in request body
        try:
            user = request_data['user_id']
        except:
            return JsonResponse({"message":"Need user_id field in request body."})

        # checking duration is present in request body
        try:
            duration = request_data['duration']
        except:
            return JsonResponse({"message":"Need duration field in request body."})


        # checking card number is present in request body
        try:
            user = request_data['card_number']
        except:
            return JsonResponse({"message":"Need card_number field in request body."})


        # checking expiration date is present in request body
        try:
            user = request_data['expiration_date']
        except:
            return JsonResponse({"message":"Need expiration_date field in request body."})


        # checking holder name is present in request body
        try:
            user = request_data['holder_name']
        except:
            return JsonResponse({"message":"Need holder_name field in request body."})


        # checking cvv is present in request body
        try:
            user = request_data['cvv']
        except:
            return JsonResponse({"message":"Need cvv field in request body."})


        # checking that a user with that id exists
        try:
            users = User.objects.get(id = request_data['user_id'])
            user_data = users.__dict__
        except:
            return JsonResponse({"message":"No user with provided id exists."})


        # get current date in same format as database dates
        current_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date()


        # check that the provided expiration date is valid
        expiration_date_test = re.search("^1[0-2]|0[1-9]/[0-9]{2}$", request_data["expiration_date"])
        if not expiration_date_test:
            return JsonResponse({"message":"Wrong expiration date format, need MM/YY."})


        # if the subscription of user is ending later than current date, his subscription is still active
        try:
            if user_data['subscription_end'] > current_date:
                return JsonResponse({"message":"Can not purchase another susbscription, yours is still active."})
        except TypeError:
            # a user that has never subscribed, has null dates in table
            pass

        # check if provided card is correct
        card_test = re.search("^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$", request_data['card_number'])
        if not card_test:
            return JsonResponse({"message":"Incorrect card number format, need XXXX-XXXX-XXXX-XXXX."})


        # check if the expiration date is correct and still valid
        try:
            expiration_date = datetime.strptime(request_data['expiration_date'], '%m/%y').date()
        except ValueError:
            return JsonResponse({"message":"Incorrect expiration date format, need MM/YY."})


        current_card_date = datetime.strptime(datetime.today().strftime('%m/%y'), '%m/%y').date()

        if expiration_date < current_card_date:
            return JsonResponse({"message":"Card has expired."})


        # check if provided cvv is correct
        cvv_test = re.search("^[0-9]{3}$", request_data['cvv'])
        if not cvv_test:
            return JsonResponse({"message":"Incorrect cvv format, need XXX, where X is a number between 0 and 9."})


        # everything is correct, update his subscription

        # starting date
        subscription_starting = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date()

        # ending date is current + subscription duration (1, 6 or 12)
        try:
            subscription_ending =  datetime.strptime((datetime.today() + relativedelta(months=int(duration))).strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({"message":"Duration has to be a number."})

        new_data = {
            'subscription_start' : subscription_starting,
            "subscription_end" : subscription_ending
        }

        # save to database
        user_serializer = UserSerializer(users, new_data)
        if user_serializer.is_valid():
            user_serializer.save()

        return JsonResponse({"message":"Subscription succesfully purchased."})


@csrf_exempt
def listen(request, track_id=0):
    # parsing the request data to json
    request_data = JSONParser().parse(request)

    # checking user id is present in request body
    try:
        user = request_data['user_id']
    except:
        return JsonResponse({"message":"Need user_id field in request body"})

    # checking that a user with that id exists
    try:
        users = User.objects.get(id = request_data['user_id'])
        user_data = users.__dict__
    except:
        return JsonResponse({"message":"No user with provided id exists."})

    # get current date in same format as database dates
    current_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date()

    # if the subscription of user has ended, he can not listen to music
    try:
        if user_data['subscription_end'] < current_date:
            return JsonResponse({"message":"Your subscription has ended, please subscribe to listen to music."})
    except TypeError:
        # a user that has never subscribed, has null dates in table
        return JsonResponse({"message":"You haven't purchased a subscription yet."})

    # checking that a track with that id exists
    try:
        tracks = Track.objects.get(id = track_id)
    except:
        return JsonResponse({"message":"No track with provided id exists."})

    return JsonResponse({"message": "Here’s your music" })


@csrf_exempt
def search(request):
    # parsing the request data to json
    request_data = JSONParser().parse(request)

    # checking a search term is present in request body
    try:
        search_term = request_data['search']
    except:
        return JsonResponse({"message":"Need search field in request body"})

    # get the artists that match, in fields that are charfield or textfield (name, short_description, genre)
    fields = [f for f in Artist._meta.fields if isinstance(f, CharField) or isinstance(f, TextField)]
    queries = [Q(**{f.name + "__icontains": search_term}) for f in fields]

    qs = Q()
    for query in queries:
        qs = qs | query

    artists_to_return = [ str(x) for x in Artist.objects.filter(qs)]

    # get the albums that match, in fields that are charfield or textfield (name, type)
    fields = [f for f in Album._meta.fields if isinstance(f, CharField) or isinstance(f, TextField)]
    queries = [Q(**{f.name+ "__icontains": search_term}) for f in fields]

    # since the album has a foreign key artist, we search the foreign key column too
    related_fields = [f.name for f in Album._meta.get_fields() if f.is_relation and f.related_model == Artist]
    related_queries = [Q(**{f + "__name__icontains": search_term}) for f in related_fields]

    qs = Q()
    for query in queries + related_queries:
        qs = qs | query

    albums_to_return = [ str(x) for x in Album.objects.filter(qs)]


    # get the tracks that match, in fields that are charfield or textfield (title, lyrics)
    fields = [f for f in Track._meta.fields if isinstance(f, CharField) or isinstance(f, TextField)]
    queries = [Q(**{f.name+ "__icontains": search_term}) for f in fields]

    # since the track has foreign keys artist and album, we search the foreign key columns too
    related_fields = [f.name for f in Track._meta.get_fields() if f.is_relation and (f.related_model == Artist or f.related_model == Album)]
    related_queries = [Q(**{f + "__name__icontains": search_term}) for f in related_fields]

    qs = Q()
    for query in queries + related_queries:
        qs = qs | query

    tracks_to_return = [ str(x) for x in Track.objects.filter(qs)]

    message = {
      "artists" : artists_to_return,
      "tracks" : tracks_to_return,
      "albums" : albums_to_return
    }
    return JsonResponse(message)
