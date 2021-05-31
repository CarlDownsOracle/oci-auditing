from time import sleep
import threading, re, sys
from tinydb import TinyDB, Query
from datetime import datetime
# local
import conf
conf.init(sys.modules[__name__])
import start

maxThreads=18 # cannot be less than 10
maxThreads=25
oci=None # oci module will be assigned with audits iniitialization

def init(a,b, c):
    global gaugeBreaks,ociServices,networkComponents,additionalNetworkComponents,sendMail,justConnectionCheck
    global validServicesInManagedCompartmentForPaaS,log,tinyDB_file,db,qry,version,tool_name,copyright,ui
    global consoleWidth
    version=a
    tool_name=b
    copyright=c
    ui=None # will be set to ui module, only in GUI runs
    sendMail=False
    justConnectionCheck=False
    global mt, lock
    mt=[] # holds Thread Objects
    lock = threading.Lock()
    
    gaugeBreaks={
        'simple':1,
        'simple+':4,
        'serviceLimits':1+10, # 1: for preparation, 10: for scanning through all services
        'allCompartments':10
    }

    xfi='xtraFieldsInfo' # Upto 4 extra fields
    ociServices = {
        'Compute': {xfi:['Shape, RAM(GB)', 'Region, Lifecycle State']},
        'Custom Image': {xfi:['Size(MB)', 'Mode', 'Lifecycle State']},
        'Boot Volume': {xfi:['Size', 'Availability Domain']},
        'Boot Volume Backup': {xfi:['Size, Backup Type:Manual/Scheduled, Type:Full/Incremental', 'Region, Expiration Time']},
        'Dedicated VM Host': {xfi:['Dedicated VM Host Shape', 'Availability Domain']},
        'Cluster Network': {xfi:['Instance Pool', 'Region']},
        'Instance Pool': {xfi:['Number of Instances in this Pool', 'Region']},
        'Block Volume': {xfi:['Size', 'Availability Domain']},
        'Block Volume Backup': {xfi:['Size, Backup Type:Manual/Scheduled, Type:Full/Incremental', 'Region, Expiration Time']},
        'Volume Group': {xfi:['Size', 'Availability Domain']},
        'Volume Group Backup': {xfi:['Size, Type:Full/Incremental', 'Region']},
        'DB System': {xfi:['DB Edition', 'Version']},
        'Autonomous Database': {xfi:['DB Version', 'Workload [ATP/ADW]']},
        'Autonomous Container Database': {xfi:['Service Level Agreement Type']},
        'Autonomous Exadata Infrastructure': {xfi:['Shape', 'Domain']},
        'Exadata Infrastructure': {xfi:['Shape']},
        'VM Cluster': {xfi:['Shape', 'GI Version']},
        'NoSQL Table': {xfi:['Max Storage', 'Max Read, Max Write Units']},
        'MySQL DB System': {xfi:['MySQL Version', 'Availability Domain']},
        'File System': {xfi:['Metered bytes', 'Availability Domain']},
        'Mount Target': {xfi:['Availability Domain']},
        'Analytics Instance': {xfi:['Feature Set', 'Description']},
        'Integration Instance': {xfi:['Integration Instance Type', 'Region']},
        'Health Check (HTTP)': {xfi:['Protocol, Interval', 'Region, Status']},
        'Health Check (Ping)': {xfi:['Protocol, Interval', 'Region, Status']},
        'Load Balancer': {xfi:['Shape Name', 'Region']},
        'Data Science': {xfi:['Status', 'Region', 'Created By', 'ID/url']},
    }
    if 'show_compute_vnics' in conf.keys: ociServices['Compute'][xfi].append('VNICs Details')
    # 'VCN Components',
    networkComponents=("Route Table,Subnet,Security List,Network Security Group,Internet Gateway,NAT Gateway,Service Gateway," +
                "VCN's DRG,Local Peering Gateway," +
                "Dynamic Routing Gateway," + 
                "FastConnect [implementation pending],Customer-Premises Equipment [pending],VPN Connections [pending]," +
                "Load Balancers [pending],IP Management [pending],DNS Management [pending]").split(',')
    additionalNetworkComponents=['route_rules','sl_egress_security_rules','sl_ingress_security_rules','nsg_security_rules','nsg_vnics']

    validServicesInManagedCompartmentForPaaS=['Boot Volume','Block Volume','Compute','VNIC Attachment','Boot Volume Backup','Block Volume Backup',
        'DB System','File System','Mount Target','Health Check (HTTP)','Health Check (Ping)','Load Balancer']

    log = conf.log
    log.info('Tool Version: ' + version)
    log.info('Start Time  : ' + conf.start_time_local)
    conf.loadConfigs()
    conf.logConfigs()

    # Initiate Tiny DB
    tinyDB_file = conf.confDr+'/db.json' # conf folder existance is already confirmed in config file check
    db = TinyDB(tinyDB_file) # db object initialized
    qry = Query()

