@prod @stage
Feature: UI tests for Insights page

Scenario: preparation - clear drafts
  Given I load Santiment Insights page and "do" log in
  Then I verify Insights page is displayed
  When I activate "My Drafts" tab
  When I clear all drafts

Scenario Outline: 1 - publish Insight menu is disabled if body or title is 5 or less characters
  Given I load Santiment Insights page and "do" log in
  Then I verify Insights page is displayed
  When I write Insight with "<title>" title, "<body>" body, "" tags and stay in Editor
  Then I verify I <can_cant> publish the Insight

  Examples:
  | title  | body   | can_cant |
  |        |        | can't    |
  | aaaaa  |        | can't    |
  | aaaaaa |        | can't    |
  |        | aaaaa  | can't    |
  | aaaaa  | aaaaa  | can't    |
  | aaaaaa | aaaaa  | can't    |
  |        | aaaaaa | can't    |
  | aaaaa  | aaaaaa | can't    |
  | aaaaaa | aaaaaa | can      |

Scenario Outline: 2 - save draft with different title and body lengths and verify draft and preview
  Given I load Santiment Insights page and "do" log in
  Then I verify Insights page is displayed
  When I save unique Insight title and body
  When I write Insight with unique <title_length> title, <body_length> body, "<tags>" tags and don't publish it
  When I activate "My Drafts" tab
  Then I verify the latest draft <has_hasnt> latest saved title and body
  When I preview the latest draft
  Then I verify read page <has_hasnt> latest saved title, body and tags

  Examples:
  | title_length  | body_length   | tags     | has_hasnt    |
  | empty         | short         |          | has          |
  | short         | short         |          | has          |
  | long          | short         |          | has          |
  | empty         | long          |          | has          |
  | short         | long          |          | has          |
  | long          | long          |          | has          |
  | long          | long          | eth, btc | has          |
  | empty         | empty         |          | doesn't have |
  | short         | empty         |          | has          |
  | long          | empty         |          | has          |

Scenario Outline: 3 - can't add more than 5 tags
  Given I load Santiment Insights page and "do" log in
  Then I verify Insights page is displayed
  When I write Insight with "scenario 3 title" title, "scenario 3 body" body, "<tags>" tags and stay in Editor
  Then I verify I <can_cant> add more tags

  Examples:
  | tags                    | can_cant |
  | eth, btc, zrx, trx, san | can't    |
  | eth, btc, zrx, trx      | can      |

Scenario: 4 - publish Insight and verify Insight and preview
  Given I load Santiment Insights page and "do" log in
  Then I verify Insights page is displayed
  When I save unique Insight title and body
  When I write Insight with unique long title, long body, "san, btc" tags and do publish it
  Then I verify the latest Insight has latest saved title, tags and tag title
  When I activate "All Insights" tab
  Then I verify the latest Insight has latest saved title, tags and tag title
  When I read the latest Insight
  Then I verify read page has latest saved title, body and tags

Scenario Outline: 5 - filtering works properly
  Given I load Santiment Insights page and "do" log in
  Then I verify Insights page is displayed
  When I save unique Insight title and body
  When I write Insight with unique long title, long body, "san, btc" tags and do publish it
  When I filter Insights by <filter_option> of the latest Insight
  Then I verify "All Insights" tab is active
  Then I verify Insights are filtered by <filter_option>
  When I activate "All Insights" tab
  When I filter Insights by <filter_option> of the latest Insight
  Then I verify "All Insights" tab is active
  Then I verify Insights are filtered by <filter_option>

  Examples:
  | filter_option |
  | author        |
  | first tag     |
