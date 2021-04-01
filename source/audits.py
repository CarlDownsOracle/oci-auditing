import re
from datetime import datetime
from time import sleep

def init(a):
	global ui,the,conf,log,oci
	global networkServiceSelection,dateFormat,gaugeBreaks
	the=a
	oci=the.oci
	ui=the.ui
	conf=the.conf
	dateFormat=the.dateFormat
	log=conf.log
	gaugeBreaks=the.gaugeBreaks
	networkServiceSelection=the.getSelection('audits', 'networkComponents')

	# These errors are handled, with this "RETRY STRATEGY"
	# Notepad++ search pattern to see if any new error came: 
		# Response status\: (?!(504|200|401|404|429))
		# Response status\: (?!(504|502|503|200|401|404|429))
		# Logview Plus format: 30 days trial%d
			# %d{%H:mm} %p Thread-%t: %m%n
		# glogg - open source
	### These errors can appear, and should be resolved with retries
	# 500-Internal Server Error, 504-Gateway Timeout, 429-Too many requests for the user
	# 503 - Not added here in list, however its getting retried, and found success on retries [seen only for integration instances, actually this is improper return code]
	# 502 - Not added here in list, however its getting retried, few are ending without retry success and time out.
		# if the real cause is just network or the maintenance kind of situation, then no need from tooling end
		# apart from this I am not finding anything sure as of now
	### These errors are handled, and should not be appeared
	# 404-NotFound [if service not available in that region, or if not validServicesInManagedCompartmentForPaaS]
	# 401-NotAuthenticated [if tenancy keys are disturbed, or if not validServicesInManagedCompartmentForPaaS]
	### These incorrect return status are ignored as of now without retry
	# 400 - this is actually for invalid syntax, but OCI returning falsely
	the.retry_strategy = oci.retry.RetryStrategyBuilder(
		# Make up to 10 service calls
		max_attempts_check=True, max_attempts=10,
		# Don't exceed a total of 60 seconds for all service calls
		total_elapsed_time_check=True, total_elapsed_time_seconds=60,
		# Wait 45 seconds between attempts
		retry_max_wait_between_calls_seconds=6,
		# Use 2 seconds as the base number for doing sleep time calculations
		retry_base_sleep_time_seconds=2,
		# Retry on certain service errors:
		#   - Any 429 (this is signified by the empty array in the retry config)
				# Todo: to avoid 429 errors, try reducing threading count
		service_error_check=True,
		service_error_retry_config={
			500: ['InternalServerError','InternalError', None], # in 500 return status, for these 2 return codes, retries will be performed
			504: [None], # empty array means, all 504 status will be retried
			429: []
		},
		# Use exponential backoff and retry with full jitter, but on throttles use exponential backoff and retry with equal jitter
		backoff_type=oci.retry.BACKOFF_FULL_JITTER_EQUAL_ON_THROTTLE_VALUE
	).get_retry_strategy()

def listUsers(idty, tenName, tenOcid):
	the.setInfo(tenName + ': Getting Users...')
	allowedNamedUsers = conf.allowedNamedUsers # Work on local variable
	
	page=None
	while True:
		response = the.getOciData(idty.list_users, tenOcid, page=page)
		usrs = response.data
		log.debug('Got Users: ' + str(len(usrs)))
		
		for usr in usrs:
			cmnt=''
			usrName=usr.name
			if conf.validate['USERS']:
				if '@' in usrName: # Named user
					if usrName in allowedNamedUsers:
						allowedNamedUsers.remove(usrName)
					else:
						cmnt='This Named-User not allowed'
				else:
					res = re.search(conf.allowed_username_pattern, usrName)
					if res==None:
						cmnt='Naming format not followed'
					else:
						usrNum = int(res.group(5))
						if usrNum > conf.allowed_username_max_number:
							cmnt = 'allowed username cannot exceed ' + conf['allowed_username_max_number']
			the.users[tenName][usr.name] = [usrName, usr.description, usr.email, usr.id, usr.time_created, cmnt]
		
		if not response.has_next_page: break
		page = response.next_page
	
	if conf.validate['USERS']:
		for nu in allowedNamedUsers: # List Missing Named Users
			the.users[tenName]['#Missing#' + nu] = [nu, '--NA--', '--NA--', '--NA--', '--NA--', 'Mandatory Named User Missing']
	the.increamentGauge(the.gaugeIncNum)

def listGroups(idty, tenName, tenOcid):
	the.setInfo(tenName + ': Getting Groups...')
	allowedNamedGroups = conf.allowedNamedGroups
	
	page=None
	while True:
		response = the.getOciData(idty.list_groups, tenOcid, page=page)
		grps = response.data
		log.debug('Got Groups: ' + str(len(grps)))
		
		for grp in grps:
			cmnt=''
			grpName=grp.name
			if conf.validate['GROUPS']:
				if grpName in allowedNamedGroups:
					allowedNamedGroups.remove(grpName)
				else:
					res = re.search(conf.allowed_groupname_pattern, grpName)
					if res==None:
						cmnt='Naming format not followed'
					else:
						grpNum = int(res.group(8))
						if grpNum>conf.allowed_groupname_max_number:
							cmnt='Group Number cannot exceed ' + conf.allowed_groupname_max_number
			the.groups[tenName][grp.name] = [grpName, grp.description, grp.id, grp.time_created, cmnt]
		
		if not response.has_next_page: break
		page = response.next_page
	
	if conf.validate['GROUPS']:
		for ng in allowedNamedGroups:
			the.groups[tenName]['#Missing#' + ng] = [ng, '--NA--', '--NA--', '--NA--', 'Mandatory Group Missing']
	the.increamentGauge(the.gaugeIncNum)

def listPolicies(idty, tenName):
	gaugeIncNumFor1Compartment = (the.gaugeIncNum*gaugeBreaks['allCompartments'])/len(the.compartments[tenName])
	## Compartments wise looping
	for compKey in the.compartments[tenName]:
		the.createThread_5belowMaxThreads(listPoliciesFor1Compartment, compKey, idty, tenName)
		the.increamentGauge(gaugeIncNumFor1Compartment)