def updateSelection(type, key ,value):
    ret = db.update({key : value}, qry.x==type)
    if len(ret)==0: db.insert({'x': type, key : value})
def getSelection(type, key):
    try:
        return db.search(qry.x==type)[0][key]
    except: # if not found returns boolean false
        return False
def getAuditSelections():
    ret=[]
    try:
        sel=db.search(qry.x=='audits')[0]
        for a in sel.keys():
            if sel[a]==True: ret.append(a)
    except:
        pass
    return sorted(ret)
def resetGlobalVariables():
    global tenancies
    global issueTenancies
    global users
    global groups, dynamicGroups, groupMembers, userGroupIds
    global compartments,compartmentIds
    global limits
    global policies
    global instances, vnicAttachments
    global events, eventDates
    global networks
    global cloudGuard, cloudAdvisor
    global mt
    global startTime
    global gaugeIncNum
    global gaugeValue
    
    # Re-initialize values [clear values of last run]
    tenancies = {}
    issueTenancies = []
    users = {}
    groups = {}; dynamicGroups={}; groupMembers={}; userGroupIds={}
    compartments={}; compartmentIds={}
    limits = {}
    policies = {}
    instances = {}; vnicAttachments={}
    events = {}; eventDates={}
    networks={}; networks['VCN']={}
    cloudGuard={}; cloudAdvisor={}
    for x in ['Problems','Recommendations']: cloudGuard[x]={}
    for nc in networkComponents: networks[nc]={}
    for nc in additionalNetworkComponents: networks[nc]={}
    mt=[]
    startTime = datetime.now().strftime('%Y%m%d_%H%M%S')
    gaugeValue=0 # initial gauge value

# Date Time pattern update
# Examples:
# 2019-08-01 06:33:51.715+0000 => 2019-08-01 06:33:51
# 2019-08-01T06:33:51.715Z => 2019-08-01 06:33:51
def dateFormat(dateTime):
    return re.sub(r'[T ](\d\d:\d\d:\d\d).*$',r' \1',str(dateTime)) if dateTime else '-'
def commaJoin(*vals):
    ret=str(vals[0])
    for v in vals[1:len(vals)]:
        v=str(v)
        if v: ret+=', '+v
    return ret

def initTenancyDicts(tenancyName):
    users[tenancyName]={};groups[tenancyName]={};dynamicGroups[tenancyName]={};groupMembers[tenancyName]={};compartments[tenancyName]={};limits[tenancyName]={}
    policies[tenancyName]={};instances[tenancyName]={};events[tenancyName]={}

