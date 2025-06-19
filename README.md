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

* Change to the Add-ons directory:
  ```
  cd /addons
  ```
* Clone the repository:
  ```
  git clone https://github.com/patrsc/energy-planner.git
  cd energy-planner
  ```
* Open the Home Assistant website
* Go to *Settings → Add-ons*
* Click *Add-on store* in the bottom right corner
* On the top right overflow menu, click the *Check for updates* button
* Refresh your webpage when needed
* You should now see a new section at the top of the store called *Local add-ons* that lists the *Energy Planner* add-on
* Click on it to go to the add-on details page.
* Install the add-on (might take several minutes)
* Start the add-on
* Optionally turn on Watchdog
* Check the logs of the addon if everything looks normal
