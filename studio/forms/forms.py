from django import forms
from studio.models import Class


class ClassForm(forms.ModelForm):

    class Meta:
        model = Class

        fields = [
            "title",
            "category",
            "difficulty",
            "focus",
            "duration",
            "status",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter class title"
            }),

            "category": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter category"
            }),

            "difficulty": forms.Select(attrs={
                "class": "form-select"
            }),

            "focus": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Focus area (e.g. strength, cardio)"
            }),

            "duration": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Duration in minutes"
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),
        }

    # OPTIONAL VALIDATION (clean and simple)
    def clean_duration(self):
        duration = self.cleaned_data.get("duration")

        if duration and duration <= 0:
            raise forms.ValidationError("Duration must be greater than 0")

        return duration