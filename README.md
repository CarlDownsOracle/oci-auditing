# oci-auditing
Oracle Cloud Infrastructure Auditing Tool: analysis of different OCI resources. Windows GUI to select just what you needed. multiple tenancies, schedule, email reports.

USE GUI MODE TO GET ALL OPTIONS ACCESSIBLE, command-line mode is with limited options required for schedulers/automations.

COMMANDLINE USAGE OF "OCI AUDITING TOOL"

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
  Further how to provide tenancies list into configuration, and all other simple steps are explained in:
  
  
<div class="WordSection1">

**Table of Contents**

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Introduction</span><span style="color:#5F5F5F;display:none;mso-hide:
screen;text-decoration:none;text-underline:none"><span style="mso-tab-count:
1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573350)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Background</span><span style="color:#5F5F5F;display:none;mso-hide:screen;
text-decoration:none;text-underline:none"><span style="mso-tab-count:1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573351)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">High-Level Steps</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"><span style="mso-tab-count:1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573352)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Prerequisite</span><span style="color:#5F5F5F;display:none;mso-hide:
screen;text-decoration:none;text-underline:none"><span style="mso-tab-count:
1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573353)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Installation</span><span style="color:#5F5F5F;display:none;mso-hide:
screen;text-decoration:none;text-underline:none"><span style="mso-tab-count:
1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573354)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Configurations</span><span style="color:#5F5F5F;display:none;mso-hide:
screen;text-decoration:none;text-underline:none"><span style="mso-tab-count:
1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573355)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Tool Demo</span><span style="color:#5F5F5F;display:none;mso-hide:screen;
text-decoration:none;text-underline:none"><span style="mso-tab-count:1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573356)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Report Details</span><span style="color:#5F5F5F;display:none;mso-hide:
screen;text-decoration:none;text-underline:none"><span style="mso-tab-count:
1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573357)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Email Notifications</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"><span style="mso-tab-count:1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573358)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Appendix</span><span style="color:#5F5F5F;display:none;mso-hide:screen;
text-decoration:none;text-underline:none"><span style="mso-tab-count:1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573359)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">User configurations on OCI</span><span style="color:#5F5F5F;display:
none;mso-hide:screen;text-decoration:none;text-underline:none"> <span style="mso-tab-count:1 dotted"></span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573360)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">RSA key pair generation</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"><span style="mso-tab-count:1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573361)</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

## <a name="_Toc52573350"></a><a name="_Toc417386207"></a><a name="_Toc51353161"></a><a name="_Toc32325022"></a><a name="_Toc32324876"></a><span style="mso-bookmark:_Toc52573350"><span style="mso-bookmark:_Toc417386207"><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">Introduction</span></span></span><span style="mso-bookmark:_Toc417386207"></span><span style="mso-bookmark:_Toc52573350"></span><span style="mso-fareast-font-family:
&quot;Times New Roman&quot;"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">The purpose of this document is to provide you the steps to configure and use the tool for automated auditing process of Oracle Cloud Infrastructure.</span>

## <a name="_Toc52573351"></a><a name="_Toc32324877"></a><a name="_Toc51353162"></a><a name="_Toc32325023"></a><span style="mso-bookmark:_Toc52573351"><span style="mso-bookmark:_Toc32324877"><span style="mso-fareast-font-family:
&quot;Times New Roman&quot;;mso-ansi-language:EN-GB" lang="EN-GB">Background</span></span></span><span style="mso-bookmark:_Toc32324877"></span><span style="mso-bookmark:_Toc52573351"></span><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

<a name="_Toc423096135"></a><a name="_Toc423096130"></a><span style="mso-bookmark:_Toc423096135"><span style="mso-ansi-language:
EN-GB" lang="EN-GB">With the increasing demand for scale of operations in OCI, visibility in managing the resources is becoming as important. While the Audit service provides the necessary governance, however, managing it manually becomes difficult for large and ever-changing infrastructures.</span></span>

<span class="e24kjd">**<span style="mso-ansi-language:
EN-IN" lang="EN-IN">OCI Audit Tool</span> **</span><span class="e24kjd"><span style="mso-ansi-language:EN-IN" lang="EN-IN">helps us in mitigating the manual work and provide an automated way to govern the infrastructure with minimal effort.</span></span>

