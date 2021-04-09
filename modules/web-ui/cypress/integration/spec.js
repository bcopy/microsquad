describe('Usquad UI Test', () => {
    beforeEach(() => {
        cy.visit('http://localhost:8000/');
        cy.wait(100);
    })

    it('Loads player models', () => {
        cy.get('#add-player').click();
    })

    it('Can run player commands', () => {
        cy.publish('players/playerA', 'add');

        cy.publish('players/playerA', 'skin,alienA');

        cy.publish('players/playerA', 'accessory,cap');

        cy.publish('players/playerA', 'animation,Run');

        cy.publish('players/playerA', 'say,Hello!');
    })

    it('Can run team commands', () => {
        cy.publish('players/playerA', 'add');

        cy.publish('players/playerB', 'add');

        cy.publish('players/playerC', 'add');

        cy.publish('players/playerA', 'team,teamA');

        cy.publish('players/playerB', 'team,teamB');

        cy.publish('players/playerC', 'team,teamA');

        cy.publish('teams/teamA', 'animation,Run');

        cy.publish('teams/teamB', 'animation,CrouchIdle');

        cy.publish('teams', 'reset');

        cy.publish('teams', 'split,team1,team2')
    })
})