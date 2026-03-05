import json
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.decorators.http import require_http_methods, require_POST, require_GET, require_safe
from django.template.loader import get_template, render_to_string
from django.db.models import Count

from bboard.forms import BbForm
from bboard.models import Bb, Rubric

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


def index(request):
    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bbs': bbs, 'rubrics': rubrics}

    return render(request, 'index.html', context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)

    context = {'bbs': bbs, 'rubrics': rubrics,
               'current_rubric': current_rubric}

    # url = reverse('by_rubric', kwargs={'rubric_id': 2})

    return render(request, 'by_rubric.html', context)


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

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