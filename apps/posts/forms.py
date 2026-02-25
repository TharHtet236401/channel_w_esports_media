from django import forms

from .models import Post, Region


class PostForm(forms.ModelForm):
    region = forms.ModelMultipleChoiceField(
        queryset=Region.objects.all().order_by("name"),
        widget=forms.SelectMultiple(
            attrs={
                "class": "select select-bordered w-full",
            }
        ),
        required=True,
        label="Regions",
    )

    class Meta:
        model = Post
        fields = ["caption", "description", "region"]
        widgets = {
            "caption": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full my-3",
                    "placeholder": "Enter caption",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full my-3",
                    "rows": 4,
                    "placeholder": "Enter description",
                }
            ),
        }

