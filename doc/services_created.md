# List of services

These OCI services are supported: 
* Compute Instances
* Custom Images
* Boot Volume, and Backups
* Block Volume, and Backups
* Volume Group, and Backups
* Dedicated VM Host
* Cluster Network
* Instance Pool
* File System, Mount Target
* Analytics Instance
* Integration Instance
* Load Balancer
* Health Check: HTTP, and Ping
* DB Systems
* Autonomous Databases
* Autonomous Container Databases
* Autonomous Exadata Infrastructure
* Exadata Infrastructure
* VM Cluster
* NoSQL Table
* MySQL DB System
* Load Balancer
* Data Science

_You can [submit request](https://github.com/KsiriCreations/oci-auditing/issues/new) for additional services to get added in to the Tool_

&nbsp;
&nbsp;

# Configurations

```ini
# Get attached VNICs details also, for Compute instances
show_compute_vnics=VNIC_OCID/HOSTNAME/PRIVATE_IP/PUBLIC_IP
# if only IPs needed
show_compute_vnics=PRIVATE_IP/PUBLIC_IP
# select parameters whichever required

# Region Specific, Service Not Availability [mentioning this will save process time]
# Format:
# service_notin_region = <Service Name>/<region-names in comma seperated>
service_notin_region= MySQL DB System/ap-seoul-1, me-jeddah-1, ap-chuncheon-1, ca-montreal-1, eu-frankfurt-1, us-phoenix-1, uk-london-1, ap-tokyo-1, ap-sydney-1, ap-osaka-1, ap-melbourne-1, eu-amsterdam-1
service_notin_region= Cluster Network / ca-toronto-1, sa-saopaulo-1, eu-zurich-1, ap-mumbai-1, ap-hyderabad-1, ap-seoul-1, me-jeddah-1, ap-chuncheon-1, ca-montreal-1

# disable_compartments, provide list of compartments which should not be scanned in comma seperated
disable_compartments=C101,C102,CompartmentABC,XYZ
;disable_compartments=Lina_Comp,tenancy05 (root),Network_Comp
```

 _Note: These options can also be used for tool runtime optimizations._

&nbsp;
&nbsp;

# Compute Instances

## Show VNICs details

Along with "Compute Instances" listing, you can also get its VNICs details.

**To enable this, add `show_compute_vnics` to configuration.**

&nbsp;
&nbsp;

Details will be added to extra-field, and shown in this format:

if only one primary VNIC attached, then `vnic-ocid`, `host-name`, `private-ip` and `public-ip` will be seperated by slashes.
```
<vnic-ocid>/<hostname*>/<private-ip>/<public-ip*>
```

_\* `hostname`, may not be their for secondary VNICs and so on ..._

_\* `public-ip`, is optional_

&nbsp;

if multiple VNICs attached, then this set will be seperated by pipe symbol.
```
<Details of Primary VNIC> | <Details of Secondary VNIC> ...
```

<br />

> _NOTE: `show_compute_vnics` configuration tag has replaced previous `show_compute_ips` and is discontinued from v3.6.20_