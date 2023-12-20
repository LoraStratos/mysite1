from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db.models import Sum, F, FloatField
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.functions import Cast
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, DeleteView, RedirectView, CreateView
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import *
from .forms import *

class Registration(CreateView):
    form_class = RegistrationForm
    template_name = 'admin/registration.html'
    success_url = reverse_lazy('profile')

    def registration(self):
        return render(self, 'admin/registration.html')

class LoginViewMy(LoginView):
    form_class = AuthenticationForm
    template_name = 'admin/login.html'
    success_url = reverse_lazy('profile')

class Profile(UpdateView):
    model = User
    fields = ['name', 'surname', 'mail', 'avatar']
    success_url = reverse_lazy('index')
    template_name = 'admin/profile.html'

class UserDelete(DeleteView):
    model = User
    context_object_name = 'user'
    template_name = 'delete_success.html'
    success_url = reverse_lazy('index')

    def user(self, pk):
        user = User.objects.filter(user=self.request.user, pk=pk)
        if user:
            user.delete()
        return redirect('index')

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')

    def index(self):
        return render(self, 'index.html')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

    def dispatch(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if VotedUsers.objects.filter(user=request.user, question=question.pk).exists():
            var=int(kwargs['pk'])
            return RedirectView.as_view(url='results')(request, *args, **kwargs)
            return redirect(reverse('results', args= (var)))

        stub = Question.objects.get(pk=kwargs['pk'])
        if stub.was_published_recently():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('index'))

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = Question.objects.get(pk=self.kwargs['pk'])
        total_votes = q.choice_set.aggregate(total_votes=Sum(Cast('votes', FloatField())))['total_votes']
        choices_with_percent = (q.choice_set.annotate(percent=(F('votes') / total_votes) * 100)
                                .values('choice_text', 'percent'))
        context['question'] = q
        context['total_votes'] = total_votes
        context['choices_with_percents'] = choices_with_percent
        return context

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': 'Вы не сделали выбор'
        })
    else:
        if VotedUsers.objects.filter(user=request.user, question=question.pk).exists():
            return HttpResponseRedirect(reverse('results', args=(question.id,)))
        else:
            VotedUsers.objects.create(user=request.user, question= question)
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('results', args=(question.id,)))

class HistoryList(generic.ListView):
    model = Question
    template_name = 'historylist.html'
    context_object_name = 'list'
