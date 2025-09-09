#noinspection CucumberUndefinedStep
Feature: SearchBar

  @regression
  Scenario Outline: Search for a “playstation” using the search bar, verify that the results displayed includes games
  for playstation 5 and playstation consoles. Then select a playstation 5 in the results listed and
  validate the title and price of the item in the page displayed.
    Given Go to liverpool.com
    When Validate Home Page is showing
    Then Input a <search_term> and press return or search button
    And Validate that the results shown make sense with <search_term>
    Examples:
      | search_term |
      | ps5         |

  @regression
  Scenario Outline: Search for “smart tv” and navigate to the page. Validate that the Size and Price filters
  are displayed. Filter the results by size: 55 inches, brand: sony. Validate the
  results count.
    Given Go to liverpool.com
    When Validate Home Page is showing
    Then Input a <search_term> and press return or search button
    And Validate that the results shown make sense with <search_term>
    When Filter the results by size: <size_filter>, brand: <brand_filter>
    Then Validate the results count
    Examples:
      | search_term | | size_filter   | | brand_filter |
      | smart tv    | | 55 pulgadas   | | SONY         |
