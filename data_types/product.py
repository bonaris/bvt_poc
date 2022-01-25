from utils.utils import Utils


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
    cart_total = None
    quick_look_element = None

    def to_string(self):
        data_dictionary = {
            "sku": self.sku,
            "name": self.name,
            "price": self.original_price,
            "sale price": self.sale_price,
            "dimensions": self.dimensions,
            "rating": self.rating,
            "reviews": self.reviews,
            "description": self.description,
            "details_dimensions": self.details_dimensions,
            "availability": self.availability,
            "quantity": self.quantity,
            "cart_total": self.cart_total,
            "expected_total": self.get_expected_total(),
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
        elif len(values) == 3:
            self.name = values[0]
            self.original_price = values[1]
            self.quick_look = values[2]

    def map_from_pdp_element(self, element_list, quantity=1):
        for element in element_list:
            if "Availability" in element.text:
                try:
                    self.availability = element.text.split('\n')[1]
                except Exception:
                    pass
            elif "Dimensions" in element.text:
                try:
                    self.dimensions = element.text.split('\n')[1]
                except Exception:
                    pass
            elif "SKU":
                try:
                    self.sku = element.text.split('\n')[1]
                except Exception:
                    pass
        self.quantity = quantity

    def map_from_drop_down_cart(self, element):
        values = element.text.split('\n')
        self.name = values[0]
        self.cart_total = values[3]

    def get_expected_total(self):
        price = Utils.price_to_number(self.original_price)
        if self.quantity is None:
            self.quantity = 0
        if self.sale_price is not None and Utils.price_to_number(self.sale_price) > 0.0:
            price = Utils.price_to_number(self.sale_price)
        return int(self.quantity) * price
