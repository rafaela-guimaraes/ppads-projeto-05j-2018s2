from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, ListView
from .forms import UserForm, EntryForm
from .models import Entry
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.utils.dates import MONTHS


class IndexView(LoginRequiredMixin, View):
    template_name = 'finances/index.html'
    login_url = 'finances:login_user'

    def get(self, request):
      return get_list_entries(request, 5, self.template_name)


class UserFormView(View):
    form_class = UserForm
    template_name = 'finances/registration_form.html'
    
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return render(request, 'finances/index.html')

        return render(request, self.template_name, {"form": form})


class CreateEntry(LoginRequiredMixin, CreateView):
    login_url = "finances:login_user"
    template_name = 'finances/entry_form.html'
    success_url = reverse_lazy('finances:list_entry')
    form_class = EntryForm
    
    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.agent = self.request.user
        entry.save()
        return super(CreateEntry, self).form_valid(form)
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['entry_type'] = self.request.GET.get('entry_type', 'EX')
        return kwargs


class ListEntry(LoginRequiredMixin, View):
    template_name = 'finances/list_entry.html'
    login_url = 'finances:login_user'

    def get(self, request):
        return get_list_entries(request, None, self.template_name)
     
    def post(self, request): 
        return get_list_entries(request, None, self.template_name) 


class EntriesStatement(LoginRequiredMixin, View):
    template_name = 'finances/entries_statement.html'
    login_url = "finances:login_user"

    def get(self, request):
        return get_list_entries(request, None, self.template_name)    


class EntriesByCategory(LoginRequiredMixin, View):
    template_name = 'finances/entries_by_category.html'
    login_url = "finances:login_user"

    def get(self, request):
        return get_list_entries(request, None, self.template_name)    

        
class UpdateEntry(LoginRequiredMixin, UpdateView):
    login_url = 'finances:login_user'
    template_name = 'finances/entry_form.html'
    form_class = EntryForm
    model = EntryForm.Meta.model
    success_url = reverse_lazy('finances:list_entry')

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.agent = self.request.user
        entry.save()
        return super(UpdateEntry, self).form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['entry_type'] = self.request.GET.get('entry_type', 'EX')
        return kwargs


class DeleteEntry(LoginRequiredMixin, DeleteView):
    login_url = 'finances:login_user'
    model = Entry
    success_url = reverse_lazy('finances:list_entry')


def login_user(request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                
                return get_list_entries(request, 5, 'finances/index.html')        
            else: 
                return render(request, 'finances/login.html', {'error_message': 'Usuário ou senha inválidos'})
    
        else:
            return render(request, 'finances/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    return render(request, 'finances/login.html', {"form":form})


def delete_entry(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    entry.delete()
    return render(request, 'finances/list_entry.html')
    

def get_list_entries(request, limit, template_name):
    entry_type = request.GET.get('entry_type', 'all')
    month = int(request.POST.get('month', datetime.date.today().month))
    year = int(request.POST.get('year', datetime.date.today().year))
    incomes = Entry.objects.get_incomes(request.user,  month, year, limit)
    expenses = Entry.objects.get_expenses(request.user, month, year, limit)
    all_entries = Entry.objects.get_all_entries(request.user, month, year, None)
    total_incomes = Entry.objects.get_entries_amount(request.user, incomes)
    total_expenses = Entry.objects.get_entries_amount(request.user, expenses)
    category_amount = Entry.objects.get_amount_expenses_by_category(request.user, month, year, None) 
    expenses_by_category = get_list_expenses_by_category(request, limit, month, year)

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_incomes': total_incomes,
        'total_expenses': total_expenses,
        'months': MONTHS.items(),
        'current_month': month,
        'years': get_years(year, 5),
        'current_year': year,
        'all_entries': all_entries,
        'entry_type': entry_type,
        'entries_by_category': expenses_by_category,
        'category_amount' : category_amount,
    }
    
    return render(request, template_name, context)


def get_years(current_year, limit):
    years = []
    for i in range(current_year - limit, current_year + limit):
        years.append(i)
    return years


def get_list_expenses_by_category(request, limit, month, year):
    expenses =  Entry.objects.get_expenses_by_category(request.user, month, year, None) 

    expenses_by_category = {}
    
    for result in expenses:
        key = result['category__description']
        if result['category__description'] in expenses_by_category:
            expenses_by_category[result['category__description']].append([
            result['entry_date'],
            result['description'],
            result['amount']
            ])
        else: 
            expenses_by_category.setdefault(key, [])
            expenses_by_category[key].append([
            result['entry_date'],
            result['description'],
            result['amount']
            ])
                

    return expenses_by_category
