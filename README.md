# SmartKitchenOPCUA2IoTCentral
Demonstrates the use of OPC-UA to Monitor the Equipment in a Smart Commercial Kitchen with Telemetry and Integration to Azure IoT Central via a Transparent Gateway with Protocol Translation. 

## Smart Kitchen Appliances
The core of this demo application for Azure IoT Central is the emulation of commercial kitchen. We have included the following standard appliance models...

* Ambient Environment
* Kitchen HVAC System
* Walk In Freezer
* Walk In Refrigerator
* Standing Refrigerator
* Standing Freezer
* Fryer
* Cold Table
* Dishwasher

Let's go through the telemetry for each model...

## Kitchen HVAC System

    ### Measurements
    * Airflow Temperature
    * Main Motor RPM
    * CFM

    ### Baselines and Trends
    * Ideal Temperature = 68 F
    * Main Motor RPM > Trend
    * CFM > Trend
