from . import admin_mgmt

@admin_mgmt.route('/users', methods=['GET'])
def get_users():
    return "Users"