## <a name="_Toc52573352"></a><a name="_Toc32324878"></a><a name="_Toc51353163"></a><a name="_Toc32325024"></a><span style="mso-bookmark:_Toc52573352"><span style="mso-bookmark:_Toc32324878"><span style="mso-fareast-font-family:
&quot;Times New Roman&quot;;mso-ansi-language:EN-GB" lang="EN-GB">High-Level Steps</span></span></span><span style="mso-bookmark:_Toc32324878"></span><span style="mso-bookmark:_Toc52573352"></span><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Install OCI Audit Tool in OCI compute or local Windows system.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Get authentication details � Tenancy OCID, Region, User OCID, API fingerprint.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Configure the tool to authenticate the required tenancy.</span>

## <a name="_Toc52573353"></a><a name="_Toc51353164"></a><a name="_Toc32325026"></a><a name="_Toc32324880"></a><span style="mso-bookmark:_Toc52573353"><span style="mso-bookmark:_Toc51353164">**<span style="font-family:
&quot;Calibri&quot;,sans-serif;mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB;font-weight:normal" lang="EN-GB">Prerequisite</span>**</span></span><span style="mso-bookmark:_Toc51353164"></span><span style="mso-bookmark:_Toc52573353"></span><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">A Windows system</span> <span style="font-size:9.0pt;mso-ansi-language:EN-GB" lang="EN-GB">(cloud or local)</span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">to install the tool.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span class="GramE"><span style="mso-ansi-language:EN-GB" lang="EN-GB">An</span></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">advanced editor installed.</span> <span class="GramE"><span style="font-size:9.0pt;mso-ansi-language:EN-GB" lang="EN-GB">example</span></span><span style="font-size:9.0pt;mso-ansi-language:EN-GB" lang="EN-GB">: notepad++</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Oracle Cloud Infrastructure account.</span> <span style="font-size:9.0pt;
mso-ansi-language:EN-GB" lang="EN-GB">https://www.oracle.com/cloud/sign-in.html</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">An OCI user.</span> <span style="font-size:9.0pt;mso-ansi-language:EN-GB" lang="EN-GB">A security best practice is to create a new user instead of existing user</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">IAM policy for the user.</span> <span class="GramE"><span style="font-size:9.0pt;
mso-ansi-language:EN-GB" lang="EN-GB">allow</span></span> <span style="font-size:
9.0pt;mso-ansi-language:EN-GB" lang="EN-GB">group <<span class="SpellE">grp_name</span>> read all-resources in tenancy</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">RSA key pair in</span>**<span style="font-size:10.0pt;mso-ansi-language:EN-GB" lang="EN-GB">PEM format</span>** <span style="font-size:10.0pt;mso-ansi-language:
EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">to generate API authentication.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Tenancy OCID, user OCID and fingerprint obtained after adding the public key.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">SMTP/TLS service details for notifications.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

## <a name="_Toc52573354"></a><a name="_Toc51353165"><span style="mso-bookmark:
_Toc52573354"><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-ansi-language:EN-GB" lang="EN-GB">Installation</span></span></a><span style="mso-bookmark:
_Toc52573354"></span><span style="mso-bookmark:_Toc51353165"></span><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Download link: <<Link>></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Navigate to the link.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Select the recent version.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Download the files �OCI Auditing Tool - <span class="SpellE">vX.X</span>� and �tool.ini�.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Extract exe to your preferred local folder.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Move �tool.ini� file inside a subfolder named �configurations�.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Add all configurations and credentials in �tool.ini� (explained in the following section).</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-GB;
mso-fareast-language:EN-US;mso-bidi-language:AR-SA" lang="EN-GB">  
</span>

<span style="font-size:24.0pt;color:#8DA6B1;
letter-spacing:-.05pt;mso-ansi-language:EN-GB" lang="EN-GB"> </span>

## <a name="_Toc52573355"></a><a name="_Toc51353166"><span style="mso-bookmark:
_Toc52573355"><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-ansi-language:EN-GB" lang="EN-GB">Configurations</span></span></a><span style="mso-bookmark:_Toc52573355"></span><span style="mso-bookmark:_Toc51353166"></span>_<span style="font-family:&quot;Calibri Light&quot;,sans-serif;mso-ansi-language:
EN-GB" lang="EN-GB"> </span>_<span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

