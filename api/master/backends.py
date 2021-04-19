# from master.models import UserProfile
from master.models import User, MasterUser
from v1.consumer.models.consumer_master import ConsumerMaster
from django.db.models import Q


class AuthBackend(object):

    def authenticate(self,request, username, password,form_factor, **kwargs):
        try:
            if (form_factor == 1 or form_factor == 2):
                user = User.objects.get(Q(email=username) | Q(user_id=username)|Q(phone_mobile=username) )
                return user if user.check_password(password) else None

            elif (form_factor == 3 or form_factor == 4):
                consumer = ConsumerMaster.objects.get(Q(email=username) |Q(consumer_no=username) | Q(phone_mobile=username))  
                return consumer if consumer.check_password(password) else None    

        except User.DoesNotExist:
            return None



























            


    # def get_user(self, user_id):
    #    try:
    #       return MasterUser.objects.get(pk=user_id)
    #    except MasterUser.DoesNotExist:
    #       return None


    
        