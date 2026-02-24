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
        # Container for checkbox list
        region_widget = self.fields["region"].widget
        existing_classes = region_widget.attrs.get("class", "")
        region_widget.attrs["class"] = (
            existing_classes + " grid grid-cols-2 gap-2 text-sm"
        ).strip()

