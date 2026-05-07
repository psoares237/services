from django import forms
from services.models import Service





class ServiceModelForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

    #def clean_price(self):
        #price = self.cleaned_data.get('price')
        #if price is not None and price < 0:
            #raise forms.ValidationError("O preço não pode ser negativo.")
        #return price    
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 100: # type: ignore
            self.add_error('price', 'O preço deve ser maior ou igual a R$ 100,00.')
        return price
         

    def clean_billing_model(self):
        billing_model = self.cleaned_data.get('billing_model')
        if billing_model not in ['Mensal', 'Anual', 'Único']:
            raise forms.ValidationError("O modelo de cobrança deve ser 'Mensal', 'Anual' ou 'Único'.")
        return billing_model