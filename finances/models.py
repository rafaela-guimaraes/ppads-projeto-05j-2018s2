from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum


class Category(models.Model):

    INCOME = 'IN'
    EXPENSE = 'EX'
    ENTRY_TYPE_CHOICES = (
        (INCOME, 'INCOME'),
        (EXPENSE, 'EXPENSE'),
    )

    entries_type = models.CharField(
        max_length=2,
        choices=ENTRY_TYPE_CHOICES,
        default= EXPENSE,
    )

    description = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % (self.description)


class EntryManager(models.Manager):

    def get_entries(self, user, month, year, limit, entry_type):
        try:
            return self.order_by('entry_date').filter(
                agent=user, category__in=Category.objects.filter(entries_type__in=entry_type),
                entry_date__month=month, entry_date__year=year
                )[:limit]
        except ObjectDoesNotExist:
            return None

    def get_incomes(self, user, month, year, limit):
        return self.get_entries(user, month, year, limit, [('IN')])

    def get_expenses(self, user, month, year, limit):
        return self.get_entries(user, month, year, limit, [('EX')])

    def get_all_entries(self, user, month, year, limit):
        return self.get_entries(user, month, year, limit, [('IN'), ('EX')])

    def get_entries_amount(self, user, entries):
        return entries.aggregate(Sum('amount'))
    
    def get_amount_expenses_by_category(self, user, month, year, limit):
        expenses = self.get_expenses(user, month, year, limit)
        return expenses.order_by('category__description').values('category__description').annotate(Sum('amount'))
    
    def get_expenses_by_category(self, user, month, year, limit):
        expenses = self.get_expenses(user, month, year, limit).values('category__description', 'description', 'amount', 'entry_date')
        return expenses.order_by('category__description', 'entry_date')
        

class Entry(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    amount = models.FloatField()
    entry_date = models.DateField(default=timezone.now)

    objects = EntryManager()

    def __str__(self):
        return 'Agent: %s, Category: %s, Description: %s, Amount: %s, Entry Date: %s' % (
            self.agent.id, self.category.description, self.description, self.amount, self.entry_date)

