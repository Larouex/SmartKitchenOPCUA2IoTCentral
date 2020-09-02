# ==================================================================================
#   File:   opcuaserver.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    This class will create an OPC-UA Server and return
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)
# ==================================================================================
import json, sys, time, string, threading, asyncio, os, copy
import logging

# For dumping and Loading Address Space option
from pathlib import Path

# opcua
from asyncua import ua, Server
from asyncua.common.methods import uamethod

# our classes
from Classes.config import Config
from Classes.devicescache import DevicesCache
from Classes.maptelemetrydevices import MapTelemetryDevices
from Classes.varianttype import VariantType


class OpcUaServer():

    def __init__(self, Log, WhatIf):
      self.logger = Log
      self.whatif = WhatIf
      self.opcua_server_instance = None

      # Namespaces
      self.opcua_id_namespace_twins = None
      self.opcua_id_namespace_devices = None

      # Load configuration
      self.config = []
      self.load_config()

      # Load Device Mapping
      self.devicescache = []
      self.load_devicescache()

      self.node_instances = {}
      self.variable_instances = {}

    # -------------------------------------------------------------------------------
    #   Function:   start
    #   Usage:      The start function starts the OPC Server
    # -------------------------------------------------------------------------------
    async def start(self):

      self.logger.info("[SERVER STARTING] GETTING ENDPOINT(s):")

      list_endpoints = self.opcua_server_instance.get_endpoints()

      self.logger.info("[SERVER STARTING] ENDPOINT(s): %s" % list_endpoints)

      async with self.opcua_server_instance:
        while True:
          await asyncio.sleep(self.config["ServerFrequencyInSeconds"])
          self.logger.info("[SERVER] Loop Executed:")

      return

    # -------------------------------------------------------------------------------
    #   Function:   stop
    #   Usage:      The start function starts the OPC Server
    # -------------------------------------------------------------------------------
    async def stop(self):
      await self.opcua_server_instance.stop()
      return

    # -------------------------------------------------------------------------------
    #   Function:   setup
    #   Usage:      The setup function preps the configuration for the OPC Server
    # -------------------------------------------------------------------------------
    async def setup(self):

      # OPCUA Server Setup
      try:

        # configure the endpoint
        opc_url = self.config["ServerUrlPattern"].format(ip = self.config["IPAddress"], port = self.config["Port"])

        # init the server
        self.opcua_server_instance = Server()
        await self.opcua_server_instance.init()

        self.opcua_server_instance.set_endpoint(opc_url)
        self.opcua_server_instance.set_server_name(self.config["ServerDiscoveryName"])
        self.opcua_server_instance.set_application_uri(self.config["ApplicationUri"])

        self.logger.info("[SERVER CONFIG] ENDPOINT: %s" % opc_url)
        self.logger.info("[SERVER CONFIG] APPLICATION URI: %s" % self.config["ApplicationUri"])
        self.logger.info("[SERVER CONFIG] APPLICATION NAME: %s" % self.config["ServerDiscoveryName"])

        # Set NameSpace(s)
        self.opcua_id_namespace_twins = await self.opcua_server_instance.register_namespace(self.config["NameSpaceTwins"])
        self.opcua_id_namespace_devices = await self.opcua_server_instance.register_namespace(self.config["NameSpaceDevices"])

        self.logger.info("[SERVER CONFIG] NAMESPACE TWINS: %s" % self.opcua_id_namespace_twins)
        self.logger.info("[SERVER CONFIG] NAMESPACE DEVICES: %s" % self.opcua_id_namespace_devices)

        return

      except Exception as ex:
        self.logger.error("[ERROR] %s" % ex)
        self.logger.error("[TERMINATING] We encountered an error in OPCUA Server Setup::setup()" )

    # -------------------------------------------------------------------------------
    #   Function:   load_nodes_from_devicecache
    #   Usage:      The load_nodes_from_devicecache function enumerates the
    #               devicescache.json and creates a node for each kind of
    #               Iot Central Device. It looks at a Twin and registers all
    #               of the interfaces and for devices, registers the interface
    # -------------------------------------------------------------------------------
    async def load_nodes_from_devicecache(self):

      # OPCUA Server Setup
      try:

        self.logger.info("[SERVER] STARTING load_nodes_from_devicecache()")

        # Data Type Mappings (OPCUA Datatypes to IoT Central Datatypes)
        variant_type = VariantType(self.logger)

        for device in self.devicescache["Devices"]:

          # DEVICE PER NODE
          if device["DeviceType"] == "device":
            self.logger.info("[SERVER] DEVICE TYPE: %s" % device["DeviceType"])
            self.logger.info("[DEVICE] DEVICE NAME: %s" % device["DeviceName"])

            self.node_instances[device["DeviceName"]] = await self.opcua_server_instance.nodes.objects.add_object(self.opcua_id_namespace_devices, device["DeviceName"])
            self.logger.info("[SERVER] NODE ID: %s" % self.node_instances[device["DeviceName"]])

            for interface in device["Interfaces"]:

              config_interface = [obj for obj in self.config["Nodes"] if obj["InterfaceInstanceName"]==interface["InterfaceInstanceName"]]
              print("----HERE------ %s" % config_interface)

              for variable in config_interface[0]["Variables"]:
                variable_name = variable["DisplayName"]
                telemetry_name = variable["TelemetryName"]
                range_value = variable["RangeValues"][0]
                opc_variant_type = variant_type.map_variant_type(variable["IoTCDataType"])

                # Log Verbose Feedback
                log_msg = "[SETUP VARIABLE] DISPLAY NAME: {dn} TELEMETRY NAME: {tn} RANGE VALUE: {rv} IoTC TYPE: {it} OPC VARIANT TYPE {ovt} OPC DATA TYPE {odt}"
                self.logger.info(log_msg.format(dn = variable["DisplayName"], vn = variable["TelemetryName"], tn = variable["TelemetryName"], rv = variable["RangeValues"][0], it = variable["IoTCDataType"], ovt = opc_variant_type, odt = opc_variant_type))

                # Create Node Variable
                nodeObject = await self.node_instances[device["DeviceName"]].add_variable(self.opcua_id_namespace_devices, telemetry_name, range_value)
                await nodeObject.set_writable()
                self.variable_instances[telemetry_name] = nodeObject

          elif device["DeviceType"] == "twin":

            self.logger.info("[SERVER] DEVICE TYPE: %s" % device["DeviceType"])
            self.logger.info("[DEVICE] TWIN NAME: %s" % device["DeviceName"])

            self.node_instances[device["DeviceName"]] = await self.opcua_server_instance.nodes.objects.add_object(self.opcua_id_namespace_devices, device["DeviceName"])
            self.logger.info("[SERVER] NODE ID: %s" % self.node_instances[device["DeviceName"]])

            for interface in device["Interfaces"]:

              config_interface = [obj for obj in self.config["Nodes"] if obj["InterfaceInstanceName"]==interface["InterfaceInstanceName"]]

              for variable in config_interface[0]["Variables"]:
                variable_name = variable["DisplayName"]
                telemetry_name = variable["TelemetryName"]
                range_value = variable["RangeValues"][0]
                opc_variant_type = variant_type.map_variant_type(variable["IoTCDataType"])

                # Log Verbose Feedback
                log_msg = "[SETUP VARIABLE] DISPLAY NAME: {dn} TELEMETRY NAME: {tn} RANGE VALUE: {rv} IoTC TYPE: {it} OPC VARIANT TYPE {ovt} OPC DATA TYPE {odt}"
                self.logger.info(log_msg.format(dn = variable["DisplayName"], vn = variable["TelemetryName"], tn = variable["TelemetryName"], rv = variable["RangeValues"][0], it = variable["IoTCDataType"], ovt = opc_variant_type, odt = opc_variant_type))

                # Create Node Variable
                nodeObject = await self.node_instances[device["DeviceName"]].add_variable(self.opcua_id_namespace_devices, telemetry_name, range_value)
                await nodeObject.set_writable()
                self.variable_instances[telemetry_name] = nodeObject

        return

      except Exception as ex:
        self.logger.error("[ERROR] %s" % ex)
        self.logger.error("[TERMINATING] We encountered an error in OPCUA Server Setup::load_nodes_from_devicecache()")

    # -------------------------------------------------------------------------------
    #   Function:   load_config
    #   Usage:      Loads the configuration from file and setup iterators for
    #               sending telemetry in sequence
    # -------------------------------------------------------------------------------
    def load_config(self):

      config = Config(self.logger)
      self.config = config.data
      return

    # -------------------------------------------------------------------------------
    #   Function:   load_devicescache
    #   Usage:      Loads the Devices that have been registered and provisioned
    # -------------------------------------------------------------------------------
    def load_devicescache(self):

      devicescache = DevicesCache(self.logger)
      self.devicescache = devicescache.data
      return