###### <span style="mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-ansi-language:EN-GB" lang="EN-GB">Configuring �tool.ini�</span><span style="mso-fareast-font-family:
&quot;Times New Roman&quot;"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Get User configurations on all tenancies following as steps in:</span> <span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:
EN-GB" lang="EN-GB">User configurations on OCI</span><span style="color:#5F5F5F;display:
none;mso-hide:screen;text-decoration:none;text-underline:none"> <span style="mso-tab-count:1"></span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573071)</span></span>

<span style="font-family:&quot;Courier New&quot;;color:#FF7700;
mso-ansi-language:EN-GB" lang="EN-GB">-</span><span style="font-size:7.0pt;
font-family:&quot;Times New Roman&quot;,serif;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> _<span style="font-family:&quot;Calibri Light&quot;,sans-serif;
mso-ansi-language:EN-GB" lang="EN-GB">Note: All lines starting with Hash or colon <span class="GramE">[ **<span style="font-size:12.0pt;color:red;font-style:normal">#</span>**</span>  </span>_**<span style="font-size:12.0pt;font-family:&quot;Calibri Light&quot;,sans-serif;
color:red;mso-ansi-language:EN-GB" lang="EN-GB">;</span>**_ <span style="font-family:&quot;Calibri Light&quot;,sans-serif;mso-ansi-language:EN-GB" lang="EN-GB">] are comment lines.</span>_

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif;mso-ansi-language:
EN-GB" lang="EN-GB">These comment lines are just for user�s reference.</span>_

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif;
mso-ansi-language:EN-GB" lang="EN-GB"> </span>_

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image009.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Copy the private key �</span><span class="SpellE">oci_api_key.pem</span>� <span style="mso-ansi-language:
EN-GB" lang="EN-GB">under the �configurations� folder created during installation.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Open the �tool.ini� file in an editor and add the tenancy details.</span>

<span style="font-size:8.0pt;mso-ansi-language:
EN-GB" lang="EN-GB"> </span>

<span class="SpellE"><span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">tenancy_name</span></span><span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">= <name of your tenancy></span>

<span class="SpellE"><span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">tenancy_ocid</span></span><span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">= <OCID of your tenancy></span>

<span class="SpellE"><span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">user_ocid</span></span><span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">   = <OCID of the user></span>

<span class="GramE"><span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">fingerprint</span></span> <span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">= <fingerprint of the user></span>

<span style="font-family:
&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">Region = <any subscribed region identifier></span>

<span class="SpellE"><span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">key_file</span></span> <span style="font-family:&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">= <private key local path></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span class="GramE"><span style="mso-ansi-language:EN-GB" lang="EN-GB">For</span></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">multiple tenancies, add multiple sets of entries as below.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image010.png)</span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-GB;
mso-fareast-language:EN-US;mso-bidi-language:AR-SA" lang="EN-GB">  
</span>

<span style="font-size:24.0pt;color:#8DA6B1;
letter-spacing:-.05pt;mso-ansi-language:EN-GB" lang="EN-GB"> </span>

## <a name="_Toc52573356"></a><a name="_Toc51353167"><span style="mso-bookmark:
_Toc52573356"><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-ansi-language:EN-GB" lang="EN-GB">Tool Demo</span></span></a><span style="mso-bookmark:
_Toc52573356"></span><span style="mso-bookmark:_Toc51353167"></span><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Once the configuration is complete, open �OCI_Auditing_Tool.exe� to launch the tool.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">The interface would look like this �</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image011.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">To test the connectivity, select required tenancies, click on �Options > Connection Check�</span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image012.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

To gather audit details:

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Select the tenancy/s on left.

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Select the type of audits required on right.

**<span style="font-family:Symbol;mso-bidi-font-family:Calibri;color:#FF7700;
font-weight:normal">�</span>****<span style="font-size:7.0pt;
color:#FF7700;font-weight:normal"></span> **Click on the green arrow button at the bottom.**<span style="font-size:10.5pt;font-family:&quot;Segoe UI&quot;,sans-serif;color:black;
background:white"></span>**

