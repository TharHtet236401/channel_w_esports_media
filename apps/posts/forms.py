from django import forms

from .models import Post, Region


class PostForm(forms.ModelForm):
    region = forms.ModelMultipleChoiceField(
        queryset=Region.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Regions",
    )

    class Meta:
        model = Post
        fields = ["caption", "description", "region"]
        widgets = {
            "caption": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter caption",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Enter description",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style region checkboxes with DaisyUI classes
        self.fields["region"].widget.attrs.update(
            {"class": "checkbox checkbox-sm checkbox-primary"}
        )

