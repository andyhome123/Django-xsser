import json
import os
import uuid
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import project, record, account

@login_required(login_url="/login/")
def createProject(request):
    if request.method == "POST":
        try:
            ant = account.objects.get(user_id=request.user)
        except account.DoesNotExist:
            ant = account.objects.create(user_id=request.user)
        title = request.POST.get('title')
        paramter = request.POST.getlist('get_paramter', '')
        if paramter is not None:
            get_paramter=','.join(paramter)
        if not title:
            return HttpResponse('title empty')
        id = str(uuid.uuid4())
        js_content = request.POST.get('js_content')
        js = bool(js_content)
        if js is True:
            f = open('/home/junyi/envs/env1/mysite2/templates/js/%s' % (id,) , 'w')
            f.write(js_content)
            f.close()
        try:
            ppp = project.objects.create(pk=id, js=js, title=title, js_content=js_content,get_paramter=get_paramter)
            ant.project.add(ppp)
            ant.save()
        except TypeError:
            return Http404('TypeError')
        return HttpResponseRedirect('/show/')
    return render(request, 'create.html')


@login_required(login_url="/login/")
def projectDetail(request):
    id = request.GET.get("id", "-1")
    try:
        ant = account.objects.get(user_id=request.user)
        a = ant.project.get(pk=id)
    except project.DoesNotExist:
        raise Http404('fail id')
    l = []
    pp = []
    rid = []
    aa = a.get_paramter.split(',')
    time = []
    for item in a.records.all():
        l.append(json.loads(item.data))
        pp.append(json.loads(item.paramter))
        rid.append(item.id)
        time.append(item.create_time)
    return render(request, 'detail.html', {'l':zip(l,pp,rid,time), 'a':aa,'project':a})



@login_required(login_url="/login/")
def projectInfo(request):
    id = request.GET.get("id", "-1")
    try:
        ant = account.objects.get(user_id=request.user)
        a = ant.project.get(pk=id)
    except project.DoesNotExist:
        raise Http404('fail id')
    return render(request, 'info.html', {'a': a })

def projectJs(request):
    id = request.GET.get("id", "-1")
    f = open('/home/junyi/envs/env1/mysite2/templates/js/%s' % (id,) , 'r')
    data = f.read()
    response = HttpResponse(data, content_type='application/x-javascript')
    response['Cache-Control'] = 'nocache'
    response['Pragma'] = 'no-cache'
    response['Server'] = 'Server'
    response['X-Powered-By'] = 'Powered'
    return response



@login_required(login_url="/login/")
def projectDelete(request, id):
    if request.method == 'GET':
        try:
            ant = account.objects.get(user_id=request.user)
            a = ant.project.get(pk=id)
        except project.DoesNotExist:
            raise Http404()
        a.records.all().delete()
        a.delete()
        f = '/home/junyi/envs/env1/mysite2/templates/js/%s' % (id,)
        if os.path.isfile(f):
            os.remove(f)
        else:
            return Http404('file does not exist')


@login_required(login_url="/login/")
def projectChange(request, id):
    if request.method == 'POST':
        js_content = request.POST.get("js_content", "")
        try:
            ant = account.objects.get(user_id=request.user)
            a = ant.project.get(pk=id)
        except project.DoesNotExist:
            raise Http404('fail id')
        paramter = request.POST.getlist('get_paramter', '')
        if paramter is not None:
            get_paramter=','.join(paramter)
        else:
            get_paramter=''
        js = bool(js_content)
        if js is True:
            f = open('/home/junyi/envs/env1/mysite2/templates/js/%s' % (id,) , 'w+')
            f.write(js_content)
            f.close()

        a.js_content = js_content
        a.get_paramter=get_paramter
        a.save()
        return HttpResponseRedirect('/info/?id='+id)
    else:
        try:
            ant = account.objects.get(user_id=request.user)
            a = ant.project.get(pk=id)
        except project.DoesNotExist:
            raise Http404('fail id')
        get_paramter = a.get_paramter.split(',')
        if '\r\n' in get_paramter:
            return render(request, 'change.html', {'a':a})
        if a.get_paramter == '':
            return render(request, 'change.html', {'a':a})
        return render(request, 'change.html', {'a':a,'p':get_paramter})


@login_required(login_url="/login/")
def showAllProject(request):
    try:
        ant = account.objects.get(user_id=request.user)
    except account.DoesNotExist:
        ant = account.objects.create(user_id=request.user)
    a = ant.project.all()
    return render(request, 'show.html', { 'p' :a })


def projectApi(request):
    if request.method == "GET":
        browser_data = dict(agent = request.META.get('HTTP_USER_AGENT'), ip = request.META.get('REMOTE_ADDR'),
                referer = request.META.get('HTTP_REFERER'))
        id = request.GET.get('id')
        try:
            p = project.objects.get(pk=id)
        except project.DoesNotExist:
            raise Http404('no data')
        paramter = p.get_paramter.split(',')
        data = {}
        data['browser_data'] = browser_data
        data2 = {}
        for key in request.GET:
            value = request.GET.get(key)
            if key in paramter:
                data2[key] = value
        fin = json.dumps(data)
        fin2 = json.dumps(data2)
        r = record.objects.create(data=fin, paramter=fin2)
        p.records.add(r)
        p.save()
        return Http404()





@csrf_exempt
def test(request):
    if request.method == 'POST':
        ids = request.POST.get('recordid', 'failj')
        if ids != 'failj':
            data = ids.split(',')
            for id in data:
                try:
                    record.objects.get(pk=id).delete()
                except record.DoesNotExist:
                    continue
    else:
        return HttpResponse('fail')