This will fetch the <span style="mso-ansi-language:
EN-GB" lang="EN-GB">required information from OCI</span> and generate an audit report in .<span class="SpellE">xlsx</span> format.

 <span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image013.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="font-family:&quot;Courier New&quot;;color:#FF7700;
mso-ansi-language:EN-GB" lang="EN-GB">-</span><span style="font-size:7.0pt;
font-family:&quot;Times New Roman&quot;,serif;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">The audit report along with an execution log will be stored in �results� folder.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-GB;
mso-fareast-language:EN-US;mso-bidi-language:AR-SA" lang="EN-GB">  
</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

## <a name="_Toc52573357"></a><a name="_Toc51353168"><span style="mso-bookmark:
_Toc52573357"><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-ansi-language:EN-GB" lang="EN-GB">Report Details</span></span></a><span style="mso-bookmark:_Toc52573357"></span><span style="mso-bookmark:_Toc51353168"></span><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="GramE">All</span> audit data will be consolidated to one report.

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Data will be spread across multiple tabs with respect to type of audit.

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Report will be named along with generated time-stamp, for future differentiation between multiple reports.

The Audit Report tabs are outlined below.

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

###### <u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-ansi-language:EN-GB" lang="EN-GB">Tenancies</span></u><span style="mso-fareast-font-family:
&quot;Times New Roman&quot;"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Report generation timestamp is displayed on top.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Shows basic details of tenancies like name, OCID, home-region, subscribed-regions and all Availability Domains.</span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image014.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<u><span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-GB;
mso-fareast-language:EN-US;mso-bidi-language:AR-SA" lang="EN-GB">  
</span></u>

**<span style="color:windowtext;mso-ansi-language:
EN-GB" lang="EN-GB"> </span>**

###### <u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-ansi-language:EN-GB" lang="EN-GB">Users</span></u><span style="mso-fareast-font-family:
&quot;Times New Roman&quot;"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Shows all user details fetched from selected tenancies.</span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image015.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

**<u><span style="mso-ansi-language:EN-GB" lang="EN-GB">Optional configurations:</span></u>**

**<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image016.png)</span>**

**<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>**

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span style="font-family:&quot;Courier New&quot;">allowed_username_<span class="GramE">pattern</span></span></span> <span class="GramE">:</span> allowed username pattern based on your preferences

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span style="font-family:&quot;Courier New&quot;">allowed_named_<span class="GramE">user</span></span></span><span class="GramE"> <span style="font-family:
&quot;Courier New&quot;"></span> :</span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">any exceptional usernames, which does not follow pattern</span>

###### <u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;">Groups</span></u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

Shows all group details fetched from selected tenancies.

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image017.jpg)</span>

**<u><span style="mso-ansi-language:EN-GB" lang="EN-GB">Optional configurations:</span></u>**

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image018.png)</span>

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span style="font-family:&quot;Courier New&quot;">allowed_groupname_<span class="GramE">pattern</span></span></span><span class="GramE"> <span style="font-family:&quot;Courier New&quot;"></span> :</span> allowed group-name pattern

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span style="font-family:&quot;Courier New&quot;">allowed_named_<span class="GramE">group</span></span></span><span class="GramE"> <span style="font-family:
&quot;Courier New&quot;"></span> :</span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">any exceptional group names, which does not follow pattern</span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-US;mso-fareast-language:
EN-US;mso-bidi-language:AR-SA">  
</span>

**<span style="color:windowtext"> </span>**

###### <u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;">Compartments</span></u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

Shows all compartments, sub-compartments up to any level.

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image019.jpg)</span>

**<u><span style="mso-ansi-language:EN-GB" lang="EN-GB">Optional configurations:</span></u>**

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image020.png)</span>

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span style="font-family:&quot;Courier New&quot;">allowed_compname_<span class="GramE">pattern</span></span></span><span class="GramE"> <span style="font-family:&quot;Courier New&quot;"></span> :</span> allowed compartment name pattern based on your preferences

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-US;mso-fareast-language:
EN-US;mso-bidi-language:AR-SA">  
</span>

###### <u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;">Service Limits</span></u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

Shows all service-limits, scanning through all available services, and diving deep through all scopes and limits.

