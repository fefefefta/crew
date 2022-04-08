from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView 

from .models import Event
from .services import notify_staff_to_publish


class FeedView(ListView):
    queryset = Event.objects.filter(is_approved=True)
    template_name = 'events/feed.html'


class EventDetailView(DetailView):
    model = Event
    object_context_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['user'] = self.request.user
        return context

    def get_object(self):
        event = super().get_object()
        if event.is_approved or self.request.user.is_staff:
            return event

        raise Exception('u r not allowed to be here zhulic')


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

        notify_staff_to_publish(self.object)

        return super().form_valid(form)


class EventEditView(UpdateView):
    model = Event
    object_context_name = 'event'
    fields = ['title', 'text', 'participants_limit', 'price', 'link_to_chat', 
        'event_date']
    template_name = 'events/event_edit.html'
    success_url = '../'

    def get_object(self):
        event = super().get_object()
        if event.author == self.request.user:
            return event

        raise Exception('u r not allowed to be here zhulic')


def event_approve(request, pk):
    event = Event.get_by_pk(pk)
    if request.user.is_staff and not event.is_approved:
        event.approve()
        return redirect('event', pk)

    raise Exception('u r not allowed to be here zhulic')
