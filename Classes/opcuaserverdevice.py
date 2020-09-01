# ==================================================================================
#   File:   opcuaserverdevice.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    This class will create an OPC-UA Server that is capable of sending
#           multiple device data
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
from Classes.maptelemetrydevices import MapTelemetryDevices
from Classes.varianttype import VariantType


class OpcUaServerDevice():
    
<<<<<<< HEAD
    def __init__(self, Log, WhatIf, InterfaceName):
      self.logger = Log
      self.whatif = WhatIf
      self.interface_name = InterfaceName
=======
    def __init__(self, Log, WhatIf):
      self.logger = Log
      self.whatif = WhatIf
>>>>>>> ab7c1046a396566a2e95fc6617baec378eb3c68d
      self.config = []
      self.nodes = []
      self.nodes_dict = {}
      self.nodes_dict_counter = {}
      self.map_telemetry = []
      self.map_telemetry_nodes = []
      self.map_telemetry_nodes_variables = []
      self.load_config()
        
    # -------------------------------------------------------------------------------
    #   Function:   start
    #   Usage:      The start function loads configuration and starts the OPC Server
    # -------------------------------------------------------------------------------
    async def start(self):

      node_obj = {}
      variable_obj = {}
      node_count = 0

      # Data Type Mappings (OPCUA Datatypes to IoT Central Datatypes)
      variant_type = VariantType(self.logger)
      
      # OPCUA Server Setup
      # Here we setup the Server and add discovery
      try:

        # configure the endpoint
        opc_url1 = self.config["PerDeviceServerUrlPattern"].format(ip = self.config["IPAddress"], port = self.config["Port"], interfaceName = self.interface_name)
        opc_url2 = self.config["PerDeviceServerUrlPattern"].format(ip = self.config["IPAddress"], port = "4841", interfaceName = self.interface_name)
        
        # init the server
        opc_server = Server()
        await opc_server.init()
        
        # set the endpoint and name
        opc_server.set_endpoint(opc_url1)
        #opc_server.iserver.add_endpoint(opc_url2)
        opc_server.set_server_name(self.config["PerDeviceServerDiscoveryName"].format(interfaceName = self.interface_name))
        
        # set discovery
        await opc_server.set_application_uri(self.config["PerDeviceApplicationUri"].format(interfaceName = self.interface_name))

        log_msg = "[SERVER CONFIG] ENDPOINT: {ep} APPLICATION URI: {au} APPLICATION NAME: {an}"
        self.logger.info(log_msg.format(ep = opc_url1, au = self.config["PerDeviceApplicationUri"].format(interfaceName = self.interface_name), an = self.config["PerDeviceServerDiscoveryName"].format(interfaceName = self.interface_name)))

        # Setup root for Map Telemetry
        self.map_telemetry = self.create_map_telemetry(self.config["PerDeviceNameSpace"].format(interfaceName = self.interface_name), self.config["PerDeviceDeviceCapabilityModelId"].format(deviceName = self.interface_name))

        # Set NameSpace
        namespace = self.config["PerDeviceNameSpace"].format(interfaceName = self.interface_name)
        id_namespace = await opc_server.register_namespace(namespace)
        self.logger.info("[NAMESPACE] %s" % namespace)

        # Create our nodes and Parameters
        for node in self.nodes:
<<<<<<< HEAD
          
          # are working on the passed Interface Name?
          if node["Name"] == self.interface_name:
        
            # Create node
            node_obj[node["Name"]] = await opc_server.nodes.objects.add_object(id_namespace, node["Name"])
          
            # Setup Map Telemetry
            self.map_telemetry["nodes"].append(self.create_map_telemetry_node(node["Name"], str(node_obj[node["Name"]]), node["InterfacelId"], node["InterfaceInstanceName"]))
            self.logger.info("[node ID] %s" % node_obj[node["Name"]])

            # Set the meta-data for the Variable
            for variable in node["Variables"]:
            
              variable_name = variable["DisplayName"]
              telemetry_name = variable["TelemetryName"]
              range_value = variable["RangeValues"][0]
              opc_variant_type = variant_type.map_variant_type(variable["IoTCDataType"])
            
              # Log Verbose Feedback
              log_msg = "[SETUP VARIABLE] node NAME: {nn} DISPLAY NAME: {dn} TELEMETRY NAME: {tn} RANGE VALUE: {rv} IoTC TYPE: {it} OPC VARIANT TYPE {ovt} OPC DATA TYPE {odt}"
              self.logger.info(log_msg.format(nn = node["Name"], dn = variable["DisplayName"], vn = variable["TelemetryName"], tn = variable["TelemetryName"], rv = variable["RangeValues"][0], it = variable["IoTCDataType"], ovt = opc_variant_type, odt = opc_variant_type))

              # Create node Variable
