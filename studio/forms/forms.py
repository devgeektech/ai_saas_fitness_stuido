from django import forms
from studio.models import AudioSegment, AvatarVideo, Class, Exercise, ClassSegment


class ClassForm(forms.ModelForm):
    class Meta:
        
        model = Class
        fields = ["title", "category", "difficulty", "focus", "duration", "status"]
        widgets = {
                "title": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter class title" }),
                "category": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter category" }),
                "difficulty": forms.Select(attrs={ "class": "form-select" }),
                "focus": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Focus area (e.g. strength, cardio)" }),
                "duration": forms.NumberInput(attrs={ "class": "form-control", "placeholder": "Duration in minutes" }),
                "status": forms.Select(attrs={ "class": "form-select" }),
            }

    # OPTIONAL VALIDATION (clean and simple)
    def clean_duration(self):
        duration = self.cleaned_data.get("duration")

        if duration and duration <= 0:
            raise forms.ValidationError("Duration must be greater than 0")

        return duration
    
    
    
# exercise form
class ExerciseForm(forms.ModelForm):
    class Meta:
        
        model = Exercise
        fields = ["name", "category", "difficulty", "muscle_group", "instructions", "safety_notes", "demo_video", "thumbnail", "status"]
        widgets = {
                "name": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter exercise name" }),
                "category": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter category" }),
                "difficulty": forms.Select(attrs={ "class": "form-select" }),
                "muscle_group": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter muscle group" }),
                "instructions": forms.Textarea(attrs={ "class": "form-control", "rows": 4, "placeholder": "Enter instructions" }),
                "safety_notes": forms.Textarea(attrs={ "class": "form-control", "rows": 4, "placeholder": "Enter safety notes" }),
                "demo_video": forms.ClearableFileInput(attrs={ "class": "form-control" }),
                "thumbnail": forms.ClearableFileInput(attrs={ "class": "form-control" }),
                "status": forms.Select(attrs={ "class": "form-select" }),
            }
        
# class segments 
class ClassSegmentForm(forms.ModelForm):
    class Meta:

        model = ClassSegment
        fields = ["class_obj", "exercise", "segment_type", "title", "script", "order", "duration"]
        widgets = {
                "class_obj": forms.Select(attrs={ "class": "form-select" }),
                "exercise": forms.Select(attrs={ "class": "form-select" }),
                "segment_type": forms.Select(attrs={ "class": "form-select" }),
                "title": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter title" }),
                "script": forms.Textarea(attrs={ "class": "form-control", "rows": 5, "placeholder": "Enter script" }),
                "order": forms.NumberInput(attrs={ "class": "form-control", "placeholder": "Enter order" }),
                "duration": forms.NumberInput(attrs={ "class": "form-control", "placeholder": "Duration in seconds" }),
            }
        
# audio segments       
class AudioSegmentForm(forms.ModelForm):
    class Meta:

        model = AudioSegment
        fields = ["segment", "audio_url", "duration", "voice_id", "status"]
        widgets = {
                "segment": forms.Select(attrs={ "class": "form-select" }),
                "audio_url": forms.URLInput(attrs={ "class": "form-control", "placeholder": "Enter audio URL" }),
                "duration": forms.NumberInput(attrs={ "class": "form-control", "placeholder": "Enter duration" }),
                "voice_id": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter voice id" }),
                "status": forms.Select(attrs={ "class": "form-select" }),
            }
        
        
# avatar vidoes
class AvatarVideoForm(forms.ModelForm):

    class Meta:

        model = AvatarVideo
        fields = ["segment", "video_url", "avatar_id", "status"]
        widgets = {
                "segment": forms.Select(attrs={ "class": "form-select" }),
                "video_url": forms.URLInput(attrs={ "class": "form-control", "placeholder": "Enter video URL" }),
                "avatar_id": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter avatar id" }),
                "status": forms.Select(attrs={ "class": "form-select" }),
            }