from django.http import HttpResponse
from django.shortcuts import render ,get_object_or_404

from .models import Post
from .form import PostForm
# Create your views here.
def post_create(request):
    form = PostForm(request.POST or None)   #for making fileds required
    if form.is_valid():
        instance = form.save(commit=False)
        print form.cleaned_data.get("title")
        instance.save()
    # if request.method=="POST":
    #     print request.POST.get("content")    #will except empty values
    #     print request.POST.get("title")
    context={
        "form":form
    }
    return render(request, "post_form.html", context)

def post_detail(request,id=None):  #retrieve
    instance = get_object_or_404(Post,id=id)
    context = {
        "title": instance.title,
        "instance": instance
    }
    return render(request,"post_detail.html",context)

def post_list(request):  #list_items
    query = Post.objects.all()
    context={
        "object_list" : query,
        "title":"List"
    }
    # if request.user.is_authenticated():  #if admin is logged in
    #     context={
    #         "title":"My users list"
    #     }
    # else:
    #     context={
    #         "title":"List"
    #     }
    return render(request,"index.html",context)

def post_update(request):
    return HttpResponse("<h1>UPDATE</h1>")

def post_delete(request):
    return HttpResponse("<h1>DELETE</h1>")

