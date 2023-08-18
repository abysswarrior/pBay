from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)


class CouponAddForm(forms.Form):
    code = forms.CharField(max_length=30)
