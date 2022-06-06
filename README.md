# MicroSquad (a.k.a uSquad)

[![Known Vulnerabilities](https://snyk.io/test/github/lucasvanmol/usquad-web-ui/badge.svg)](https://snyk.io/test/github/lucasvanmol/usquad-web-ui)
![Build](https://github.com/cmcrobotics/microsquad/workflows/build-action/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lucasvanmol_usquad-web-ui&metric=alert_status)](https://sonarcloud.io/dashboard?id=lucasvanmol_usquad-web-ui)

A Microbit orchestration library based on [Bitio](https://github.com/AdventuresInMinecraft/bitio) : Using a single Microbit as a gateway, control remote Microbits via the radio.
Messages are exchanged using the Influx line protocol (with a small custom parser implemented in micropython)

![Microbit](https://microbit-micropython.readthedocs.io/en/v1.0.1/_images/happy.png)

**Basic functionalities include :**
* Broadcast, group and unicast messaging
* Assigning session identifiers (will be resent with each message from the client)
* Remotely controlling displays
* Requesting remote sensor readings (buttons, gyroscope, compass, temperature, votes etc...)


# Dependencies

For the **uSquad** Gateway :
* Python 3.8+
* [https://github.com/AdventuresInMinecraft/Bitio](https://github.com/AdventuresInMinecraft/bitio)

For the **uSquad** clients :
* The provided **uSquad** firmware to upload on each Microbit.

For the **uSquad** Web Interface :
* The spectacular [Kenney Character Assets](https://kenney.itch.io/kenney-character-assets) under Creative Commons Zero

# How to use it

## Flash the Microbits

## Start the Gateway

## Connect to the administration web interface

# How to develop
