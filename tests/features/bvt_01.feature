Feature: Guest user should be able to add products to cart and checkout



  Scenario: TC-01 Guest user should be able to add products to cart using PLP Page
    Given Z Gallerie website should be up and running
    When user provides Meganav to get to a PLP, for example "Tabletop > Serveware & Flatware"
    Then PLP is displayed as per selection
    And Product Grid is displayed on the page
    And each product has a name, price and a "Quick Look" link
    And there are filters like: color, price range
    And there is a dropdown for color filter to select best match

  Scenario: TC-01-2
    When user selects one of the colors in a filter
    Then Product List is updated based on the best match

#    And there is a dropdown for color filter to select best match
#    When user scrolls down a page or two and selects a product by clicking on it
#    And expected SKU of the product is known
#    Then PDP page is displayed for selected product
#    And SKU of displayed product matches expected SKU
#    When user clicks button 'Add to Cart'
#    And selects attributes like size & fabric, where applicable
#    Then product(s) should be added to the cart
#    And an overlay should be displayed confirming the qty of product(s) added to cart
#    And price and total should be displayed and calculated as expected


