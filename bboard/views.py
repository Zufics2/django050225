from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric


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
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}

    return render(request, 'index.html', context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)

    context = {'bbs': bbs, 'rubrics': rubrics,
               'current_rubric': current_rubric}

    return render(request, 'by_rubric.html', context)


class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
