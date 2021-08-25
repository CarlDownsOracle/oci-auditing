# Copyright (c) 2019-2021, Oracle and/or its affiliates
# Licensed under the Universal Permissive License v1.0 as shown at https://oss.oracle.com/licenses/upl

import os,re
from datetime import datetime
from time import gmtime, strftime, sleep

def init(a):
    global ui,the,conf
    the=a
    ui=the.ui
    conf=the.conf

def generateReport():
    import xlsxwriter
    end_time_local = datetime.now().strftime('%Y-%m-%d %H:%M:%S'); time_zone = strftime("[%z]", gmtime())
    end_time_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    the.setInfo('Generating final Excel Report ...')
    global workbook,ws,row,format,startRow,data,head,cols,service,lnk
    lnk={} # used to store any hashed/dictionaries/linked kind of datas
    auditIssuesFound=False
    reportName = the.startTime + ' OCI Auditing Report.xlsx'
    reportDirPath = conf.resDr
    reportPath = os.path.abspath(reportDirPath + '/' + reportName)
    workbook = xlsxwriter.Workbook(reportPath)
    
    workbook.set_properties({
        'title'   : 'OCI Auditing Report',
        'subject' : 'Reports of Oracle Cloud Infrastructure tenancy components',
        'author'  : 'Karthik Kumar HP',
        'manager' : 'Karthik.Hiraskar@oracle.com',
        'company' : 'Oracle',
        'category': 'Reports',
        'keywords': 'OCI, Report, Audit',
        'comments': 'Created by '+the.tool_name+', ver '+the.version,
        'status'  : ' ',
    })
    
    format = addAllFormatsToWorkbook()
    
    addTab('Tenancies', colWidths=[14,50,40,65])
    
    ws.write_rich_string('B1', format['bold'], end_time_local, format['normal'], '  ', time_zone)
    ws.write_rich_string('C1', format['bold'], end_time_utc, format['normal'], '  [UTC]')
    
    row=2
    ws.write(row,2, '** first one is home-region', format['normal_small'])
    row+=1
    writeHeader('Tenancy','Tenancy OCID','Subscribed Regions','Availability Domains')
    ws.freeze_panes(row,0)
    sortedTenancies = sorted(the.tenancies.keys())
    
    for t in sortedTenancies:
        regions = the.tenancies[t][1]
        rowHeight = 8.5 * len(regions)
        if rowHeight>15: ws.set_row(row, rowHeight) # 15 is normal height
        avlDomains=[]
        for rgn in regions:
            avlDomains.append(', '.join(the.tenancies[t][2][rgn]))
        ws.write(row,0, t, format['tblCell'])
        ws.write(row,1, the.tenancies[t][0], format['tblCell_f6_wrap'])
        if len(regions)>0:
            homeRegion = regions.pop(0) # home-region taken out from regions list 
            otherSubscribedRegions = ', -'
            if len(regions)>0: otherSubscribedRegions = ', ' + ', '.join(regions)
            ws.write_rich_string(row,2, format['italic_underlined'], homeRegion, format['normal'], otherSubscribedRegions, format['tblCell_wrap'])
        else:
            ws.write_rich_string(row,2, format['italic'], '-- Not Able to get Regions', format['normal'], ' !', format['tblCell'])
            
        ws.write(row,3, '\n'.join(avlDomains), format['tblCell_f6_wrap'])
        row+=1
    ws.autofilter(startRow, 0, row-1, 3)
    row+=2
    if len(the.issueTenancies)>0:
        ws.write(row,1, 'Tenancies failed to connect:',format['bold_underlined'])
        row+=1
        for t in the.issueTenancies:
            ws.write(row,1, t, format['italic'])
            row+=1
    row+=2; ws.write_rich_string(row, 1, '-- This Report is Created by: ', format['bold'], the.tool_name, format['normal'], ', Version ', format['bold'], the.version, format['normal'])
    row+=1; ws.write(row, 1, 'Log File: ' + conf.logfile, format['normal_small'])
    row+=2; ws.set_selection(row, 0, row, 0)
    # print('KK - Tenancies Over')
    
    def addCountSummary(row, dict):
        ws.write(row,0, 'Count Summary:',format['bold_underlined'])
        row+=1
        for t in sortedTenancies:
            ws.write(row,0, t, format['italic'])
            ws.write(row,1, len(dict[t]), format['italic_left'])
            row+=1
        ws.set_selection(row+1, 2, row+1, 2)
    
    addTab('Compartments', colWidths=[14,30,65,7,9,35,35])
    writeHeader('Tenancy','Compartment Name','Compartment OCID','Level','Status','Compartment Description','Report Comments')
    ws.freeze_panes(row,0)
    for t in sortedTenancies:
        for k in sorted(the.compartments[t].keys()):
            cl_format = format['tblCell']
            cl_format_small = format['tblCell_f8']
            if the.compartments[t][k][5]:
                cl_format = format['tblCell_hig']
                cl_format_small = format['tblCell_hig_f8']
            ws.write(row,0, t, cl_format)
            ws.write(row,1, the.compartments[t][k][0], cl_format)
            ws.write(row,2, the.compartments[t][k][1], cl_format_small)
            ws.write(row,3, the.compartments[t][k][2], cl_format)
            ws.write(row,4, the.compartments[t][k][3], cl_format)
            ws.write(row,5, the.compartments[t][k][4], cl_format)
            ws.write(row,6, the.compartments[t][k][5], cl_format_small)
            row+=1
    ws.autofilter(0, 0, row-1, 6)
    addCountSummary(row+2, the.compartments)

    if the.getSelection('audits','usersAndGroups'):
        ### Users
        addTab('Users', colWidths=[14,30,30,30,65,20,30,20])
        writeHeader('Tenancy','User Name','Description','Email','OCID','Created','Report Comments','Last Login Time')
        ws.freeze_panes(row,0)
        
        for t in sortedTenancies:
            for k in sorted(the.users[t].keys()):
                # Date Time pattern update, Ex: 2019-08-01T06:33:51.715+0000 => 2019-08-01 06:33:51
                creatDate=the.dateFormat(the.users[t][k][4])
                lastLoginTime=the.dateFormat(the.users[t][k][6])
                cmnt=the.users[t][k][5]
                cl_format = format['tblCell']
                cl_format_small = format['tblCell_f8']
                if cmnt:
                    cl_format = format['tblCell_hig']
                    cl_format_small = format['tblCell_hig_f8']
                ws.write(row,0, t, cl_format)
                ws.write(row,1, the.users[t][k][0], cl_format)
                ws.write(row,2, the.users[t][k][1], cl_format)
                ws.write(row,3, the.users[t][k][2], cl_format)
                ws.write(row,4, the.users[t][k][3], cl_format_small)
                ws.write(row,5, creatDate,      cl_format)
                ws.write(row,6, cmnt,           cl_format_small)
                ws.write(row,7, lastLoginTime, cl_format)
                row+=1
        ws.autofilter(0, 0, row-1, 7)
        addCountSummary(row+2, the.users)
    
        ### Groups
        addTab('Groups', colWidths=[14,30,30,65,20,30])
        writeHeader('Tenancy','Group Name','Description','OCID','Created','Report Comments')
        ws.freeze_panes(row,0)
        
        for t in sortedTenancies:
            for k in sorted(the.groups[t].keys()):
                creationDate=the.dateFormat(the.groups[t][k][3])
                cmnt=the.groups[t][k][4]
                cl_format = format['tblCell']
                cl_format_small = format['tblCell_f8']
                if cmnt:
                    cl_format = format['tblCell_hig']
                    cl_format_small = format['tblCell_hig_f8']
                ws.write(row,0, t, cl_format)
                ws.write(row,1, the.groups[t][k][0], cl_format)
                ws.write(row,2, the.groups[t][k][1], cl_format_small)
                ws.write(row,3, the.groups[t][k][2], cl_format_small)
                ws.write(row,4, creationDate, cl_format)
                ws.write(row,5, cmnt, cl_format_small)
                row+=1
        ws.autofilter(0, 0, row-1, 5)
        addCountSummary(row+2, the.groups)

        ### Group Members
        addTab('GroupMembers', colWidths=[14,30,30,10,20])
        writeHeader('Tenancy','Group Name','User Name','Status','Created')
        ws.freeze_panes(row,0)
        
        for t in sortedTenancies:
            for k in sorted(the.groupMembers[t].keys()):
                creationDate=the.dateFormat(the.groupMembers[t][k][3])
                cl_format = format['tblCell']
                ws.write(row,0, t, cl_format)
                ws.write(row,1, the.groupMembers[t][k][0], cl_format)
                ws.write(row,2, the.groupMembers[t][k][1], cl_format)
                ws.write(row,3, the.groupMembers[t][k][2], cl_format)
                ws.write(row,4, creationDate, cl_format)
                row+=1
        ws.autofilter(0, 0, row-1, 4)
        addCountSummary(row+2, the.groupMembers)

        ### Dynamic Groups
        addTab('DynamicGroups', colWidths=[14,30,30,65,20])
        writeHeader('Tenancy','Dynamic Group Name','Description','OCID','Created')
        ws.freeze_panes(row,0)
        for t in sortedTenancies:
            for grp in sorted(the.dynamicGroups[t].keys()):
                writeRow(data=[t,grp,
                            the.dynamicGroups[t][grp][0],the.dynamicGroups[t][grp][1],
                            the.dateFormat(the.dynamicGroups[t][grp][2])],
                         style=getStyle(f8=[2,3])
                        )
        finalTouchTable()
        addCountSummary(row+2, the.dynamicGroups)
        
    if the.getSelection('audits', 'limits'):
        addTab('Service Limits', colWidths=[14,22,22,25,30,18,18,18])
        if conf.limitsShowUsed:
            writeHeader('Tenancy','Service','Scope','Limit Name','Limit Description','Service Limit','Service Used','Service Available')
        else:
            writeHeader('Tenancy','Service','Scope','Limit Name','Limit Description','Service Limit')
        ws.freeze_panes(row,0)
        
        for t in sortedTenancies:
            for k in sorted(the.limits[t].keys()):
                cl_format = format['tblCell']
                lmt = the.limits[t][k][4]
                if conf.limitsShowUsed:
                    usd = the.limits[t][k][5]
                    avl = the.limits[t][k][6]
                    if usd!=0 and conf.validate['LIMITS']:
                        if   usd>lmt : cl_format=format['tblCell_hig']
                        elif usd>(lmt*conf.limits_alert_value): cl_format=format['tblCell_med']
                ws.write(row,0, t, cl_format)
                ws.write(row,1, the.limits[t][k][0], cl_format)
                ws.write(row,2, the.limits[t][k][1], cl_format)
                ws.write(row,3, the.limits[t][k][2], cl_format)
                ws.write(row,4, the.limits[t][k][3], cl_format)
                ws.write(row,5, lmt, cl_format)
                if conf.limitsShowUsed:
                    ws.write(row,6, usd, cl_format)
                    ws.write(row,7, avl, cl_format)
                row+=1
        if conf.limitsShowUsed: ws.autofilter(0, 0, row-1, 7)
        else: ws.autofilter(0, 0, row-1, 5)
        
        if len(conf.limitsSkipServices)>0:
            row+=3
            ws.write(row,0, 'Skipped Services:', format['bold_underlined'])
            row+=1
            colStart=0; colEnd=7
            col=colStart
            for srv in conf.limitsSkipServices:
                ws.write(row,col, srv, format['italic'])
                if col<colEnd:
                    col+=1
                else:
                    row+=1 # Next row & reinitiate col
                    col=colStart
        # addCountSummary(row+2, the.limits)
    
    if the.getSelection('audits', 'policies'):
        addTab('Policies', colWidths=[14,30,30,70,35])
        writeHeader('Tenancy','Compartment','Policy Name','Policy Statement','Report Comments')
        ws.freeze_panes(row,0)
        
        for t in sortedTenancies:
            for k in sorted(the.policies[t].keys()):
                cl_format = format['tblCell']
                cl_format_small = format['tblCell_f8']
                if the.policies[t][k][3]:
                    cl_format = format['tblCell_hig']
                    cl_format_small = format['tblCell_hig_f8']
                ws.write(row,0, t, cl_format)
                ws.write(row,1, the.policies[t][k][0], cl_format)
                ws.write(row,2, the.policies[t][k][1], cl_format)
                ws.write(row,3, the.policies[t][k][2], cl_format_small)
                ws.write(row,4, the.policies[t][k][3], cl_format_small)
                row+=1
        ws.autofilter(0, 0, row-1, 4)
        addCountSummary(row+2, the.policies)
        
    if the.getSelection('audits', 'instances'):
        addTab('Services Created', colWidths=[14,25,30,30,20,30,30,30,30,30,30,30,30])
        ws.write(row,5,'* Ref. extra fields details after the table',format['normal_small'])
        row+=1
        writeHeader('Tenancy','Compartment','Cloud Service','Display Name','Created','ExtraField-1','ExtraField-2','ExtraField-3','ExtraField-4')
        maxCol=8
        ws.freeze_panes(row,0)
        
        for t in sortedTenancies:
            for k in sorted(the.instances[t].keys()):
                ws.write(row,0, t, format['tblCell'])
                col=1
                for data in the.instances[t][k]:
                    ws.write(row,col, data, format['tblCell'])
                    col+=1
                while col<=maxCol:
                    ws.write(row,col, '-', format['tblCell'])
                    col+=1
                row+=1
        ws.autofilter(1, 0, row-1, maxCol)
        
        row+=1
        ws.write(row,0, 'EXTRA FIELDS DETAILS:', format['bold_underlined'])
        col=2
        for data in ['Cloud Service','ExtraField-1','ExtraField-2','ExtraField-3','ExtraField-4']:
            ws.write(row,col, data, format['italicBold_downBorder'])
            col+=1
        selectedServices = the.getSelection('audits', 'ociServices') # array of selected services
        for srv in selectedServices:
            row+=1
            col=2
            for data in [srv] + the.ociServices[srv]['xtraFieldsInfo']:
                ws.write(row,col, data, format['italic_downBorder'])
                col+=1
        
        if len(conf.disableCompartments)>0:
            row+=2
            ws.write(row,0, 'Disabled Compartments List:', format['bold_underlined'])
            row+=1
            colStart=0; colEnd=6
            col=colStart
            for comp in conf.disableCompartments:
                ws.write(row,col, comp, format['italic'])
                if col<colEnd:
                    col+=1
                else:
                    row+=1 # Next row & reinitiate col
                    col=colStart
        addCountSummary(row+2, the.instances)
    
    if the.getSelection('audits', 'events'):
        addTab('Events', colWidths=[14,20,15,40,30,30,30,19])
        writeHeader('Tenancy','Compartment','Region / AD','User Details','Event Source','Event Name','Network Access','Event Time')
        ws.freeze_panes(row,0)
        
        showAll=False
        if 'events_show_all' in conf.keys: showAll=True
        cl_format = format['tblCell']
        cl_format_small = format['tblCell_f8']
        for t in sortedTenancies:
            for k in sorted(the.events[t].keys()):
                evt=the.events[t][k]
                event_source = evt[4]
                event_name = evt[5]
                if evt[0] or showAll:
                    if evt[0]: auditIssuesFound=True
                    writeRow(data=[t,evt[1],evt[2],evt[3],event_source,event_name,evt[6],evt[7]], style=getStyle(risk=evt[0]))
        ws.autofilter(0, 0, row-1, 7)
        row+=2; ws.write(row,0, 'Audit Events, selected start & end dates [UTC format]:',format['bold_underlined'])
        row+=1
        ws.write(row,0, str(the.eventDates['start']), format['italic'])
        ws.write(row,2, str(the.eventDates['end']), format['italic'])
        addCountSummary(row+2, the.events)
    
    if the.getSelection('audits', 'networks'):
        ## VCN
        srvc='VCN'
        addTab(srvc, colWidths=[20,20,20,20,20,15,18], tabColor='#632523')
        addHeading2(srvc)
        writeHeader('Tenancy','Region','Compartment','Name','OCID','CIDR Block','Created Time')
        lnk[srvc]={}
        for t in sorted(the.networks[srvc].keys()):
            for r in sorted(the.networks[srvc][t].keys()):
                for c in sorted(the.networks[srvc][t][r].keys()):
                    for n in sorted(the.networks[srvc][t][r][c].keys()):
                        v=the.networks[srvc][t][r][c][n]
                        writeRow(data=[t,r,c,n,v[0],v[1],v[2]], style=getStyle(f6=[4]))
                        lnk[srvc][v[0]] = n+' ['+t+'/'+c+']' # vcn-ocid = name [tenancy/comp]
        finalTouchTable()
        
        if len(conf.disableCompartments)>0:
            row+=3
            ws.write(row,0, 'Disabled Compartments List:', format['bold_underlined'])
            row+=1
            colStart=0; colEnd=7
            col=colStart
            for comp in conf.disableCompartments:
                ws.write(row,col, comp, format['italic'])
                if col<colEnd:
                    col+=1
                else:
                    row+=1 # Next row & reinitiate col
                    col=colStart
        
        nwSerSel=the.getSelection('audits', 'networkComponents')
        
        service='Route Table'
        if service in nwSerSel:
            addTab('RT', colWidths=[20,20,20,20,20,20], tabColor='#632523')
            addHeading2(service+'s')
            generateHeaderList('VCN OCID','RT Name','RT OCID','Created Time')
            for vcnID in the.networks[service].keys():
                for rt in the.networks[service][vcnID]: data.append([vcnID, rt[0], rt[1], rt[2]])
            addTable()
                
            service='route_rules'
            row+=1
            addHeading2('Route Rules', hx='h3')
            writeHeader('RT OCID','Destination','Destination Type','Network Entity OCID','Description')
            for rtID in the.networks[service].keys():
                for rr in the.networks[service][rtID]:
                    writeRow(data=[rtID, rr[0], rr[1], rr[2], rr[3]], style=['tblCell_f6','tblCell','tblCell','tblCell_f6','tblCell'])
            finalTouchTable()
        
        service='Subnet'
        if service in nwSerSel:
            addTab(service, colWidths=[20,30,20,15,18,20,18], tabColor='#632523')
            addHeading2(service+'s')
            generateHeaderList('VCN [Tenancy/Compartment] ~','Name','OCID','CIDR','Access','Security List OCIDs','Created Time')
            for vcnID in the.networks[service].keys():
                for sn in the.networks[service][vcnID]: data.append([getLnk('VCN',vcnID), sn[0], sn[1], sn[2], sn[3], sn[4], sn[5]])
            addTable()
                
        service='Security List'
        srvc='SL'
        if service in nwSerSel:
            lnk[srvc]={}
            addTab(srvc, colWidths=[25,20,20,20,20,12,20,20,20], tabColor='#632523')
            addHeading2(service+'s')
            writeHeader('VCN [Tenancy/Compartment]','SL Name','SL OCID','Created Time',"Subnet's Privacy")
            for vcnID in the.networks[service].keys():
                for sl in the.networks[service][vcnID]:
                    writeRow(data=[getLnk('VCN',vcnID), sl[0], sl[1], sl[2], sl[3]], style=getStyle(f6=[0,2,4]))
                    lnk[srvc][sl[1]]=sl[0] # sl-ocid = name
            finalTouchTable()
            
            row+=1
            ws.merge_range(row,0,row,3,'SL - Security Rules',format['h3'])
            ws.write(row,6,'type / source_port_range',format['normal_small'])
            ws.write(row,7,'code / destination_port_range',format['normal_small'])
            row+=1
            writeHeader('SL','Egress/Ingress Rule','Stateless','Destination/Source Type','Destination/Source','Protocol','Field-1','Field-2','Description')
            service='sl_egress_security_rules'
            for slID in the.networks[service].keys():
                for egr in the.networks[service][slID]:
                    if egr[0]: auditIssuesFound=True
                    writeRow(data=[getLnk('SL',slID), 'Egress', egr[1], egr[2], egr[3], egr[4], egr[5], egr[6], egr[7]], style=getStyle(risk=egr[0], f6=[0]))
            service='sl_ingress_security_rules'
            for slID in the.networks[service].keys():
                for ing in the.networks[service][slID]:
                    if ing[0]: auditIssuesFound=True
                    writeRow(data=[getLnk('SL',slID), 'Ingress', ing[1], ing[2], ing[3], ing[4], ing[5], ing[6], ing[7]], style=getStyle(risk=ing[0], f6=[0]))
            finalTouchTable()
                
        service='Network Security Group'
        if service in nwSerSel:
            srvc='NSG'
            lnk[srvc]={}
            addTab(srvc, colWidths=[20,20,20,20,20,12,20,20,20,18], tabColor='#632523')
            addHeading2(service+'s')
            generateHeaderList('VCN [Tenancy/Compartment] ~','NSG Name','NSG OCID','Created Time')
            for vcnID in the.networks[service].keys():
                for nsg in the.networks[service][vcnID]:
                    data.append([getLnk('VCN',vcnID), nsg[0], nsg[1], nsg[2]])
                    lnk[srvc][nsg[1]] = nsg[0] # nsg-ocid=nsg-name
            addTable()
                
            service='nsg_security_rules'
            row+=1
            ws.merge_range(row,0,row,3,'NSG - Security Rules',format['h3'])
            ws.write(row,6,'type / source-port-range',format['normal_small'])
            ws.write(row,7,'code / destination-port-range',format['normal_small'])
            row+=1
            writeHeader('NSG ~','Stateless','Direction','Type Source/Destination','Source/Destination','Protocol','Field-1','Field-2','Description','Created Time')
            for nsgID in the.networks[service].keys():
                for sr in the.networks[service][nsgID]:
                    if sr[0]: auditIssuesFound=True
                    writeRow([getLnk('NSG',nsgID), sr[1], sr[2], sr[3], sr[4], sr[5], sr[6], sr[7], sr[8], sr[9]], style=getStyle(risk=sr[0], f6=[0]))
            finalTouchTable()
                
            service='nsg_vnics'
            #row+=1
            addHeading2('NSG - VNICs', hx='h3')
            generateHeaderList('NSG ~','Parent resource OCID','VNIC OCID','Time Associated')
            for nsgID in the.networks[service].keys():
                for v in the.networks[service][nsgID]: data.append([getLnk('NSG',nsgID), v[0], v[1], v[2]])
            addTable()
        
        service='Internet Gateway'
        if service in nwSerSel:
            addTab('IG', colWidths=[20,30,20,12,10,18], tabColor='#632523')
            addHeading2(service+'s')
            generateHeaderList('VCN OCID','Name','OCID','State','Enabled','Created Time')
            for vcnID in the.networks[service].keys():
                for ig in the.networks[service][vcnID]: data.append([vcnID, ig[0], ig[1], ig[2], ig[3], ig[4]])
            addTable()
            
        service='NAT Gateway'
        if service in nwSerSel:
            addTab('NG', colWidths=[20,30,20,12,10,17,18], tabColor='#632523')
            addHeading2(service+'s')
            generateHeaderList('VCN OCID','Name','OCID','State','Block Traffic','Public IP Address','Created Time')
            for vcnID in the.networks[service].keys():
                for nat in the.networks[service][vcnID]: data.append([vcnID, nat[0], nat[1], nat[2], nat[3], nat[4], nat[5]])
            addTable()
        
        service='Service Gateway'
        if service in nwSerSel:
            addTab('SG', colWidths=[20,30,20,12,40,20,12,18], tabColor='#632523')
            addHeading2(service+'s')
            generateHeaderList('VCN OCID','Name','OCID','State','Services','Route Table OCID','Block Traffic','Created Time')
            for vcnID in the.networks[service].keys():
                for sg in the.networks[service][vcnID]: data.append([vcnID, sg[0],sg[1],sg[2],sg[3],sg[4],sg[5],sg[6]])
            addTable()

        service="VCN's DRG"
        service1="Dynamic Routing Gateway"
        if service in nwSerSel or service1 in nwSerSel:
            addTab('DRG', colWidths=[20,20,30,20,12,18,20], tabColor='#632523')
            if service in nwSerSel:
                addHeading2(service+'s')
                generateHeaderList('VCN OCID','DRG OCID','Name','Route Table OCID','State','Created Time')
                for vcnID in the.networks[service].keys():
                    for att in the.networks[service][vcnID]: data.append([vcnID, att[0],att[1],att[2],att[3],att[4]])
                addTable()
            service=service1; row+=1
            if service in nwSerSel:
                addHeading2(service+'s')
                writeHeader('Tenancy','Compartment','Name','DRG OCID','State','Region','Created Time')
                for t in sorted(the.networks[service].keys()):
                    for r in sorted(the.networks[service][t].keys()):
                        for c in sorted(the.networks[service][t][r].keys()):
                            for n in sorted(the.networks[service][t][r][c].keys()):
                                drg=the.networks[service][t][r][c][n]
                                writeRow(data=[t,c,n,drg[0],drg[1],r,drg[2]], style=getStyle(f6=[3]))
                finalTouchTable()

        service="Local Peering Gateway"
        if service in nwSerSel:
            addTab('LPG', colWidths=[20,25,12,15,20,18,15,18], tabColor='#632523')
            if service in nwSerSel:
                addHeading2(service+'s')
                generateHeaderList('VCN OCID','Name','State','Peering Status','Route Table OCID','Peer Advertised CIDR','Cross-Tenancy','Created Time')
                for vcnID in the.networks[service].keys():
                    for obj in the.networks[service][vcnID]: data.append([vcnID, obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6]])
                addTable()
        
    if the.getSelection('audits', 'cloudGuard'):
        tabName="CloudGuard"
        cGws = addTab(tabName, colWidths=[40,11], tabColor='#F08080', header=False)
        riskInit={'Critical':0,'High':0,'Medium':0,'Low':0,'Minor':0}
        riskDict = riskInit.copy(); rgnDict={}
        service="Problems"
        addTab('CG '+service, colWidths=[14,20,22,18,20,25,15,12,18,18], tabColor='#F08080')
        addHeading2(tabName + ' ' + service)
        writeHeader('Tenancy','Compartment','Labels','State','Regions(Affected)','Resource Name','Resource Type','Risk','First Found On','Last Found On')
        for t in the.cloudGuard[service].keys():
            for c in the.cloudGuard[service][t].keys():
                for pr in the.cloudGuard[service][t][c]:
                    risk=pr[5]
                    rgn=pr[2]
                    writeRow([t,c, pr[0],pr[1],rgn,pr[3],pr[4],risk,pr[6],pr[7]], getStyle(risk=risk))
                    riskDict[risk]+=1
                    if not rgn in rgnDict: rgnDict[rgn]=riskInit.copy()
                    rgnDict[rgn][risk]+=1
        finalTouchTable()
        row=2; ws=cGws
        writeHeader('Risk', 'Problems #')
        totalProblems=0
        for r in riskDict.keys():
            writeRow([r,riskDict[r]])
            totalProblems+=riskDict[r]
        writeRow(['Total Problems Identified', totalProblems], ['tblCell_bold','tblCell_bold'])
        prblmsChart = workbook.add_chart({'type': 'doughnut'})
        prblmsChart.add_series({
            'name': 'CloudGuard Detected Risks',
            'categories': [tabName,3,0,row-2,0],
            'values':     [tabName,3,1,row-2,1],
            'data_labels': {'percentage': True, 'value':True},
        })
        prblmsChart.set_title({'name': 'CloudGuard PROBLEMS'})
        prblmsChart.set_style(10)
        prblmsChart.set_chartarea({'border': {'none': True}})
        ws.insert_chart('C1', prblmsChart, {'x_offset': 1, 'y_offset': 0})
        row=16
        writeHeader('Regions / Risks','Critical','High','Medium','Low','Minor','Total')
        startRow=row
        rgnProblems=riskInit.copy()
        grandTotalProblems=0
        for rgn in sorted(rgnDict.keys()):
            totalProblems=0
            for k in rgnDict[rgn].keys():
                rgnProblems[k]+=rgnDict[rgn][k]
                totalProblems+=rgnDict[rgn][k]
            writeRow([rgn,rgnDict[rgn]['Critical'],rgnDict[rgn]['High'],rgnDict[rgn]['Medium'],rgnDict[rgn]['Low'],rgnDict[rgn]['Minor'],totalProblems])
            grandTotalProblems+=totalProblems
        writeRow(['Total Problems Identified',rgnProblems['Critical'],rgnProblems['High'],rgnProblems['Medium'],rgnProblems['Low'],rgnProblems['Minor'],grandTotalProblems],style=boldStyle_max15Cells)
        prblmsChart = workbook.add_chart({'type': 'bar', 'subtype': 'stacked'})
        categories=[tabName,startRow,0,row-2,0]
        prblmsChart.add_series({'name':'Critical','categories': categories, 'values': [tabName,startRow,1,row-2,1]})
        prblmsChart.add_series({'name':'High',    'categories': categories, 'values': [tabName,startRow,2,row-2,2]})
        prblmsChart.add_series({'name':'Medium',  'categories': categories, 'values': [tabName,startRow,3,row-2,3]})
        prblmsChart.add_series({'name':'Low',     'categories': categories, 'values': [tabName,startRow,4,row-2,4]})
        prblmsChart.add_series({'name':'Minor',   'categories': categories, 'values': [tabName,startRow,5,row-2,5]})
        prblmsChart.set_title({'name': 'Regions Affected'})
        prblmsChart.set_style(10)
        prblmsChart.set_x_axis({'major_gridlines': {'visible': False}})
        prblmsChart.set_legend({'position': 'bottom'})
        prblmsChart.set_chartarea({'border': {'none': True}})
        ws.insert_chart('H14', prblmsChart, {'x_offset': 1, 'y_offset': 0})
        ws.set_zoom(80)
        service="Recommendations"
        addTab('CG '+service, colWidths=[14,20,18,20,12,10,35,25,18,18], tabColor='#F08080')
        addHeading2(tabName + ' ' + service)
        writeHeader('Tenancy','Compartment','State','Type','Risk','Count','Name','Details','Created On','Updated On')
        for t in the.cloudGuard[service].keys():
            for c in the.cloudGuard[service][t].keys():
                for rc in the.cloudGuard[service][t][c]: writeRow([t,c, rc[0],rc[1],rc[2],rc[3],rc[4],rc[5],rc[6],rc[7]], getStyle(risk=rc[2]))
        finalTouchTable()

    if the.getSelection('audits', 'cloudAdvisor'):
        tabName="CloudAdvisor"
        cAws = addTab(tabName, colWidths=[11,7,14,14,14,14,22], tabColor='#F08080', header=False)
        riskInit={'Critical':[0,0,0,0,0],'High':[0,0,0,0,0],'Medium':[0,0,0,0,0],'Low':[0,0,0,0,0],'Minor':[0,0,0,0,0]}
        riskDict = riskInit.copy()
        addTab("CA Recommendations", colWidths=[14,32,18,9,14,14,14,14,14,17,17,17,17], tabColor='#F08080')
        addHeading2(tabName + " Recommendations")
        writeHeader('Tenancy','Name','Estimated Savings','State','Importance','Pending','Dismissed','Postponed','Implemented','Created','Updated','State Start', 'State End')
        for t in the.cloudAdvisor.keys():
                for rc in the.cloudAdvisor[t]:
                    imp=rc[3]
                    writeRow([t,rc[0],rc[1],rc[2],imp,rc[4],rc[5],rc[6],rc[7],rc[8],rc[9],rc[10],rc[11]], getStyle(risk=imp))
                    riskDict[imp][0]+=1
                    riskDict[imp][1]+=rc[4]
                    riskDict[imp][2]+=rc[5]
                    riskDict[imp][3]+=rc[6]
                    riskDict[imp][4]+=rc[7]
        finalTouchTable()
        row=15; ws=cAws
        writeHeader('Importance', 'Entries', 'Pending #','Dismissed #','Postponed #','Implemented #','Total Recommendations')
        startRow=row
        totals=[0,0,0,0,0,0]
        for i in riskDict.keys():
            rd=riskDict[i]
            totRc=0
            for j in range(1,5): totRc+=rd[j]
            writeRow([i] + rd + [totRc])
            for j in range(5):
                totals[j]+=rd[j]
            totals[5]+=totRc
        writeRow(['Totals'] + totals, style=boldStyle_max15Cells)
        prblmsChart = workbook.add_chart({'type': 'doughnut'})
        prblmsChart.add_series({
            'name': 'CloudAdvisor Recommendations',
            'categories': [tabName,startRow,0,row-2,0],
            'values':     [tabName,startRow,1,row-2,1],
            'data_labels': {'percentage':True, 'value':True},
        })
        prblmsChart.set_title({'name': 'CloudAdvisor Recommendations'})
        prblmsChart.set_style(10)
        prblmsChart.set_chartarea({'border': {'none': True}})
        ws.insert_chart('A1', prblmsChart, {'x_offset': 1, 'y_offset': 0})
    
    if the.getSelection('audits', 'usage'): #Todo pending # Not working for Oracle internal tenancies
        addTab('UsagesCosts', colWidths=[14,30,15,20,40])
        writeHeader('Tenancy','Unit','Quantity','Amount','Usage Time')
        ws.freeze_panes(row,0)
        data=[]
        for t in sortedTenancies:
            for k in sorted(the.usages[t].keys()):
                usg = the.usages[t][k]
                data.append([t,usg[0],usg[1],usg[2],usg[3]])
        # custom sort logic on data
        for x in sorted(sorted(data, key=lambda l:l[4]), key=lambda l:l[1]): writeRow(data=x)
        finalTouchTable()
        ws.write(row,0, 'Usage dates betweeen [UTC format]:',format['bold_underlined'])
        row+=1
        ws.write(row,0, str(the.usageDates['start']), format['italic'])
        ws.write(row,2, str(the.usageDates['end']), format['italic'])
        addCountSummary(row+2, the.usages)

    # if len(workbook.worksheets())>0: # If no worksheet created, then excel file will not be saved
    workbook.close()
    reportsString='Audit Report placed at "' + reportPath + '"'
    the.setInfo('Job Completed.\n' + reportsString)
    the.setGauge(99)
    the.increamentGauge(1)
    
    if not ui: # Commandline Mode
        if the.sendMail:
            sendMail=False
            if 'sendmail_onlyif_audit_issues' not in conf.keys: sendMail=True # Default, send mail even if audit issues not found
            elif auditIssuesFound: sendMail=True # send mail only if audit issues found
            if sendMail:
                the.setInfo('Sending generated report via email..')
                import mail
                mail.init(conf, the)
                mail.sendMail(attachmentDir=reportDirPath, attachmentName=reportName, tenancies=sortedTenancies)
            else:
                the.setWarn("E-mail not sent!!, as no audit issues found. If you still wish to get email, disable config tag 'sendmail_onlyif_audit_issues'")
        sleep(5)
        os._exit(0)
    else: # Normal GUI mode
        wx=ui.wx
        dlg=wx.MessageDialog(ui.parentWindow, "Job Completed.\n\n" + reportsString, 'Done', wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_INFORMATION)
        dlg.SetYesNoCancelLabels("&OK", "Open &Report", "&Close")
        ans=dlg.ShowModal()
        if ans==wx.ID_NO:
            os.startfile('"' + reportPath + '"')
            os._exit(0)
        elif ans==wx.ID_CANCEL:
            os._exit(0)

