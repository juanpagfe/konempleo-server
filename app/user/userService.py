from app.auth.authService import get_password_hash
from app.baseController import ControllerBase
from app.user.userDTO import UserInsert, UserSoftDelete, UserUpdateUser
from models.user import Users

import pandas as pd

class ServiceUser(ControllerBase[Users, UserInsert, UserUpdateUser, UserSoftDelete]): 
    ...

userServices = ServiceUser(Users)