from django import forms


class TrackForm(forms.Form):
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={"placeholder": "مثلاً ۰۹۱۲۳۴۵۶۷۸۹", "type": "tel"}
        ),
    )

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(filter(str.isdigit, phone))
        if len(digits) < 10:
            raise forms.ValidationError("شماره موبایل معتبر وارد کنید.")
        return digits