# Author    : Karthik Kumar
# Email     : Karthik.Hiraskar@Oracle.com
# Purpose   : Auditing Tool, for OCI tenancies
# - - - - - - - - - - - - - - - - - - - - - - - -
#
version='3.6.7' # In version file just use "version.subversion", # "x.x.minor_subversion" while development, just set in this file it should be enough
tool_name='OCI Auditing'

# Todo:
# * Optimization for few return status to stop further processing on each compartment looping


# importing standard/open-source modules
import sys,os
help='''
USE GUI MODE TO GET ALL OPTIONS ACCESSIBLE, command-line mode is with limited options required for schedulers/automations.

COMMANDLINE USAGE OF "OCI AUDITING TOOL"

	Arg 1    [*Mandatory argument]
        Tenancy Names, each separated by a space, and enclosed by quotes
            ex: "tenancy1"
                "tenancy1 tenancy2 tenancy3"

	Arg 2    [*Mandatory argument]
        Use one or more of these below options seperated by space, and enclosed by quotes
            ex: "users groups"
                "networks"
                "limits policies networks"

        Type of analysis:
        ------------------
        compartments = list & analyse Compartments, audits naming formats
        users        = list & analyse Users, audits naming formats
        groups       = list & analyse Groups, audits naming formats
        limits       = list & analyse Service Limits, warnings on near to limits
        policies     = list & analyse Policies, audits for mandatory policies, missing policies, additional policies
        instances    = lists instances created for all the OCI services supported
        events       = list & analyse Audit Events, alerts for all create/modify/terminate events
        networks     = list & analyse VCN and all of it's sub-components, audits CIDR, Protocols
        cloudGuard   = lists all Cloud Guard findings, with colorings as per Severity
        all          = all these audits
            Note: select only required audits, to save big run-times.
                  optimization in configurations can also save longer run-times.

	Arg 3    [-Optional argument]
        sendMail = sends report generated directly to your mail inbox
                   [as per SMTP/TLS configurations]

Note: 
   * all configurations to be done in file "configurations\\tool.ini"
   * all alerts are highlighted with suitable background colors.
'''
# first index 0, says program name itself
argLen=len(sys.argv)
argLen_min=3; argLen_max=4
if argLen==2:
	if sys.argv[1] in ['-v','-V','--version']:
		print('OCI Auditing Tool, version '+version)
	elif sys.argv[1] in ['--help','-?']:
		print('OCI Auditing Tool, version '+version)
		print(help)
	else:
		print('== Error: Invalid arguments ==\n'+help)
	os._exit(0)
elif (argLen>1 and argLen<argLen_min) or argLen>argLen_max:
	print('== Error: Invalid number of arguments ==\n'+help)
	os._exit(0)

import wx
import the
the.init(version,tool_name) # after this initialization only, import ui
import ui

# Process command line arguments
# Commandline usage supported with limited options, for normal options, use directly with GUI
if argLen>1: # Todo: need to complete
	ui.commandlineMode=True
	ui.commandlineTenancies = sys.argv[1].split()
	the.analysisType=sys.argv[2].split()
	if argLen==4:
		if sys.argv[3]=='sendMail': the.sendMail=True
app = wx.App(False) #mandatory in wx, create an app, False stands for not redirection stdin/stdout
self = ui.MainFrame(None)
app.MainLoop() #start the applications
