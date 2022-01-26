class StoreLocation:

    element = None
    product = None
    displayed_name = None
    displayed_quantity = None
    zip_code = None
    distance = None

    zip_code_element = None
    distance_element = None
    search_button = None

    def __init__(self):
        pass

    def to_string(self):
        data_dictionary = {
            "displayed_name": self.displayed_name,
            "displayed_quantity": self.displayed_quantity,
            "zip_code": self.zip_code,
            "distance": self.distance
        }
        return data_dictionary


