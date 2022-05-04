Feature: The pet store service back-end
    As a Store Owner
    I need a RESTful service
    So that I can keep track of all the orders

Background:
    Given the following orders
        | customer       | date | 
        | 12345          | 01-20-2022      | 
        | 34523          | 03-10-2022      | 
        | 65434          | 03-17-2022      | 


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Order
    When I visit the "Home Page"
    And I set the "Customer" to "111"
    And I set the "Date" to "04/22/2021"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Customer" field should be empty
    And the "Date" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "111" in the "Customer" field



Scenario: List all Orders 
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "12345" in the results
    And I should see "34523" in the results

Scenario: Search for customer
    When I visit the "Home Page"
    And I set the "Customer" to "34523"
    And I press the "Search" button
    Then I should see "34523" in the results

# Scenario: Update a Order
#     When I visit the "Home Page"
#     And I set the "Customer" to "34523"
#     And I press the "Search" button
#     Then I should see "34523" in the "Customer" field
#     When I change "Customer" to "999"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     And I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see the message "Success"
#     Then I should see "999" in the "Customer" field
#     When I press the "Clear" button
#     And I press the "Search" button
#     Then I should see the message "Success"
#     Then I should see "999" in the results
