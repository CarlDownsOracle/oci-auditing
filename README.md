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
  
  
