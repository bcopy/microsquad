# Controller for Homie devices

A Microsquad controller obtains MQTT events and performs callbacks for potential subscribers.
Also allows to update settable properties.

Note that the controller is a pure MQTT implementation - it does not
depend on any Homie API.
Callbacks are handled by RxPy observables.

## Supported reactive event types

* on_new_terminal
* on_new_player
* on_new_game
* on_update_terminal_property

## Supported remote calls

* update_terminal_property(terminal_id,property_name,property_value)
* update_gateway_property(gateway_id,property_name,property_value)
* update_player_property(player_id,property_name,property_value)