def generateHeaderList(*headers):
    global data,head
    data=[]
    head=[]
    for h in headers:
        f={'header': h,'header_format':format['tbl_head'],'format':format['tblCell']} #format['font_10']
        if 'OCID' in h or '~' in h: f['format']=format['tblCell_f6']
        head.append(f)
    #print('Debug| Service1: ' + service)
    #print(head)
def writeHeader(*headers, colStart=0):
    global row,startRow,cols
    startRow=row
    i=colStart
    for h in headers:
        ws.write(row,i,h,format['tbl_head'])
        i+=1
    cols=i
    row+=1
boldStyle_max15Cells=['tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold','tblCell_bold']
normalStyle_max20Cells=['tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell','tblCell',]
def getStyle(risk='', f6=[], f8=[]):
    rs = '_'+risk.lower()[0:3] if risk else '' # first three characters of, risk string
    norm = 'tblCell'+rs
    norm6 = norm+'_f6'; norm8 = norm+'_f8'
    style=[]
    for i in range(0,cols): style.append(norm6 if i in f6 else norm8 if i in f8 else norm)
    return style
def writeRow(data=[], style=normalStyle_max20Cells, colStart=0):
    global row
    col=colStart
    for d in data:
        ws.write(row,col, d, format[style[col]])
        col+=1
    row+=1
