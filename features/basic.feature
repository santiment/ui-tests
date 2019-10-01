@debug
Feature: basic stuff

Scenario: Load Main Page
   Given I load Santiment main page and "do not" log in
   Then page title is "SANbase"

@lightweight
Scenario: View Main Page Text
   Given I load Santiment main page and "do" log in
   Then I ensure main page is displayed

Scenario: View Main Page Text 2
Given I load Santiment main page and "do not" log in
Then I ensure main page is displayed
When I search for "Ethereum" in graph search bar

Scenario: Select Period
   Given I load Santiment main page and "do not" log in
   Then I ensure main page is displayed
   When I select "1y" period

Scenario: Select Category
   Given I load Santiment main page and "do not" log in
   Then I ensure main page is displayed
   When I select "Development" category

Scenario: Select Metric
   Given I load Santiment main page and "do not" log in
   Then I ensure main page is displayed
   When I search for "Ethereum" in graph search bar
   When I select "Twitter" metric
   and I deselect "Price" metric

Scenario: Clear all metrics
   Given I load Santiment main page and "do not" log in
   When I search for "Ethereum" in graph search bar
   When I select "1m" period
   When I select "Twitter" metric
   and I select "Volume" metric
   and I select "Development Activity" metric
   When I clear all active metrics
   Then I ensure main page is displayed

Scenario: Select Metric New
   Given I load Santiment main page and "do not" log in
   When I clear all active metrics
   When I select "Price" metric
   When I select "Volume" metric
   When I deselect "Price" metric
   When I clear all active metrics
   Then I ensure main page is displayed


Scenario Outline: Verify Link
   Given I load Santiment main page and "do not" log in
   When I search for "<token>" in graph search bar and select the result
   When I select "1m" period
   When I select "Price" metric
   When I select "Social Volume" metric
   When I select "Volume" metric
   When I deselect "Development Activity" metric
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


Scenario Outline: Verify dates
   Given I load Santiment main page and "do not" log in
   When I select "<period>" period
   When I wait for "2" seconds
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

Scenario Outline: Verify token info
   Given I load Santiment main page and "do not" log in
   When I search for "<token>" in graph search bar and select the result
   Then I verify that token info is displayed correctly
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

Scenario: Account menu
   Given I load Santiment main page and "do" log in
   When I open account menu


Scenario: Select multiple metrics
   Given I load Santiment main page and "do not" log in
   When I select "Price, Volume, Development Activity, Social Volume, Social Dominance" metrics
   When I wait for "3" seconds
   When I clear all active metrics
   When I wait for "3" seconds
   When I select "Price, Volume, Development Activity, Social Volume, Social Dominance" metrics
   When I wait for "3" seconds
   Then I verify that "Price, Volume, Development Activity, Social Volume, Social Dominance" metrics are active
