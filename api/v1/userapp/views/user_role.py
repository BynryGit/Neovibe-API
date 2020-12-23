import traceback
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.messages import *
from api.constants import *
from master.models import get_user_by_id_string
from v1.commonapp.common_functions import get_user_from_token
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.views.logger import logger
from v1.userapp.decorators import is_token_validate, role_required, utility_required
from v1.userapp.models.role import get_role_by_id
from v1.userapp.models.user_role import get_user_role_by_user_id, get_record_by_values, get_record_values_by_id
from v1.utility.models.utility_module import get_utility_module_by_id_string
from v1.utility.models.utility_module import UtilityModule as UtilityModuleTbl,get_utility_modules_by_utility_id_string,get_utility_module_by_id
from v1.utility.serializers.utility_module import UtilityModuleViewSerializer
from v1.utility.serializers.utility_sub_module import UtilitySubModuleViewSerializer
from v1.utility.models.utility_sub_module import UtilitySubModule as UtilitySubModuleTbl,get_utility_submodule_by_id
from v1.commonapp.models.module import get_module_by_id_string
from v1.commonapp.models.sub_module import get_sub_module_by_id_string
from v1.userapp.models.role_privilege import RolePrivilege
from v1.userapp.models.role import get_role_by_id_string

# API Header
# API end Point: api/v1/user/:id_string/role
# API verb: GET, POST, PUT
# Package: Basic
# Modules: User
# Sub Module: User
# Interaction: Get, Add, Edit user role and privilege
# Usage: Get, Add, Edit User role and privileges
# Tables used: 2.5.2. Users & Privileges - Role Privileges
# Author: Arpita
# Created on: 14/05/2020
# Updated on: 21/05/2020
from v1.userapp.serializers.role import RoleDetailViewSerializer
from v1.userapp.serializers.role_privilege import RolePrivilegeViewSerializer
from v1.userapp.serializers.user import GetUserSerializer
from v1.userapp.serializers.user_role import UserRoleSerializer, UserRoleViewSerializer


