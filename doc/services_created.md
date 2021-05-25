# Compute Instances

## Show VNICs details

Along with "Compute Instances" listing, you can also get its VNICs details like IPs and hostname.

To enable this, add `show_compute_ips` to configuration.
```ini
# Get attached VNICs details also, for Compute instance [IPs, hostname]
show_compute_ips=x
```

&nbsp;
&nbsp;

Details will be added to extra-field, and shown in this format:

if only one primary VNIC attached, then `host-name`, `private-ip` and `public-ip` will be seperated by slashes.
```
<hostname*>/<private-ip>/<public-ip*>
```

\* `hostname`, may not be their for secondary VNICs and so on ...

\* `public-ip`, is optional

&nbsp;

if multiple VNICs attached, then this set will be seperated by pipe symbol.
```
<hostname>/<private-ip>/<public-ip> | <hostname>/<private-ip>/<public-ip> | <hostname>/<private-ip>/<public-ip> ...
```
