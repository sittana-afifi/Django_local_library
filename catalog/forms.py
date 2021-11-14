import datetime

from django import forms
from django.contrib.auth.models import User
from django.shortcuts import  render

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from catalog.models import BookInstance , Book



class RenewBookForm(forms.Form):
    
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


    


class BorrowBookForm(forms.Form):
    
    borrow_date = forms.DateField(help_text="The default date is today.")
    due_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), empty_label=None)
    book = forms.ModelChoiceField(queryset= BookInstance.objects.filter(status__exact='a'), empty_label=None)

    #book = forms.ModelMultipleChoiceField(queryset=None)

    #class FooMultipleChoiceForm(forms.Form):
     #   book = forms.ModelChoiceField(queryset=None)

      #  def __init__(self, *args, **kwargs):
       #     super().__init__(*args, **kwargs)
        #    self.fields['book'].queryset = BookInstance.objects.filter(status__exact='o').filter(self=id)
         #   return book
#def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
         #   context = super().get_context_data(**kwargs)
            # Add in a QuerySet of all the books
            #####
            #context['list'] = Book.objects.all().filter(author.id = Book.author_id)
           #context['booksByAuthor'] = Book.objects.all().filter(author= context.get('author'))
            
           # return context

            
    def clean_borrow_date(self):
        data = self.cleaned_data['borrow_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - borrow in past'))

        return data
     


    def clean_due_date(self):
        data = self.cleaned_data['borrow_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - borrow in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - borrowal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
     

    def clean_user(request):
        data = request.cleaned_data['user']
        return data

   