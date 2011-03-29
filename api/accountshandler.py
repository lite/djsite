from piston.handler import BaseHandler
from piston.utils import rc, throttle

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

from apps.accounts.models import UserProfile
from apps.accounts.models import School, Grade, Classes

from csrfhandler import CsrfHandler
  
class RegisterHandler(CsrfHandler):
    allowed_methods = ('POST', )
    
    def create(self, request):
        username = request.POST['username']
        users = User.objects.filter(username__iexact=username)
        if not users:
            password = request.POST['password']
            email = request.POST['email']
            user = User.objects.create_user(username, email, password)
            if user is not None:
                user.save()
                profile = UserProfile()
                profile.user = user
                profile.mobile = request.POST['mobile']
                profile.save()
                return {'status':0, "message": "Register successfully."}
            else:
                return {'status':-3, "message": "Sorry, create user failed."}
        else:
            return {'status':-2, "message": "Sorry, user has been existed."}
    
class LoginHandler(CsrfHandler):
    allowed_methods = ('POST', )
    
    def create(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return {'status':0, "message": "Login successfully."}
        else:
            return {'status':-1, "message": "Sorry, that's not a valid username or password"}
            
class SchoolHandler(BaseHandler):
    allowed_methods = ('GET', )
    model = Grade
    fields = (('id', 'name'))
    
    def read(self, request, school_id):
        school = School.objects.get(pk=school_id)
        grades = Grade.objects.all().filter(school__exact=school)
        return {'grades': grades }
        
class GradeHandler(BaseHandler):
    allowed_methods = ('GET', )
    model = Classes
    fields = (('id', 'name'))

    def read(self, request, grade_id):
        grade = Grade.objects.get(pk=grade_id)
        classess = Classes.objects.all().filter(grade__exact=grade)
        return {'classess': classess }
        
class ClassesHandler(BaseHandler):
    allowed_methods = ('GET', )
    model = UserProfile
    fields = ('mobile', ('user', ('username',) ))
    
    def read(self, request, classes_id):
        classes = Classes.objects.get(pk=classes_id)
        profiles = UserProfile.objects.all().filter(classes__exact=classes)
        return {'profiles': profiles }