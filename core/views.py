from django.shortcuts import render, get_object_or_404
from .models import Journal, Category
from django.db.models import Q, Count
from rest_framework import generics
from .serializers import JournalSerializer
import json
from django.http import JsonResponse

def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    qs = Journal.objects.all()
    categories = Category.objects.all()

    title_contains_query = request.GET.get('title_contains')
    id_exact_query = request.GET.get('id_exact')
    title_or_author_query = request.GET.get('title_or_author')
    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    category = request.GET.get('category')
    reviewed = request.GET.get('reviewed')
    not_reviewed = request.GET.get('notReviewed')

    if is_valid_queryparam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)

    elif is_valid_queryparam(id_exact_query):
        qs = qs.filter(id=id_exact_query)

    elif is_valid_queryparam(title_or_author_query):
        qs = qs.filter(Q(title__icontains=title_or_author_query)
                       | Q(author__name__icontains=title_or_author_query)
                       ).distinct()

    if is_valid_queryparam(view_count_min):
        qs = qs.filter(views__gte=view_count_min)

    if is_valid_queryparam(view_count_max):
        qs = qs.filter(views__lt=view_count_max)

    if is_valid_queryparam(date_min):
        qs = qs.filter(publish_date__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(publish_date__lt=date_max)

    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(categories__name=category)

    if reviewed == 'on':
        qs = qs.filter(reviewed=True)

    elif not_reviewed == 'on':
        qs = qs.filter(reviewed=False)

    return qs


def filterView(request):
    qs = filter(request)

    context = {
        'queryset': qs,
        'categories': Category.objects.all()
    }
    return render(request, "form.html", context)


def search_result(request):
    qs = Journal.objects.all()
    if request.method == "POST":
        title_contains_query = json.loads(request.body).get("searchText")
        # title_contains_query = json.loads(request.body).get("title_contains")
        id_exact_query = json.loads(request.body).get('idText')
        view_count_min = json.loads(request.body).get('countMin')
        view_count_max = json.loads(request.body).get('countMax')
        date_min = json.loads(request.body).get('dateMin')
        date_max = json.loads(request.body).get('dateMax')
        category = json.loads(request.body).get('category')
        reviewed = json.loads(request.body).get('reviewed')
        not_reviewed = json.loads(request.body).get('notReviewed')

        if is_valid_queryparam(title_contains_query):
            qs = qs.filter(title__icontains=title_contains_query)

        elif is_valid_queryparam(id_exact_query):
            qs = qs.filter(id=id_exact_query)

        if is_valid_queryparam(view_count_min):
            qs = qs.filter(views__gte=view_count_min)

        if is_valid_queryparam(view_count_max):
            qs = qs.filter(views__lt=view_count_max)

        if is_valid_queryparam(date_min):
            qs = qs.filter(publish_date__gte=date_min)

        if is_valid_queryparam(date_max):
            qs = qs.filter(publish_date__lt=date_max)

        if is_valid_queryparam(category) and category != 'Choose...':
            qs = qs.filter(categories__name=category)

        if reviewed == 'on':
            qs = qs.filter(reviewed=True)

        elif not_reviewed == 'on':
            qs = qs.filter(reviewed=False)

        data = qs.values()
        return JsonResponse(list(data), safe=False)


class FilterListView(generics.ListAPIView):
    serializer_class = JournalSerializer

    def get_queryset(self):
        qs = filter(self.request)
        return qs
