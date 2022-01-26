class StoreLocation:
    element = None
    product = None
    displayed_name = None
    displayed_quantity = None
    zip_code = None
    distance = None

    locations = []

    zip_code_element = None
    distance_element = None
    search_button = None

    def __init__(self, driver, product=None):
        self.driver = driver
        self.products = product
        self.refresh()

    def refresh(self):
        pass
