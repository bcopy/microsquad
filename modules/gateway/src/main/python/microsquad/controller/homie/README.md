# Controller for Homie devices

A Microsquad controller obtains MQTT events and performs callbacks for potential subscribers.
Also allows to update settable properties.

Callbacks are handled by RxPy observables.

## Supported reactive event types

* terminal_discovered
* player_discovered
* game_discovered
* terminal property update : vote,accel,button,temperature (c.f. Microsquad event types)

## Supported settable property updates

* update_terminal_property(terminal_id,property_name,property_value)
* update_gateway_property(gateway_id,property_name,property_value)
* update_player_property(player_id,property_name,property_value)



