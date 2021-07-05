from django import forms
from bbs.models import Post

#models.pyとforms.pyをここで連携される　だからform.pyを使うとデータベースに追加される
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)