import json
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.decorators.http import require_http_methods, require_POST, require_GET, require_safe
from django.template.loader import get_template, render_to_string
from django.db.models import Count
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User

from bboard.forms import BbForm
from bboard.models import Bb, Rubric

from .models import Task
from .forms import TaskForm

# def index(request):
#     resp = HttpResponse('Здесь будет', content_type='text/plain; charset=utf-8')
#     resp.write(' главная')
#     resp.writelines((' страница', ' сайта'))
#     resp['keywords'] = 'Python, Django'
#     return resp

# def index(request):
#     bbs = Bb.objects.order_by('-published')
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#     context = {'bbs' : bbs, 'rubrics': rubrics}
#     template = get_template('index.html')
#     return HttpResponse(template.render(context, request))

# def index(request):
#     bbs = Bb.objects.order_by('-published')
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#     context = {'bbs' : bbs, 'rubrics': rubrics}
#     return HttpResponse(render_to_string('index.html', context, request))

# def index(request):
#     s = 'Список объявлений\r\n\r\n\r\n'
#
#     for bb in Bb.objects.order_by('-published'):
#         s += bb.title + '\r\n' + bb.content + '\r\n\r\n'
#
#     return HttpResponse(s, content_type='text/plain; charset=utf-8')


# def index(request):
#     template = loader.get_template('index.html')
#     bbs = Bb.objects.order_by('-published')
#     context = {'bbs': bbs}
#
#     return HttpResponse(template.render(context, request))


# def index(request):
#     bbs = Bb.objects.order_by('-published')
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#     context = {'bbs': bbs, 'rubrics': rubrics}
#
#     return render(request, 'index.html', context)

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.order_by('-published')
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        context['current_rubric'] = {'bbs': context['bbs'], 'rubrics': context['rubrics']}
        return context



def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)

    context = {'bbs': bbs, 'rubrics': rubrics,
               'current_rubric': current_rubric}

    # url = reverse('by_rubric', kwargs={'rubric_id': 2})

    return render(request, 'by_rubric.html', context)

# class BbRubricBbsView(TemplateView):
#     template_name = 'by_rubric.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         return context

class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    # success_url = reverse_lazy('bboard:index')
    # success_url = '/bb/{id}'
    success_url = '/rubric/{rubric_id}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context

# class BbCreateView(View):
#     def get(self, request, *args, **kwargs):
#         form = BbForm()
#         context = {'form': form, 'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}
#         return render(request, 'create.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = BbForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('bboard:by_rubric',
#                                                 kwargs={'rubric_id': form.cleaned_data['rubric'].pk}))
#         else:
#             context = {'form': form, 'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)}
#             return render(request, 'create.html', context)


def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'create.html', context)

def add_save(request):
    bbf = BbForm(request.POST)
    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(reverse('bboard:by_rubric',
                                            kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'create.html', context)

def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric',
                                                kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'create.html', context)

@require_http_methods(['GET', 'POST'])
def bb_detail(request, bb_id):
    try:
        # bb = Bb.objects.get(pk=bb_id)
        bb = get_object_or_404(Bb, pk=bb_id)
        rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        context = {'bb': bb, 'rubrics': rubrics}
    except Bb.DoesNotExist:
        # return HttpResponseNotFound('Такого объявления не существует')
        raise Http404('Такого объявления не существует')

    return render(request, 'bb_detail.html', context)
    # return redirect('bboard:index', rubric_id=bb.rubric.pk)

class BbDetailView(DetailView):
    model = Bb
    # template_name = 'bb_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


class BbRubricBbsView(ListView):
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context

class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/rubric/{rubric_id}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context

#PR 05.03.26
def logging_check(request):
    login = request.GET.get("login")
    if not login:
        return redirect("/no_login/")
    with open("request_log.txt", "a", encoding="utf-8") as file:
        file.write(f"Path: {request.path}\n")
        file.write(f"Method: {request.method}\n")
        file.write(f"GET: {request.GET}\n")
        file.write(f"POST: {request.POST}\n")
    return HttpResponse("Пользователь авторизрован")

def no_login(request):
    return HttpResponse("Нет логина")

#PR 12.03.26
class FirstUserView(TemplateView):
    template_name = 'first_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_user'] = User.objects.first()
        return context

# def bb_detail(request, bb_id):
#     bb = Bb.objects.get(pk=bb_id)
#     # data = {'title': 'Мотоцикл', 'content': 'Старый', 'price': 10_000.0}
#     data = {'title': bb.title, 'content': bb.content, 'price': bb.price}
#     return JsonResponse(data)

#PR
# def index(request):
#     return HttpResponse('Здесь был текст 1 задания', content_type='text/plain; charset=utf-8')

# def index(request):
#     text_html = """
#         <h1>Тут </h1>
#         <i>уже </i>
#         <b>второе задание</b>
#         """
#     return HttpResponse(text_html)

#dz
# def sms_list(request):
#     sms_list = SMS.objects.all().order_by("-id")
#     return render(request, "templates/sms_list.html", {"sms_list": sms_list})

#LIST ZADACH
def index(request):
    tasks = Task.objects.all()[:5]
    return render(request, 'tasks/index.html', {'tasks': tasks})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task':task})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
        else:
            form = TaskForm()
        return render(request, 'tasks/task_create.html', {'form':form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_detail', pk=task.pk)
        else:
            form = TaskForm(instance=task)
        return render(request, 'tasks/task_update.html', {'form':form, 'task': task})