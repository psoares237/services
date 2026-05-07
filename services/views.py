from services.models import Service
from services.forms import ServiceModelForm
from openai_api.client import get_service_ai_value

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


class ServiceListView(ListView):
    model = Service
    template_name = 'services.html'
    context_object_name = 'services'

    def get_queryset(self):
        services = super().get_queryset().order_by('name')
        search = self.request.GET.get('search')

        if search:
            services = services.filter(name__icontains=search)

        return services


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class NewServiceCreateView(CreateView):
    model = Service
    form_class = ServiceModelForm
    template_name = 'new_service.html'
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        service = form.save(commit=False)

        if not service.value_generated:
            service.value_generated = get_service_ai_value(
                service.name,
                service.category.name
            )

        service.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceModelForm
    template_name = 'service_update.html'

    def form_valid(self, form):
        service = form.save(commit=False)

        if not service.value_generated:
            service.value_generated = get_service_ai_value(
                service.name,
                service.category.name
            )

        service.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('service_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = reverse_lazy('services')