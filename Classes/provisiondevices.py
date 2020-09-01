
# ==================================================================================
#   File:   provisiondevices.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Provisions Devices and updates cache file and do device provisioning 
#           via DPS for IoT Central
#
#   Online: www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import time, logging, string, json, os, binascii, struct, threading, asyncio, datetime

# Sur classes
from Classes.devicescache import DevicesCache
from Classes.secrets import Secrets
from Classes.symmetrickey import SymmetricKey
from Classes.config import Config


# uses the Azure IoT Device SDK for Python (Native Python libraries)
from azure.iot.device.aio import ProvisioningDeviceClient

# -------------------------------------------------------------------------------
#   ProvisionDevices Class
# -------------------------------------------------------------------------------
class ProvisionDevices():

    timer = None
    timer_ran = False
    dcm_value = None

    def __init__(self, Log, WhatIf, Id, InFileName, ModelType, NumberOfDevices):
      self.logger = Log
      self.whatif = WhatIf
      self.iddevice = Id
      self.in_file_name = InFileName
      self.model_type = ModelType
      self.number_of_devices = NumberOfDevices
      self.config = {}
      self.nodes = {}
      self.data = []
      self.devices_provision = []
      self.new_devices = []
      self.characteristics = []
      self.load_config()
      self.device_secrets = []
  
    async def provision_devices(self):

      # First up we gather all of the needed provisioning meta-data and secrets
      try:

        # Make a working copy of the cache file
        devicescache = DevicesCache(self.logger)
        self.data = devicescache.data
        print("self.data %s" % self.data)
        #return
        #self.data["Devices"] = [x for x in devicescache.data["Devices"] if x["DeviceName"] == "Simulated Device"]
        self.logger.info("[DEVICES] self.data Count %s" % len(self.data["Devices"]))

        # load the secrets
        secrets = Secrets(self.logger)
        secrets.init()

        # Symetric Key for handling Device Specific SaS Keys
        symmetrickey = SymmetricKey(self.logger)
      
      except Exception as ex:
        self.logger.error("[ERROR] %s" % ex)
        self.logger.error("[TERMINATING] We encountered an error gathering needed provisioning meta-data and secrets" )
        return

      # [TWIN] Provisioning
      # Based upon the type of provisionign we are performing (twin or device), we gather
      # up all of our meta-data and enumerate to create the devices in IoT Central
      if (self.model_type == "twin"):
        
        try:

          # Gather and Define the DCM Information
          
          # Device Id is formatted as [larouex-smart-kitchen-{id}]
          id_number_str = str(self.iddevice)
          id_number_str = id_number_str.zfill(3)
          device_id = self.config["DeviceNameTwin"].format(id=id_number_str)

          dcm_id = self.config["DeviceCapabilityModelId"]
          device_capability_model = self.create_device_capability_model(device_id, dcm_id)
          self.logger.info("[DCM ID] %s" % dcm_id)
          self.logger.info("[DEVICE ID] %s" % device_id)
          self.logger.info("[DCM] %s" % device_capability_model)

          # Let's Look at the config file and generate 
          # our twin device from the interfaces configuration
          for node in self.nodes:
            device_interface = self.create_device_interface(node["Name"], node["InterfacelId"], node["InterfaceInstanceName"])
            device_capability_model["Interfaces"].append(device_interface)
            self.logger.info("[INTERFACE] %s" % device_interface)

          # Dump the Device Info  
          self.logger.info("[DEVICE] MODEL %s" % device_capability_model)
           
          # Get a Device Specific Symetric Key
          device_symmetrickey = symmetrickey.compute_derived_symmetric_key(device_capability_model["DeviceName"], secrets.get_device_secondary_key())
          self.logger.info("[SYMETRIC KEY] %s" % device_symmetrickey)

          # Provision the Device
          self.logger.info("[PROVISIONING] %s" % device_capability_model["DeviceName"])
          
          # Check if we are in WhatIf and if not, let's provision the device as collective
          # twin patterm into IoT Central...
          if not self.whatif:
            
            self.logger.info("[PROVISIONING HOST]: %s" % secrets.get_provisioning_host())

            # Azure IoT Central SDK Call to create the provisioning_device_client
            provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
              provisioning_host = secrets.get_provisioning_host(),
              registration_id = device_capability_model["DeviceName"],
              id_scope = secrets.get_scope_id(),
              symmetric_key = device_symmetrickey,
              websockets=True
            )

            # Azure IoT Central SDK call to set the DCM payload and provision the device
            provisioning_device_client.provisioning_payload = '{"iotcModelId":"%s"}' % (device_capability_model["DeviceCapabilityModelId"])
            registration_result = await provisioning_device_client.register()
            device_capability_model["DeviceName"]
            self.device_secrets.append(self.create_device_secret(device_capability_model["DeviceName"], registration_result.registration_state.assigned_hub, device_symmetrickey))
            self.logger.info("[REGISTRATION RESULT] %s" % registration_result)

          self.data["Devices"].append(device_capability_model)

        except Exception as ex:
          self.logger.error("[ERROR] %s" % ex)
          self.logger.error("[TERMINATING] We encountered an error provisioning the twin as a device in IoT Central" )
          return

        # Update the Cache
        if not self.whatif:
          devicescache.update_file(self.data)
          secrets.update_device_secrets(self.device_secrets)

        return

      # [DEVICE] Provisioning
      # Based upon the type of provisionign we are performing (twin or device), we gather
      # up all of our meta-data and enumerate to create the devices in IoT Central
      elif (self.model_type == "device"):
        
        try:

          # Let's Look at the config file and generate 
          # our twin device from the interfaces configuration
          for node in self.nodes:
            
            # check if we are excluding 
            if self.config["PerDeviceDeviceIgnoreInterfaceIds"].count(node["InterfacelId"]) == 0:

              # We will enumerate the number of devices we are going to create
              for x in range(self.number_of_devices):
                
                # Gather and Define the DCM Information
                id_number_str = str(int(self.iddevice) + x)
                id_number_str = id_number_str.zfill(3)
                
                # Device Id is formatted as [larouex-smart-kitchen-{deviceName}-{id}]
                device_id = self.config["DeviceNameDevice"].format(deviceName = node["Name"], id=id_number_str)

                # PerDeviceDeviceCapabilityModelId is formatted as [urn:LarouexSmartKitchen:{deviceName}:1]
                dcm_id = self.config["PerDeviceDeviceCapabilityModelId"].format(deviceName = node["Name"])

                # Get our DCM Instantiated
                device_capability_model = self.create_device_capability_model(device_id, dcm_id)
                self.logger.info("[DCM ID] %s" % dcm_id)
                self.logger.info("[DEVICE ID] %s" % device_id)
                self.logger.info("[DCM] %s" % device_capability_model)

                device_interface = self.create_device_interface(node["Name"], node["InterfacelId"], node["InterfaceInstanceName"])
                device_capability_model["Interfaces"].append(device_interface)
                self.logger.info("[INTERFACE] %s" % device_interface)

                # Dump the Device Info  
                self.logger.info("[DEVICE] MODEL %s" % device_capability_model)
                
                # Get a Device Specific Symetric Key
                device_symmetrickey = symmetrickey.compute_derived_symmetric_key(device_capability_model["DeviceName"], secrets.get_device_secondary_key())
                self.logger.info("[SYMETRIC KEY] %s" % device_symmetrickey)

                # Provision the Device
                self.logger.info("[PROVISIONING] %s" % device_capability_model["DeviceName"])
            
                # Check if we are in WhatIf and if not, let's provision the device as collective
                # twin patterm into IoT Central...
                if not self.whatif:
                  
                  self.logger.info("[PROVISIONING HOST]: %s" % secrets.get_provisioning_host())

                  # Azure IoT Central SDK Call to create the provisioning_device_client
                  provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
                    provisioning_host = secrets.get_provisioning_host(),
                    registration_id = device_capability_model["DeviceName"],
                    id_scope = secrets.get_scope_id(),
                    symmetric_key = device_symmetrickey,
                    websockets=True
                  )

                  # Azure IoT Central SDK call to set the DCM payload and provision the device
                  provisioning_device_client.provisioning_payload = '{"iotcModelId":"%s"}' % (device_capability_model["DeviceCapabilityModelId"])
                  registration_result = await provisioning_device_client.register()
                  device_capability_model["DeviceName"]
                  self.device_secrets.append(self.create_device_secret(device_capability_model["DeviceName"], registration_result.registration_state.assigned_hub, device_symmetrickey))
                  self.logger.info("[REGISTRATION RESULT] %s" % registration_result)

                try:
                  device_previous_index = [x for x in devicescache.data["Devices"] if x["DeviceName"] == device_capability_model["DeviceName"]].index()
                  print("device_previous_index %s" % device_previous_index)
                  self.data["Devices"][device_previous_index] = device_capability_model
                except:
                  self.data["Devices"].append(device_capability_model)
              
            else:
              self.logger.info("[SKIPPING NODE] Included PerDeviceDeviceIgnoreInterfaceIds")

        except Exception as ex:
          self.logger.error("[ERROR] %s" % ex)
          self.logger.error("[TERMINATING] We encountered an error provisioning the device as a device in IoT Central" )
          return

        # Update the Cache
        if not self.whatif:
          devicescache.update_file(self.data)
          secrets.update_device_secrets(self.device_secrets)

    # -------------------------------------------------------------------------------
    #   Function:   load_config
    #   Usage:      Loads the configuration
    # -------------------------------------------------------------------------------
    def load_config(self):
      
      # Load all the configuration
      config = Config(self.logger)
      self.config = config.data
      self.nodes = self.config["Nodes"]

    # -------------------------------------------------------------------------------
    #   Function:   create_device_interface
    #   Usage:      Returns a Device Interface for Interfaces Array
    # -------------------------------------------------------------------------------
    def create_device_capability_model(self, deviceName, id):
      newDeviceCapabilityModel = {
        "DeviceName": deviceName, 
        "DeviceType": self.model_type,
        "DeviceCapabilityModelId": id,
        "Interfaces": [
        ],
        "LastProvisioned": str(datetime.datetime.now())
      } 
      return newDeviceCapabilityModel 

    # -------------------------------------------------------------------------------
    #   Function:   create_device_interface
    #   Usage:      Returns a Device Interface for Interfaces Array
    # -------------------------------------------------------------------------------
    def create_device_interface(self, name, id, instantName):
      newInterface = {
        "Name": name,
        "InterfacelId": id,
        "InterfaceInstanceName": instantName
      }
      return newInterface 

    # -------------------------------------------------------------------------------
    #   Function:   create_device_interface
    #   Usage:      Returns a Device Interface for Interfaces Array
    # -------------------------------------------------------------------------------
    def create_device_secret(self, name, assigned_hub, device_symmetric_key):
      newDeviceSecret = {
        "Name": name,
        "AssignedHub": assigned_hub,
        "DeviceSymmetricKey": device_symmetric_key
      }
      return newDeviceSecret 

