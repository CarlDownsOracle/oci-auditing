# oci-auditing
Oracle Cloud Infrastructure Auditing Tool
* automated auditing process of analysing different OCI resources.
* Windows GUI to select just what you needed.
* multiple tenancies, schedule, email reports & lot more.

USE GUI MODE TO GET ALL OPTIONS ACCESSIBLE,
command-line mode is with limited options required for schedulers/automations.

    Commandline Usage of "OCI Auditing Tool":

    Arg 1 = Tenancy Names, each separated by a space
            complete list should be as single argument, so use double-quotes to cover the complete list
            *Mandatory argument

    Arg 2 = Type of analysis:
            compartments = list & analyse Compartments, audits naming formats
            users        = list & analyse Users, audits naming formats
            groups       = list & analyse Groups, audits naming formats
            limits       = list & analyse Service Limits, warnings on near to limits
            policies     = list & analyse Policies, audits for mandatory policies, missing policies, additional policies
            instances    = lists instances created for all the OCI services supported
            events       = list & analyse Audit Events, alerts for all create/modify/terminate events
            networks     = list & analyse VCN and all of it's sub-components, audits CIDR, Protocols
                           [planned to include all other network components in next release]
            all          = all these audits
			[select only required audits, to save big run-times. Using optimization options in configurations can save run-times.]
            *Mandatory argument

    Arg 3 : Options available as of now: sendMail
            -Optional argument

Note: 
   * All alerts are normally highlighted with suitable background colors.
   * selected analysis will always list all respective OCI components in to the report, along with auditing, unless if some components are avoided by user configurations.
   
   
GUI options self-explorable, person who manages OCI, can understand UI easily.
Further how to provide tenancies list into configuration, and all other simple steps are explained below:
  

###### Table of further contents

