class Product:

    element = None
    sku = None
    name = None
    original_price = None
    sale_price = None
    discount = None
    dimensions = None
    rating = None
    reviews = None
    description = None
    details_dimensions = None
    other_info = None
    quick_look = None
    availability = None
    quantity = None

    def to_string(self):
        data_dictionary = {
            "sku": self.sku,
            "name": self.name,
            "price": self.original_price,
            "dimensions": self.dimensions,
            "rating": self.rating,
            "reviews": self.reviews,
            "description": self.description,
            "details_dimensions": self.details_dimensions,
            "availability": self.availability,
            "quantity": self.quantity,
            "other_info": self.other_info
        }
        return str(data_dictionary)

    def map_from_plp_element(self, element):
        self.element = element
        values = element.text.split('\n')
        if len(values) == 5:
            self.discount = values[0]
            self.name = values[1]
            self.original_price = values[2]
            self.sale_price = values[3]
            self.quick_look = values[4]

    def map_from_pdp_element(self, element_list, quantity=1):
        self.dimensions = element_list[0].text.split('\n')[1]
        self.availability = element_list[1].text.split('\n')[1]
        self.sku = element_list[2].text.split('\n')[1]
        self.quantity = quantity
