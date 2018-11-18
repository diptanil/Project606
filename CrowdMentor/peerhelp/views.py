# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Question, Answer, QuestionVotes, AnswerVotes

from .forms import QuestionForm, AnswerForm

@login_required
def index(request):
    questions = Question.objects.all()
    context = {
            'questions': questions,
        }
    return render(request, 'questions/index.html', context)

@login_required
def add_question(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            ques = form.save(commit=False)
            ques.creator_id = user
            ques.save()
            messages.info(request, 'New Question Added')
            return HttpResponseRedirect('/help/')
    else:
        form = QuestionForm()
    return render(request, 'questions/add_question.html', {'form': form})

@login_required
def detail(request, ques_id):
    user = User.objects.get(username=request.user.username)
    try:
        ques = Question.objects.get(pk=ques_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.question = ques
            ans.creator_id = user
            ans.save()
            messages.info(request, 'New Answer Added')
            return HttpResponseRedirect(request.path_info)
    else:
        answers = Answer.objects.filter(question = ques)
        form = AnswerForm()
    context = {
            'question':ques,
            'answers': answers,
            'form': form
        }
    return render(request, 'questions/detail.html', context)

@login_required
def ques_upvote(request, ques_id):
    user = User.objects.get(username=request.user.username)
    try:
        ques = Question.objects.get(pk=ques_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    vote_exist = QuestionVotes.objects.filter(voter_id=user, question=ques, up_vote = True)
    if  vote_exist:
        messages.info(request, 'You already liked this')
        return HttpResponseRedirect('/help/')
    else:
        ques_votes = QuestionVotes()
        ques_votes.question = ques
        ques_votes.voter_id = user
        ques_votes.up_vote = True
        ques_votes.save()
        ques.up_votes += 1
        ques.save()
    return HttpResponseRedirect('/help')

@login_required
def ans_upvote(request, ques_id, ans_id):
    user = User.objects.get(username=request.user.username)
    try:
        ans = Answer.objects.get(pk=ans_id)
    except AnswerVotes.DoesNotExist:
        raise Http404("Question does not exist")
    vote_exist = AnswerVotes.objects.filter(voter_id=user, answer=ans, up_vote = True)
    if  vote_exist:
        messages.info(request, 'You already liked this')
        return HttpResponseRedirect('/help/'+str(ques_id)+'/')
    else:
        ans_votes = AnswerVotes()
        ans_votes.answer = ans
        ans_votes.voter_id = user
        ans_votes.up_vote = True
        ans_votes.save()
        ans.up_votes += 1
        ans.save()
    return HttpResponseRedirect('/help/'+str(ques_id)+'/')


@login_required
def ques_downvote(request, ques_id):
    user = User.objects.get(username=request.user.username)
    try:
        ques = Question.objects.get(pk=ques_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    vote_exist = QuestionVotes.objects.filter(voter_id=user, question=ques, down_vote = True)
    if  vote_exist:
        messages.info(request, 'You already disliked this')
        return HttpResponseRedirect('/help/')
    else:
        ques_votes = QuestionVotes()
        ques_votes.question = ques
        ques_votes.voter_id = user
        ques_votes.down_vote = True
        ques_votes.save()
        ques.down_votes += 1
        ques.save()
    return HttpResponseRedirect('/help')

@login_required
def ans_downvote(request, ques_id, ans_id):
    user = User.objects.get(username=request.user.username)
    try:
        ans = Answer.objects.get(pk=ans_id)
    except Answer.DoesNotExist:
        raise Http404("Question does not exist")
    vote_exist = AnswerVotes.objects.filter(voter_id=user, answer=ans, down_vote = True)
    if  vote_exist:
        messages.info(request, 'You already disliked this')
        return HttpResponseRedirect('/help/'+str(ques_id)+'/')
    else:
        ans_votes = AnswerVotes()
        ans_votes.answer = ans
        ans_votes.voter_id = user
        ans_votes.down_vote = True
        ans_votes.save()
        ans.down_votes += 1
        ans.save()
    return HttpResponseRedirect('/help/'+str(ques_id)+'/')