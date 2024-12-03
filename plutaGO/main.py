from controllers.UserController import UserController
db_path = 'plutaGO.db'
userController = UserController(db_path=db_path)
# userController.create('Nikodem', 'Mlynski', 'niko@spoko.pl', 'asdf', 'admin')

logged_user = userController.login('niko@spoko.pl', 'asdf')
print(logged_user)
print(logged_user.name)
print(logged_user.email)
