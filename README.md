# Energy Planner

Plan when your devices should be switched on or off based on electricity price.

## Introduction

This is an add-on for [Home Assistant](https://www.home-assistant.io/), which runs a background
job every hour. This job:
* Downloads the latest electricity prices
* If prices are available for the next day it runs planning for your devices
* Planning optimizes at what times your devices should be turned on and off on the next day
* It saves the electricity prices and plans in `/config/data/energy-planner`
* The files in that directory can then be used to create virtual sensors in Home Assistant that trigger your automation to turn your devices on and off

## Installation

Connect to your Home Assistant with SSH. In the SSH session, do the following:

* TODO
