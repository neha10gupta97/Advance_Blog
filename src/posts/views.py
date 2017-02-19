from urllib import quote_plus
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render ,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Post
from .forms import PostForm
# Create your views here.
def post_create(request):
    form = PostForm(request.POST or None,request.FILES or None)   #for making fileds required
    if form.is_valid():
        instance = form.save(commit=False)
        print form.cleaned_data.get("title")
        instance.save()
        messages.success(request,"Successsfully Created") #,extra_tags="html_safe/something"
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not Successsfully Created")
    # if request.method=="POST":
    #     print request.POST.get("content")    #will except empty values
    #     print request.POST.get("title")
    context={
        "form":form
    }
    return render(request, "post_form.html", context)

def post_detail(request,slug=None):  #retrieve
    instance = get_object_or_404(Post,slug=slug)
    share_string= quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string":share_string,
    }
    return render(request,"post_detail.html",context)

def post_list(request):  #list_items
    queryset_list = Post.objects.all() #order_by("-timestamp")
    paginator = Paginator(queryset_list, 10)  # Show 25 contacts per page
    page_request_var ='page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context={
        "object_list" : queryset,
        "title":"List",
        "page_request_var":page_request_var
    }
    # if request.user.is_authenticated():  #if admin is logged in
    #     context={
    #         "title":"My users list"
    #     }
    # else:
    #     context={
    #         "title":"List"
    #     }
    return render(request,"post_list.html",context)



def post_update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,request.FILES or None,instance=instance)  # for making fileds required
    if form.is_valid():
        instance = form.save(commit=False)
        print form.cleaned_data.get("title")
        instance.save()
        messages.success(request, "Successsfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())   #message succes


    context = {
        "title": instance.title,
        "instance": instance,
        "form":form
    }
    return render(request, "post_form.html", context)

def post_delete(request,slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successsfully Deleted")
    return redirect("posts:list")

