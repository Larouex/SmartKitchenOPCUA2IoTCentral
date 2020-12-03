# Smart Kitchen OPC-UA Integration with Azure IoT Central
Demonstrates the use of OPC-UA to Monitor the Equipment in a Smart Commercial Kitchen with Telemetry and Integration to Azure IoT Central via a Transparent Gateway with Protocol Translation.

This project is designed to assist you in understanding how to integrate an OPC-UA topology with Azure IoT Central. We have organized this project that supports all of the scenarios that you may encounter bringing in this kind of integration with Azure IoT Central.

This project is targeted at system integrators, developers and administrators of an OPC-UA system. This project is for learning purposes and supports the OPC-UA emulation, modeling and Azure IoT concepts that will help you gain deeper knowledge of this scenario.

<b>IMPORTANT:</b> If you are pursuant of a production or commercial implementation of Industrial IoT with and Azure IoT Central; The Microsoft Industrial IoT Team have developed a production ready system and you should start here {{{TDB}}}

## Overview
This demonstration is a reference implementation of the following...

* <b>OPC-UA Server</b> - Based on the popular FreeOPcUa project for Python.
* <b>Powerful Emulation</b> - Dynamic Configuration of OPC-UA Server, Nodes and Variables allow you to emulate topologies. In this project it is an instance of a Smart Commercial Kitchen.
* <b>Azure IoT Central SaaS Integration</b> - Azure IoT Central is a rich Software as a Service (SaaS) application that provides Telemetry, Device Management and Data Visualizations. That is just a small part of what it can do. We want to provide you with a way to understand and leverage these features with little coding and tons of power!

## Roles and Starting Points  Project and Tutorial
| Role | Area | Entry Point | Do This! |
|---|---|---|---|
| Developer | Coding | Starting from Scratch | [LINK: Getting Started](./developer-getting-started.md) |
| Developer | Coding | Already Developing on Python  | [LINK: Download the Project](./developer-getting-started.md) |
| All | OPC-UA | Configuration of the OPC-UA Client | [LINK: Configuration of the OPC-UA Client](./OpcUaClientOverview.md) |
| All | Modeling | PnP Modeling  | [LINK: Modeling Overview](./developer-getting-started.md) |


## Smart Kitchen Appliances
The core of this demo application for Azure IoT Central is the emulation of commercial kitchen. We have included the following emulated appliance models that you would find in a commercial kitchen...

* Ambient Environment
* Kitchen HVAC System [LINK: Detailed Overview for the Kitchen HVAC System](./KitchenHVACSystemOverview.md)
* Walk In Freezer [LINK: Detailed Overview for the Walk In Freezer](./WalkInFreezerOverview.md)
* Walk In Refrigerator [LINK: Detailed Overview for the Walk In Refrigerator](./WalkInRefrigeratorOverview.md)
* Standing Freezer [LINK: Detailed Overview for the Standing Freezer](./StandingFreezerOverview.md)
* Standing Refrigerator [LINK: Detailed Overview for the Fryer](./StandingRefrigeratorOverview.md)
* Fryer [LINK: Detailed Overview for the Fryer](./FryerOverview.md)
* Cold Table [LINK: Detailed Overview for the Cold Table](./ColdTableOverview.md)
* Dishwasher [LINK: Detailed Overview for the Dishwasher](./DishwasherOverview.md)

## Telemetry for the Smart Kitchen...

## Kitchen HVAC System
![alt text](./Assets/commercial-hvac-header.png "Kitchen HVAC System") 

[LINK: Detailed Overview for the Kitchen HVAC System](./KitchenHVACSystemOverview.md)

    Measurements
    ---------------------------------
    * Airflow Temperature
    * Main Motor RPM
    * CFM

    Baselines and Trends
    ---------------------------------
    * Ideal Temperature = 68 F
    * Main Motor RPM > Trend
    * CFM > Trend

## Walk In Freezer
![alt text](./Assets/commercial-walkin-freezer-header.png "Walk In Freezer") 

[LINK: Detailed Overview for the Walk In Freezer](./WalkInFreezerOverview.md)

    Measurements
    ---------------------------------
    Temperature
    Humidity
    Door Open Count
    Door Ajar
    Compressor Health

    Baselines and Trends
    ---------------------------------
    Ideal Temperature = 0 F
    Ideal Humidity = 100 RH
    Door Open Count is a Trend
    Door Ajar is a Trend
    Compressor Health > 98

## Walk In Refrigerator
![alt text](./Assets/commercial-walkin-fridge-header.png "Walk In Refrigerator") 

[LINK: Detailed Overview for the Walk In Refrigerator](./WalkInRefrigeratorOverview.md)

    Measurements
    ---------------------------------
    Temperature
    Humidity
    Door Open Count
    Door Ajar
    Compressor Health

    Baselines and Trends
    ---------------------------------
    Ideal Temperature = 39 F
    Ideal Humidity = 65 RH
    Door Open Count is a Trend
    Door Ajar is a Trend
    Compressor Health > 98

## Standing Freezer
![alt text](./Assets/commercial-standing-freezer-header.png "Standing Freezer")

[LINK: Detailed Overview for the Standing Freezer](./StandingFreezerOverview.md)

    Measurements
    ---------------------------------
    Temperature
    Humidity
    Door Open Count
    Door Ajar
    Compressor Health

    Baselines and Trends
    ---------------------------------
    Ideal Temperature = 0 F
    Ideal Humidity = 100 RH
    Door Open Count is a Trend
    Door Ajar is a Trend
    Compressor Health > 98

## Standing Refrigerator
![alt text](./Assets/commercial-standing-fridge-header.png "Standing Refrigerator")

[LINK: Detailed Overview for the Standing Refrigerator](./StandingRefrigeratorOverview.md)

    Measurements
    ---------------------------------
    Temperature
    Humidity
    Door Open Count
    Door Ajar
    Compressor Health

    Baselines and Trends
    ---------------------------------
    Ideal Temperature = 39 F
    Ideal Humidity = 65 RH
    Door Open Count is a Trend
    Door Ajar is a Trend
    Compressor Health > 98

## Fryer
![alt text](./Assets/commercial-fryer-header.png "Fryer")

[LINK: Detailed Overview for the Fryer](./FryerOverview.md)

    Measurements
    ---------------------------------
      Temperature
      Oil Quality
      Fryer Heater Health

    Baselines and Trends
    ---------------------------------
      Ideal Temperature = 350-360 F
      Oil Quality > 75
      Fryer Heater Health > 98

## Cold Table
![alt text](./Assets/commercial-cold-table.png "Cold Table")

[LINK: Detailed Overview for the Cold Table](./FryerOverview.md)

    Measurements
    ---------------------------------
      Temperature
      Compressor Health

    Baselines and Trends
    ---------------------------------
      Ideal Temperature = 39 F
      Compressor Health > 98

## Dishwasher
![alt text](./Assets/commercial-dishwasher.png "Dishwasher")

[LINK: Detailed Overview for the Dishwasher](./DishwasherOverview.md)

    Measurements
    ---------------------------------
      Heating Element Health
      Motor Health
      Wash Cycles
      Temperature

    Baselines and Trends
    ---------------------------------
      Ideal Temperature = 180-185 F
      Heating Element Health > 98
      Motor Health > 98
      Wash Cycles - Trend Count