def createThread(func, *argv, max=maxThreads, **kwargv):
    waitSeconds=1
    msgInterval=20 # seconds
    maxIntervals=100 # seconds
    bypassWait=False
    while True:
        threadCount = threading.active_count()
        if threadCount<=max or bypassWait:
            with lock:
                mt.append(threading.Thread(target=func, args=argv, kwargs=kwargv))
                t=mt[-1]; t.start()
                log.debug('Started New Thread. Total threads now: '+str(threadCount+1))
                return t
        else:
            sleep(1); waitSeconds+=1
            if not waitSeconds%msgInterval:
                setInfo(threading.current_thread().name + ': All ' + str(threadCount) + ' threads busy.. waited ' + str(waitSeconds) + 'secs..')
                log.debug('Current Running Threads: ' + str(getActiveThreadNames()))
                if waitSeconds >= maxIntervals: bypassWait=True

def getActiveThreadNames():
    thrds=[]
    for t in threading.enumerate(): thrds.append(t.name)
    return thrds
        
def createThread_5belowMaxThreads(func, *argv, **kwargv): # use for sub threads, allowing 5 more still available for other
    return createThread(func, *argv, max=maxThreads-5, **kwargv)

internetIssuePopup=False
def raiseInternetIssue(retryCount):
    global internetIssuePopup
    showPopup=True # if shown while waiting, then no need to show again
    msg='Issues while connecting to internet.\n\nplease check and proceed..\nAbort will close complete application !!'
    log.warning(msg)
    while True:
        if internetIssuePopup:
            sleep(2)
            # if already one popup is shown from another thread, then avoid showing multiple times and just wait until UI approved to proceed / try again 
            showPopup=False
        else:
            break
    if showPopup and ui:
        wx=ui.wx
        dlg=wx.MessageDialog(None, msg, 'Unstable Connection', wx.OK | wx.CANCEL | wx.OK_DEFAULT | wx.ICON_EXCLAMATION)
        dlg.SetOKCancelLabels("&Proceed Now", "&Abort")
        with lock: internetIssuePopup=True
        ans=dlg.ShowModal()
        if ans==wx.ID_CANCEL: os._exit()
        with lock: internetIssuePopup=False
    setInfo('[' + str(retryCount+1) + '] Retrying connection..')

def getOciData(ociFunc, *argv, **kwargv):
    for i in range(4): # retry on issues
        try:
            res=ociFunc(*argv, retry_strategy=retry_strategy, **kwargv)
            if res.status!=200:
                log.warning('Response status: '+str(res.status)+'!')
                sleep(2)
                log.info('[' + str(i+1) + '] Retrying ..')
                continue # retry after few second
            return res # completed without any issue
        except oci.exceptions.ServiceError as e:
            log.debug(str(e))
            return False # no access to service or something else
        except oci.exceptions.RequestException as e: # connection issue
            raiseInternetIssue(i)
    log.error('Failed with all retries.. # Many mechanisms handled, this error should never come # !!!')
    return False # failed with all retries

currency=''
def getCurrency():
    global currency
    if currency: return currency
    else:
        #getOciData()
        return 'INR :-)'

def setMsg(txt):
    if ui: ui.parentWindow.SetStatusText(str(txt))
    else: print(str(txt))
def setInfo(txt):
    log.info(txt)
    setMsg(txt)
previousInfoText=''
def setInfo_avoidRedundant(txt):
    global previousInfoText
    if previousInfoText!=txt:
        setInfo(txt)
        previousInfoText=txt
def setError(txt):
    log.error(txt)
    setMsg("Error: " + str(txt))
def setWarn(txt):
    log.warning(txt)
    setMsg("Warning: " + str(txt))
prvGaugeValue=0
def increamentGauge(incrementBy):
    global gaugeValue,prvGaugeValue
    with lock: gaugeValue+=incrementBy
    if ui:
        ui.parentWindow.gauge.SetValue(gaugeValue)
    elif gaugeValue-prvGaugeValue>1:
        print(('[ ' + str(int(gaugeValue)) + '% ]').rjust(consoleWidth))
        prvGaugeValue=gaugeValue
def setGauge(setVal):
    global gaugeValue
    with lock: gaugeValue=setVal
    if ui: ui.parentWindow.gauge.SetValue(gaugeValue)
