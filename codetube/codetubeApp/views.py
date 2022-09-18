from django.shortcuts import render, redirect
from .models import *      # from codetubeApp.models import *
from django.contrib import messages
import bcrypt


# General Routes ----------------------------------------------------------------------------

def index(request):
    context = {
        'all_videos' : Video.objects.all()
    }
    return render(request, 'index.html', context)

# need to add search term here as a path param then run filter query on sql light
def search(request): 
    return render(request, 'search.html')


# Testing Routes ----------------------------------------------------------------------------

# def login_reg(request):
#     return render(request, 'login_reg.html')

# def dashboard(request):
#     return render(request, 'dashboard.html')

# def new_video(request):
#     return render(request, 'new_video.html')

# def edit_video(request):
#     return render(request, 'edit_video.html')

# def play(request):
#     return render(request, 'play.html')


# Login and Registration --------------------------------------------------------------------

# maybe let them go here and if they are logged in render logout button "you are logged in as xyz click here to log out"
def login_reg(request):
    return render(request, 'login_reg.html')

# Register a New User
def register(request):
    if request.method=='POST':
        errors = User.objects.reg_validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/login_reg')
        user_pw = request.POST['password']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hash_pw)
        request.session['user_id'] = new_user.id
        request.session['user_name'] = f"{new_user.first_name} {new_user.last_name}"
        return redirect('/dashboard')
    return redirect('/')

# Login - add if already logged in then what?
def login(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_name'] = f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/dashboard')
            else:
                messages.error(request,"Password is incorrect.")
        else:
            messages.error(request,"Email was not found.")
    return redirect('/')

# Logout
def logout(request):
    request.session.clear()
    return redirect('/')

# Dashboard - Check if Logged in
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user,
        'all_videos': Video.objects.all(),
        'all_likes': Liked.objects.all(),
    }
    return render(request,'dashboard.html', context)


# Videos ------------------------------------------------------------------------------------

# Play video - NEED TO ADD INCRIMENT ONE VIEW, what is sql lite equivelent to patch request to update one field
def play_video(request, id):
    context = {
        'video' : Video.objects.get(id=id)
    }
    # Video.objects.views 
    return render(request, 'play.html', context)

# New video form page
def new_video(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'new_video.html')

# Create a new video
def create_video(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method=='POST':
        errors = Video.objects.video_validate(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/new_video')
        Video.objects.create(title=request.POST['title'],video=request.POST['video'],thumbnail=request.POST['thumbnail'],description=request.POST['description'],user=User.objects.get(id=request.session['user_id']))
        return redirect('/dashboard')
    return redirect('/new_video')

# Edit video form page
def edit_video(request, id):
    if 'user_id' not in request.session: 
        return redirect('/')
    video = Video.objects.get(id=id)
    if request.session['user_id'] != video.user.id:
        return redirect('/')
    context = {
        'video' : Video.objects.get(id=id)
    }
    return render(request, 'edit_video.html', context)

# Update video
def update_video(request, id):
    if 'user_id' not in request.session: 
        return redirect('/')
    video = Video.objects.get(id=id)
    if request.session['user_id'] != video.user.id:
        return redirect('/')
    if request.method=='POST':
        errors = Video.objects.video_validate(request.POST) # create video validations same as update?
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(f"/edit_video/{id}")
        video = Video.objects.get(id=id)
        video.title=request.POST['title']
        video.video=request.POST['video']
        video.thumbnail=request.POST['thumbnail']
        video.description=request.POST['description']
        video.save()
        return redirect('/dashboard')
    return redirect('/edit_video/<int:id>')

# Delete video - Completed
def delete_video(request, id):
    if 'user_id' not in request.session: 
        return redirect('/')
    video = Video.objects.get(id=id)
    if request.session['user_id'] != video.user.id:
        return redirect('/')
    video = Video.objects.get(id=id)
    video.delete()
    return redirect('/dashboard')


# Likes -------------------------------------------------------------------------------------

# def like_video(request):
#     if request.method=='POST':
#         Liked.objects.create(liked=request.POST['liked'], user=User.objects.get(id=request.session['user_id']), video=request.POST['video'])
#         context = {
#             'all_likes': Liked.objects.all.count()
#         }
#         return redirect('/success')

#  def unlike_video










# Other Notes -------------------------------------------------------------------------------

# def account_page(request,id):
#     context = {
#         'user': User.objects.get(id=id)
#     }
#     return render(request,'edit_account.html',context)

# def user_page(request,id):
#     user = User.objects.get(id=id)
#     context = {
#         'user': user
#     }
#     return render(request,'user_page.html', context)

# Update a user if we wanted to add
# def update_user(request,id):
#     if request.method=='POST':
#         ## validations
#         errors = User.objects.update_validate(request.POST)
#         if errors:
#             for error in errors:
#                 messages.error(request, errors[error])
#             return redirect(f"/myaccount/{id}")
#         user = User.objects.get(id=id)
#         user.first_name=request.POST['first_name']
#         user.last_name=request.POST['last_name']
#         user.email=request.POST['email']
#         user.save()
#         request.session['user_name'] = f"{user.first_name} {user.last_name}"
#         return redirect('/success')
#     return redirect('/myaccount/<int:id>')