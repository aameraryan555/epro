

class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': "First Name"}))
    last_name = forms.CharField(label="Last Name", max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': "Last Name"}))
    full_name = forms.CharField(label="Full Name", max_length=200, help_text= "(as per documents)",
                                widget=forms.TextInput(attrs={'placeholder': "Full Name"}))
    city = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'placeholder': "City"}))
    zip_code = forms.IntegerField(max_value=1000000,
                                  widget=forms.NumberInput(attrs={'placeholder': "Zip Code"}))
    qualification = forms.CharField(max_length=150)
    experience = forms.CharField(max_length=150)
    resume = forms.FileField(required=False,
                             widget=forms.ClearableFileInput())
    details = forms.Textarea()

    def __init__(self, candidate=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate is not None:
            self.fields["first_name"].initial = candidate.first_name
            self.fields["last_name"].initial = candidate.last_name
            self.fields["full_name"].initial = candidate.full_name
            self.fields["qualification"].initial = candidate.qualification
            self.fields["experience"].initial = candidate.experience
            self.fields["city"].initial = candidate.city
            self.fields["zip_code"].initial = candidate.zip_code
            # self.fields["resume"].initial = candidate.resume.file

        else:
          pass









#View function

@login_required
def update_profile(request):
    candidate = request.user.candidate
    if request.method == "POST":
        form = UpdateProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            full_name = form.cleaned_data.get('full_name')
            city = form.cleaned_data.get('city')
            zip_code = form.cleaned_data.get('zip_code')
            qualification = form.cleaned_data.get('qualification')
            experience = form.cleaned_data.get('experience')
            details = form.cleaned_data.get('details')
            resume = form.cleaned_data.get('resume')
            candidate.first_name = first_name
            candidate.last_name = last_name
            candidate.full_name = full_name
            candidate.city = city
            candidate.zip_code = zip_code
            candidate.qualification = qualification
            candidate.experience = experience
            candidate.details = details
            if resume:
                candidate.resume = resume
            candidate.save()
            messages.success(request, 'Profile Suucessfully Updated')
            return redirect('profile')
        else:
            form = UpdateProfileForm(candidate=candidate)
            return render(request, 'portal/update_profile.html', {'form': form, 'form_invalid': "form is invalid !"})
    else:
        form = UpdateProfileForm(candidate=candidate)
        return render(request, 'portal/update_profile.html', {'form': form})
