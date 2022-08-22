Feature: Displays Base Application

    Scenario: Displays 'hacker' title
        Given I start the application
         Then I see text displaying, exactly, HACKER
         And it is above all other widgets

    Scenario: Displays hacker view
        Given I start the application
         When I can identify a hacker view with a player
         Then it has 7 rows and 7 columns
         And the player is in the top row, column 4

    Scenario: Displays score sidebar
        Given I start the application
         When I can identify a score sidebar
         Then collected count equals 0
         And destroyed count equals 0
