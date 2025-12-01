from . import auth

@auth.route('/login', methods=['POST'])
def login():
    return "Login"
