# ==================================================================================
#   File:   createiotctemplate.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Loads the Config and Generates a Device Template for use with Azure
#           IoT Central
#
#   Online: www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import getopt, sys, time, string, threading, asyncio, os
import logging as Log

# our classes
from Classes.createiotctemplate import CreateIoTCTemplate
from Classes.config import Config
from Classes.varianttype import VariantType

# -------------------------------------------------------------------------------
#   Create the Template
# -------------------------------------------------------------------------------
async def create_template(infilename, outfilename):

  create_iotc_template = CreateIoTCTemplate(Log, infilename, outfilename)
  await create_iotc_template.create()

  return

async def main(argv):

    infilename = None
    outfilename = None

    # execution state from args
    short_options = "hvdi:o:"
    long_options = ["help", "verbose", "debug", "infilename=", "outfilename="]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    try:
      arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
      print (str(err))
    
    for current_argument, current_value in arguments:
      
      if current_argument in ("-h", "--help"):
        print("HELP for createiotctemplate.py")
        print("------------------------------------------------------------------------------------------------------------------")
        print("-h or --help - Print out this Help Information")
        print("-v or --verbose - Verbose Mode with lots of INFO will be Output to Assist with Tracing and Debugging")
        print("-d or --debug - Debug Mode with lots of DEBUG Data will be Output to Assist with Tracing and Debugging")
        print("-i or --infilename - Name of the Config File to Process for DCM Mapping")
        print("-o or --outfilename - Name of the DCM File that will be output into ./DeviceTemplates Folder")
        print("------------------------------------------------------------------------------------------------------------------")
        return
    
      if current_argument in ("-v", "--verbose"):
        Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.INFO)
        Log.info("Verbose Logging Mode...")
      else:
        Log.basicConfig(format="%(levelname)s: %(message)s")

      if current_argument in ("-d", "--debug"):
        Log.basicConfig(format="%(levelname)s: %(message)s", level=Log.DEBUG)
        Log.info("Debug Logging Mode...")
      else:
        Log.basicConfig(format="%(levelname)s: %(message)s")

      if current_argument in ("-i", "--infilename"):
        infilename = current_value
        Log.info("In File Name is Specified...")
        
      if current_argument in ("-o", "--outfilename"):
        outfilename = current_value
        Log.info("Out File Name is Specified...")

    # Create the Template
    await create_template(infilename, outfilename)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
