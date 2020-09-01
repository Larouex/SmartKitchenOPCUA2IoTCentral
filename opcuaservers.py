#!/home/Larouex/Python-3.8.5 python3.8
# ==================================================================================
#   File:   opcuaservers.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Complex OPC/UA Server for testing Azure IoT Central Scenarios that
#           supports multiple OPC-UA servers on an endpoint mapping to the
#           multiple twin apporach or many devices
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)
# ==================================================================================
import  getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from Classes.opcuaserverdevice import OpcUaServerDevice
from Classes.opcuaserver import OpcUaServer

from Classes.config import Config
from Classes.varianttype import VariantType

# -------------------------------------------------------------------------------
#   Setup the OPC Server for Multiple Twin and Device Patterns
# -------------------------------------------------------------------------------
async def setup_server(WhatIf, OpcuaServer):

  try:

    Log.info("[SERVER] setup_server...")
    return await OpcuaServer.setup()

  except Exception as ex:
    Log.error("[ERROR] %s" % ex)
    Log.error("[TERMINATING] We encountered an error in [setup_server]" )
    return


# -------------------------------------------------------------------------------
#   Start the OPC Server for Multiple Twin and Device Patterns
# -------------------------------------------------------------------------------
async def start_server(WhatIf, OpcuaServer):

  try:

    Log.info("[SERVER] start_server...")
    return await OpcuaServer.start()

  except Exception as ex:
    Log.error("[ERROR] %s" % ex)
    Log.error("[TERMINATING] We encountered an error in [start_server]" )

  finally:
    await stop_server(WhatIf, OpcuaServer)

# -------------------------------------------------------------------------------
#   Start the OPC Server for Multiple Twin and Device Patterns
# -------------------------------------------------------------------------------
async def stop_server(WhatIf, OpcuaServer):

  try:

    Log.info("[SERVER] stop_server...")
    await OpcuaServer.stop()
    return

  except Exception as ex:
    Log.error("[ERROR] %s" % ex)
    Log.error("[TERMINATING] We encountered an error in [stop_server]" )


# -------------------------------------------------------------------------------
#   Start the OPC Server for Multiple Devices
# -------------------------------------------------------------------------------
async def start_server_device(WhatIf, InterfaceName):

  # Start Server
  opc_server = OpcUaServerDevice(Log, WhatIf, InterfaceName)
  await opc_server.start()

  return

async def main(argv):

  # parameters
  whatif = False
  model_type = "twin"
  interface_name = None

  # execution state from args
  short_options = "hvdwm:i:"
  long_options = ["help", "verbose", "debug", "whatif", "modeltype=", "interfacename="]
  full_cmd_arguments = sys.argv
  argument_list = full_cmd_arguments[1:]
  try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
  except getopt.error as err:
    print (str(err))
  
  for current_argument, current_value in arguments:
    
    if current_argument in ("-h", "--help"):
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("HELP for opcuaservers.py")
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      print("")
      print("  BASIC PARAMETERS...")
      print("")
      print("  -h or --help - Print out this Help Information")
      print("  -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging")
      print("  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging")
      print("  -w or --whatif - Combine with Verbose it will Output the Configuration sans starting the Server")
      print("")
      print("  REQUIRED PARAMETERS...")
      print("")
      print("    -i or --interfacename - Indicate the name (case-senstive) of the Iterface Node to Instantiate the OPC-UA Server.")
      print("       USAGE: -m WalkinFreezer")
      print("")
      print("  OPTIONAL PARAMETERS...")
      print("")
      print("    -m or --modeltype - Execute the OPC-UA Server as Twin Collection of Interfaces or Specific Devices.")
      print("       USAGE: -m device")
      print("       DEFAULT: twin")
      print("------------------------------------------------------------------------------------------------------------------------------------------")
      return
      
    if current_argument in ("-v", "--verbose"):
      Log.basicConfig(format="%(levelname)s: %(message)s", level = Log.INFO)
      Log.info("Verbose Logging Mode...")
    else:
      Log.basicConfig(format="%(levelname)s: %(message)s")

    if current_argument in ("-d", "--debug"):
      Log.basicConfig(format="%(levelname)s: %(message)s", level = Log.DEBUG)
      Log.info("Debug Logging Mode...")
    else:
      Log.basicConfig(format="%(levelname)s: %(message)s")

    if current_argument in ("-w", "--whatif"):
      whatif = True
      Log.info("WhatIf Mode...")

    if current_argument in ("-i", "--interfacename"):
      interface_name = current_value
      Log.info("Interface Name is Specified as: {interface_name}".format(interface_name = interface_name))

    if current_argument in ("-m", "--modeltype"):
      model_type = current_value
      Log.info("Model Type is Specified as: {model_type}".format(model_type = model_type))

      # validate the value is one of our allowed parameters
      if (model_type != "twin" and model_type != "device"):
        Log.info("[ERROR] -m --modeltype must be specified as either twin | device")
        return

  # validate the value is one of our allowed parameters
  if (interface_name == None):
    Log.info("[ERROR] Missing --interfacename parameter. Indicate the name (case-senstive) of the Iterface Node to Instantiate the OPC-UA Server.")
    return

  # Configure Server
  opcua_server = OpcUaServer(Log, whatif)
  await setup_server(whatif, opcua_server)
  Log.info("[SERVER] Instance Info (opcua_server): %s" % opcua_server)
  
  await start_server(whatif, opcua_server)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))

