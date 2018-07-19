from django import forms


class BlogForm(forms.Form):
	title = forms.CharField(max_length=100,)
	body = forms.CharField( widget=forms.Textarea, max_length=2000, required=False)
	tags = forms.CharField(max_length=500, required=False, help_text="Enter tags separated by comma ',' ")
	categories = forms.CharField(required=False, help_text="Enter categories this blog might fall into separated by comma ',' ")
	
	