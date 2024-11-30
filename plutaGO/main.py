from controllers.UserController import UserController


userController = UserController()
userController.create('Nikodem', 'Mlynski', 'niko@spoko.pl', 'asdf', 'admin')

print(userController.get_all())