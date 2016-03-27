from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from user.utils import user_alreadyloggedin, get_userrole, review_permission
from siteinfo.views import site_topnav

from user.models import User
from .models import Facilities, Room

def list_facilities_floor(request):

    # case 1: return all facilities with floor
    # case 2: return specific floor facilities
    # case 3: return facilities status

    # 1. Check permission
    if not user_alreadyloggedin(request):
        return HttpResponseRedirect(reverse('index'))

    user = User.objects.get(username = request.session['user'])
    if not review_permission(user, 'view:facilites'):
        return HttpResponseRedirect(reverse('index_home'))

    facilities_obj = Facilities.objects.all().order_by('room')

    return render(request, 'home.html', {
        'page_title': 'Welcome home!',
        'page_header': 'Good to seeing you, ',
        'topnav': site_topnav(get_userrole(request.session['user'])['level']),
        'template': 'list',
        'content': {   
            'list': {
                'name': 'booking',
                'body': facilities_obj,
            },
        },
    })



def add_facilities(request):
    pass

def modify_facilities(request):
    pass

def remove_facilities(request):
    pass