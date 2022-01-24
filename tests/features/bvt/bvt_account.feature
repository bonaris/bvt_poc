Feature: Registered User should be able to Sign In from the Top User Menu and access My Account profile data

  Scenario: Registered User signs validates orders and updates info
    Given Z Gallerie website should be up and running
    When user clicks on Sign In at a Top User Menu and signs in with valid credentials
    Then My Account Page is displayed
#    And current user information is displayed
#    And current shipping address info is displayed
    When user updates Account information
    Then information is updated successfully


#    And Order section


