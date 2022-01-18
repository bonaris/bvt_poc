class User:
    def __init__(self, find_by_list=None, values=None):
        self.first_name = None
        self.last_name = None
        self.email = None
        self.password = None
        self.rep_password = None
        self.phone = None

        self.first_name_find_by = None
        self.last_name_find_by = None
        self.email_find_by = None
        self.password_find_by = None
        self.rep_password_find_by = None
        self.phone_find_by = None

        self.mapped_keys_find_by = None
        self.mapped_keys = None

        self.find_by_list = find_by_list
        self.values = values
        self.map_keys()
        self.map_form_data()

    def map_keys(self):
        if self.values:
            # if self.values.get("first"):
            #     self.first_name = self.values.get("first")
            #
            # if self.values.get("last"):
            #     self.last_name = self.values.get("last")
            self.email = self.values.get("email")
            self.password = self.values.get("pwd")

        if self.find_by_list:
            self.email_find_by = self.find_by_list.get("email")
            self.password_find_by = self.find_by_list.get("pwd")
#            self.first_name_find_by = self.find_by_list.get("first")

    def map_form_data(self):
        if self.values and self.find_by_list:
            self.mapped_keys = [
                (self.email_find_by, self.email),
                (self.password_find_by, self.password)
            ]

    def get_user_login_form_data(self, username_find_by, password_find_by):
        keys_and_values = [
            (username_find_by, self.email),
            (password_find_by, self.password)
        ]
        return keys_and_values
