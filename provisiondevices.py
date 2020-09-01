# ==================================================================================
#   File:   provisiondevices.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Simple OPC/UA Server for testing Azure IoT Central Scenarios.
#           This module provisions devices and updates the devicescache. 
#           It either re-provisions all devices or just those that have null in
#           LastProvisioned option in the file i.e "LastProvisioned": null
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import  getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from Classes.provisiondevices import ProvisionDevices
from Classes.config import Config

# -------------------------------------------------------------------------------
#   Provision Devices
# -------------------------------------------------------------------------------
async def provision_devices(Whatif, Id, InFileName, ModelType, NumberOfDevices):

  provisiondevices = ProvisionDevices(Log, Whatif, Id, InFileName, ModelType, NumberOfDevices)
  await provisiondevices.provision_devices()
  return True

async def main(argv):

    # execution state from args
    whatif = False
    id = 1
    infilename = None
    model_type = "twin"
    number_of_devices = 1

    short_options = "hvdwr:i:m:n:"
    long_options = ["help", "verbose", "debug", "whatif", "registerid=", "infilename=", "modeltype=", "numberofdevices="]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))
    
    for current_argument, current_value in arguments:
      if current_argument in ("-h", "--help"):
        print("------------------------------------------------------------------------------------------------------------------------------------------")
        print("HELP for provisiondevices.py")
        print("------------------------------------------------------------------------------------------------------------------------------------------")
        print("")
        print("  BASIC PARAMETERS...")
        print("")
        print("  -h or --help - Print out this Help Information")
        print("  -v or --verbose - Debug Mode with lots of Data will be Output to Assist with Debugging")
        print("  -d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging")
        print("  -w or --whatif - Combine with Verbose it will Output the Configuration sans starting the Server")
        print("")
        print("  OPTIONAL PARAMETERS...")
        print("")
        print("    -r or --registerid - This numeric value will get appended to your provisioned device. Example '1' would result in larouex-smart-kitchen-1")
        print("       USAGE: -r 5")
        print("       DEFAULT: 1")
        print("")
        print("    -i or --infilename - Name of the configuration file to process for generation of the DTDL mapping.")
        print("       USAGE: -i config_smartkitchen.json")
        print("       DEFAULT: config.json")
        print("")
        print("    -m or --modeltype - Provision as collective Twin Pattern or by Device Pattern.")
        print("       USAGE: -m device")
        print("       DEFAULT: twin")
        print("")
        print("    -n or --numberofdevices - The value is used to enumerate and provision the device(s) count specificed.")
        print("       USAGE: -n 10")
        print("       DEFAULT: 1")
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
        Log.info("Whatif Mode...")

      if current_argument in ("-r", "--registerid"):
        id = current_value
        Log.info("Register Id is Specified as: {id}".format(id = id))

        # validate the number is a NUMBER
        if (id.isnumeric() == False):
          print("[ERROR] -r --registerid must be a numeric value")
          return

      if current_argument in ("-i", "--infilename"):
        infilename = current_value
        Log.info("In File Name is Specified as: {infilename}".format(infilename = infilename))
        
      if current_argument in ("-m", "--modeltype"):
        model_type = current_value
        Log.info("Model Type is Specified as: {model_type}".format(model_type = model_type))
        
        # validate the value is one of our allowed parameters
        if (model_type != "twin" and model_type != "device"):
          print("[ERROR] -m --modeltype must be specified as either twin | device")
          return

      if current_argument in ("-n", "--numberofdevices"):
        number_of_devices = current_value
        Log.info("Number of Devices is Specified as: {numberofdevices}".format(numberofdevices = number_of_devices))
        
        # validate the number is a NUMBER
        if (isinstance(number_of_devices, str) and not number_of_devices.isnumeric()):
          print("[ERROR] -n --numberofdevices must be a numeric value between 1 and 10")
          return
        elif isinstance(number_of_devices, str):
          number_of_devices = int(number_of_devices)
        
        # validate the number is contrained to our boundry
        if (number_of_devices > 10):
          print("[ERROR] -n --numberofdevices must be a numeric value between 1 and 10")
          return

    await provision_devices(whatif, id, infilename, model_type, number_of_devices)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))

