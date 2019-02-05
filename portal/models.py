from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
User._meta.get_field('email')._unique = True


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Candidate.objects.create(user=instance, email=instance.email)
    instance.candidate.save()


class Role(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Industries'


class Qualification(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Qualifications'


class City(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT, null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.PROTECT, blank=True, null=True)
    experience = models.CharField(max_length=150, null=True, blank=True)

    address = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=True)
    zip_code = models.PositiveIntegerField(null=True, blank=True)

    resume = models.FileField(null=True, blank=True, upload_to='resumes/')
    details = models.TextField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.user, self.email, self.qualification)


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.PositiveIntegerField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.name, self.company)


class Job(models.Model):
    name = models.CharField(max_length=100)
    headline = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    salary_from = models.PositiveIntegerField(default=0)
    salary_upto = models.PositiveIntegerField(default=0)
    upload_by = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    requirements = models.TextField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.headline)
