from django.core import paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import PfreeEateries
from django.utils import timezone 
from .forms import PfreeEateriesForm
from datetime import datetime
from django.core.paginator import Paginator

def index(request):
    """
    Output for PfreeEateries
    """
    # page count
    page = request.GET.get('page', '1')

    # query
    PfreeEateries_list = PfreeEateries.objects.order_by('-create_date')

    # handling pages
    paginator = Paginator(PfreeEateries_list, 10) # Show 10 per page
    page_obj = paginator.get_page(page)

    #context = {'PfreeEateries_list': PfreeEateries_list}
    context = {'PfreeEateries_list': page_obj}
    return render(request, 'pfreers/pfreeElist.html', context)

def detail(request, PfreeEateries_id):
    """
    List of PfreeEateries
    """
    elist = PfreeEateries.objects.get(id=PfreeEateries_id)
    context = {'elist': elist}
    return render(request, 'pfreers/pfreeElist_detail.html', context)

def PfreeEateries_create(request):
    """
    Register a eatery
    """
    if request.method == 'POST':
        form = PfreeEateriesForm(request.POST)

        if form.is_valid():
           PfreeEateries = form.save(commit=False)
           PfreeEateries.echolv = ''
           PfreeEateries.perf = '0'
           PfreeEateries.create_date = timezone.now()
           #now = datetime.now()
           #PfreeEateries.create_date = now.strftime("%Y-%m-%d %I:%M %p")
           PfreeEateries.save()
           return redirect('/pfreers/')
    else:
        form = PfreeEateriesForm()
    context = {'form': form}
    return render(request, 'pfreers/PfreeEateries_form.html', context)

