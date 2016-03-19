from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from django.contrib.auth.hashers import check_password, make_password

from .models import User, Permission, Permission_meta
from inbox.models import Inbox
from classroom.models import Classroom, User_assignment

from .form import UserForm

import random, string
from datetime import datetime

"""
template = ('home', 'list', 'form', 'detail', 'none')
"""

def generate_token(length = 8):
    """
    Generate random token for session
    """
    random_string = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

    return make_password(random_string, hasher='md5')[4:]

def review_permission(user, permission):
    pass
    
def index(request):
    if 'token' in request.session and 'user' in request.session:
        return HttpResponseRedirect(reverse('index_home'))

    if request.GET.get('logout', ''):
        error_message = 'Logout successful, goodbye!'
    else:
        error_message = 'Please log-in before using SchoolPro system.'

    return render(request, 'login.html', {'error_message': error_message})

def index_home(request):
    if not ('token' in request.session and 'user' in request.session):
        return HttpResponseRedirect(reverse('index')+'?login_first')
    
    user = User.objects.get(username = request.session['user'])
    current_sysdate = datetime.now().strftime("%B %d, %Y")

    # inbox count
    inbox_count = Inbox.objects.filter(read=False, receiver=user.id).count()

    # classroom count
    classroom_count = User_assignment.objects.filter(user=user.id).count()

    return render(request, 'home.html', {
        'page_header': 'Good to seeing you, ' + user.lastname,
        'notification': {    
            'current_date': current_sysdate,
            'inbox': inbox_count,
            'classroom': classroom_count,
        },
        'template': 'home',
        'form': UserForm(request.POST),
    })

def login(request):
    redirect_page = 'index'

    # Review login session status
    already_logged = False
    if 'token' in request.session and 'user' in request.session:
        already_logged = True

        # Break process, return to index page
        return render(request, 'login.html', {
            'error_message': "Already logged, token:"+request.session['token'],
        })

    # Login authentication
    login_account = request.POST.get('account', '')
    login_password = request.POST.get('password', '')

    if not (login_account and login_password):
        ## Skip database process, return index page
        return render(request, 'login.html', {
            'error_message': "Login failed: Empty username or password!",
        })
        
    ## Access database for user data
    try:
        user_object = User.objects.get(username = login_account)

    except ObjectDoesNotExist:
        return render(request, 'login.html', {
            'error_message': "Login failed: No such user!",
        })

    ## Check password hash, assign session for logged user
    if check_password(login_password, user_object.password_hash):
        if not already_logged:
            session_timeout_minutes = 30
            request.session.set_expiry(session_timeout_minutes * 60)
            request.session['token'] = generate_token()
            request.session['user'] = user_object.username

        # Redirect to page
        # return render(request, 'login.html', {
        #    'error_message': "Successful logged.",
        # })
        return HttpResponseRedirect(reverse('index_home'))

    return render(request, 'login.html', {
           'error_message': "Looks like these are not your correct details. Please try again.",
        })

def logout(request):
    """
    Logout user account, remove token and user session
    """

    logout_progress = False
    if 'token' in request.session:
        del request.session['token']
        logout_progress = True
    if 'user' in request.session:
        del request.session['user']
        logout_progress = True

    # Logout success, return index page
    if logout_progress:
        return HttpResponseRedirect(reverse('index')+'?logout=True')

    return HttpResponseRedirect(reverse('index'))

def edituser_view(request, process, user = None):
    # case 1: new user -> blank table, sumbit to view "add_user"
    if process == 'add':
        return render(request, 'home.html', {
            'page_header': 'Add a user',
            'template': 'form',
            'form': UserForm(request.POST),
        })

    elif process == 'modify':
        pass

def adduser_view(request):
    return render(request, 'home.html', {
        'page_header': 'Add a user',
        'template': 'form',
        'redirect_url': 'user:add_user',
        'form': UserForm().as_ul(),
    })

def modifyuser_view(request, username):
    user_object = get_object_or_404(User, username = username)

    edituser_view(request, process='modify', user=user_object)

def add_user(request):
    # form check
    form = UserForm(request.POST)
    if not form.is_valid():
        return HttpResponse('No enoughs parameters received')

    try:
        form.save(commit=False)
        form.save()
    
    except:
        pass

    return HttpResponse('user added.')


def remove_user(request):
    if not request.POST.get(remove_confirm, ''):
        return HttpResponse('User does not removed')

    try:
        delete_obj = get_object_or_404(User, pk=request.POST.get(user_id))
        delete_obj.delete()

    except IntegrityError:
        pass

    return HttpResponse('user removed.')


def modify_user(request, user_id):
    return HttpResponse(user_id)

def view_user(request, user_id, specific_usertype=None):
    pass

def list_user(request, page=1, row_count=50, specific_usertype=None, classcode=None):
    pass

    # case 1: list all user
    # case 2: list specific_usertype
    # case 3: filter class_code
    # case 4: search mode (GET + POST data)