=======

          # Add Node and Begin Populating our Address Space
          if not self.whatif:
            # Create Node
            node_obj[node["Name"]] = await opc_server.nodes.objects.add_object(id_namespace, node["Name"])
            self.logger.info("[NODE ID] %s" % node_obj[node["Name"]])
            # Setup nodes for Map Telemetry
            self.map_telemetry["Nodes"].append(self.create_map_telemetry_node(node["Name"], str(node_obj[node["Name"]]), node["InterfacelId"], node["InterfaceInstanceName"]))

          for variable in node["Variables"]:
            variable_name = variable["DisplayName"]
            telemetry_name = variable["TelemetryName"]
            range_value = variable["RangeValues"][0]
            opc_variant_type = variant_type.map_variant_type(variable["IoTCDataType"])
            log_msg = "[SETUP VARIABLE] NODE NAME: {nn} DISPLAY NAME: {dn} TELEMETRY NAME: {tn} RANGE VALUE: {rv} " \
              "IoTC TYPE: {it} OPC VARIANT TYPE {ovt} OPC DATA TYPE {odt}"
            self.logger.info(log_msg.format(nn = node["Name"], dn = variable["DisplayName"], vn = variable["TelemetryName"], \
              tn = variable["TelemetryName"], rv = variable["RangeValues"][0], it = variable["IoTCDataType"], \
                ovt = opc_variant_type, odt = opc_variant_type))

            if not self.whatif:
              # Create Node Variable
>>>>>>> ab7c1046a396566a2e95fc6617baec378eb3c68d
              nodeObject = await node_obj[node["Name"]].add_variable(id_namespace, telemetry_name, range_value)
              await nodeObject.set_writable()
              variable_obj[telemetry_name] = nodeObject
              self.map_telemetry_nodes_variables.append(self.create_map_telemetry_variable(variable_name, telemetry_name, str(variable_obj[telemetry_name]), variable["IoTCDataType"]))
<<<<<<< HEAD
          
          node_count = node_count + 1
        
        self.update_map_telemetry()
=======

          if not self.whatif:
            self.map_telemetry["Nodes"][node_count]["Variables"] = copy.copy(self.map_telemetry_nodes_variables)
            self.logger.info("[MAP] %s" % self.map_telemetry)
            self.map_telemetry_nodes_variables =  []

          node_count += 1