def listPoliciesFor1Compartment(compKey, idty, tenName):
	compName= the.compartments[tenName][compKey][0]
	compId  = the.compartments[tenName][compKey][1]
	compCmts= the.compartments[tenName][compKey][5]
	the.setInfo(tenName + ': Getting Policies - ' + compName)
	
	compNum=''
	res = re.search(r'([0-1]?\d{2})$', compName)
	if res!=None:
		cn=res.group(1)
		if cn.isdigit(): compNum=cn
	
	policyType=''
	groupFormat=''
	policiesToMatch=[]
	policiesFound=[]
	key_c = compName
	
	if compName==tenName+' (root)':
		policiesToMatch=conf.rootPolicies
		policyType='root'
		key_c = '(root)'
	elif compName=='ManagedCompartmentForPaaS':
		policyType='managed-compartment'
	else:
		policiesToMatch = [cp.replace('<compartment-name>', compName).lower() for cp in conf.compartmentPolicies]
		policyType='compartment'
		
	page=None
	while True:
		response = the.getOciData(idty.list_policies, compId, page=page)
		polys = response.data
		
		## Policy wise looping
		for poly in polys:
			p_stmts = poly.statements # this will be a list of policy statements
			# print('KK-5')
			## Statements wise looping
			for j in range(len(p_stmts)):
				stmt=p_stmts[j]
				cmnts=''
				if conf.validate['POLICIES']:
					# start with copying compartment comments, this will be empty if compartment is okay
					cmnts=compCmts
					if not cmnts: # if empty, means valid compartment. Validate policy statements also
						# Determine either valid policy or extra policy
						stmt_mod = ' '.join(stmt.split()).lower() # Replace multiple spaces to one space and all lower case
						if policyType=='compartment':
							if not groupFormat:
								if stmt_mod.startswith('allow group'):
									if stmt_mod.startswith('allow group demo.group'+compNum):
										groupFormat='demo.group'+compNum # should be in all smalls
									elif stmt_mod.startswith('allow group grplab.user'+compNum):
										groupFormat='grplab.user'+compNum # should be in all smalls
									elif stmt_mod.startswith('allow group grp'):
										res = re.search(r"grp(([5|6]\d{6})|(9\d{7}))\-lab\.user" + compNum, stmt_mod)
										if res!=None:
											eventId = res.group(1)
											groupFormat='grp'+eventId+'-lab.user'+compNum # should be in all smalls
								if groupFormat:			
									policiesToMatch = [cp.replace('<group-name>', groupFormat) for cp in policiesToMatch]
								
							if stmt_mod in policiesToMatch:
								policiesFound.append(stmt_mod)
							else:
								cmnts='Extra Policy'
						elif policyType=='root':
							if stmt_mod in policiesToMatch:
								policiesFound.append(stmt_mod)
							else:
								cmnts='Extra Policy'
				
				key = (key_c + poly.name + '_p' + str(j)).lower()
				the.policies[tenName][key] = [compName, poly.name, stmt, cmnts]
				
		
		if conf.validate['POLICIES']: # Add missing policies
			if len(polys)==0:
				key = (key_c + '_no-policy').lower()
				cmnts='No Policy'
				if compCmts: cmnts=compCmts
				the.policies[tenName][key] = [compName, '--NA--', '-- No Policies added in this Compartment --', cmnts]
			elif not compCmts and (policyType=='root' or policyType=='compartment'): # add missing policies, only if compartment is valid one
				missingPolicies=policiesToMatch[:] # copy by value
				c=1
				for s in policiesToMatch: # remove all matched policies
					if s in policiesFound: missingPolicies.remove(s)
				for s in missingPolicies: # add remaining missing policies
					key = (key_c + '_m' + str(c)).lower()
					c+=1
					the.policies[tenName][key] = [compName, '--NA--', s, 'Missing Policy']
		if response.has_next_page: page = response.next_page
		else: break

def listLimits(config, tenName):
	tenancyOcid = config['tenancy']
	lmts = oci.limits.LimitsClient(config)
	
	the.setInfo(tenName + ': Getting Service Names and Definitions - for Limits ...')
	## Getting Service Names, with local code to handle paging [This method is preserved just as examples]
	serviceNames = {}
	page=None # This is manual way of handling pages, automated way is "oci.pagination.list_call_get_all_results"
	while True:
		response = the.getOciData(lmts.list_services, tenancyOcid, page=page)
		services = response.data
		log.debug('Got Services: ' + str(len(services)))
		for s in services: serviceNames[s.name] = s.description
		if not response.has_next_page: break
		page = response.next_page
	
	## Getting Service Definitions, with ready OCI pagination functions
	serviceDefs = {}
	response = the.getOciData(oci.pagination.list_call_get_all_results, lmts.list_limit_definitions, tenancyOcid)
	limitDefs = response.data
	log.debug('Got Limit Definitions: ' + str(len(limitDefs)))
	for defn in limitDefs: serviceDefs[defn.name] = {'service': defn.service_name,	'desc': defn.description}
	the.increamentGauge(the.gaugeIncNum)

	gaugeIncNumFor1Region = (the.gaugeIncNum*(gaugeBreaks['serviceLimits']-1))/len(getRegionsSubscribed(tenName))
	loopRegions(listLimitsForRegion, config, tenName, serviceDefs=serviceDefs, serviceNames=serviceNames, gaugeIncNumFor1Region=gaugeIncNumFor1Region)
def listLimitsForRegion(config, tenName, serviceDefs={}, serviceNames={}, gaugeIncNumFor1Region=0):
	lmts = oci.limits.LimitsClient(config) # with region changed config
	tenancyOcid=config['tenancy']
	region=config['region']
	##Todo: # All services cannot be listed separately based on region, coz "Service=Compartments" shows number for all regions, 
	## which is not true
	for serviceName in serviceNames.keys():
		serviceDesc = serviceNames[serviceName]
		if serviceDesc in conf.limitsSkipServices: continue
		the.createThread(listLimitsFor1RegionService, tenancyOcid, tenName, region, lmts, serviceDefs, serviceName, serviceDesc)
	the.increamentGauge(gaugeIncNumFor1Region)
def listLimitsFor1RegionService(tenancyOcid, tenName, region, lmts, serviceDefs, serviceName, serviceDesc):
	the.setInfo(tenName + ' > ' + region + ': Getting Service Limits - ' + serviceDesc + ' ...')
	
	res1 = the.getOciData(oci.pagination.list_call_get_all_results, lmts.list_limit_values, tenancyOcid, service_name=serviceName)
	limitValues = res1.data
	log.debug('Got Limits: ' + str(len(limitValues)))
	
	for l in limitValues:
		scopeType = l.scope_type
		scope = l.availability_domain
		if scopeType=='AD': pass # already initialized with AD variable
		elif scopeType=='REGION': scope = region
		elif scopeType=='GLOBAL': scope = 'Tenancy'
		key = serviceName + scope + l.name
		if conf.limitsShowUsed: # Adds Used and Available values also
			try:
				if(scopeType=='AD'):
					res2 = the.getOciData(lmts.get_resource_availability, serviceName, l.name, tenancyOcid, availability_domain=scope)
				else:
					res2 = the.getOciData(lmts.get_resource_availability, serviceName, l.name, tenancyOcid)
			except oci.exceptions.ServiceError as e:
				the.setError(str(e))
			resourceData = res2.data
			used = resourceData.used if resourceData.used else 0
			available = resourceData.available if resourceData.available else 0
			the.limits[tenName][key] = [serviceDesc, scope, l.name, serviceDefs[l.name]['desc'], l.value, used, available]
		else:
			the.limits[tenName][key] = [serviceDesc, scope, l.name, serviceDefs[l.name]['desc'], l.value]

