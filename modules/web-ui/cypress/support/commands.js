Cypress.Commands.add("publish", (topic, message) => {
    cy.get('#pub-topic').clear().type(topic);
    cy.get('#pub-payload').clear().type(message);
    cy.get('#publish-button').click();
});