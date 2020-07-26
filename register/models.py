from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        # if (len(postData['profil_url']) == 0):
        #     if len(postData['profil_url']) < 2:
        #         errors['profil_url'] = "First name can not be shorter than 2 characters"

        if (postData['name'].isalpha()) == False:
            if len(postData['name']) < 2:
                errors['name'] = "Last name can not be shorter than 2 characters"

        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"

        if (AppUsers.objects.filter(email=postData['email'])):
            errors['email'] = "Email already used"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too short!"

        return errors

class AppUsers(models.Model):
    # first_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    profil_url = models.ImageField(upload_to='images/')
    is_login = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add = True)
    # updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class User(models.Model):
    email = models.EmailField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=50, default='ngopi-dulu')
    profil_url = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class ToDoList(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class Item(models.Model):
#     todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
#     text = models.CharField(max_length=300)
#     complex = models.BooleanField()

#     def __str__(self):
#         return self.text