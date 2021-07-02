from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum


# example of calculated fields
class Budget(models.Model):
    date = models.DateField()
    total_spend = models.IntegerField(default=0, null=False)
    total_budgeted = models.IntegerField(default=0, null=False)
    total_difference = models.IntegerField(default=0, null=False)
    total_income = models.IntegerField(default=0, null=False)

    def calc_total_spend(self):
        return self.budgetitem_set.all().aggregate(total_spend = Sum('purchase_total'))['total_spend']

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.date)

    def save(self, *args, **kwargs):
        if self.budgetitem_set.all().exists():
            self.total_spend = self.budgetitem_set.all().aggregate(total_spend = Sum('purchase_total'))['total_spend']
            self.total_budgeted = self.budgetitem_set.all().aggregate(total_budgeted = Sum('amount'))['total_budgeted']       
        self.total_difference = self.total_budgeted - self.total_spend

        if self.incomeitem_set.all().exists():
            self.total_income = self.incomeitem_set.all().aggregate(total_income = Sum('total_income'))['total_income']

        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'user'], name='unique_month')
        ]
        ordering = ['date']


class BudgetItem(models.Model):
    category = models.ForeignKey(
        'purchases.Category',
        null = False,
        blank = False,
        on_delete = models.CASCADE,
    )

    budget = models.ForeignKey(
        Budget,
        null = False,
        blank = False,
        on_delete = models.CASCADE
    )

    amount = models.IntegerField(default=0, blank=False, null=False)
    purchase_total = models.IntegerField(default = 0, blank = True, null = False)
    income_total = models.IntegerField(default = 0, blank = True, null = False)
    difference = models.IntegerField(default = 0, blank = True, null=False)

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.category) + str(self.amount)

    def save(self, *args, **kwargs):
        qs_purchase = self.category.purchase_set.all().filter(date__year = self.budget.date.year, date__month = self.budget.date.month)
        if qs_purchase.exists():
            self.purchase_total = qs_purchase.aggregate(purchase_total = Sum('price'))['purchase_total']
        else:
            self.purchase_total = 0

        self.difference = self.amount - self.purchase_total
        return super().save(*args, **kwargs)
    
    
    class Meta:
        ordering = ['category__name']
        constraints = [
            models.UniqueConstraint(fields=['category', 'budget'], name='unique_budgetitem')
        ]
