Feature: Gameplay: Shooting

    Scenario: I can destroy the destroyable
        Given I start the application
        When I can identify a hacker view with a player
        And the game steps

        And I press 'D'
         Then row 0 has the following entities: "...D.D."

        When I press 'Space'
         Then row 0 has the following entities: ".....D."
        
        When I can identify a score sidebar
         Then destroyed count equals 1

    Scenario: I can collect the collectable
        Given I start the application
        When I can identify a hacker view with a player
        And the game steps 3 times

        And I press 'A' 3 times
         Then row 0 has the following entities: "...C.B."

        When I press 'Return'
         Then row 0 has the following entities: ".....B."

        When I can identify a score sidebar
         Then collected count equals 1