def finalTouchTable():
    global row
    ws.autofilter(startRow, 0, row-1, cols-1)
    if row==startRow+1: ws.write(row,0,'No data found !',format['normal']) # means no data, row still at first line
    row+=1
def addTab(name, tabColor='#FFFFFF', colWidths=[],header=True):
    global ws,row
    row=0
    ws = workbook.add_worksheet(name)
    ws.hide_gridlines(2)
    if not header: ws.hide_row_col_headers()
    ws.set_tab_color(tabColor)
    i=0
    for cw in colWidths:
        ws.set_column(i,i,cw)
        i+=1
    return ws
def addTable():
    global startRow,row,data,head,service
    dataLen = len(data)
    if dataLen>0:
        startRow=row
        endRow = startRow + dataLen
        endCol = len(data[0]) - 1
        name=re.sub(r"[\s\'\(\)]", '', service)
        ws.add_table(startRow, 0, endRow, endCol, {'data':data, 'columns':head, 'banded_rows':False, 'name':name, 'style':'Table Style Medium 15'})
        row=endRow
    else:
        ws.write(row,0, 'No data found !', format['normal'])
    row+=1
def addHeading2(heading, hx='h2'):
    global row
    ws.merge_range(row,0,row,3,heading,format[hx])
    row+=1
