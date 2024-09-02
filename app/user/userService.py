
from app.baseController import ControllerBase
from app.user.userDTO import UserInsert, UserSoftDelete, UserUpdateUser

from models.models import Users

class ServiceUser(ControllerBase[Users, UserInsert, UserUpdateUser, UserSoftDelete]): 
    ...

userServices = ServiceUser(Users)