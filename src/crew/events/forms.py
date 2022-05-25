from django import forms

from .models import Event


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'text', 'participants_limit', 'price', 
                  'link_to_chat', 'event_date']

    title = forms.CharField(
            label='',
            max_length=128,
            strip=True,
            widget=forms.TextInput(attrs={
                    "class": "title-field event-create-field",
                    "placeholder": "краткий заголовок",
                }
            )
        )
    text = forms.CharField(
            label='',
            widget=forms.Textarea(attrs={
                    "class": "text-field event-create-field",
                    "placeholder": "описание события",
                }
            )
        )
    participants_limit = forms.IntegerField(
            label='',
            min_value=1,
            max_value=1000,
            required=False,
            widget=forms.NumberInput(attrs={
                    "class": "participants-limit-field event-create-field",
                    "placeholder": "максимальное количество участников",
                }
            )
        )
    price = forms.IntegerField(
            label='',
            min_value=0,
            widget=forms.NumberInput(attrs={
                    "class": "price-field event-create-field",
                    "placeholder": "стоимость в рублях",
                }
            )
        )
    link_to_chat = forms.URLField(
            label='',
            required=False,
            widget=forms.URLInput(attrs={
                    "class": "chat-link-field event-create-field",
                    "placeholder": "ссылка на чат",
                }
            )
        )
    event_date = forms.DateField(
            label='',
            widget=forms.DateInput(attrs={
                    "class": "date-field event-create-field",
                    "placeholder": "когда произойдет",
                }
            )
        )