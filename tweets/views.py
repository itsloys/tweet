# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy

from django.views.generic import (
	CreateView,
	DetailView,
	DeleteView,
	ListView,
	UpdateView
	)

from .forms import TweetModelForm

from .models import Tweet

from .mixins import FormUserNeededMixin, UserOwnerMixin

# Create your views here.

class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = 'tweets/create_view.html'
	# success_url = reverse_lazy("tweet:detail")
	login_url = "/admin/login/"

class TweetUpdateView(UserOwnerMixin, LoginRequiredMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = 'tweets/update_view.html'
	# success_url = '/tweet/'

class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweet
	success_url = reverse_lazy("tweet:list")
	template_name = 'tweets/delete_confirm.html'
	

class TweetDetailView(DetailView):
	queryset = Tweet.objects.all()

class TweetListView(ListView):
	def get_queryset(self, *args, **kwargs):
		qs = Tweet.objects.all()
		# print(self.request.GET)
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
					Q(content__icontains=query)|
					Q(user__username__icontains=query)
					)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		context['create_form'] = TweetModelForm()
		context['create_url'] = reverse_lazy('tweet:create')
		return context