<span class="GramE">also</span>, shows limit usage and availability if required.

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image021.jpg)</span>

**<u><span style="mso-ansi-language:EN-GB" lang="EN-GB">Optional configurations:</span></u>**

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image022.png)</span>

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span style="font-family:&quot;Courier New&quot;">limits_alert_<span class="GramE">value</span></span></span><span class="GramE"> <span style="font-family:
&quot;Courier New&quot;"></span> :</span> threshold for Service limit alerts

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span style="font-family:&quot;Courier New&quot;">limits_show_used_and_<span class="GramE">available</span></span></span><span class="GramE"> <span style="font-family:&quot;Courier New&quot;"></span> :</span> show services used and available also

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span style="font-family:&quot;Courier New&quot;">limits_skip_<span class="GramE">services</span></span></span><span class="GramE"> <span style="font-family:&quot;Courier New&quot;"></span> :</span> bypass these services

Marks row,

*   <span style="mso-fareast-font-family:&quot;Times New Roman&quot;">red, if usage is above the limit</span>
*   <span style="mso-fareast-font-family:&quot;Times New Roman&quot;">yellow, if usage is above alert value</span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-US;mso-fareast-language:
EN-US;mso-bidi-language:AR-SA">  
</span>

**<span style="color:windowtext"> </span>**

###### <u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;">Policies</span></u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

Shows all policies present in each compartment.

Scans through every policy and all of its statements, and shows as policy statement per row format.

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image023.jpg)</span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-US;mso-fareast-language:
EN-US;mso-bidi-language:AR-SA">  
</span>

###### <u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;">Services Created</span></u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Shows all services created by users, scanning in to every regions, availability domains and, compartments.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">These OCI services are supported: </span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Compute</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Boot Volume, and Backups</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Block Volume, and Backups</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Volume Group, and Backups</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Dedicated VM Host</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Cluster Network</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Instance Pool</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">File System, Mount Target</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Analytics Instance</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Integration Instance</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Load Balancer</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Health Check: HTTP, and Ping</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">DB Systems</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Autonomous Databases</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Autonomous Container Databases</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Autonomous <span class="SpellE">Exadata</span> Infrastructure</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span class="SpellE"><span style="mso-ansi-language:EN-GB" lang="EN-GB">Exadata</span></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Infrastructure</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">VM Cluster</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">NoSQL Table</span>

<span style="font-size:10.0pt;font-family:Symbol;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">MySQL DB System</span>

<span style="font-family:&quot;Courier New&quot;;color:#FF7700;
mso-ansi-language:EN-GB" lang="EN-GB">-</span><span style="font-size:7.0pt;
font-family:&quot;Times New Roman&quot;,serif;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> _<span style="font-family:&quot;Calibri Light&quot;,sans-serif;
mso-ansi-language:EN-GB" lang="EN-GB">You can send request for additional services to get added in to the Tool</span>_

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image024.jpg)</span>

**<u><span style="mso-ansi-language:EN-GB" lang="EN-GB">Optional configurations:</span></u>**

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image025.png)</span>

<span style="font-family:&quot;Courier New&quot;;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">-</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> _<span style="font-family:&quot;Calibri Light&quot;,sans-serif;mso-ansi-language:EN-GB" lang="EN-GB">These options are for tool runtime optimization only.</span>_

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-GB;
mso-fareast-language:EN-US;mso-bidi-language:AR-SA" lang="EN-GB">  
</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

###### <u><span style="font-size:10.5pt;line-height:115%;font-family:&quot;Segoe UI&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#172B4D">Events</span></u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

Shows all OCI Audit Events like creating or updating instances, listing security lists, route tables, etc.

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image026.jpg)</span>

Marks row,

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Red upon creating or deleting a resource.

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Yellow upon updating a resource.

OCI Audit Events can be collected for these date ranges:

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Past 1 hour

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Past 1 day

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> Past 1 month

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> All events from last run

<span style="font-family:&quot;Courier New&quot;;color:#FF7700;mso-ansi-language:
EN-GB" lang="EN-GB">-</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> _<span style="font-family:&quot;Calibri Light&quot;,sans-serif;mso-ansi-language:EN-GB" lang="EN-GB">These options are available on tool GUI</span>_

