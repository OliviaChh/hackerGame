Feature: Gameplay: Movement

    Scenario: Entities progress expectedly
        Given I start the application
        When I can identify a hacker view with a player
        And the game steps
         Then row 0 has the following entities: "..D.D.."

    Scenario: Entities progress expectedly, advanced
        Given I start the application
        When I can identify a hacker view with a player
        When the game steps 4 times

        Then row 0 has the following entities: ".CC.DD."
         And row 1 has the following entities: ".B....C"
         And row 2 has the following entities: "......."
         And row 3 has the following entities: "..D.D.."

    Scenario: I can shift entities
        Given I start the application
        When I can identify a hacker view with a player
        When the game steps

        And I press 'A'
         Then row 0 has the following entities: ".D.D..."

        When I press 'D'
         Then row 0 has the following entities: "..D.D.."

    Scenario: I can shift entities, advanced
        Given I start the application
        When I can identify a hacker view with a player
        When the game steps

        And I press 'A' 2 times
         Then row 0 has the following entities: "D.D...."

        When I press 'A'
         Then row 0 has the following entities: ".D....D"
