from datetime import datetime,timedelta

def init(a):
    global the,conf,threading
    global gaugeBreaks
    the=a
    conf=the.conf
    threading=the.threading
    gaugeBreaks=the.gaugeBreaks

def start():
    try:
        the.setInfo('Preparing OCI connections ...')
        the.resetGlobalVariables()

        # for 1 tenancy, calculating totalGaugeBreaks
        totalGaugeBreaks = gaugeBreaks['simple+'] # for getting tenancy details
        if not the.justConnectionCheck:
            if the.getSelection('audits','usersAndGroups'): totalGaugeBreaks+=gaugeBreaks['simple']*4
            if the.getSelection('audits', 'compartments'): totalGaugeBreaks+=gaugeBreaks['simple']
            if the.getSelection('audits', 'limits'): totalGaugeBreaks+=gaugeBreaks['serviceLimits']
            if the.getSelection('audits', 'policies'): totalGaugeBreaks+=gaugeBreaks['allCompartments']
            if the.getSelection('audits', 'instances'):
                selectedServices = the.getSelection('audits', 'ociServices')
                totalGaugeBreaks+= gaugeBreaks['allCompartments'] * len(selectedServices)
                if 'Data Science' in selectedServices: totalGaugeBreaks+= gaugeBreaks['allCompartments']*2 # 2 more for notebook sessions, and models
            if the.getSelection('audits', 'events'): totalGaugeBreaks+=gaugeBreaks['allCompartments']
            if the.getSelection('audits', 'networks'): totalGaugeBreaks+=gaugeBreaks['allCompartments'] * (len(the.getSelection('audits', 'networkComponents'))+1) # +1 for VCN itself
            if the.getSelection('audits', 'cloudGuard'): totalGaugeBreaks+=gaugeBreaks['simple']*2
            if the.getSelection('audits', 'cloudAdvisor'): totalGaugeBreaks+=gaugeBreaks['simple']
            
            if totalGaugeBreaks==gaugeBreaks['simple+']:
                err="No valid Audits Selected !!\n\nSelect required Audits and try again.\n\n"
                the.setError(err)
                if the.ui: wx.MessageBox(err, 'Select required Audits', wx.OK | wx.ICON_EXCLAMATION)
                return # Todo: should end on console, and return back to UI
            
        # Nr: Total 100% - initial value - 5% last progress for reports
        # Dr: Remaining Value of Nr. is divided to number of domains and audits selected
        selectedDomains = the.getSelection('domains', 'selection')
        numOfSelectedTenancies = len(selectedDomains)
        gaugeIncNumPerTenancy = float(100-5)/numOfSelectedTenancies

        the.gaugeIncNum = gaugeIncNumPerTenancy/totalGaugeBreaks
        # print("gaugeIncNum: " + str(the.gaugeIncNum))

        global oci, reports, audits
        import reports, audits, oci # Lazy loading
        the.oci=oci
        audits.init(the)
        reports.init(the)

        for tenancyName in the.getSelection('domains', 'selection'):
            tenancyOcid = conf.tenancyOcids[tenancyName]
            userOcid    = conf.userOcids[tenancyName]
            region      = conf.regions[tenancyName]
            key_file    = conf.key_files[tenancyName]
            fingerprint = conf.fingerprints[tenancyName]
            if not(tenancyOcid and userOcid and region and key_file and fingerprint):
                err="Missing configurations !!\n\nTenancyID/UserID/Region/Key/Fingerprint not configured in " + configFileName + ", for domain " + tenancyName + " !!"
                the.setError(err)
                if ui:
                    dlg=wx.MessageDialog(self, 
                        err + "\n\nDo you want to proceed with next tenancy or terminate ?",
                        tenancyName + ' - missing configurations', wx.OK | wx.CANCEL | wx.OK_DEFAULT | wx.ICON_EXCLAMATION)
                    dlg.SetOKCancelLabels("&Proceed", "&Terminate")
                    ans=dlg.ShowModal()
                    if ans==wx.ID_CANCEL: return
                    else: continue
                else:
                    return # not given option to continue for next tenancy in non ui mode
            
            the.setInfo("Connecting: " + tenancyName + "  . . .")

            config = {
                "tenancy": tenancyOcid,
                "user": userOcid,
                "key_file": key_file,
                "fingerprint": fingerprint,
                "region": region,
                "log_requests": False # set this to true, if required more details on requests and responses
            }

            try:
                idnty = oci.identity.IdentityClient(config)
                regions = idnty.list_region_subscriptions(tenancyOcid).data
                the.setInfo("Connection Success: " + tenancyName)
                if the.justConnectionCheck:
                    the.increamentGauge(gaugeIncNumPerTenancy)
                    continue

                global rgns, ads
                rgns = []; ads = {}
                the.initTenancyDicts(tenancyName)
                gaugeIncNumForRegion=(the.gaugeIncNum*gaugeBreaks['simple+'])/2
                the.increamentGauge(gaugeIncNumForRegion)
                thrds=[]
                the.setInfo(tenancyName + ": Getting Regions & Availability Domains . . .")
                for r in regions: thrds.append(the.createThread(getRegionsAndADs, r, config.copy())) # pass config's copy, modifying same dictionary parallely in threads creates uncertain results
                the.increamentGauge(gaugeIncNumForRegion)
                #if the.getSelection('audits', 'compartments'): #Default always find compartments
                thrds.append(the.createThread(audits.listCompartments, idnty, tenancyName, tenancyOcid))
                if the.getSelection('audits','usersAndGroups'):
                    the.createThread(audits.listUserGroups, idnty, tenancyName, tenancyOcid)
                for t in thrds: t.join() # wait for all mandatory threads to finish
                thrds=[]
                the.tenancies[tenancyName] = [tenancyOcid, rgns, ads]
                config['region']=rgns[0] # Setting default to home region, change whenever required by taking copy of this config
                if the.getSelection('audits', 'limits'):
                    the.createThread(audits.listLimits, config.copy(), tenancyName)
                if the.getSelection('audits', 'policies'):
                    the.createThread(audits.listPolicies, idnty, tenancyName)
                #if self.m_checkBox_Billing.GetValue():
                    # the.setInfo(tenancyName + ': Getting Billing...')
                    # the.increamentGauge(the.gaugeIncNum)
                if the.getSelection('audits', 'instances'):
                    the.createThread(audits.loopRegions, audits.listInstancesOfRegion, config.copy(), tenancyName)
                if the.getSelection('audits', 'events'):
                    eventEnd = datetime.utcnow()
                    eventStart = getAuditEventsStartDate(eventEnd)
                    #eventEnd   = datetime.strptime('2021-04-18 05:11:07.035284', '%Y-%m-%d %H:%M:%S.%f')
                    #eventStart = datetime.strptime('2021-04-17 05:11:07.035284', '%Y-%m-%d %H:%M:%S.%f')
                    the.updateSelection('audits', 'eventsLastRun', str(eventEnd))
                    the.eventDates = {'start':eventStart,'end':eventEnd} # used in reports
                    the.createThread(audits.loopRegions, audits.auditEventsOfRegion, config.copy(), tenancyName, start=eventStart, end=eventEnd)
                if the.getSelection('audits', 'networks'):
                    the.createThread(audits.loopRegions, audits.networksOfRegion, config.copy(), tenancyName)
                if the.getSelection('audits', 'cloudGuard'):
                    the.createThread(audits.cloudGuard, config.copy(), tenancyName)
                if the.getSelection('audits', 'cloudAdvisor'):
                    the.createThread(audits.cloudAdvisor, config.copy(), tenancyName)
                if False: #Not working for OU internal tenancies
                    the.createThread(usageFn, config.copy(), tenancyName)
            except (IOError,OSError) as e:
                err=str(e)
                if('No such file' in err):
                    err = "Private Key file not found\n\n" + err + "\n\n"
                    head = 'Key File Not Available !'
                elif('ConnectionError' in err):
                    err = "Check URL or Internet Connection !\n\n" + err
                    head = 'Connection issue !'
                elif('read timeout' in err):
                    err = "Internet Connection Time out !\n\n" + err
                    head = 'Connection issue !'
                else:
                    err = "Unhandled IOError:\n\n" + err
                    head = 'Unhandled IOError'
                the.setError(err)
                if the.ui: wx.MessageBox(err, head, wx.OK | wx.ICON_ERROR)
                return
            except oci.exceptions.ServiceError as e:
                if e.status == 401:
                    #the.setMsg('Connection FAILED: ' + tenancyName)
                    the.increamentGauge(gaugeIncNumPerTenancy)
                    the.issueTenancies.append(tenancyName)
                    err = "Authentication setup failed for tenancy - " + tenancyName + "\n\n" + str(e)
                    the.setError(err)
            except Exception as e:	# show unhandeled exception, and continue
                err = "Unhandled exception occured\n\n" + str(e)
                the.setError(err)
                raise

        if the.justConnectionCheck:
            the.setInfo('Selected Tenancies Connection Check Completed.')
            the.justConnectionCheck=False
            if len(the.issueTenancies)>0:
                msg = "These Tenancies Authentication Failed:\n\n"
                msg += "\n".join(the.issueTenancies)
                msg += "\n\nThis list also printed to log.\n"
                the.setWarn(msg)
                return 'warn', 'Tenancies Connection Test', msg
            else:
                msg = "Good..\n\nWe are able to connect all selected Tenancies, No issue in Authentication setup.\n"
                the.setInfo(msg)
                return 'info', 'Tenancies Connection Test', msg
        else:
            for t in the.mt:
                # t.join()
                while t.is_alive():
                    tc = threading.active_count() - 1
                    the.setInfo('Waiting for (' + str(tc) + ') threads to Complete ...')
                    if the.gaugeValue > 55: # rolling back few
                        g=the.gaugeValue
                        if   tc>5: g=55
                        elif tc>4: g=60
                        elif tc>3: g=70
                        elif tc>2: g=80
                        elif tc>1: g=90
                        the.setGauge(g)
                        # print(str(tc) + ' threads, ' + str(g))
                    the.sleep(1)
            the.setInfo('Closing all OCI Connections ... ..')
            reports.generateReport()
        the.setInfo('Done')
    except Exception as e:
        err=str(e)
        the.setError(err)
        raise
	
