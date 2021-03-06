from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from user.utils import user_alreadyloggedin, get_userrole, review_permission
from siteinfo.views import site_topnav

import json
from datetime import datetime

from .models import *
from .forms import *
from user.models import User, Class_code

# Create your views here.
def rule_list(request):
    if not user_alreadyloggedin(request):
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(username = request.session['user'])
    if not review_permission(user, 'allow:attendance_edit'):
        return HttpResponseRedirect(reverse('index_home')) 

    rule = Rule.objects.all()

    return render(request, 'home.html', {
        'page_header': 'Inbox',
        'template': 'list', # operation, list,
        'topnav': site_topnav(get_userrole(request.session['user'])['level']),
        'content': {
            'operation': ( 
                # operation pattern ('title', 'url(url:name)', 'url_para' 'assign html class name in list')
                ({'title':'Add rule', 
                   'url': 'attendance:add_rule',
                   'html_class': 'add_rule'}),
                ({'title':'Apply rule', 
                   'url': 'attendance:apply_rule',
                   'html_class': 'apple_rule'}),

            ),
            'list': {
                'checkbox': True,
                'name': 'rule',
                'body': rule,
                'foot': (),
            },
        },
    })

def add_rule(request):
    # 1. Check permission
    if not user_alreadyloggedin(request):
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(username = request.session['user'])
    if not review_permission(user, 'allow:attendance_edit'):
        return HttpResponseRedirect(reverse('index_home'))

    ruleform = RuleForm()

    if request.method == 'POST':

        ruleform = RuleForm(request.POST)

        if ruleform.is_valid():
            ruleform.save()

            return render(request, 'home.html', {
                'page_title': 'Attendance rule assignment',
                'page_header': 'Attendance rule assignment',
                'topnav': site_topnav(get_userrole(request.session['user'])['level']),
                'template': 'notification',
                'content': {
                    'notification': 'Rule add successful',
                    'redirect_text': 'Attendance rule page',
                    'redirect_url': 'attendance:rulelist',
                    'auto_redirect': True,
                },
            })

        return render(request, 'home.html', {
        'page_title': 'Attendance rule assignment',
        'page_header': 'Attendance rule assignment',
        'topnav': site_topnav(get_userrole(request.session['user'])['level']),
        'template': 'form',
        'content': {
            'form': ruleform.as_ul(),
            'submit_url': 'attendance:add_rule',
        },
    })

    return render(request, 'home.html', {
        'page_title': 'Attendance rule assignment',
        'page_header': 'Attendance rule assignment',
        'topnav': site_topnav(get_userrole(request.session['user'])['level']),
        'template': 'form',
        'content': {
            'form': ruleform.as_ul(),
            'submit_url': 'attendance:add_rule',
        },
    })

def apply_rule(request):
    # 1. Check permission
    if not user_alreadyloggedin(request):
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(username = request.session['user'])
    if not review_permission(user, 'allow:attendance_edit'):
        return HttpResponseRedirect(reverse('index_home'))

    applyform = ApplyForm()

    if request.method == 'POST':

        applyform = ApplyForm(request.POST)

        if applyform.is_valid():
            insert_list = request.POST.getlist('class_assign')

            z = applyform.save(commit=False)
            commit_list = []
            for applied_rule in insert_list:
                commit_list.append(Applied_rule(rule=z.rule, end_date=z.end_date, start_date=z.start_date, exclude_weekend=z.exclude_weekend, class_code=Class_code.objects.get(pk=applied_rule)))

            Applied_rule.objects.bulk_create(commit_list);

            return render(request, 'home.html', {
                'page_title': 'Attendance rule assignment',
                'page_header': 'Attendance rule assignment',
                'topnav': site_topnav(get_userrole(request.session['user'])['level']),
                'template': 'notification',
                'content': {
                    'notification': 'Assign successful',
                    'redirect_text': 'Attendance rule page',
                    'redirect_url': 'attendance:rulelist',
                    'auto_redirect': True,
                },
            })

        return render(request, 'home.html', {
        'page_title': 'Welcome home!',
        'page_header': 'Good to seeing you, ',
        'topnav': site_topnav(get_userrole(request.session['user'])['level']),
        'template': 'form',
        'content': {
            'form': applyform.as_ul(),
            'submit_url': 'attendance:apply_rule',
        },
    })

    return render(request, 'home.html', {
        'page_title': 'Room Reservation',
        'page_header': 'Reserve for a room',
        'topnav': site_topnav(get_userrole(request.session['user'])['level']),
        'template': 'form',
        'content': {
            'form': applyform.as_ul(),
            'submit_url': 'attendance:apply_rule',
        },
    })

