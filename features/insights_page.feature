Feature: UI tests for Insights page
@wip
Scenario: 1 - log in and verify that page is displayed
  Given I load Santiment Insights page and "do" log in
  Then I verify Insights page is displayed
  When I activate "My Drafts" tab
