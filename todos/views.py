from django.shortcuts import render, HttpResponse
from django.http import (
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    HttpResponseForbidden,
    # HttpResponseNotModified,
)
from django.core.handlers.wsgi import WSGIRequest
from .models import Permission, Project, User, Todo, Task


def new_project(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    username = request.POST.get("user")
    if username and User.objects.filter(username=username).count() == 0:
        return HttpResponseNotFound("目标用户不存在!")
    user = User.objects.get(username=username)

    name = request.POST.get("name")

    level = request.POST.get("level")
    if Permission.objects.filter(level=level).count() == 0:
        return HttpResponseNotFound("权限不存在!")
    permission = Permission.objects.get(level=level)
    # elif Permission.objects.get(level=level) > workas.permission.level:
    #     return HttpResponseForbidden("权限不足, 拒绝访问.")

    priority = request.POST.get("priority")
    content = request.POST.get("content")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")

    Project.objects.create(
        user=user,
        name=name,
        permission=permission,
        priority=priority,
        content=content,
        start_time=start_time,
        end_time=end_time,
        is_checked=False,
    )
    return HttpResponse("新项目创建成功!")


def new_todo(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    pid = request.POST.get("project")
    if pid and Project.objects.filter(id=pid).count() == 0:
        return HttpResponseNotFound("目标项目不存在!")
    project = Project.objects.get(id=pid)
    # else:
    #     project = Project.objects.get(id=pid)
    #     if project.is_checked:
    #         return HttpResponseNotModified("目标项目已经结项!")

    username = request.POST.get("user")
    if username and User.objects.filter(username=username).count() == 0:
        return HttpResponseNotFound("目标用户不存在!")
    user = User.objects.get(username=username)

    name = request.POST.get("name")

    level = request.POST.get("level")
    if Permission.objects.filter(level=level).count() == 0:
        return HttpResponseNotFound("权限不存在!")
    permission = Permission.objects.get(level=level)
    # elif Permission.objects.get(level=level) > workas.permission.level:
    #     return HttpResponseForbidden("权限不足, 拒绝访问.")

    priority = request.POST.get("priority")
    content = request.POST.get("content")
    desc = request.POST.get("desc")
    startline = request.POST.get("startline")
    endline = request.POST.get("endline")
    tid = request.POST.get("parent")
    if Todo.objects.filter(id=tid).count() == 0:
        return Todo.objects.get(id=tid)
    parent = Todo.objects.get(id=tid)

    Todo.objects.create(
        project=project,
        user=user,
        name=name,
        permission=permission,
        priority=priority,
        content=content,
        desc=desc,
        start_time=startline,
        duration=endline,
        parent=parent,
        is_checked=False,
    )
    return HttpResponse("新任务创建成功!")


def new_task(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    pid = request.POST.get("project")
    if pid and Project.objects.filter(id=pid).count() == 0:
        return HttpResponseNotFound("目标项目不存在!")
    project = Project.objects.get(id=pid)
    # else:
    #     project = Project.objects.get(id=pid)
    #     if project.is_checked:
    #         return HttpResponseNotModified("目标项目已经结项!")

    username = request.POST.get("user")
    if User.objects.filter(username=username).count() == 0:
        return HttpResponseNotFound("目标用户不存在!")
    user = User.objects.get(username=username)

    name = request.POST.get("name")

    level = request.POST.get("level")
    if Permission.objects.filter(level=level).count() == 0:
        return HttpResponseNotFound("权限不存在!")
    permission = Permission.objects.get(level=level)
    # elif Permission.objects.get(level=level) > workas.permission.level:
    #     return HttpResponseForbidden("权限不足, 拒绝访问.")

    priority = request.POST.get("priority")
    content = request.POST.get("content")
    desc = request.POST.get("desc")
    start_time = request.POST.get("start_time")
    duration = request.POST.get("duration")
    tid = request.POST.get("parent")
    if Task.objects.filter(id=tid).count() == 0:
        return HttpResponseNotFound("父进程不存在!")
    parent = Task.objects.get(id=tid)

    Task.objects.create(
        project=project,
        user=user,
        name=name,
        permission=permission,
        priority=priority,
        content=content,
        desc=desc,
        start_time=start_time,
        duration=duration,
        parent=parent,
        is_checked=False,
    )
    return HttpResponse("新任务创建成功!")


def take_project(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    pid = request.POST.get("id")
    if pid and Project.objects.filter(id=pid).count() == 0:
        return HttpResponseNotFound("目标项目不存在!")
    project = Project.objects.get(id=pid)
    if project.user:
        return HttpResponseForbidden("目标项目已经被承接了.")

    Project.objects.filter(id=pid).update(user=User.objects.get(username=request.session.get("username")))
    return HttpResponse("项目承接成功!")

def take_task(request: WSGIRequest):
    if request.method == "GET":
        return HttpResponseNotAllowed("POST")

    pid = request.POST.get("id")
    if pid and Task.objects.filter(id=pid).count() == 0:
        return HttpResponseNotFound("目标项目不存在!")
    task = Task.objects.get(id=pid)
    if task.user:
        return HttpResponseForbidden("目标项目已经被承接了.")

    Task.objects.filter(id=pid).update(user=User.objects.get(username=request.session.get("username")))
    return HttpResponse("任务承接成功!")



    