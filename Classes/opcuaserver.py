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
from Classes.maptelemetrydevices import MapTelemetryDevices
from Classes.varianttype import VariantType


class OpcUaServer():

    def __init__(self, Log, WhatIf):
      self.logger = Log
      self.whatif = WhatIf
      self.opcua_server_instance = None
      self.config = []
      self.load_config()

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
        await self.opcua_server_instance.set_endpoint(opc_url)
        await self.opcua_server_instance.set_server_name(self.config["ServerDiscoveryName"])
        await self.opcua_server_instance.set_application_uri(self.config["ApplicationUri"])

        self.logger.info("[SERVER CONFIG] ENDPOINT: %s" % opc_url)
        self.logger.info("[SERVER CONFIG] APPLICATION URI: %s" % self.config["ApplicationUri"])
        self.logger.info("[SERVER CONFIG] APPLICATION NAME: %s" % self.config["ServerDiscoveryName"])

        return

      except Exception as ex:
        self.logger.error("[ERROR] %s" % ex)
        self.logger.error("[TERMINATING] We encountered an error in OPCUA Server Setup" )

    # -------------------------------------------------------------------------------
    #   Function:   load_config
    #   Usage:      Loads the configuration from file and setup iterators for
    #               sending telemetry in sequence
    # -------------------------------------------------------------------------------
    def load_config(self):

      config = Config(self.logger)
      self.config = config.data
      return

