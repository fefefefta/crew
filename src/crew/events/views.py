from re import template
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView 

from .models import Event


class FeedView(ListView):
    model = Event
    template_name = 'events/feed.html'


class EventDetailView(DetailView):
    model = Event
    object_context_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['user'] = self.request.user
        return context


class EventCreateView(CreateView):
    model = Event
    fields = ['title', 'text', 'participants_limit', 'price', 'link_to_chat', 
        'event_date']
    template_name = 'events/new.html'
    success_url = '../'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        
        self.object.save()
        return super().form_valid(form)


class EventEditView(UpdateView):
    model = Event
    object_context_name = 'event'
    fields = ['title', 'text', 'participants_limit', 'price', 'link_to_chat', 
        'event_date']
    template_name = 'events/event_edit.html'
    success_url = '../'