class UserRole(GenericAPIView):

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, id_string):
        try:
            data = {}
            role_list = []
            user = get_user_by_id_string(id_string)
            if user:
                data['email'] = user.email
                data['id_string'] = id_string
                user_roles = get_user_role_by_user_id(user.id)
                if user_roles:
                    for user_role in user_roles:
                        role_obj = get_role_by_id(user_role.role_id)
                        role = RoleDetailViewSerializer(instance=role_obj, context={'request': request})
                        role_list.append(role.data)
                    data['roles'] = role_list
                    return Response({
                        STATE: SUCCESS,
                        DATA: data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        STATE: ERROR,
                        DATA: ROLES_NOT_ASSIGNED,
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User Role')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def post(self, request, id_string):
        try:
            role_list = []
            data = {}
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                data['email'] = user_obj.email
                data['id_string'] = id_string
                for role in request.data:
                    # validate_data = {'user_id': str(id_string), 'utility_id': request.data['utility_id'], 'role_id': role['role_id_string']}
                    validate_data = {'user_id': str(id_string), 'role_id': role['role_id_string']}

                    serializer = UserRoleSerializer(data=validate_data)
                    if serializer.is_valid(raise_exception=False):
                        user_id_string = get_user_from_token(request.headers['Authorization'])
                        user = get_user_by_id_string(user_id_string)
                        user_role_obj = serializer.create(serializer.validated_data, user)
                        role_obj = get_role_by_id(user_role_obj.role_id)
                        view_serializer = RoleDetailViewSerializer(instance=role_obj,
                                                                      context={'request': request})
                        role_list.append(view_serializer.data)
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: list(serializer.errors.values())[0][0],
                        }, status=status.HTTP_400_BAD_REQUEST)
                data['roles'] = role_list
                return Response({
                    STATE: SUCCESS,
                    RESULTS: data,
                }, status=status.HTTP_201_CREATED)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Role')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, USER, EDIT)
    def put(self, request, id_string):
        try:
            data = {}
            role_list = []
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                data['email'] = user_obj.email
                data['id_string'] = id_string
                for role in request.data['roles']:
                    validate_data = {'user_id': str(id_string), 'role_id': role['role_id_string']}
                    serializer = UserRoleSerializer(data=validate_data)
                    if serializer.is_valid(raise_exception=False):
                        user_role = get_record_by_values(str(id_string), role['role_id_string'])
                        user_id_string = get_user_from_token(request.headers['token'])
                        user = get_user_by_id_string(user_id_string)
                        if user_role:
                            user_role_obj = serializer.update(user_role, serializer.validated_data, user)
                        else:
                            user_role_obj = serializer.create(serializer.validated_data, user)
                        role_obj = get_role_by_id(user_role_obj.role_id)
                        view_serializer = RoleDetailViewSerializer(instance=role_obj,
                                                                      context={'request': request})
                        role_list.append(view_serializer.data['role'])
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: list(serializer.errors.values())[0][0],
                        }, status=status.HTTP_400_BAD_REQUEST)
                data['roles'] = role_list
                return Response({
                    STATE: SUCCESS,
                    RESULTS: data,
                }, status=status.HTTP_200_OK)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Role')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)

    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def delete(self, request, id_string):
        try:
            user_obj = get_user_by_id_string(id_string)
            if user_obj:
                for role in request.data['roles']:
                    validate_data = {'user_id': str(id_string), 'role_id': role['role_id_string'], "is_active": 'False'}
                    serializer = UserRoleSerializer(data=validate_data)
                    if serializer.is_valid(raise_exception=False):
                        user_role = get_record_values_by_id(user_obj.id, role['role_id_string'])
                        if user_role:
                            user_id_string = get_user_from_token(request.headers['token'])
                            user = get_user_by_id_string(user_id_string)
                            serializer.update(user_role, serializer.validated_data, user)
                        else:
                            raise CustomAPIException("User Roles not found.", status_code=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({
                            STATE: ERROR,
                            RESULTS: serializer.errors,
                        }, status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    STATE: SUCCESS,
                    RESULTS: ROLES_DELETED,
                }, status=status.HTTP_200_OK)
            else:
                raise CustomAPIException(ID_STRING_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger().log(e, 'HIGH', module = 'Admin', sub_module = 'User Role')
            res = self.handle_exception(e)
            return Response({
                STATE: EXCEPTION,
                RESULT: str(e),
            }, status=res.status_code)


class UserRoleByUtilityModules(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, user_id_string,utility_id_string):
        try:
            data = {}
            role_list = []
            user = get_user_by_id_string(user_id_string)
            utility_module_obj = get_utility_modules_by_utility_id_string(utility_id_string)
            module_obj_data=[]
            if user:
                user_roles = get_user_role_by_user_id(user.id)
                if user_roles:
                    for user_role in user_roles:
                        role_obj = get_role_by_id(user_role.role_id)
                        role = RoleDetailViewSerializer(instance=role_obj, context={'request': request})
                        role_list.append(role.data)
                    module_obj_list = []                    
                    for a in role_list:
                        for d in a['modules']['module']:
                            module_data ={}
                            module_data['role_id_string'] = a['id_string']
                            module_data['name'] = d['name'] 
                            module_data['id_string'] = d['id_string']
                            module_obj_list.append(module_data)
                
            else:
                return Response({
                    STATE: ERROR,
                    DATA: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)

            if utility_module_obj:
                for b in utility_module_obj:
                    module_obj = get_utility_module_by_id(b.id)

                    module = UtilityModuleViewSerializer(instance=module_obj, context={'request': request})
                    module_obj_data.append(module.data)
                    utility_module_list=[]
                for l in module_obj_data:  
                    utility_module_list.append(l)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)

            new_list=[]
            for roleprivilege in module_obj_list:
                for utility in utility_module_list:
                    data={}
                    if roleprivilege['name'] == utility['module_id']['name']:
                        data['name'] = utility['module_id']['name']
                        data['id_string'] = utility['id_string']   
                        data['role_id_string'] = roleprivilege['role_id_string']                                     
                        new_list.append(data)
            return Response({
                STATE: SUCCESS,
                DATA: new_list,
            }, status=status.HTTP_200_OK)
                # else:
                #     return Response({
                #         STATE: ERROR,
                #         DATA: ROLES_NOT_ASSIGNED,
                #     }, status=status.HTTP_404_NOT_FOUND)
            
            
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User Role')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRoleByUtilitySubModule(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request, user_id_string,module_id_string):
        try:
            data = {}
            role_list = []
            user = get_user_by_id_string(user_id_string)

            utility_module_obj = get_utility_module_by_id_string(module_id_string)
            sub_module_list = UtilitySubModuleTbl.objects.filter(module_id=utility_module_obj.id, is_active=True)

            module_obj_data=[]
            if user:
                data['email'] = user.email
                data['id_string'] = user_id_string

                user_roles = get_user_role_by_user_id(user.id)
                if user_roles:
                    for user_role in user_roles:
                        role_obj = get_role_by_id(user_role.role_id)
                        role = RoleDetailViewSerializer(instance=role_obj, context={'request': request})
                        role_list.append(role.data)
                    for a in role_list:
                        module_obj_list = []
                        for d in a['modules']['module']:
                            for submodule in d['sub_module']:
                                module_data ={}
                                module_data['role_id_string'] = a['id_string']
                                module_data['modulename'] = d['name']
                                module_data['name'] = submodule['name'] 
                                module_data['id_string'] = submodule['id_string']
                                module_obj_list.append(module_data)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)

            if sub_module_list:
                for sub_module in sub_module_list:
                    submodule_obj = get_utility_submodule_by_id(sub_module.id)
                    module = UtilitySubModuleViewSerializer(instance=submodule_obj, context={'request': request})
                    module_obj_data.append(module.data)
                utility_submodule_list=[]
                for l in module_obj_data:
                    utility_submodule_list.append(l)
            else:
                return Response({
                    STATE: ERROR,
                    DATA: ID_STRING_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)

            new_list=[]
            for roleprivilege in module_obj_list:
                for utility in utility_submodule_list:
                    data={}
                    if (roleprivilege['name'] == utility['label']) &(roleprivilege['modulename'] == utility['utility_module_id']['module_id']['name']) :
                        data['module_id_string'] = utility['utility_module_id']['module_id']['id_string']
                        data['module_name'] = utility['utility_module_id']['module_id']['name']
                        data['name'] = utility['submodule_id']['name']
                        data['id_string'] = roleprivilege['id_string']
                        data['role_id_string'] = roleprivilege['role_id_string']
                        new_list.append(data)
            return Response({
                STATE: SUCCESS,
                DATA: new_list,
            }, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User Role')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ModulePrivilegesList(GenericAPIView):
    @is_token_validate
    @role_required(ADMIN, USER, VIEW)
    def get(self, request,role_id_string, module_id_string,sub_module_id_string):
        try:
            privilege_list = []
            role_obj = get_role_by_id_string(role_id_string)
            module_obj = get_module_by_id_string(module_id_string)
            sub_module_obj = get_sub_module_by_id_string(sub_module_id_string)
            privileageLists = RolePrivilege.objects.filter(role_id=role_obj.id,module_id=module_obj.id,sub_module_id=sub_module_obj.id, is_active=True)
            for privileageList in privileageLists:
                print('********privileageList**********',privileageList.id)
                view_serializer = RolePrivilegeViewSerializer(instance=privileageList,context={'request': request})
                privilege_list.append(view_serializer.data)
            # print('*******privilege_list**********',privilege_list)
            return Response({
                STATE: SUCCESS,
                DATA: privilege_list,
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger().log(e, 'MEDIUM', module = 'Admin', sub_module = 'User Role')
            return Response({
                STATE: EXCEPTION,
                DATA: '',
                ERROR: str(traceback.print_exc(e))
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)