def getRegionsAndADs(rgn,conf):
	rName=rgn.region_name
	avDs=[]; conf['region']=rName
	idnty = oci.identity.IdentityClient(conf)
	avlDomains = idnty.list_availability_domains(conf['tenancy']).data
	for a in avlDomains: avDs.append(a.name)
	ads[rName]=avDs
	rgns.insert(0,rName) if rgn.is_home_region else rgns.append(rName)

# Constants
EVENTS1HOUR  = 0
EVENTS1DAY   = 1
EVENTS1MONTH = 2
EVENTSLASTRUN= 3
def getAuditEventsStartDate(end):
	opt = the.getSelection('audits', 'eventsDateRange')
	if opt==EVENTS1HOUR: return end-timedelta(hours=1)
	elif opt==EVENTS1DAY: return end-timedelta(days=1)
	elif opt==EVENTS1MONTH: return end-timedelta(days=30)
	elif opt==EVENTSLASTRUN:
		lastRunDateTime = the.getSelection('audits', 'eventsLastRun')
		if not lastRunDateTime: # Returns boolean false, if audit events last run not available
			the.setWarn('Audit events last run not available !!, proceeding with just last 1 hour..')
			return end-timedelta(hours=1)
		else:
			return datetime.strptime(lastRunDateTime, '%Y-%m-%d %H:%M:%S.%f')
        

