from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Avg, Count, Max, Min

from bookapp.forms import BookForm
from bookapp.models import Book


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required='bookapp.add_book'
    model = Book
    form_class = BookForm
    template_name = 'bookapp/form.html'
    success_url = reverse_lazy('book_list')

class BookList(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'bookapp/list.html'
    paginate_by = 10

    ALLOWED_SORT_FIELDS = ['title', 'pages', 'rating', 'status', 'published_date']

    def get_queryset(self):
        queryset = Book.objects.all()

        
        title = self.request.GET.get('title', '')
        if title:
            queryset = queryset.filter(title__icontains=title)

        
        sort = self.request.GET.get('sort', 'title')
        direction = self.request.GET.get('direction', 'asc')

        if sort not in self.ALLOWED_SORT_FIELDS:
            sort = 'title'
        if direction not in ['asc', 'desc']:
            direction = 'asc'

        if direction == 'desc':
            queryset = queryset.order_by(f'-{sort}')
        else:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'title')
        context['direction'] = self.request.GET.get('direction', 'asc')
        context['title_filter'] = self.request.GET.get('title', '')

        
        get_params = self.request.GET.copy()
        if 'page' in get_params:
            get_params.pop('page')
        context['get_params'] = get_params.urlencode()

        return context

class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'bookapp.change_book'
    model = Book
    form_class = BookForm
    template_name = 'bookapp/form.html'
    success_url = reverse_lazy('book_list')

class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'bookapp.delete_book'
    model = Book
    template_name = 'bookapp/confirm_delete.html'
    success_url = reverse_lazy('book_list')

class BookDetail(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'bookapp/detail.html'
    context_object_name = 'book'

class BookStats(TemplateView):
    template_name = 'bookapp/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['max_pages_book'] = Book.objects.order_by('-pages').first()
        context['min_pages_book'] = Book.objects.order_by('pages').first()
        context['avg_pages'] = Book.objects.aggregate(avg=Avg('pages'))['avg'] or 0
        context['avg_rating'] = Book.objects.aggregate(avg=Avg('rating'))['avg'] or 0

        
        status_data = Book.objects.values('status').annotate(total=Count('id')).order_by('status')
        status_labels = []
        status_counts = []
        status_display = dict(Book.STATUS_CHOICES)
        for item in status_data:
            status_labels.append(status_display.get(item['status'], item['status']))
            status_counts.append(item['total'])
        context['status_labels'] = status_labels
        context['status_counts'] = status_counts

        
        rating_data = Book.objects.values('rating').annotate(total=Count('id')).order_by('rating')
        rating_labels = []
        rating_counts = []
        for item in rating_data:
            rating_labels.append(item['rating'])
            rating_counts.append(item['total'])
        context['rating_labels'] = rating_labels
        context['rating_counts'] = rating_counts

        return context

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        return redirect('book_list')
    return render(request, 'bookapp/form.html', {'form': form})
