from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

### Generic View (class-based views)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    """Return the last five published questions."""
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        checked_list = request.POST.getlist('choice') #선택된 선택지들의 value를 리스트로 받아옴
        selected_choices = [] #choice_set의 값을 저장할 리스트 생성

        for i in range(len(checked_list)): #선택된 선택지의 개수만큼 반복
            selected_choice = question.choice_set.get(pk=checked_list[i]) #선택된 값의 choice_set 값을 저장
            selected_choices.append(selected_choice) #차례대로 리스트에 추가

    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message': "You didn't select a choice.",
        })
    else:
        for i in range(len(selected_choices)): #선택된 값의 개수만큼 반복
            selected_choices[i].votes += 1 #선택된 값의 투표값을 1씩 증가시킨다
            selected_choices[i].save() #투표 수를 저장한다

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))