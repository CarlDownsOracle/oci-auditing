# Author    : Karthik Kumar
# Email     : Karthik.Hiraskar@Oracle.com
# Purpose   : Auditing Tool, for OCI tenancies
# - - - - - - - - - - - - - - - - - - - - - - - -
#
version='3.7.11' # In version file just use "version.subversion", # "x.x.minor_subversion" while development, just set in this file it should be enough
tool_name='OCI Auditing'
copyright="KK Hiraskar\n©2019-2021"

# Todo:
# * Optimization for few return status to stop further processing on each compartment looping


# importing standard/open-source modules
import sys,os
help='''
COMMANDLINE USAGE:

    Arg 1    [*Mandatory argument]
        Tenancy Names, each separated by a space, and enclosed by quotes
            ex: "tenancy1"
                "tenancy1 tenancy2 tenancy3"

    Arg 2    [*Mandatory argument]
        Use one or more of these below options seperated by space, and enclosed by quotes
            ex: "usersAndGroups limits"
                "networks"
                "limits policies networks"

        Types of analysis:
        ------------------
        compartments  = list & analyse Compartments, audits naming formats
        usersAndGroups= list & analyse Users and Groups, audits naming formats
        limits        = list & analyse Service Limits, warnings on near to limits
        policies      = list & analyse Policies, audits for mandatory policies, missing policies, additional policies
        instances     = lists instances created for all the OCI services supported
        events        = list & analyse Audit Events from last run, alerts for all create/modify/terminate events
        networks      = list & analyse VCN and all of it's sub-components, audits CIDR, Protocols
        cloudGuard    = lists all Cloud Guard findings, with graphs and colorings as per Severity
        cloudAdvisor  = lists all Cloud Advisor Recommendations, with estimated savings
        all           = all these audits
        
        Note: select only required audits, to save big run-times.
              optimization in configurations can also save longer run-times.

    Arg 3    [-Optional argument]
        sendMail      = send report generated directly to mailbox
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
    elif sys.argv[1] in ['--help','-?','-h']:
        print('OCI Auditing Tool, version '+version)
        print(help)
    else:
        print('== Error: Invalid arguments ==\n'+help)
    os._exit(0)
elif (argLen>1 and argLen<argLen_min) or argLen>argLen_max:
    print('== Error: Invalid number of arguments ==\n'+help)
    os._exit(0)
else:
    try:
        import the
        the.init(version,tool_name, copyright) # after this initialization only, import ui
        conf=the.conf
        
        if os.name=='nt' and argLen==1: # Windows UI mode
            import wx
            import ui
            #the.ui=ui, the.ui is assigned within ui module, so no need again here
            # this variable can be used in any other modules to determine if UI mode
            app = wx.App(False) #mandatory in wx, create an app, False stands for not redirection stdin/stdout
            self = ui.MainFrame(None)
            app.MainLoop() #start the applications
        elif argLen>1: # Command line mode
            commandlineTenancies = sys.argv[1].split()
            analysisType         = sys.argv[2].split()
            if argLen==4 and sys.argv[3]=='sendMail': the.sendMail=True
            the.consoleWidth=os.get_terminal_size().columns
            selectedTenancies=[]; selectedAudits=[]
            # select requested tenancies
            for tenancy in conf.tenancyNames:
                if tenancy in commandlineTenancies: selectedTenancies.append(tenancy)
            the.updateSelection('domains', 'selection', selectedTenancies)
            if len(selectedTenancies)>0: # if more than one valid tenancies selected
                for audt in ['usersAndGroups','limits','policies','instances','events','networks','cloudGuard','cloudAdvisor']:
                    if 'all' in analysisType or audt in analysisType:
                        the.updateSelection('audits', audt, True)
                        selectedAudits.append(audt)
                    else:
                        the.updateSelection('audits', audt, False)
                if 'instances' in selectedAudits: # selects all OCI services
                    the.updateSelection('audits', 'ociServices', list(the.ociServices))
                if 'events' in selectedAudits: # select from last run
                    the.updateSelection('audits', 'eventsDateRange', 3)
                if 'networks' in selectedAudits: # selects all networkComponents
                    the.updateSelection('audits', 'networkComponents', the.networkComponents)
                the.setInfo('''
    * * * Commandline Mode * * *
        
    Audit Components: {}
    Tenancies       : {}
    ----------------------
            '''.format(selectedAudits, selectedTenancies))
                import start
                start.init(the)
                ret=start.start()
            else:
                the.setError('INVALID TENANCIES: ' + str(commandlineTenancies) +
                '\nCheck if these tenancies are in, ' + conf.configFilePath)
                os._exit(0)
        else:
            print('== Error: Invalid number of arguments ==\n'+help)
            os._exit(0)
    except Exception as e:
        f=open('traceback.log', "w")
        f.write(str(e))
        f.write(traceback.format_exc())
        f.close()
