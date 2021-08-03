# <a name="cli"></a>Command-line options
CLI can be used for schedulers/automations.

    COMMANDLINE USAGE:

    Arg 1    [*Mandatory argument]
        Tenancy Names, each separated by a space, and enclosed by quotes
            ex: "tenancy1"
                "tenancy1 tenancy2 tenancy3"

    Arg 2    [*Mandatory argument]
        Use one or more of these below options separated by space, and enclosed by quotes
            ex: "usersAndGroups limits"
                "networks"
                "limits policies networks"

        Types of analysis:
        ------------------
        compartments  = list & analyse Compartments, audits naming formats
        usersAndGroups= list & analyse Users and Groups, audits naming formats
        limits        = list & analyse Service Limits, warnings on near to limits
        policies      = list & analyse Policies, audits for mandatory policies, missing, additional policies
        instances     = lists instances created for all the OCI services supported
        events        = list & analyse Audit Events from last run, alerts for all create/modify/terminate
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
   * all configurations to be done in file "configurations\tool.ini"
   * applicable for both Windows and Linux platforms.
   * All alerts are normally highlighted with suitable background colors.
   * selected analysis will always list all respective OCI components in to the report, plus auditing, unless if some components are avoided by user configurations.

&nbsp;

[![](https://img.shields.io/badge/go%20to-Index-white?style=for-the-badge&logo=ardour&logoColor=white)](../README.md#toc)