<span style="font-size:10.5pt;font-family:&quot;Segoe UI&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#172B4D;mso-ansi-language:EN-US;mso-fareast-language:
EN-US;mso-bidi-language:AR-SA">  
</span>

**<span style="font-size:10.5pt;font-family:&quot;Segoe UI&quot;,sans-serif;
color:#172B4D"> </span>**

###### <u><span style="font-size:10.5pt;line-height:115%;font-family:&quot;Segoe UI&quot;,sans-serif;
mso-fareast-font-family:&quot;Times New Roman&quot;;color:#172B4D">Networking</span></u><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

<u>Virtual Cloud Network</u>: Shows VCN details such as VCN name, OCID, CIDR, etc.

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image027.jpg)</span>

<u>Route Table</u>: Shows Route Tables available along with the implemented route rules.

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image028.jpg)</span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image029.jpg)</span>

<u>Subnet</u>: Shows a list of all the subnets configured.

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image030.jpg)</span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-US;mso-fareast-language:
EN-US;mso-bidi-language:AR-SA">  
</span>

<u>Security List:</u>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image031.jpg)</span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image032.jpg)</span>

<u>Network Security Groups:</u>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image033.jpg)</span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image034.jpg)</span>

<span style="font-family:&quot;Courier New&quot;;
color:#FF7700">-</span><span style="font-size:7.0pt;line-height:150%;
font-family:&quot;Times New Roman&quot;,serif;color:#FF7700"></span> Rows are color coded as below:

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image035.png)</span>

<span style="font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif;mso-fareast-font-family:
&quot;Times New Roman&quot;;color:#5F5F5F;mso-ansi-language:EN-US;mso-fareast-language:
EN-US;mso-bidi-language:AR-SA">  
</span>

## <a name="_Toc52573358"></a><a name="_Toc51353169"><span style="mso-bookmark:
_Toc52573358"><span style="mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-ansi-language:EN-GB" lang="EN-GB">Email Notifications</span></span></a><span style="mso-bookmark:_Toc52573358"></span><span style="mso-bookmark:_Toc51353169"></span><span style="mso-fareast-font-family:&quot;Times New Roman&quot;"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">If you are scheduling this tool for daily or weekly reports, then, email notification feature can send the report right to your inbox.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

**<u><span style="mso-ansi-language:EN-GB" lang="EN-GB">Configurations for Email Notifications</span></u>**

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image036.png)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

## <a name="_Toc52573359"><span style="mso-fareast-font-family:
&quot;Times New Roman&quot;;mso-ansi-language:EN-GB" lang="EN-GB">Appendix</span></a><span style="mso-bookmark:_Toc52573359"></span><span style="mso-fareast-font-family:
&quot;Times New Roman&quot;"></span>

## <a name="_Toc52573360"><span style="font-size:19.0pt;mso-bidi-font-size:
24.0pt;mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:EN-GB" lang="EN-GB">User configurations on OCI</span></a><span style="mso-bookmark:_Toc52573360"></span><span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">The details below would be required for the configuration</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">RSA key pair in PEM format</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Tenancy name</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Tenancy OCID</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">User OCID</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">API fingerprint of the user</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Login to your OCI console and click on the Profile button > Tenancy.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image003.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">On the Tenancy Details page, find the OCID and click on �Show� to view the complete OCID or click on �Copy� to copy it into clipboard and paste on a notepad.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image004.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">In the OCI console, click on the Profile button > Username.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image005.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">On the User Details page, find the user OCID and click on �Show� to view the complete OCID or click on �Copy� to copy it into clipboard and paste on a notepad.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image006.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Upload the public key �</span><span class="SpellE">oci_api_key_public.pem</span>� generated.

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"><span style="mso-tab-count:1 dotted">................................................................................</span> </span>[How to generate: <span class="MsoHyperlink"><span style="mso-no-proof:yes">[<span style="mso-fareast-font-family:&quot;Times New Roman&quot;;
mso-ansi-language:EN-GB" lang="EN-GB">RSA key pair generation</span><span style="color:#5F5F5F;
display:none;mso-hide:screen;text-decoration:none;text-underline:none"><span style="mso-tab-count:1 dotted">.</span> </span><span style="color:#5F5F5F;display:none;mso-hide:screen;text-decoration:none;
text-underline:none">1</span><span style="color:#5F5F5F;display:none;
mso-hide:screen;text-decoration:none;text-underline:none"></span>](#_Toc52573072)]</span></span><span style="mso-ascii-font-family:Calibri;mso-ascii-theme-font:minor-latin;
mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin;mso-bidi-font-family:
&quot;Times New Roman&quot;;mso-bidi-theme-font:minor-bidi;color:windowtext;mso-no-proof:
yes"></span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;line-height:150%;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">On the User Details page, scroll down to Resources and click on API Keys > Add Public Key.</span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;line-height:150%;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">Select or drop the public key and hit �Add�.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image007.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="font-family:Symbol;color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700;mso-ansi-language:EN-GB" lang="EN-GB"></span> <span class="GramE"><span style="mso-ansi-language:EN-GB" lang="EN-GB">A</span></span> <span style="mso-ansi-language:EN-GB" lang="EN-GB">fingerprint will be generated. Copy this fingerprint and keep handy on a notepad.</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

