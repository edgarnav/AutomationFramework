#noinspection CucumberUndefinedStep
Feature: Categories

  @regression
  Scenario Outline: Expand the “Categorias” menu, place the cursor over the “Belleza” option, select the “Perfumes
  de Hombre” option in the menu displayed and filter the results displayed by “Dior” brand.
    Given Go to liverpool.com
    When Validate Home Page is showing
    Then Open category menu
    When Select the <category> option and press <subcategory> subcategory
    Then Validate that the results shown make sense with <search>
    And Filter results by brand: <brand>
    Examples:
      | category | | subcategory     | | search | | brand |
      | Belleza  | | Perfumes Hombre | | parfum | | DIOR  |