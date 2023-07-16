from django import forms
from cities_light.models import Country, City
from django.http import JsonResponse
from django.shortcuts import render

from users.models import User


class AddressForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all())
    city = forms.ModelChoiceField(queryset=City.objects.none())

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set


def get_cities(request):
    country_id = request.GET.get('country_id')
    # cities = City.objects.all()
    c = Country.objects.all()
    cities = City.objects.filter(country_id=192)
    city_list = list(cities.values('id', 'name'))
    print(11111, c[0].alternate_names)

    # form = AddressForm()
    return render(request, "clothes/forms.html", {"form": city_list, "c": c})
    # return JsonResponse(city_list, safe=False)


class Change_person_data(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "city", "post_office"]
        widgets = {name: forms.TextInput(attrs={'class': 'text-16 info',
                                                "disable": True,
                                                "placeholder": "Заполните поле"}) for name in fields}


