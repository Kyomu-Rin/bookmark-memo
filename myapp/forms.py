from django import forms
from .models import Post


# 新規追加するときに使う
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('site_url', 'memo', 'tag', 'image', 'title')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'