def listCompartments(idty, tenName, tenancyOcid):
	cmps_dict = {}
	# namePattern  = re.compile(r"(^([5|6]\d{6}\-C)|(9\d{7}\-C)|(C))[0-1]?\d{2}$")
	namePattern  = re.compile(conf.allowed_compname_pattern)
	
	the.setInfo(tenName + ': Getting Compartments...')

	page=None
	while True:
		response = the.getOciData(idty.list_compartments, tenancyOcid, compartment_id_in_subtree=True, page=page)
		cmps = response.data
		log.debug('Got Compartments: ' + str(len(cmps)))
		# process all compartment details to dictionary
		for cmp in cmps:
			cmps_dict[cmp.id] = { # Compartment's own id
				'compartment_id' : cmp.compartment_id, # Parent Compartment's id
				'name'           : cmp.name,
				'description'    : cmp.description,
				'lifecycle_state': cmp.lifecycle_state.capitalize()
			}
		if response.has_next_page:
			page = response.next_page
		else:
			break
	
	# Add root compartment to list, and Root Compartment OCID is same as Tenancy OCID
	key='(root)'
	the.compartments[tenName][key] = [tenName+' (root)', tenancyOcid, 0, 'Active', 'The root Compartment of the tenancy', '']
	the.compartmentIds[tenancyOcid]=[tenName,key]

	# Add all other compartments under root
	for id in cmps_dict.keys(): # id is Compartment's OCID
		cmp=cmps_dict[id]
		
		# Derive Compartment-Name and Hirarchy-Level
		cmp_name=cmp['name']
		level=1
		cmp_cmps_id=cmp['compartment_id'] # This will be set to parent compartment id, and loops back until parent becomes root, forming a string of full navigation path
		while True:
			if cmp_cmps_id==tenancyOcid:
				break
			else:
				level+=1
				cmp_name = cmps_dict[cmp_cmps_id]['name'] + ' >> ' + cmp_name # get name before cmp_cmps_id variable is overriden to parent in next statement
				cmp_cmps_id = cmps_dict[cmp_cmps_id]['compartment_id']
			
		cmnts='' # add report comments
		if conf.validate['COMPARTMENTS']:
			if '>' in cmp_name:
				cmnts = 'Child compartment not allowed'
			elif not (namePattern.match(cmp_name) or cmp_name==tenName+' (root)' or cmp_name=='ManagedCompartmentForPaaS'):
				cmnts = 'Compartment naming-format not followed'
		key=cmp_name
		the.compartments[tenName][key] = [cmp_name, id, level, cmp['lifecycle_state'], cmp['description'], cmnts]
		the.compartmentIds[id]=[tenName,key]
	the.increamentGauge(the.gaugeIncNum)

# Todo: incomplete/untested functionality
def usageFn(config, tenName): # This functionality always returning None for OU internal tenancies, may work for other.
	global usages
	usages = {}
	usages[tenName] = {}
	tenancyOcid = config['tenancy']
	usgCl = oci.usage_api.UsageapiClient(config)
	reqObj = oci.usage_api.models.RequestSummarizedUsagesDetails(tenant_id=tenancyOcid, granularity='DAILY', query_type='USAGE', 
		time_usage_started=datetime(2020,7,1, 0,0), time_usage_ended=datetime(2020,7,16,0,0))
	usgAggr = the.getOciData(usgCl.request_summarized_usages, reqObj)
	for usg in usgAggr.data.items:
		log.debug(usg)
		ad = str(usg.ad)
		comp = str(usg.compartment_name)
		# compPath = usg.compartment_path
		qty = str(usg.computed_quantity)
		amt = str(usg.computed_amount) + ' ' + usg.currency
		rgn = str(usg.region)
		name = str(usg.resource_name)
		srv = str(usg.service)
		shape = str(usg.shape)
		key = rgn+ad+comp+srv+name
		usages[tenName][key] = [comp, rgn+' / '+ad, srv, name, amt, qty+' / '+shape]
def cloudGuard(config, tenName):
	incGaugeCG=the.gaugeIncNum*gaugeBreaks['simple']/2
	rootCompId=config['tenancy'] # or with getRootCompartmentID(tenName)
	cgCl = oci.cloud_guard.CloudGuardClient(config)
	the.createThread(callCgService, tenName, rootCompId, 'Problems', cgCl.list_problems, cgProblems, incGaugeCG)
	the.createThread(callCgService, tenName, rootCompId, 'Recommendations', cgCl.list_recommendations, cgRecommendations, incGaugeCG)
def callCgService(tenName, rootCompId, service, ociFunc, locFunc, incGaugeCG):
	the.setInfo(tenName + ': ' + service + ' ...')
	the.cloudGuard[service][tenName]={}
	res=the.getOciData(oci.pagination.list_call_get_all_results, ociFunc, rootCompId, compartment_id_in_subtree=True, access_level='ACCESSIBLE')
	if res:
		# log.debug(res.data)
		for obj in res.data: locFunc(obj, tenName, service)
	the.increamentGauge(incGaugeCG)
def cgProblems(pr, tenName, srv):
	comp = getCompartmentName(pr.compartment_id)
	labels = '; '.join(pr.labels)
	state = pr.lifecycle_detail.title() + ', ' + pr.lifecycle_state.title()
	regions = ', '.join(pr.regions)
	name = pr.resource_name
	type = pr.resource_type
	risk = pr.risk_level.title()
	firstFound = dateFormat(pr.time_first_detected)
	lastFound = dateFormat(pr.time_last_detected)
	initKeyIfNew(the.cloudGuard[srv][tenName],comp,[])
	the.cloudGuard[srv][tenName][comp].append([labels,state,regions,name,type,risk,firstFound,lastFound])
def cgRecommendations(rc, tenName, srv):
	comp = getCompartmentName(rc.compartment_id)
	state = rc.lifecycle_detail.title() + ', ' + rc.lifecycle_state.title()
	type = rc.type
	risk = rc.risk_level.title()
	name = rc.name
	details = rc.details['detectorRuleId']
	created = dateFormat(rc.time_created)
	updated = dateFormat(rc.time_updated)
	initKeyIfNew(the.cloudGuard[srv][tenName],comp,[])
	the.cloudGuard[srv][tenName][comp].append([state,type,risk,rc.problem_count,name,details,created,updated])

def auditEventsOfRegion(config, tenName, start='', end=''):
	region=config['region']
	auditCl = oci.audit.AuditClient(config)
	loopCompartments(auditCl.list_events, eventsOfComp, tenName, region, 'Event', f1X=f11_parms, start_time=start, end_time=end)
