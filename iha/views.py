from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def DashboardPage(request):
    context = {}
    return render(request, 'dashboard/index.html', context=context)

@login_required
def ihaAddPage(request):
    context = {}
    return render(request, 'iha/add.html', context=context)

def ihaListPage(request):
    context = {}
    return render(request, 'iha/list.html', context=context)

@login_required
def ihaUpdatePage(request,id):
    context = {
        "ihaId":id
    }
    return render(request, 'iha/update.html', context=context)


def handler404(request, *args, **argv):
    return render(request,'error_page/404.html')