def addAllFormatsToWorkbook():
    f={
        'normal' : {},
        'bold' : {'bold':True},
        'bold_underlined' : {'bold':True, 'underline':True},
        'bold_italic' : {'bold':True, 'italic':True},
        'italic_underlined' : {'underline':True, 'italic':True},
        'font_10' : {'font_size':10},
        'normal_small' : {'font_size':8},
        'italic' : {'italic':True},
        'italic_left' : {'italic':True, 'align':'left'},
        'italic_downBorder' : {'italic':True, 'bottom':1},
        'italicBold_downBorder' : {'bold':True, 'italic':True, 'bottom':1},
        'center' : {'align':'center'},
        'bold_fntRed' : {'bold':True, 'font_size':11, 'font_color':'red'},
        'fntPaleRed'  : {'font_size':10, 'font_color':'#FF3300'},
        'fntRed'      : {'font_size':10, 'font_color':'red'},
        'tbl_head'  : {'bold':True, 'bg_color':'#BDD7EE', 'font_color':'#000000', 'border':1, 'align':'left'},
        'tblCell'    :                       {'border':1, 'align':'left', 'valign':'vcenter'},
        'tblCell_cri': {'bg_color':'#FF5229', 'border':1, 'align':'left', 'valign':'vcenter'},
        'tblCell_hig': {'bg_color':'#F08080', 'border':1, 'align':'left', 'valign':'vcenter'},
        'tblCell_med': {'bg_color':'#ffff60', 'border':1, 'align':'left', 'valign':'vcenter'},
        'tblCell_low': {'bg_color':'#a0ec6e', 'border':1, 'align':'left', 'valign':'vcenter'},
        'tblCell_min': {'bg_color':'#e5fad6', 'border':1, 'align':'left', 'valign':'vcenter'},
        'tblCell_yl_rd' : {'bg_color':'#FFFF00', 'font_color':'#FF0000', 'bold':True, 'border':1, 'align':'left'},
        'tblCell_rd' : {'font_color':'#FF0000', 'bold':True, 'border':1, 'align':'left'},
        'tblCell_br' : {'font_color':'#8B2500', 'bold':True, 'border':1, 'align':'left'},
        'tblCell_bold' : {'bold':True, 'border':1, 'align':'left'},
        'tblCell_bold1' : {'bold':True, 'border':1},
        'h1' : {'font_size':14, 'font_color':'#1f497d', 'font_name':'Cambria'},
        'h2' : {'font_size':15, 'bold':True, 'font_color':'#1f497d', 'bottom':2, 'bottom_color':'#1f497d'},
        'h3' : {'font_size':13, 'bold':True, 'font_color':'#000000', 'bottom':2, 'bottom_color':'#1f497d'},
    }
    def addSmaller(siz):
        for n in ['tblCell','tblCell_cri','tblCell_hig','tblCell_med','tblCell_low','tblCell_min']:
            n1=n+'_f'+str(siz)
            f[n1]={**f[n], 'font_size':siz}
            f[n+'_wrap'] ={**f[n],  'text_wrap':1} # add also wraps
            f[n1+'_wrap']={**f[n1], 'text_wrap':1}
    addSmaller(8)
    addSmaller(6)
    format={}
    for n in f.keys(): format[n]=workbook.add_format(f[n])
    return format
def getLnk(a,b):
    # as of now a=service, b=ocid, and its value will be linked details
    # return linked details if available, else return just an hyphen (-) symbol
    return lnk[a].get(b, '-')
#