def eventsOfComp(evt, compName, tenName, region):
	time = dateFormat(evt.event_time)
	src  = evt.source
	data = evt.data
	name = giveAdashOnNothing(data.event_name)
	usr  = giveAdashOnNothing(data.identity.principal_name if data.identity.principal_name else data.identity.principal_id)
	resName = giveAdashOnNothing(data.resource_name)
	# response = data.response.status
	key = compName+region+usr+src+name+resName+time
	# Auditing
	risk=''
	if re.search(r'Detach|Delete|Terminate|Create', name, re.IGNORECASE): risk='High'
	elif re.search(r'Modify|Update', name, re.IGNORECASE): risk='Medium'
	the.events[tenName][key]=[risk, compName, region, usr, src, name, resName, time]

def networksOfRegion(config, tenName):
	region=config['region']
	vnCl = oci.core.VirtualNetworkClient(config)
	vcnThreads = loopCompartments(vnCl.list_vcns, vcns, tenName, region, 'VCN')
	
	service = 'Dynamic Routing Gateway'
	if service in networkServiceSelection:
		loopCompartments(vnCl.list_drgs, dynamicRoutingGateways, tenName, region, service)
	
	for t in vcnThreads: t.join() # wait for VCN listings to complete
	if (tenName in the.networks['VCN']) and (region in the.networks['VCN'][tenName]):
		call_vcnComponents('Route Table', vnCl.list_route_tables, routeTables, tenName, region)
		call_vcnComponents('Subnet', vnCl.list_subnets, subnets, tenName, region)
		call_vcnComponents('Security List', vnCl.list_security_lists, securityLists, tenName, region)
		call_vcnComponents('Network Security Group', vnCl.list_network_security_groups, networkSecurityGroups, tenName, region, f1X=f11, vnCl=vnCl)
		call_vcnComponents('Internet Gateway', vnCl.list_internet_gateways, internetGateways, tenName, region)
		call_vcnComponents('NAT Gateway', vnCl.list_nat_gateways, natGateways, tenName, region)
		call_vcnComponents('Service Gateway', vnCl.list_service_gateways, serviceGateways, tenName, region)
		call_vcnComponents("VCN's DRG", vnCl.list_drg_attachments, drgAttachments, tenName, region)
		call_vcnComponents('Local Peering Gateway', vnCl.list_local_peering_gateways, localPeeringGateways, tenName, region)
	else:
		log.debug('IGNORE VCN SUB-COMPONENTS: No VCN in : ' + tenName + ' > ' + region)
		regionsSubscribed=len(getRegionsSubscribed(tenName))
		incGaugePerRegion=(the.gaugeIncNum*gaugeBreaks['allCompartments'])/regionsSubscribed
		the.increamentGauge(incGaugePerRegion)
def initiateDictsForNetworkComponents(srv,ten,rgn,comp):
	if not ten in the.networks[srv]: the.networks[srv][ten]={}
	if not rgn in the.networks[srv][ten]: the.networks[srv][ten][rgn]={}
	if not comp in the.networks[srv][ten][rgn]: the.networks[srv][ten][rgn][comp]={}
def vcns(vcn, compName, tenName, service, region):
	name=getDisplayName(vcn)
	initiateDictsForNetworkComponents(service,tenName,region,compName)
	the.networks[service][tenName][region][compName][name]=[vcn.id, vcn.cidr_block, dateFormat(vcn.time_created)]
def getPortRange(pr): 
	if pr:
		if pr.min==pr.max: return str(pr.min)
		else: return str(pr.min)+' - '+str(pr.max)
	return '-'
def getProtocolOptions(ie):
	prtcl = ie.protocol
	if prtcl.isnumeric():
		if   prtcl=='1' : prtcl='ICMP'
		elif prtcl=='6' : prtcl='TCP'
		elif prtcl=='17': prtcl='UDP'
		elif prtcl=='58': prtcl='ICMPv6'

		if 'ICMP' in prtcl and ie.icmp_options: return [prtcl, ie.icmp_options.type,ie.icmp_options.code]
		elif 'TCP' in prtcl and ie.tcp_options: return [prtcl, getPortRange(ie.tcp_options.source_port_range),getPortRange(ie.tcp_options.destination_port_range)]
		elif 'UDP' in prtcl and ie.udp_options: return [prtcl, getPortRange(ie.udp_options.source_port_range),getPortRange(ie.udp_options.destination_port_range)]
	return [prtcl,'-','-']
def getVcnId(srv,obj):
	vcnID=obj.vcn_id
	if not vcnID in the.networks[srv]: the.networks[srv][vcnID]=[]
	return vcnID
def subnets(sn, compName, tenName, srv, region):
	name=getDisplayName(sn)
	vcnID=getVcnId(srv,sn)
	ad = sn.availability_domain if sn.availability_domain else 'Regional'
	pr_pb = 'Private' if sn.prohibit_public_ip_on_vnic else 'Public'
	access = pr_pb+' ('+ad+')'
	secLists = '\n'.join(sn.security_list_ids)
	the.networks[srv][vcnID].append([name, sn.id, sn.cidr_block, access, secLists, dateFormat(sn.time_created)])

def routeTables(rt, compName, tenName, srv, region):
	name=getDisplayName(rt)
	vcnID=getVcnId(srv,rt)
	the.networks[srv][vcnID].append([name, rt.id, dateFormat(rt.time_created)])
	
	srv='route_rules'
	the.networks[srv][rt.id]=[]
	for rul in rt.route_rules:
		desc = rul.description if rul.description else ' '
		the.networks[srv][rt.id].append([rul.destination, rul.destination_type, rul.network_entity_id, desc])
	
def securityLists(sl, compName, tenName, srv, region):
	name=getDisplayName(sl)
	vcnID=getVcnId(srv,sl)
	the.networks[srv][vcnID].append([name, sl.id, dateFormat(sl.time_created)])
		
	srv='sl_egress_security_rules'
	the.networks[srv][sl.id]=[]
	for egr in sl.egress_security_rules:
		stateless = 'Yes' if egr.is_stateless else 'No'
		[protocol,fld1,fld2] = getProtocolOptions(egr)
		dst=egr.destination
		# Auditing
		risk=''
		if dst=='0.0.0.0/0': risk = 'High' if protocol=='all' else 'Medium'
		the.networks[srv][sl.id].append([risk, stateless, egr.destination_type, dst, protocol, fld1, fld2, egr.description])
	
	srv='sl_ingress_security_rules'
	the.networks[srv][sl.id]=[]
	for ing in sl.ingress_security_rules:
		stateless = 'Yes' if ing.is_stateless else 'No'
		[protocol,fld1,fld2] = getProtocolOptions(ing)
		src=ing.source
		# Auditing
		risk=''
		if src=='0.0.0.0/0': risk='High'
		elif src=='10.0.0.0/16' and protocol=='all': risk='Medium'
		elif (src=='10.0.0.0/16' and protocol=='ICMP') or (src=='10.0.0.0/24' and protocol=='TCP'): risk='Low'
		the.networks[srv][sl.id].append([risk, stateless, ing.source_type, src, protocol, fld1, fld2, ing.description])