<span>[<span lang="EN-GB">Background</span>](#_Toc52579461)</span>

<span>[<span lang="EN-GB">High-Level Steps</span>](#_Toc52579462)</span>

<span>[<span lang="EN-GB">Prerequisite</span>](#_Toc52579463)</span>

<span>[<span lang="EN-GB">Installation</span>](#_Toc52579464)</span>

<span>[<span lang="EN-GB">Configurations</span>](#_Toc52579465)</span>

<span>[<span lang="EN-GB">Tool Demo</span>](#_Toc52579466)</span>

<span>[<span lang="EN-GB">Report Details</span>](#_Toc52579467)</span>

<span>[<span lang="EN-GB">Email Notifications</span>](#_Toc52579468)</span>

<span>[<span lang="EN-GB">Appendix</span>](#_Toc52579469)</span>

<span>[<span lang="EN-GB">User configurations on OCI</span>](#_Toc52579470)</span>



## <a name="_Toc52579461"></a><a name="_Toc52573351"></a><a name="_Toc32324877"></a><a name="_Toc51353162"></a><a name="_Toc32325023"></a><span lang="EN-GB">Background</span>

<a name="_Toc423096135"></a><a name="_Toc423096130"></a><span lang="EN-GB">With the increasing demand for scale of operations in OCI, visibility in managing the resources is becoming as important. While the Audit service provides the necessary governance, however, managing it manually becomes difficult for large and ever-changing infrastructures.</span>

<span class="e24kjd">"OCI Audit Tool" </span><span class="e24kjd"><span lang="EN-IN">helps us in mitigating the manual work and provide an automated way to govern the infrastructure with minimal effort.</span></span>

## <a name="_Toc52579462"></a><a name="_Toc52573352"></a><a name="_Toc32324878"></a><a name="_Toc51353163"></a><a name="_Toc32325024"></a><span lang="EN-GB">High-Level Steps</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Place OCI Audit Tool in OCI compute or local Windows system.</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Get authentication details: Tenancy OCID, Region, User OCID, API fingerprint.</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Configure the tool to authenticate the required tenancy.</span>

## <a name="_Toc52579463"></a><a name="_Toc52573353"></a><a name="_Toc51353164"></a><a name="_Toc32325026"></a><a name="_Toc32324880"></a>**<span style="font-family:&quot;Calibri&quot;,sans-serif;font-weight:normal" lang="EN-GB">Prerequisite</span>**

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">A Windows system</span> <span style="font-size:9.0pt" lang="EN-GB">(cloud or local)</span> <span lang="EN-GB">to install the tool.</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">An advanced editor installed.</span> <span style="font-size:9.0pt" lang="EN-GB">example: notepad++</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Oracle Cloud Infrastructure account.</span> <span style="font-size:9.0pt" lang="EN-GB">https://www.oracle.com/cloud/sign-in.html</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">An OCI user.</span> <span style="font-size:
9.0pt" lang="EN-GB">A security best practice is to create a new user instead of existing user</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">IAM policy for the user.</span> <span style="font-size:9.0pt" lang="EN-GB">allow group <grp_name> read all-resources in tenancy</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">RSA key pair in</span>**<span style="font-size:10.0pt" lang="EN-GB">PEM format</span>** <span style="font-size:10.0pt" lang="EN-GB"></span> <span lang="EN-GB">to generate API authentication.</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Tenancy OCID, user OCID and fingerprint obtained after adding the public key.</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">SMTP/TLS service details for notifications.</span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

## <a name="_Toc52579464"></a><a name="_Toc51353165"></a><a name="_Toc52573354"><span lang="EN-GB">Installation</span></a>

<span lang="EN-GB">Download the windows executable directly from here [compressed with 7zip format], both stable and recent beta versions will be available.</span>

<span lang="EN-GB"> </span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Download the files "OCI Auditing Tool - vX.X" and "configurations\tool.ini".</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Extract exe to your preferred local folder.</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Move "tool.ini" file inside a subfolder named "configurations".</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Add all configurations and credentials in "tool.ini" (explained in the following section).</span>

<span lang="EN-GB"> </span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
color:#5F5F5F" lang="EN-GB">  
</span>

<span style="font-size:24.0pt;color:#8DA6B1;
letter-spacing:-.05pt" lang="EN-GB"> </span>

## <a name="_Toc52579465"></a><a name="_Toc51353166"></a><a name="_Toc52573355"><span lang="EN-GB">Configurations</span></a>

###### <span lang="EN-GB">Configuring "tool.ini"</span>

<span lang="EN-GB">Get User configurations on all tenancies following as steps in:</span> <span>[<span lang="EN-GB">User configurations on OCI</span>](#_Toc52579470)</span>

<span style="font-family:&quot;Courier New&quot;;color:#FF7700" lang="EN-GB">-</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> _<span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB">Note: All lines starting with Hash or colon [</span> _**<span style="font-size:12.0pt;font-family:&quot;Calibri Light&quot;,sans-serif;color:red" lang="EN-GB">#</span>**_ <span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB"></span>_**<span style="font-size:12.0pt;font-family:&quot;Calibri Light&quot;,sans-serif;
color:red" lang="EN-GB">;</span>**_ <span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB">] are comment lines.</span>_

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB">These comment lines are just for user"s reference.</span>_

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB"> </span>_

![image-mouse-hover-text](./doc/images/image009.jpg)

<span lang="EN-GB"> </span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Copy the private key "</span>oci_api_key.pem" <span lang="EN-GB">under the "configurations" folder created during installation.</span>
    
<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Open the "tool.ini" file in an editor and add the tenancy details.</span>

    tenancy_name= <name of your tenancy>
    tenancy_ocid= <OCID of your tenancy>
    user_ocid = <OCID of the user>
    fingerprint = <fingerprint of the user>
    Region = <any subscribed region identifier>
    key_file = <private key local path>


<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">For multiple tenancies, add multiple sets of entries as below.</span>

<span lang="EN-GB"> </span>

![](./doc/images/image010.png)

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
color:#5F5F5F" lang="EN-GB">  
</span>

<span style="font-size:24.0pt;color:#8DA6B1;
letter-spacing:-.05pt" lang="EN-GB"> </span>

## <a name="_Toc52579466"></a><a name="_Toc51353167"></a><a name="_Toc52573356"><span lang="EN-GB">Tool Demo</span></a>

<span lang="EN-GB">Once the configuration is complete, open "OCI_Auditing_Tool.exe" to launch the tool.</span>

<span lang="EN-GB">The interface would look like this "</span>

<span lang="EN-GB"> </span>

![](./doc/images/image011.jpg)

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB">To test the connectivity, select required tenancies, click on "Options > Connection Check"</span>

![](./doc/images/image012.jpg)

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

To gather audit details:

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Select the tenancy/s on left.

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Select the type of audits required on right.

**<span style="font-family:Symbol;color:#FF7700;font-weight:normal">*</span>****<span style="font-size:7.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:#FF7700;
font-weight:normal"></span> **Click on the green arrow button at the bottom.**<span style="font-size:10.5pt;
font-family:&quot;Segoe UI&quot;,sans-serif;color:black;background:white"></span>**

This will fetch the <span lang="EN-GB">required information from OCI</span> and generate an audit report in .xlsx format.

 ![](./doc/images/image013.jpg)

<span lang="EN-GB"> </span>

<span style="font-family:&quot;Courier New&quot;;color:#FF7700" lang="EN-GB">-</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">The audit report along with an execution log will be stored in "results" folder.</span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
color:#5F5F5F" lang="EN-GB">  
</span>

<span lang="EN-GB"> </span>

## <a name="_Toc52579467"></a><a name="_Toc51353168"></a><a name="_Toc52573357"><span lang="EN-GB">Report Details</span></a>

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> All audit data will be consolidated to one report.

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Data will be spread across multiple tabs with respect to type of audit.

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Report will be named along with generated time-stamp, for future differentiation between multiple reports.

The Audit Report tabs are outlined below.

<span lang="EN-GB"> </span>

###### <u><span lang="EN-GB">Tenancies</span></u>

<span lang="EN-GB"> </span>

<span lang="EN-GB">Report generation timestamp is displayed on top.</span>

<span lang="EN-GB"> </span>

<span lang="EN-GB">Shows basic details of tenancies like name, OCID, home-region, subscribed-regions and all Availability Domains.</span>

![](./doc/images/image014.jpg)

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<u><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
color:#5F5F5F" lang="EN-GB">  
</span></u>

**<span style="color:windowtext" lang="EN-GB"> </span>**

###### <u><span lang="EN-GB">Users</span></u>

<span lang="EN-GB"> </span>

<span lang="EN-GB">Shows all user details fetched from selected tenancies.</span>

![](./doc/images/image015.jpg)

<span lang="EN-GB"> </span>

**<u><span lang="EN-GB">Optional configurations:</span></u>**

**![](./doc/images/image016.png)**

**<span lang="EN-GB"> </span>**

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span style="font-family:&quot;Courier New&quot;">allowed_username_pattern</span> : allowed username pattern based on your preferences

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span style="font-family:&quot;Courier New&quot;">allowed_named_user</span> : <span lang="EN-GB">any exceptional usernames, which does not follow pattern</span>

###### <u>Groups</u>

Shows all group details fetched from selected tenancies.

![](./doc/images/image017.jpg)

**<u><span lang="EN-GB">Optional configurations:</span></u>**

![](./doc/images/image018.png)

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span style="font-family:&quot;Courier New&quot;">allowed_groupname_pattern</span> : allowed group-name pattern

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span style="font-family:&quot;Courier New&quot;">allowed_named_group</span> : <span lang="EN-GB">any exceptional group names, which does not follow pattern</span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:#5F5F5F">  
</span>

**<span style="color:windowtext"> </span>**

###### <u>Compartments</u>

Shows all compartments, sub-compartments up to any level.

![](./doc/images/image019.jpg)

**<u><span lang="EN-GB">Optional configurations:</span></u>**

![](./doc/images/image020.png)

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span style="font-family:&quot;Courier New&quot;">allowed_compname_pattern</span> : allowed compartment name pattern based on your preferences

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:#5F5F5F">  
</span>

###### <u>Service Limits</u>

Shows all service-limits, scanning through all available services, and diving deep through all scopes and limits.

also, shows limit usage and availability if required.

![](./doc/images/image021.jpg)

**<u><span lang="EN-GB">Optional configurations:</span></u>**

![](./doc/images/image022.png)

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span style="font-family:&quot;Courier New&quot;">limits_alert_value</span> : threshold for Service limit alerts

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span style="font-family:&quot;Courier New&quot;">limits_show_used_and_available</span> : show services used and available also

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span style="font-family:&quot;Courier New&quot;">limits_skip_services</span> : bypass these services

Marks row,

*   red, if usage is above the limit
*   yellow, if usage is above alert value

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:#5F5F5F">  
</span>

**<span style="color:windowtext"> </span>**

###### <u>Policies</u>

Shows all policies present in each compartment.

Scans through every policy and all of its statements, and shows as policy statement per row format.

![](./doc/images/image023.jpg)

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:#5F5F5F">  
</span>

###### <u>Services Created</u>

<span lang="EN-GB">Shows all services created by users, scanning in to every regions, availability domains and, compartments.</span>

<span lang="EN-GB"> </span>

<span lang="EN-GB">These OCI services are supported: </span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Compute</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Boot Volume, and Backups</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Block Volume, and Backups</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Volume Group, and Backups</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Dedicated VM Host</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Cluster Network</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Instance Pool</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">File System, Mount Target</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Analytics Instance</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Integration Instance</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Load Balancer</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Health Check: HTTP, and Ping</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">DB Systems</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Autonomous Databases</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Autonomous Container Databases</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Autonomous Exadata Infrastructure</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Exadata Infrastructure</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">VM Cluster</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">NoSQL Table</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">MySQL DB System</span>

<span style="font-family:&quot;Courier New&quot;;color:#FF7700" lang="EN-GB">-</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> _<span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB">You can send request for additional services to get added in to the Tool</span>_

![](./doc/images/image024.jpg)

**<u><span lang="EN-GB">Optional configurations:</span></u>**

![](./doc/images/image025.png)

<span style="font-family:&quot;Courier New&quot;;color:#FF7700" lang="EN-GB">-</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> _<span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB">These options are for tool runtime optimization only.</span>_

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
color:#5F5F5F" lang="EN-GB">  
</span>

<span lang="EN-GB"> </span>

###### <u><span style="font-size:10.5pt;line-height:115%;font-family:&quot;Segoe UI&quot;,sans-serif; color:#172B4D">Events</span></u>

Shows all OCI Audit Events like creating or updating instances, listing security lists, route tables, etc.

![](./doc/images/image026.jpg)

Marks row,

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Red upon creating or deleting a resource.

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Yellow upon updating a resource.

OCI Audit Events can be collected for these date ranges:

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Past 1 hour

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Past 1 day

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Past 1 month

<span style="font-family:
Symbol;color:#FF7700">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> All events from last run

<span style="font-family:&quot;Courier New&quot;;color:#FF7700" lang="EN-GB">-</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> _<span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB">These options are available on tool GUI</span>_

###### <u><span style="font-size:10.5pt;line-height:115%;font-family:&quot;Segoe UI&quot;,sans-serif; color:#172B4D">Networking</span></u>

<u>Virtual Cloud Network</u>: Shows VCN details such as VCN name, OCID, CIDR, etc.

![](./doc/images/image027.jpg)

<u>Route Table</u>: Shows Route Tables available along with the implemented route rules.

![](./doc/images/image028.jpg)

![](./doc/images/image029.jpg)

<u>Subnet</u>: Shows a list of all the subnets configured.

![](./doc/images/image030.jpg)

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:#5F5F5F">  
</span>

<u>Security List:</u>

![](./doc/images/image031.jpg)

![](./doc/images/image032.jpg)

<u>Network Security Groups:</u>

![](./doc/images/image033.jpg)

![](./doc/images/image034.jpg)

<span style="font-family:&quot;Courier New&quot;;
color:#FF7700">-</span><span style="font-size:7.0pt;line-height:150%;
font-family:&quot;Times New Roman&quot;,serif;color:#FF7700"></span> Rows are color coded as below:

![](./doc/images/image035.png)

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;color:#5F5F5F">  
</span>

## <a name="_Toc52579468"></a><a name="_Toc51353169"></a><a name="_Toc52573358"><span lang="EN-GB">Email Notifications</span></a>

<span lang="EN-GB">If you are scheduling this tool for daily or weekly reports, then, email notification feature can send the report right to your inbox.</span>

<span lang="EN-GB"> </span>

**<u><span lang="EN-GB">Configurations for Email Notifications</span></u>**

<span lang="EN-GB"> </span>

![](./doc/images/image036.png)

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

## <a name="_Toc52579469"></a><a name="_Toc52573359"><span lang="EN-GB">Appendix</span></a>

## <a name="_Toc52579470"></a><a name="_Toc52573360"><span style="font-size:19.0pt" lang="EN-GB">User configurations on OCI</span></a>

<span lang="EN-GB">The details below would be required for the configuration</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">RSA key pair in PEM format</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Tenancy name</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Tenancy OCID</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">User OCID</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">API fingerprint of the user</span>

<span lang="EN-GB">Login to your OCI console and click on the Profile button > Tenancy.</span>

<span lang="EN-GB"> </span>

![](./doc/images/image003.jpg)

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span lang="EN-GB">On the Tenancy Details page, find the OCID and click on "Show" to view the complete OCID or click on "Copy" to copy it into clipboard and paste on a notepad.</span>

<span lang="EN-GB"> </span>

![](./doc/images/image004.jpg)

<span lang="EN-GB">In the OCI console, click on the Profile button > Username.</span>

<span lang="EN-GB"> </span>

![](./doc/images/image005.jpg)

<span lang="EN-GB"> </span>

<span lang="EN-GB">On the User Details page, find the user OCID and click on "Show" to view the complete OCID or click on "Copy" to copy it into clipboard and paste on a notepad.</span>

<span lang="EN-GB"> </span>

![](./doc/images/image006.jpg)

<span lang="EN-GB"> </span>

<span lang="EN-GB"> </span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Upload the public key "</span>oci_api_key_public.pem" generated.

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">................................................................................</span> [How to generate: <span>[<span lang="EN-GB">RSA key pair generation</span>](#_Toc52573361)]</span>
................................................................................ [How to generate: [RSA key pair generation](#./doc/rsa_key_pair_generation.md)]

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;line-height:150%;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">On the User Details page, scroll down to Resources and click on API Keys > Add Public Key.</span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;line-height:150%;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">Select or drop the public key and hit "Add".</span>

<span lang="EN-GB"> </span>

![](./doc/images/image007.jpg)

<span lang="EN-GB"> </span>

<span style="font-family:Symbol;color:#FF7700" lang="EN-GB">*</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#FF7700" lang="EN-GB"></span> <span lang="EN-GB">A fingerprint will be generated. Copy this fingerprint and keep handy on a notepad.</span>

<span lang="EN-GB"> </span>

![](./doc/images/image008.jpg)

<span lang="EN-GB"> </span>

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB">Note: In similar way, get details of all other tenancies in scope for audit.</span>_

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB"> </span>_

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif" lang="EN-GB"> </span>_