<span style="mso-no-proof:yes">![](OCI-Auditing-Tool-Document_files/image008.jpg)</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB"> </span>

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif;
mso-ansi-language:EN-GB" lang="EN-GB">Note: In similar way, get details of all other tenancies in scope for audit.</span>_

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif;
mso-ansi-language:EN-GB" lang="EN-GB"></span>_

_<span style="font-family:&quot;Calibri Light&quot;,sans-serif;
mso-ansi-language:EN-GB" lang="EN-GB"></span>_

## <a name="_Toc52573361"><span style="font-size:19.0pt;mso-bidi-font-size:
24.0pt;mso-fareast-font-family:&quot;Times New Roman&quot;;mso-ansi-language:EN-GB" lang="EN-GB">RSA key pair generation</span></a><span style="mso-bookmark:_Toc52573361"></span><span style="mso-ansi-language:EN-GB" lang="EN-GB"></span>

Use any one of these:

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> bash console on Linux

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span class="GramE">git</span></span> bash or <span class="SpellE">cygwin</span> or <span class="SpellE">ubuntu</span> console on Windows-10

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Navigate to home directory, and create </span><span style="font-family:
&quot;Courier New&quot;;mso-ansi-language:EN-GB" lang="EN-GB">.<span class="SpellE">oci</span></span><span style="mso-ansi-language:EN-GB" lang="EN-GB"> directory to store the credentials:</span>

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span class="GramE"><span style="font-family:&quot;Courier New&quot;">mkdir</span></span></span> <span style="font-family:&quot;Courier New&quot;">~/.<span class="SpellE">oci</span></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Generate the private key with no passphrase:</span>

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span class="GramE"><span style="font-family:&quot;Courier New&quot;">openssl</span></span></span> <span style="font-family:&quot;Courier New&quot;"><span class="SpellE">genrsa</span> -out ~/.<span class="SpellE">oci</span>/<span class="SpellE">oci_api_key.pem</span> 2048</span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Ensure that only you can read the private key file:</span>

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span class="GramE"><span style="font-family:&quot;Courier New&quot;">chmod</span></span></span> <span style="font-family:&quot;Courier New&quot;">go-<span class="SpellE">rwx</span> ~/.<span class="SpellE">oci</span>/<span class="SpellE">oci_api_key.pem</span></span>

<span style="mso-ansi-language:EN-GB" lang="EN-GB">Generate the public key:</span>

<span style="font-family:
Symbol;color:#FF7700">�</span><span style="font-size:7.0pt;font-family:&quot;Times New Roman&quot;,serif;
color:#FF7700"></span> <span class="SpellE"><span class="GramE"><span style="font-family:&quot;Courier New&quot;">openssl</span></span></span> <span style="font-family:&quot;Courier New&quot;"><span class="SpellE">rsa</span> -<span class="SpellE">pubout</span> -in ~/.<span class="SpellE">oci</span>/<span class="SpellE">oci_api_key.pem</span> -out ~/.<span class="SpellE">oci</span>/<span class="SpellE">oci_api_key_public.pem</span></span>

</div>