def internetGateways(ig, compName, tenName, srv, region):
	name=getDisplayName(ig)
	vcnID=getVcnId(srv,ig)
	state=ig.lifecycle_state.title()
	enabled = 'Enabled' if ig.is_enabled else 'Disabled'
	the.networks[srv][vcnID].append([name, ig.id, state, enabled, dateFormat(ig.time_created)])
def natGateways(nat, compName, tenName, srv, region):
	name=getDisplayName(nat)
	vcnID=getVcnId(srv,nat)
	state=nat.lifecycle_state.title()
	block_traffic = 'Yes' if nat.block_traffic else 'No'
	the.networks[srv][vcnID].append([name, nat.id, state, block_traffic, nat.nat_ip, dateFormat(nat.time_created)])
def serviceGateways(sg, compName, tenName, srv, region):
	name=getDisplayName(sg)
	vcnID=getVcnId(srv,sg)
	state=sg.lifecycle_state.title()
	block_traffic = 'Yes' if sg.block_traffic else 'No'
	servNames=[]
	for serv in sg.services: servNames.append(serv.service_name)
	servNames = ", ".join(servNames)
	the.networks[srv][vcnID].append([name,sg.id,state,servNames,sg.route_table_id, block_traffic,dateFormat(sg.time_created)])
def drgAttachments(att, compName, tenName, srv, region):
	name=getDisplayName(att)
	vcnID=getVcnId(srv,att)
	state=att.lifecycle_state.title()
	the.networks[srv][vcnID].append([att.drg_id,name,att.route_table_id,state,dateFormat(att.time_created)])
def localPeeringGateways(obj, compName, tenName, srv, region):
	name=getDisplayName(obj)
	vcnID=getVcnId(srv,obj)
	state=obj.lifecycle_state.title()
	peeringStatus=obj.peering_status.title()
	crossTenancy = 'Yes' if obj.is_cross_tenancy_peering else 'No'
	the.networks[srv][vcnID].append([name,state,peeringStatus,obj.route_table_id,obj.peer_advertised_cidr,crossTenancy,dateFormat(obj.time_created)])
def dynamicRoutingGateways(drg, compName, tenName, srv, region):
	name=getDisplayName(drg)
	state=drg.lifecycle_state.title()
	initiateDictsForNetworkComponents(srv,tenName,region,compName)
	the.networks[srv][tenName][region][compName][name]=[drg.id,state,dateFormat(drg.time_created)]
	
def scanNSG(service, ociFunc, locFunc, nsgId):
	try:
		res=the.getOciData(oci.pagination.list_call_get_all_results, ociFunc, nsgId)
		if res:
			log.debug('Count: '+str(len(res.data)))
			for obj in res.data:
				locFunc(obj, service, nsgId)
	except Exception:
		log.exception('Something Error happened !!') # send to log
		raise # send also to console
def securityRules(sr, srv, nsgId):
	stateless = 'Yes' if sr.is_stateless else 'No'
	dir=sr.direction
	src_dst=''; type='' # source/destination
	if dir=="EGRESS":
		src_dst=sr.destination
		type=sr.destination_type
	elif dir=="INGRESS":
		src_dst=sr.source
		type=sr.source_type
	else:
		return
	[protocol,fld1,fld2] = getProtocolOptions(sr)
	desc=sr.description
	created=dateFormat(sr.time_created)
	# Auditing
	risk=''
	if src_dst=='0.0.0.0/0': risk='High'
	elif src_dst=='10.0.0.0/16' and protocol=='all': risk='Medium'
	elif (src_dst=='10.0.0.0/16' and protocol=='ICMP') or (src_dst=='10.0.0.0/24' and protocol=='TCP'): risk='Low'
	if not nsgId in the.networks[srv]: the.networks[srv][nsgId]=[]
	the.networks[srv][nsgId].append([risk, stateless, dir, type, src_dst, protocol, fld1, fld2, desc,created])
def vnics(v, srv, nsgId):
	if not nsgId in the.networks[srv]: the.networks[srv][nsgId]=[]
	the.networks[srv][nsgId].append([v.resource_id, v.vnic_id, dateFormat(v.time_associated)])
def networkSecurityGroups(nsg, compName, tenName, srv, region, vnCl):
	name=getDisplayName(nsg)
	the.setInfo('Scanning NSG:' + name + ' ...')
	if not nsg.vcn_id in the.networks[srv]: the.networks[srv][nsg.vcn_id]=[]
	the.networks[srv][nsg.vcn_id].append([name, nsg.id, dateFormat(nsg.time_created)])
	
	scanNSG('nsg_security_rules', vnCl.list_network_security_group_security_rules, securityRules, nsg.id)
	scanNSG('nsg_vnics', vnCl.list_network_security_group_vnics, vnics, nsg.id)

def scanCompartment(ociFunc, locFunc, compId, compName, tenName, region, service, **kwargs):
	try:
		the.setInfo(tenName + ' > ' + region + ' > ' + compName + ' > ' + service + 's ...')
		res=the.getOciData(oci.pagination.list_call_get_all_results, ociFunc, compId)
		if res:
			log.debug('Count: '+str(len(res.data)))
			for srv in res.data:
				locFunc(srv, compName, tenName, service, region, **kwargs)
	except Exception:
		log.exception('Something Error happened !!') # send to log
		raise # send also to console
f11=scanCompartment
def f11_networkComponents(ociFunc, locFunc, compId, compName, tenName, region, service, **kwargs):
	try:
		if compName in the.networks['VCN'][tenName][region]:
			the.setInfo(tenName + ' > ' + region + ' > ' + compName + ' > ' + service + 's ...')
			res=the.getOciData(oci.pagination.list_call_get_all_results, ociFunc, compId)
			if res:
				log.debug('Count: '+str(len(res.data)))
				for srv in res.data:
					locFunc(srv, compName, tenName, service, region, **kwargs)
		# else: log.debug('IGNORE: No VCN in '+region+', '+compName+': ' + tenName + ' > ' + region + ' > ' + compName + ' > ' + service + 's')
	except Exception:
		log.exception('Something Error happened !!') # send to log
		raise
def call_vcnComponents(service, ociFunc, locFunc, tenName, region, f1X=f11_networkComponents, **kwargs):
	if service in networkServiceSelection:
		log.info('Scanning "'+service+'" in: '+tenName+' > '+region+' ...')
		loopCompartments(ociFunc, locFunc, tenName, region, service, f1X=f1X, **kwargs)