>>>>>>> ab7c1046a396566a2e95fc6617baec378eb3c68d

      except Exception as ex:
        self.logger.error("[ERROR] %s" % ex)
        self.logger.error("[TERMINATING] We encountered an error in OPCUA Server Setup" )
        return
      
      # Start the server loop
      self.logger.info("[STARTING SERVER] %s" % opc_url1)
      #await opc_server.start()

      async with opc_server:
        while True:
          await asyncio.sleep(self.config["ServerFrequencyInSeconds"])
          
          for node in self.nodes:
              
            # Only execute the passed node for the instance
            if node["Name"] == self.interface_name:

              temp_dict = self.nodes_dict[node["Name"]]
              temp_dict_counter = self.nodes_dict_counter[node["Name"]]
                
              for variable in node["Variables"]:
                count = temp_dict_counter[variable["TelemetryName"]]
                sequence_count = temp_dict[variable["TelemetryName"]]

                if count > (sequence_count - 1):
                  count = 0              

                # Choose the next value in the telemetry sequence for the variable
                self.nodes_dict_counter[node["Name"]][variable["TelemetryName"]] = (count + 1)
                value = variable["RangeValues"][count]
                  
                await variable_obj[variable["TelemetryName"]].write_value(value)
                  
                log_msg = "[LOOP] {nn} {tn} {vw} {tc} SEQ({sc}) CUR({cc})"
                self.logger.info(log_msg.format(nn = node["Name"], tn = variable["TelemetryName"], vw = value, tc = count, sc = temp_dict[variable["TelemetryName"]], cc = temp_dict_counter[variable["TelemetryName"]]))

      return

    # -------------------------------------------------------------------------------
    #   Function:   load_config
    #   Usage:      Loads the configuration from file and setup iterators for
    #               sending telemetry in sequence
    # -------------------------------------------------------------------------------
    def load_config(self):
      
      # Load all the configuration
      config = Config(self.logger)
      self.config = config.data
      self.nodes = self.config["Nodes"]
      
      # These counters support looping through our bounded telemetry values
      for node in self.nodes:
        if node["Name"] == self.interface_name:
          variable_dict = {}
          variable_dict_counter = {}
          for variable in node["Variables"]:
            variable_dict[variable["TelemetryName"]] = len(variable["RangeValues"])
            variable_dict_counter[variable["TelemetryName"]] = 0

          self.nodes_dict[node["Name"]] = copy.deepcopy(variable_dict)
          self.nodes_dict_counter[node["Name"]] = copy.copy(variable_dict_counter)
          log_msg = "[LOOP DICTIONARY] NAME: {n} COUNTER: {c}"
          self.logger.info(log_msg.format(n = self.nodes_dict[node["Name"]], c = self.nodes_dict_counter[node["Name"]]))
          break
        else:
          self.logger.info("[Node MATCH FAIL] %s" % node["Name"] + " != " + self.interface_name)
      
      self.logger.info("[NODES_DICT] %s" % self.nodes_dict)
      self.logger.info("[NODES_DICT_COUNTER] %s" % self.nodes_dict_counter)
      return

    # -------------------------------------------------------------------------------
    #   Function:   create_map_telemetry
    #   Usage:      Sets the root for the Map Telemetry configuration file
    # -------------------------------------------------------------------------------
    def create_map_telemetry(self, NameSpace, DeviceCapabilityModelId):
      mapTelemetry = {
        "NameSpace": NameSpace, 
        "DeviceCapabilityModelId": DeviceCapabilityModelId,
        "nodes": [
        ]
      }
      return mapTelemetry 

    # -------------------------------------------------------------------------------
    #   Function:   create_map_telemetry_node
    #   Usage:      Sets the node for the Map Telemetry configuration file
    # -------------------------------------------------------------------------------
    def create_map_telemetry_node(self, Name, nodeId, InterfacelId, InterfaceInstanceName):
      mapTelemetrynode = {
        "Name": Name,
        "nodeId": nodeId,
        "InterfacelId": InterfacelId,
        "InterfaceInstanceName": InterfaceInstanceName,
        "Variables":[
        ]
      }
      return mapTelemetrynode 
    
    # -------------------------------------------------------------------------------
    #   Function:   create_map_telemetry_variable
    #   Usage:      Sets the variable for the Map Telemetry configuration file
    # -------------------------------------------------------------------------------
    def create_map_telemetry_variable(self, DisplayName, TelemetryName, nodeId, IoTCDataType):
      mapTelemetrynodeVariable = {
        "DisplayName": DisplayName,
        "TelemetryName": TelemetryName,
        "nodeId": nodeId,
        "IoTCDataType": IoTCDataType
      }
      return mapTelemetrynodeVariable 

    # -------------------------------------------------------------------------------
    #   Function:   update_map_telemetry
    #   Usage:      Saves the generated Map Telemetry File
    # -------------------------------------------------------------------------------
    def update_map_telemetry(self):
      map_telemetry_file = MapTelemetryDevices(self.logger)
      map_telemetry_file.update_file(self.map_telemetry)
      return
