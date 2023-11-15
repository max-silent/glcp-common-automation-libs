class OpsrampConstantPayload:
    """
    payload page object model class.
    """

    @staticmethod
    def get_instance_data(client_id, client_secret):
        """
        Payload for Create Service Instance API.
        """
        instance_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
        return instance_data

    @staticmethod
    def create_role_data(name, description, scope):
        role_data = {
            "name": name,
            "description": description,
            "defaultRole": False,
            "scope": scope,
            "allDevices": True,
            "allCredentials": True,
            "allClients": True,
        }
        return role_data

    @staticmethod
    def create_user_group_data(name, description, email):
        user_group_data = {
            "name": name,
            "description": description,
            "email": email,
        }
        return user_group_data

    @staticmethod
    def create_user_data(
        login_name,
        password,
        firstname,
        lastname,
        designation,
        address,
        city,
        state,
        country,
        email,
        mobile_number,
    ):
        user_data = {
            "loginName": login_name,
            "password": password,
            "firstName": firstname,
            "lastName": lastname,
            "designation": designation,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "email": email,
            "mobileNumber": mobile_number,
        }
        return user_data

    @staticmethod
    def assign_role_to_user_data(users):
        assign_role_user = {"users": []}
        for user in users:
            assign_role_user["users"].append({"id": user})
        return assign_role_user

    @staticmethod
    def assign_role_to_user_group(user_group_id):
        assign_role_user_group = {"userGroups": [{"uniqueId": user_group_id}]}
        return assign_role_user_group

    @staticmethod
    def add_user_to_user_user_group(user_id):
        user_unique_id = [{"id": user_id}]
        return user_unique_id

    @staticmethod
    def update_role_data(users, name):
        role_data = {"name": name}
        assign_role_user = {"users": []}
        for user in users:
            assign_role_user["users"].append({"id": user})
        role_data.update(assign_role_user)
        return role_data