def f11_parms(ociFunc, locFunc, compId, compName, tenName, region, service, **kwargs):
	try:
		the.setInfo(tenName + ' > ' + region + ' > ' + compName + ' > ' + service + 's ...')
		page=None
		while True:
			res=the.getOciData(ociFunc, compId, **kwargs, page=page)
			if res:
				log.debug('Count: '+str(len(res.data)))
				for srv in res.data: locFunc(srv, compName, tenName, region)
			# This function is interupt enabled
			if the.getSelection('audits', 'interuptRaised'): break
			if res and res.has_next_page: page=res.next_page
			else: break
	except Exception:
		log.exception('Something Error happened !!') # send to log
		raise # send also to console
def f12(ociFunc, locFunc, compId, compName, tenName, region, service): # Loops through every AD with Paging, Parmeter: 1.Compartment, 2.AvailabilityDomain
	try:
		for ad in the.tenancies[tenName][2][region]: # Loop through ADs
			the.setInfo(tenName + ' > ' + region + ' > ' + compName + ' > ' + ad + ' > ' + service + 's ...')
			page=None
			while True:
				res=the.getOciData(ociFunc, compartment_id=compId, availability_domain=ad, page=page)
				if res:
					log.debug('Service Count: '+str(len(res.data)))
					for srv in res.data: locFunc(srv, compName, tenName, service, ad)
				if res and res.has_next_page: page=res.next_page
				else: break
	except Exception:
		log.exception('Something Error happened !!') # send to log
		raise # send also to console
def f13(ociFunc, locFunc, compId, compName, tenName, region, service, **kwargs): # non-iterable listing
	try:
		the.setInfo(tenName + ' > ' + region + ' > ' + compName + ' > ' + service + 's ...')
		res=the.getOciData(oci.pagination.list_call_get_all_results, ociFunc, compId, **kwargs)
		if res:
			locFunc(res.data, compName, tenName, service, region)
	except Exception:
		log.exception('Something Error happened !!') # send to log
		raise # send also to console
def loopCompartments(ociFunc, locFunc, tenName, region, service='', f1X=f11, **kwargv):
	regionsSubscribed=len(getRegionsSubscribed(tenName))
	incGaugePerRegion=(the.gaugeIncNum*gaugeBreaks['allCompartments'])/regionsSubscribed
	if service and (service in conf.serviceNotinRegions) and (region in conf.serviceNotinRegions[service]):
		the.increamentGauge(incGaugePerRegion)
		return # if configured as, service not available in region
	
	# Creates Thread for Each Compartment
	incGaugePerComp=incGaugePerRegion/len(the.compartments[tenName])
	threads=[]
	for key in the.compartments[tenName]:
		compName  =the.compartments[tenName][key][0]
		compId    =the.compartments[tenName][key][1]
		compStatus=the.compartments[tenName][key][3] # Active / Deleted
		
		if compName in conf.disableCompartments: # Donot process Disabled compartments [as per tool configurations]
			pass #log.debug('IGNORE: Compartment Disabled in Tool: ' + tenName + ' > ' + region + ' > ' + compName + ' > ' + service + 's')
		elif compStatus=='Deleted': # This compartment is returning 404 for few services, and as per OCI compartment can be deleted only if empty
			pass #log.debug('IGNORE: Deleted Compartment: ' + tenName + ' > ' + region + ' > ' + compName + ' > ' + service + 's')
		elif service and (compName=='ManagedCompartmentForPaaS') and (service not in the.validServicesInManagedCompartmentForPaaS): # This compartment is returning 404 & 401 errors for unsupported services
			pass #log.debug('IGNORE: Unsupported Service in Managed Compartment: ' + tenName + ' > ' + region + ' > ' + compName + ' > ' + service + 's')
		else:
			t=the.createThread_5belowMaxThreads(f1X, ociFunc, locFunc, compId, compName, tenName, region, service, **kwargv)
			threads.append(t)
		the.increamentGauge(incGaugePerComp)
	return threads
f1=loopCompartments
def loopRegions(fn, config, tenName, **kwargs): # Loops through all subscribed regions
	if ui: ui.parentWindow.m_staticField1.Show()
	for regn in getRegionsSubscribed(tenName):
		config['region']=regn
		if ui: ui.parentWindow.m_staticField1.SetLabel('')
		sleep(1) # go and comes new value effect, and no problem of 1 second sleep, many threads will be running in this interval
		if ui: ui.parentWindow.m_staticField1.SetLabel('Processing - "'+regn+'"')
		fn(config, tenName, **kwargs)
	if ui: ui.parentWindow.m_staticField1.Hide()

