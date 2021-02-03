from time import sleep
import threading, re
from tinydb import TinyDB, Query
from datetime import datetime
# local
import conf

maxThreads=18 # cannot be less than 10
maxThreads=25
oci=None # oci module will be assigned with audits iniitialization
analysisType=[]

def init(a,b):
	global gaugeBreaks,ociServices,networkComponents,additionalNetworkComponents,sendMail
	global validServicesInManagedCompartmentForPaaS,log,tinyDB_file,db,qry,version,tool_name,ui
	version=a
	tool_name=b
	
	sendMail=False
	
	global mt, lock
	mt=[] # holds Thread Objects
	lock = threading.Lock()
	
	gaugeBreaks={
		'simple':1,
		'simple+':4,
		'serviceLimits':1+10, # 1: for preparation, 10: for scanning through all services
		'allCompartments':10
	}

	xfi='xtraFieldsInfo'
	ociServices = {
		'Compute': {xfi:['Shape', 'Region, Lifecycle State']},
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
		'Autonomous Container Database': {xfi:['-', 'Service Level Agreement Type']},
		'Autonomous Exadata Infrastructure': {xfi:['Shape', 'Domain']},
		'Exadata Infrastructure': {xfi:['Shape', '-']},
		'VM Cluster': {xfi:['Shape', 'GI Version']},
		'NoSQL Table': {xfi:['Max Storage', 'Max Read, Max Write Units']},
		'MySQL DB System': {xfi:['MySQL Version', 'Availability Domain']},
		'File System': {xfi:['Metered bytes', 'Availability Domain']},
		'Mount Target': {xfi:['-', 'Availability Domain']},
		'Analytics Instance': {xfi:['Feature Set', 'Description']},
		'Integration Instance': {xfi:['Integration Instance Type', 'Region']},
		'Health Check (HTTP)': {xfi:['Protocol, Interval', 'Region, Status']},
		'Health Check (Ping)': {xfi:['Protocol, Interval', 'Region, Status']},
		'Load Balancer': {xfi:['Shape Name', 'Region']},
	}
	# 'VCN Components',
	networkComponents=("Route Table,Subnet,Security List,Network Security Group,Internet Gateway,NAT Gateway,Service Gateway," +
				"VCN's DRG,Local Peering Gateway," +
				"Dynamic Routing Gateway," + 
				"FastConnect [implementation pending],Customer-Premises Equipment [pending],VPN Connections [pending]," +
				"Load Balancers [pending],IP Management [pending],DNS Management [pending]").split(',')
	additionalNetworkComponents=['route_rules','sl_egress_security_rules','sl_ingress_security_rules','nsg_security_rules','nsg_vnics']

	validServicesInManagedCompartmentForPaaS=['Boot Volume','Block Volume','Compute','Boot Volume Backup','Block Volume Backup',
		'DB System','File System','Mount Target','Health Check (HTTP)','Health Check (Ping)','Load Balancer']

	log = conf.log
	log.info('Tool Version: ' + version)
	log.info('Start Time  : ' + conf.start_time_local)
	conf.logConfigs()

	# Initiate Tiny DB
	tinyDB_file = conf.confDr+'/db.json' # conf folder existance is already confirmed in config file check
	db = TinyDB(tinyDB_file) # db object initialized
	qry = Query()

def resetGlobalVariables():
	global tenancies
	global issueTenancies
	global users
	global groups
	global compartments,compartmentIds
	global limits
	global policies
	global instances
	global events, eventDates
	global networks
	global cloudGuard
	global mt
	global startTime
	global gaugeIncNum
	global gaugeValue
	
	# Re-initialize values [clear values of last run]
	tenancies = {}
	issueTenancies = []
	users = {}
	groups = {}
	compartments={}; compartmentIds={}
	limits = {}
	policies = {}
	instances = {}
	events = {}; eventDates={}
	networks={}; networks['VCN']={}
	cloudGuard={}
	for x in ['Problems','Recommendations']: cloudGuard[x]={}
	for nc in networkComponents: networks[nc]={}
	for nc in additionalNetworkComponents: networks[nc]={}
	mt=[]
	startTime = datetime.now().strftime('%Y%m%d_%H%M%S')
	gaugeValue=0 # initial gauge value

def dateFormat(dateTime):
	if dateTime:
		return re.sub(r' (\d\d:\d\d:\d\d).*$',r' \1',str(dateTime)) # Date Time pattern update, Ex: 2019-08-01T06:33:51.715+0000 => 2019-08-01 06:33:51
	else:
		return ''
def commaJoin(*vals):
	ret=str(vals[0])
	for v in vals[1:len(vals)]:
		v=str(v)
		if v: ret+=', '+v
	return ret

def initTenancyDicts(tenancyName):
	users[tenancyName]={};groups[tenancyName]={};compartments[tenancyName]={};limits[tenancyName]={}
	policies[tenancyName]={};instances[tenancyName]={};events[tenancyName]={}

def createThread(func, *argv, max=maxThreads, **kwargv):
	waitSeconds=1
	msgInterval=40 # seconds
	maxIntervals=2
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
			if waitSeconds%msgInterval:
				ui.setInfo(threading.current_thread().name + ': All ' + str(threadCount) + ' threads busy.. waited ' + str(waitSeconds) + 'secs..')
				log.debug('Current Running Threads: ' + str(getActiveThreadNames()))
				if waitSeconds >= msgInterval*maxIntervals: bypassWait=True

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
	if showPopup:
		wx=ui.wx
		dlg=wx.MessageDialog(self, msg, 'Unstable Connection', wx.OK | wx.CANCEL | wx.OK_DEFAULT | wx.ICON_EXCLAMATION)
		dlg.SetOKCancelLabels("&Proceed Now", "&Abort")
		with lock: internetIssuePopup=True
		ans=dlg.ShowModal()
		if ans==wx.ID_CANCEL: os._exit()
		with lock: internetIssuePopup=False
	ui.setInfo('[' + str(retryCount+1) + '] Retrying connection..')

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
