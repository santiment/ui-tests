@prod @stage
Feature: UI tests for app main page

Scenario: 1 - page defaults are displayed correctly
    Given I load Santiment main page and "do not" log in
    Then I verify that "6m" period is selected
    Then I verify that calendar dates are correct for "6m" period
    Then I verify that chart dates are correct for "6m" period
    Then I verify that Bitcoin token info is displayed correctly

Scenario Outline: 2 - period selection works correctly
    Given I load Santiment main page and "do not" log in
    When I select "<period>" period
    Then I verify that chart dates are correct for "<period>" period
    And I verify that calendar dates are correct for "<period>" period

Examples:
| period |
| 1d |
| 1w |
| 1m |
| 3m |
| 6m |
| 1y |
| all |

Scenario Outline: 3 - token search works properly
    Given I load Santiment main page and "do not" log in
    When I search for "<token>" in graph search bar and select the result
    Then I verify that <token> token info is displayed correctly

Examples:
| token |
| bitcoin |
| Litecoin |
| Cardano |
| Ripple |
| ChainLink |
| santiment |
| Stellar |
| Tezos |
| Binance Coin |
| TRON |

Scenario: 4 - metric selection and clearing works properly
    Given I load Santiment main page and "do not" log in
    When I select "Price, Volume, Social Volume, Social Dominance, Development Activity" metrics
    When I clear active metrics
    When I select "Price, Volume, Social Volume, Social Dominance, Development Activity" metrics
    Then I verify that "Price, Volume, Social Volume, Social Dominance, Development Activity" metrics are active

Scenario Outline: 5 - Share link contains correct data
    Given I load Santiment main page and "do not" log in
    When I search for "<token>" in graph search bar and select the result
    When I select "1m" period
    When I select "Price, Volume, Social Volume, Social Dominance" metrics
    Then I verify that share link contains correct data
Examples:
| token |
| bitcoin |
| Litecoin |
| Cardano |
| Ripple |
| ChainLink |
| santiment |
| Stellar |
| Tezos |
| Binance Coin |
| TRON |

Scenario: 6 - Search order is by market cap
    Given I load Santiment main page and "do not" log in
    Then I verify default search order is by market cap