def listInstancesOfRegion(config, tenName):
	region=config['region']
	selectedServices = the.getSelection('audits', 'ociServices') # array of selected services
	def fn1(srvcs): return any(x in selectedServices for x in srvcs)
	
	# ClientObjects wise grouping, that support Services
	dbSrvcs     = ['DB System','Autonomous Database','Autonomous Container Database','Autonomous Exadata Infrastructure','Exadata Infrastructure','VM Cluster']
	blkStrgSrvcs= ['Boot Volume','Boot Volume Backup','Block Volume','Block Volume Backup','Volume Group','Volume Group Backup']
	filStrgSrvcs= ['File System','Mount Target']
	compSrvcs   = ['Compute','Dedicated VM Host']
	compMngSrvcs= ['Cluster Network','Instance Pool']
	hltChkSrvcs = ['Health Check (HTTP)','Health Check (Ping)']
	
	# Creates only necessary client objects
	if fn1(blkStrgSrvcs): blkStrgCl = oci.core.BlockstorageClient(config)
	if fn1(filStrgSrvcs): filStrgCl = oci.file_storage.FileStorageClient(config)
	if fn1(compSrvcs): compCl = oci.core.ComputeClient(config)
	if fn1(compMngSrvcs): compMngCl = oci.core.ComputeManagementClient(config)
	if fn1(dbSrvcs): dbCl = oci.database.DatabaseClient(config)
	if fn1(hltChkSrvcs): hltCl = oci.healthchecks.HealthChecksClient(config)
	if 'Load Balancer' in selectedServices: ldBalCl = oci.load_balancer.LoadBalancerClient(config)
	if 'NoSQL Table' in selectedServices: noSqlCl = oci.nosql.NosqlClient(config)
	if 'MySQL DB System' in selectedServices: mySqlDbCl = oci.mysql.DbSystemClient(config)
	if 'Analytics Instance' in selectedServices: anlyCl = oci.analytics.AnalyticsClient(config)
	if 'Integration Instance' in selectedServices: intgCl = oci.integration.IntegrationInstanceClient(config)
	if 'Data Science' in selectedServices: dsCl = oci.data_science.DataScienceClient(config)
	
	for service in selectedServices:
		if   service=='Boot Volume': f1(blkStrgCl.list_boot_volumes, bootVolume, tenName, region, service, f1X=f12)
		elif service=='Boot Volume Backup': f1(blkStrgCl.list_boot_volume_backups, volumesBackup, tenName, region, service)
		elif service=='Block Volume': f1(blkStrgCl.list_volumes, volumes, tenName, region, service)
		elif service=='Block Volume Backup': f1(blkStrgCl.list_volume_backups, volumesBackup, tenName, region, service)
		elif service=='Volume Group': f1(blkStrgCl.list_volume_groups, volumes, tenName, region, service)
		elif service=='Volume Group Backup': f1(blkStrgCl.list_volume_group_backups, volumeGroupBackups, tenName, region, service)
		elif service=='Compute':
			vnCl=None
			if 'show_compute_ips' in conf.keys:
				vnCl = oci.core.VirtualNetworkClient(config)
				f1(compCl.list_vnic_attachments, vnicAttachment, tenName, region, 'VNIC Attachments')
			f1(compCl.list_instances, compute, tenName, region, service, vnCl=vnCl)
		elif service=='File System': f1(filStrgCl.list_file_systems, fileSystem, tenName, region, service, f1X=f12)
		elif service=='Mount Target': f1(filStrgCl.list_mount_targets, mountTarget, tenName, region, service, f1X=f12)
		elif service=='Cluster Network': f1(compMngCl.list_cluster_networks, clusterNetwork, tenName, region, service)
		elif service=='Instance Pool': f1(compMngCl.list_instance_pools, instancePool, tenName, region, service)
		elif service=='Dedicated VM Host': f1(compCl.list_dedicated_vm_hosts, dedicatedVmHost, tenName, region, service)
		elif service=='DB System': f1(dbCl.list_db_systems, dbSystem, tenName, region, service)
		elif service=='Autonomous Database': f1(dbCl.list_autonomous_databases, autoDB, tenName, region, service)
		elif service=='Autonomous Container Database': f1(dbCl.list_autonomous_container_databases, autoContainerDB, tenName, region, service)
		elif service=='Autonomous Exadata Infrastructure': f1(dbCl.list_autonomous_exadata_infrastructures, autoExaDB, tenName, region, service)
		elif service=='Exadata Infrastructure': f1(dbCl.list_exadata_infrastructures, exaDB, tenName, region, service)
		elif service=='VM Cluster': f1(dbCl.list_vm_clusters, vmCluster, tenName, region, service)
		elif service=='NoSQL Table': f1(noSqlCl.list_tables, noSqlTables, tenName, region, service, f1X=f13)
		elif service=='MySQL DB System': f1(mySqlDbCl.list_db_systems, mySqlDbSystem, tenName, region, service)
		elif service=='Load Balancer': f1(ldBalCl.list_load_balancers, loadBalancer, tenName, region, service)
		elif service=='Analytics Instance': f1(anlyCl.list_analytics_instances, analytics, tenName, region, service)
		elif service=='Integration Instance': f1(intgCl.list_integration_instances, integration, tenName, region, service)
		elif service=='Health Check (HTTP)': f1(hltCl.list_http_monitors, healthCheck, tenName, region, service)
		elif service=='Health Check (Ping)': f1(hltCl.list_ping_monitors, healthCheck, tenName, region, service)
		elif service=='Data Science':
			f1(dsCl.list_projects, dataScience, tenName, region, service+' - Project')
			f1(dsCl.list_notebook_sessions, dataScience_notebookSessions, tenName, region, service+' Notebook Session')
			f1(dsCl.list_models, dataScience_models, tenName, region, service+' Model')
def getDisplayName(obj):
	if obj.display_name: # it's observed some resources with no display_name
		return obj.display_name
	else:
		return '#NoDisplayName# '+obj.id
def toServices(key, ten, comp, service, name, created, *extraFields):
	the.instances[ten][key] = [comp, service, name, created, *extraFields]
	log.debug(the.instances[ten][key])
def dataScience(ds, compName, tenName, serviceName, region):
	key=compName+serviceName+region+ds.display_name+ds.id # its seen with same name service can again be created once deleted, so adding id also to key
	toServices(key, tenName, compName, serviceName, ds.display_name, dateFormat(ds.time_created), ds.lifecycle_state, region, ds.created_by, ds.id)
def dataScience_notebookSessions(ds, compName, tenName, serviceName, region):
	key=compName+serviceName+region+ds.project_id+ds.display_name
	toServices(key, tenName, compName, serviceName, ds.display_name+' ['+ds.project_id+']', dateFormat(ds.time_created), ds.lifecycle_state, region, ds.created_by, ds.notebook_session_url)
def dataScience_models(ds, compName, tenName, serviceName, region):
	key=compName+serviceName+region+ds.project_id+ds.display_name
	toServices(key, tenName, compName, serviceName, ds.display_name+' ['+ds.project_id+']', dateFormat(ds.time_created), ds.lifecycle_state, region, ds.created_by)
def bootVolume(vol, compName, tenName, serviceName, ad):
	key=compName+ad+serviceName+vol.display_name
	toServices(key, tenName, compName, serviceName, vol.display_name, dateFormat(vol.time_created), str(vol.size_in_gbs)+' GB', ad)
def volumesBackup(vol, compName, tenName, serviceName, region): # Same used for: Boot & Block Volume Backups
	key=compName+region+serviceName+vol.display_name
	fld1=the.commaJoin(str(vol.size_in_gbs)+' GB', vol.source_type, vol.type)
	fld2=the.commaJoin(region, dateFormat(vol.expiration_time))
	toServices(key, tenName, compName, serviceName, vol.display_name, dateFormat(vol.time_created), fld1, fld2)
def volumeGroupBackups(vol, compName, tenName, serviceName, region):
	key=compName+region+serviceName+vol.display_name
	fld1=the.commaJoin(str(vol.size_in_gbs)+' GB', vol.type)
	toServices(key, tenName, compName, serviceName, vol.display_name, dateFormat(vol.time_created), fld1, region)
def volumes(vol, compName, tenName, serviceName, region): # Same used for: Block Volumes & Volume Groups
	key=compName+region+serviceName+vol.display_name
	toServices(key, tenName, compName, serviceName, vol.display_name, dateFormat(vol.time_created), str(vol.size_in_gbs)+' GB', vol.availability_domain)
def vnicAttachment(va, compName, tenName, serviceName, region):
	theVa = the.vnicAttachments
	if va.instance_id not in theVa: theVa[va.instance_id]={}
	theVaI=theVa[va.instance_id]
	if 'VNICs' not in theVaI: theVaI['VNICs']=[]
	theVaI['VNICs'].append(va.vnic_id)
	log.debug("instance's vnic: " + va.instance_id + ' > ' + va.vnic_id)
