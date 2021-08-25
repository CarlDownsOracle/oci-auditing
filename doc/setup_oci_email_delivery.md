# Setting up OCI "Email Delivery" Service

## Admin Actions
Add a policy for user to manage approved senders  
`Allow group <group-name> to manage email-family in compartment <compartment-name>`

_<u>Note:</u>_  
_* if admin itself managing Email Delivery Service, then skip this policy, and directly perform below stated User Actions._  
_* if user need to manage suppression list also, then give same permission on tenancy, instead on compartment._  


&nbsp;

## User Actions
* Login to OCI Tenancy web console, and goto 
    > User Settings > Resources > SMTP Credentials > Generate SMTP Credentials  
    Write down `Username` and `Password`
* then goto
    > Main Menu > Developer Services > Application Integration > Email Delivery > Configuration
* In Configuration,  
    Write down `PublicEndpoint`, this should be used as SMTP Host.  
    _SMTP Ports will be same 25, 587_  
    _And TLS security is required as per industry standards_
* Switch to "Approved Senders"  
    Create an approved sender here by adding an `FROM email address` through which you want to send email  
    _email IDs added here only can be used to send email_

&nbsp;

That's it, you have all the values now to configure email delivery in "OCI Audit Tool", using "OCI's Email Delivery service".
```ini
smtp_tls_port=587
smtp_tls_username = <Username>
smtp_tls_password = <Password>
smtp_tls_host = <PublicEndpoint>
smtp_tls_from = <email added as approved sender>
smtp_tls_to = <"TO" email/s, multiple emails to be seperated with comma(,)>
```

&nbsp;

<u>Reference:</u>  
[Getting Started with Email Delivery](https://docs.oracle.com/en-us/iaas/Content/Email/Reference/gettingstarted.htm)