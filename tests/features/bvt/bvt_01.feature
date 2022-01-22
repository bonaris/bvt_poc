Feature: Guest user should be able to add products to cart and checkout

  Scenario: Guest user should be able to add products to cart using PLP Page
    Given Z Gallerie website should be up and running
    When user provides Meganav to get to a PLP, for example "Tabletop > Serveware & Flatware"
    Then PLP is displayed as per selection with expected header
    And Product Grid is displayed on the page
    And each product has a name, price and a "Quick Look" link
    And there are filters like: color, price range
    And there is a dropdown for color filter to select best match

#    When user selects one of the colors in a filter
#    When user selects one of the price-range in a filter
#    Then Product List is updated based on the best match
#    And breadcrumbs filter links are available on the page
#
#    When user clicks on price range link
#    Then price range filter is cleared
#    And Product List is updated
#
#    When user clicks on Clear All link
#    Then all filters are cleared
#    And Product List is the same as originally displayed

    When user scrolls down a page or two and selects a product by clicking on it
    Then PDP page is displayed for selected product
    And  And it is the same product as selected from PLP
    And SKU of selected product is displayed

    When user clicks button Add to Cart
    Then drop down cart frame is displayed
    And price and total should be displayed and calculated as expected
#    And selects attributes like size & fabric, where applicable
#    And an overlay should be displayed confirming the qty of product(s) added to cart

    When user provides Meganav to get to a PLP, for example "Home > Collections > $30 & Under"
    Then PLP is displayed as per selection with expected header
    And Product Grid is displayed on the page
    And each product has a name, price and a "Quick Look" link

    When user provides Meganav to get to a PLP, for example "Home > Collections > $30 & Under"
    Then PLP is displayed as per selection with expected header
    And Product Grid is displayed on the page
    And each product has a name, price and a "Quick Look" link

    When user selects a product and clicks on Quick Look
    Then Quick Look modal is displayed
#    And and it contains selected product information