def remove_rule(request, rule_id):
    if not user_alreadyloggedin(request):
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(username = request.session['user'])
    if not review_permission(user, 'allow:attendance_edit'):
        return HttpResponseRedirect(reverse('index_home')) 

    try:
        rule = Rule.objects.get(pk = rule_id)
    except:
        return HttpResponseRedirect(reverse('attendance:rulelist')) 

    rule.delete()

    return render(request, 'home.html', {
        'page_title': 'Attendance rule assignment',
        'page_header': 'Attendance rule assignment',
        'topnav': site_topnav(get_userrole(request.session['user'])['level']),
        'template': 'notification',
        'content': {
            'notification': 'Rule delete successful',
            'redirect_text': 'Attendance rule page',
            'redirect_url': 'attendance:rulelist',
            'auto_redirect': True,
        },
    })

def edit_rule(request, rule_id):
    if not user_alreadyloggedin(request):
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(username = request.session['user'])
    if not review_permission(user, 'allow:attendance_edit'):
        return HttpResponseRedirect(reverse('index_home')) 

    try:
        rule = Rule.objects.get(pk = rule_id)
    except:
        return HttpResponseRedirect(reverse('attendance:rulelist')) 

    CLASS_CODE_OPTIONS = {i.pk: i.class_name for i in Class_code.objects.all()}
    applied_rule = rule.applied_rule_set.all()

    """
    return render(request, 'home.html', {
        'page_title': 'Room Reservation',
        'page_header': 'Reserve for a room',
        'topnav': site_topnav(get_userrole(request.session['user'])['level']),
        'template': 'detail',
        'content': {
            'fields': (
                ({'title': 'Rule',
                    'content': '',
                    'url_para': '',
                    'url': '',
                    'html_class': '',}),

                ({'title': 'Rule',
                    'content': '',
                    'url_para': '',
                    'url': '',
                    'html_class': '',}),
            ),
        },
    })
    """

    return render(request, 'home.html', {
        'page_title': 'Room Reservation',
        'page_header': 'Reserve for a room',
        'topnav': site_topnav(get_userrole(request.session['user'])['level']),
        'template': 'detail',
        'content': {
            'custom_rule': {
                'block1': rule,
                'block2': applied_rule,
            },
        },
    })

def remove_arule(request, arule_id):
    if not user_alreadyloggedin(request):
        return HttpResponseRedirect(reverse('index'))
    user = User.objects.get(username = request.session['user'])
    if not review_permission(user, 'allow:attendance_edit'):
        return HttpResponseRedirect(reverse('index_home'))

    try:
        rule = Applied_rule.objects.get(pk = arule_id)
    except:
        return HttpResponseRedirect(reverse('attendance:rulelist')) 

    rule.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def rollcall(request):
    response_data = {}

    if request.method == 'GET':
        response_data['status'] = False
        response_data['message'] = 'Please use POST to send the rollcall data'

    elif request.method == 'POST':
        card_id = request.POST.get('card_id', '')
        token = 'b8293a1035a1c929105ea870ecbef6f8'
        received_token = request.POST.get('token', '') == token

        response_data['status'] = False
        response_data['message'] = 'Unknown situation'

        if not card_id:
            response_data['status'] = False
            response_data['message'] = 'No data received'

        
        if not received_token:
            response_data['status'] = False
            response_data['message'] = 'Illegal access'

        if received_token and card_id:
            try:
                user = User.objects.get(card_id=card_id)
                Attandance(user=user).save()

                response_data['status'] = True
                response_data['message'] = 'Attandance logged'
                response_data['user'] = user.username
                response_data['datetime'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

            except ObjectDoesNotExist:
                response_data['status'] = False
                response_data['message'] = 'No user record'

            

    return HttpResponse(json.dumps(response_data), content_type="application/json")