def compute(cmp, compName, tenName, serviceName, region, vnCl):
	name=getDisplayName(cmp)
	key=compName+region+serviceName+name
	fld1=cmp.shape + ', ' + str(cmp.shape_config.memory_in_gbs)
	fld2=cmp.region + ', ' + cmp.lifecycle_state
	fld3='-'
	if 'show_compute_ips' in conf.keys:
		ips=[]
		vnics = [vnCl.get_vnic(vnicId).data for vnicId in the.vnicAttachments[cmp.id]['VNICs']]
		for vnic in vnics:
			ip=vnic.private_ip
			if vnic.public_ip: ip+='/'+vnic.public_ip
			ips.append(ip)
		fld3=' | '.join(ips)
	toServices(key, tenName, compName, serviceName, name, dateFormat(cmp.time_created), fld1, fld2, fld3)
def fileSystem(fs, compName, tenName, serviceName, ad):
	key=compName+ad+serviceName+fs.display_name
	toServices(key, tenName, compName, serviceName, fs.display_name, dateFormat(fs.time_created), fs.metered_bytes, ad)
def mountTarget(mnt, compName, tenName, serviceName, ad):
	key=compName+ad+serviceName+mnt.display_name
	toServices(key, tenName, compName, serviceName, dateFormat(mnt.time_created), mnt.display_name, ad)
def clusterNetwork(cn, compName, tenName, serviceName, region):
	key=compName+region+serviceName+cn.display_name
	toServices(key, tenName, compName, serviceName, cn.display_name, dateFormat(cn.time_created), cn.instance_pools.display_name, region)
def instancePool(ip, compName, tenName, serviceName, region):
	key=compName+region+serviceName+ip.display_name
	toServices(key, tenName, compName, serviceName, ip.display_name, dateFormat(ip.time_created), ip.size, region)
def dedicatedVmHost(dvh, compName, tenName, serviceName, region):
	key=compName+region+serviceName+dvh.display_name
	toServices(key, tenName, compName, serviceName, dvh.display_name, dateFormat(dvh.time_created), dvh.dedicated_vm_host_shape, dvh.availability_domain)
def customImages(cmp, compName, tenName, serviceName, region): #Todo: Pending
	## This is listing custom images, along with all other oracle images, not getting right filter from docs
	## Submitted MyHelp Ticket 200615-001123
	# res = compCl.list_images(compId, lifecycle_state='AVAILABLE', page=page)
	# for cmp in res.data:
		# key=compName+region+serviceName+cmp.display_name
		# toServices(key, tenName, compName, serviceName, cmp.display_name+' / '+cmp.launch_mode, cmp.operating_system+' ['+cmp.operating_system_version+']', dateFormat(cmp.time_created))
	dummy='remove this'
def dbSystem(db, compName, tenName, serviceName, region):
	key=compName+region+serviceName+db.display_name
	toServices(key, tenName, compName, serviceName, db.display_name, dateFormat(db.time_created), db.database_edition, db.version)
def autoDB(db, compName, tenName, serviceName, region):
	key=compName+region+serviceName+db.display_name
	toServices(key, tenName, compName, serviceName, db.display_name, dateFormat(db.time_created), db.db_version, db.db_workload)
def autoContainerDB(db, compName, tenName, serviceName, region):
	key=compName+region+serviceName+db.display_name
	toServices(key, tenName, compName, serviceName, db.display_name, dateFormat(db.time_created), db.service_level_agreement_type)
def autoExaDB(db, compName, tenName, serviceName, region):
	key=compName+region+serviceName+db.display_name
	toServices(key, tenName, compName, serviceName, db.display_name, dateFormat(db.time_created), db.shape, db.domain)
def exaDB(db, compName, tenName, serviceName, region):
	key=compName+region+serviceName+db.display_name
	toServices(key, tenName, compName, serviceName, db.display_name, dateFormat(db.time_created), db.shape)
def vmCluster(db, compName, tenName, serviceName, region):
	key=compName+region+serviceName+db.display_name
	toServices(key, tenName, compName, serviceName, db.display_name, dateFormat(db.time_created), db.shape, db.gi_version)
def mySqlDbSystem(db, compName, tenName, serviceName, region):
	key=compName+region+serviceName+db.display_name
	toServices(key, tenName, compName, serviceName, db.display_name, dateFormat(db.time_created), db.mysql_version, db.availability_domain)
def noSqlTables(tb, compName, tenName, serviceName, region):
	try:
		log.debug('Service Count: '+str(len(tb.items)))
	except AttributeError:
		log.debug('NoSqlTables TableCollection, no items obtained !')
		return
	for tbl in tb.items:
		lmts=tbl.table_limits
		fld1=str(lmts.max_storage_in_g_bs)+' GB'
		fld2=the.commaJoin(lmts.max_read_units, lmts.max_write_units)
		key=compName+region+serviceName+tbl.name
		toServices(key, tenName, compName, serviceName, tbl.name, dateFormat(tbl.time_created), fld1, fld2)
def analytics(anl, compName, tenName, serviceName, region):
	key=compName+region+serviceName+anl.name
	toServices(key, tenName, compName, serviceName, anl.name, dateFormat(anl.time_created), anl.feature_set, anl.description)
def integration(int, compName, tenName, serviceName, region):
	key=compName+region+serviceName+int.display_name
	toServices(key, tenName, compName, serviceName, int.display_name, dateFormat(int.time_created), int.integration_instance_type, region)
def loadBalancer(lb, compName, tenName, serviceName, region):
	key=compName+region+serviceName+lb.display_name
	toServices(key, tenName, compName, serviceName, lb.display_name, dateFormat(lb.time_created), lb.shape_name, region)
def healthCheck(hlt, compName, tenName, serviceName, region): # Uses same function for both HTTP and Ping type services
	key=compName+region+serviceName+hlt.display_name
	fld1 = hlt.protocol + ', '
	fld1 += str(hlt.interval_in_seconds)+'s'
	fld2 = region + ', '
	fld2 += 'Enabled' if hlt.is_enabled else 'Disabled'
	toServices(key, tenName, compName, serviceName, hlt.display_name, dateFormat(hlt.time_created), fld1, fld2)

def getRootCompartmentName(tenName): return tenName+' (root)'
def getRootCompartmentID(tenName): return the.compartments[tenName]['(root)'][1]
def getCompartmentName(id):
	[t,k]=the.compartmentIds[id]
	return the.compartments[t][k][0]
def getCompartmentID(tenName, compName): return the.compartments[tenName][compName][1]
def getRegionsSubscribed(tenName): return the.tenancies[tenName][1]
def initKeyIfNew(dict,key,init):
	if key not in dict: dict[key]=init
def giveAdashOnNothing(str):
	if str: return str
	else: return '-'
#