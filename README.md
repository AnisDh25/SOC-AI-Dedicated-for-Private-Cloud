# OpenStack Flamingo on Ubuntu 24.04 with Ansible

This playbook deploys OpenStack 2025.2 "Flamingo" on Ubuntu 24.04.
It follows the Server World series
[OpenStack Flamingo on Ubuntu 24.04](https://www.server-world.info/en/note?os=Ubuntu_24.04&p=openstack_flamingo&f=1)
from start to finish, items (01) to (59).

You can deploy it three ways:
- **All-in-one:** everything on one server, `dlp.tekup.world` (10.0.0.30). This is the default.
- **Multi-node:** 2 controllers, 2 compute nodes and 1 storage node, as in the guide. No redundancy. See [Multi-node deployment](#multi-node-deployment).
- **High availability:** 3 controllers behind a VIP (`openstack.tekup.world`), 2 computes and 1 storage node. See [High availability (HA)](#high-availability-ha).

The guide calls the main host `dlp.srv.world`; here it's `dlp.tekup.world`.

> **Status:** Every YAML file and Jinja template has been syntax-checked, and the main config templates have been rendered with test values.
> The playbook has **not** been run against real servers yet. Expect to fix a few things on the first run.

---

## Contents

1. [What gets installed](#what-gets-installed)
2. [Topology](#topology)
3. [Multi-node deployment](#multi-node-deployment)
4. [High availability (HA)](#high-availability-ha)
5. [Requirements](#requirements)
6. [Quick start](#quick-start)
7. [Secrets and Ansible Vault](#secrets-and-ansible-vault)
8. [Configuration](#configuration)
9. [Running parts of the playbook](#running-parts-of-the-playbook)
10. [After the installation](#after-the-installation)
11. [Checking the deployment](#checking-the-deployment)
12. [Project layout](#project-layout)
13. [Differences from the Server World guide](#differences-from-the-server-world-guide)
14. [Troubleshooting](#troubleshooting)

---

## What gets installed

| Service | What it does | Server World items | Turn it off with |
|---|---|---|---|
| MariaDB, RabbitMQ, Memcached, Nginx | Database, message queue, cache, TLS proxy | 02 | — |
| Keystone | Identity | 03–04 | — |
| Glance | Images (the Ubuntu 24.04 cloud image is uploaded) | 05–06 | — |
| Nova + Placement | Compute | 07–09, 17 | — |
| Neutron ML2/OVN | Networking | 10–12, 23–25 | — |
| Users and flavors | Project `hiroshima`, user `serverworld`, m1/m2 flavors | 13–14 | — |
| Cinder | Block storage: LVM and NFS backends, volume types, NFS backups | 27–32 | `enable_cinder`, `enable_cinder_nfs`, `enable_cinder_backup` |
| Heat | Orchestration | 33–35 | `enable_heat` |
| Barbican | Key manager | 36–37 | `enable_barbican` |
| Swift | Object storage | 38–41 | `enable_swift` |
| Manila | Shared filesystems (LVM driver, NFS) | 42–44 | `enable_manila` |
| Designate | DNS, with BIND 9 as the backend | 45–47 | `enable_designate` |
| Octavia | Load balancer, **OVN provider** only | 48–51 | `enable_octavia` |
| Gnocchi + Ceilometer | Metrics and telemetry | 52–57 | `enable_telemetry` |
| CloudKitty | Rating and billing | 58–59 | `enable_cloudkitty` |
| Horizon | Web dashboard, with Heat, Manila, DNS and LB panels | not in the series | `enable_horizon` |

These parts of the series are **not** automated:
- (16) Windows instances
- (26) GPU compute nodes
- (18)–(22) the Open vSwitch variant of Neutron; OVN is used instead
- The Octavia amphora image, pages (49)–(50)

---

## Topology

Roles run on **inventory groups**, not on fixed hostnames.
Each group matches a node from the guide:

| Group | Node in the guide | What runs there |
|---|---|---|
| `controller` | `dlp` | MariaDB, RabbitMQ, Memcached, Keystone, Glance, Nova API/conductor/scheduler/noVNC, Placement, Cinder API, Barbican, Manila API, Horizon |
| `network` | `network` | neutron-server, OVN NB/SB + northd, gateway chassis, Heat, Designate + BIND 9, Octavia, Gnocchi, Ceilometer central, CloudKitty |
| `compute` | `node01` | nova-compute (KVM), ovn-controller, OVN metadata agent, ceilometer-compute |
| `storage` | `network` | cinder-volume (LVM + NFS), cinder-backup, manila-share |
| `swift_proxy` | `network` | Swift proxy, ring builder |
| `swift_storage` | `snode01-03` | Swift account, container and object servers, rsync |
| `nfs` | `nfs` | NFS exports for the Cinder NFS backend and for backups |

Three inventories are included:

| Inventory | Layout |
|---|---|
| `inventory/hosts.yml` (default, set in `ansible.cfg`) | **All-in-one:** every group holds only `dlp.tekup.world` |
| `inventory/hosts-multinode.yml` | **5 nodes:** 2 controllers, 2 computes, 1 storage. See [Multi-node deployment](#multi-node-deployment) |
| `inventory/hosts-ha.yml` | **HA, 6 nodes:** 3 controllers behind a VIP, 2 computes, 1 storage. See [High availability (HA)](#high-availability-ha) |

Every API is served as follows:

```
client ──HTTPS──▶ nginx (mgmt_ip:<port>, TLS) ──▶ service on 127.0.0.1:<port>
```

Keystone (:5000) and Horizon (:443) are the exception: Apache serves them over TLS itself.

| Port | Service | Port | Service |
|---|---|---|---|
| 5000 | Keystone | 8786 | Manila |
| 9292 | Glance | 8080 | Swift |
| 8774 / 8775 | Nova API / metadata | 9001 | Designate |
| 8778 | Placement | 9876 | Octavia |
| 6080 | noVNC console | 8041 | Gnocchi |
| 9696 | Neutron | 8004 / 8000 | Heat (plain HTTP, as in the guide) |
| 8776 | Cinder | 8889 | CloudKitty (plain HTTP, as in the guide) |
| 9311 / 9312 | Barbican | 443 | Horizon |

Each service is published on the host of the group it belongs to.
For example, in the multi-node layout Neutron answers on `https://network.tekup.world:9696`.

---

## Multi-node deployment

`inventory/hosts-multinode.yml` spreads the cloud over 5 machines, following the guide's multi-node layout.
The second controller plays the guide's **network node**.

| Host | IP | Groups | Runs |
|---|---|---|---|
| `dlp.tekup.world` (ctl1) | 10.0.0.30 | controller | MariaDB, RabbitMQ, Memcached, Keystone, Glance, Nova API/conductor/scheduler/noVNC, Placement, Cinder API, Barbican, Manila API, Horizon |
| `network.tekup.world` (ctl2) | 10.0.0.50 | network, swift_proxy | neutron-server, OVN NB/SB + northd, gateway chassis, DHCP agent, Heat, Designate + BIND 9, Octavia (OVN), Gnocchi, Ceilometer central, CloudKitty, Swift proxy |
| `node01.tekup.world` (cmp1) | 10.0.0.51 | compute | nova-compute, ovn-controller, OVN metadata + DHCP agents, ceilometer-compute |
| `node02.tekup.world` (cmp2) | 10.0.0.52 | compute | same as cmp1 |
| `storage.tekup.world` (stor1) | 10.0.0.60 | storage, nfs, swift_storage | cinder-volume (LVM + NFS), cinder-backup, manila-share, NFS server, Swift storage |

```
                          10.0.0.0/24  management network (eth0)
   ─────┬──────────────┬───────────────┬───────────────┬───────────────┬─────
        │              │               │               │               │
   ┌────┴────┐   ┌─────┴─────┐   ┌─────┴────┐    ┌─────┴────┐    ┌─────┴─────┐
   │  ctl1   │   │   ctl2    │   │   cmp1   │    │   cmp2   │    │   stor1   │
   │  dlp    │   │  network  │   │  node01  │    │  node02  │    │  storage  │
   │  .30    │   │   .50     │   │   .51    │    │   .52    │    │   .60     │
   └─────────┘   └─────┬─────┘   └─────┬────┘    └─────┬────┘    └───────────┘
                       │ eth1          │ eth1          │ eth1
   ────────────────────┴───────────────┴───────────────┴──── provider / external network
```

> **No high availability.** Each service runs on exactly one node.
> - If **ctl1** is down, Keystone and the databases are gone, so the whole cloud stops.
> - If **ctl2** is down, networking APIs, DNS, orchestration, load balancing and telemetry stop.
>
> Running VMs keep running either way.
> For redundancy, use the [HA layout](#high-availability-ha) instead: 3 controllers behind a VIP.

### Hardware per node

| Node | CPU / RAM | NICs | Disks |
|---|---|---|---|
| ctl1 | 4 vCPU / 8 GB+ | eth0 | system disk |
| ctl2 | 4 vCPU / 8 GB+ | eth0 + **eth1 (no IP)** | system disk |
| cmp1, cmp2 | 4+ vCPU / 8 GB+, nested KVM | eth0 + **eth1 (no IP)** | system disk |
| stor1 | 2 vCPU / 4 GB+ | eth0 | system + **`/dev/sdb`** (Cinder) + **`/dev/sdc`** (Manila) + **`/dev/sdd`** (Swift) |

**What every node needs:**
- the same management network
- a fresh Ubuntu 24.04
- SSH access as `ubuntu` with sudo

The `common` role fills in `/etc/hosts` on every node, so the nodes resolve each other.
Your workstation still needs `dlp.tekup.world` and `network.tekup.world` to resolve, for Horizon and the APIs.

### Run it

```bash
ansible-inventory -i inventory/hosts-multinode.yml --graph      # check the groups
ansible -i inventory/hosts-multinode.yml all -m ping --ask-vault-pass
ansible-playbook -i inventory/hosts-multinode.yml site.yml --ask-vault-pass
ansible-playbook -i inventory/hosts-multinode.yml verify.yml --ask-vault-pass
```

Use `-i inventory/hosts-multinode.yml` on **every** command, including tagged runs and `smoke_test`.
Without it, Ansible uses the all-in-one inventory from `ansible.cfg`.
To make multi-node the default, set `inventory = inventory/hosts-multinode.yml` in `ansible.cfg`.

### Changing IPs, hostnames or disks

- Each host has a file `inventory/host_vars/<fqdn>.yml`. Set these there:
  - `ansible_host` and `mgmt_ip`
  - `provider_interface`
  - on the storage node: `cinder_lvm_device`, `manila_lvm_device` and `swift_devices`
- To rename a host, rename its host_vars file and change the name in `inventory/hosts-multinode.yml`. Names must be FQDNs.
- To add a third compute node, add `node03.tekup.world` under `compute` and create its host_vars file.

### Good to know

- **Swift replicas:** with one device on stor1, Swift keeps **1 replica**. For 3 replicas, list 3 devices in `swift_devices` or add more hosts to `swift_storage`.
- **eth1 on the computes:** `compute_is_gateway_chassis: true` (the guide's default) makes the computes gateways too, so their eth1 must be wired to the provider network.
  If you set it to `false`, only ctl2 routes external traffic. The computes still need eth1 in `flat` mode.
- **Volumes:** computes attach LVM volumes from stor1 over iSCSI (`open-iscsi` is installed on them) and NFS volumes over NFS.
- **Live migration** between cmp1 and cmp2 isn't configured, just as in the guide. It needs SSH keys shared between the `nova` users.

---

## High availability (HA)

`inventory/hosts-ha.yml` deploys a **fresh** HA cloud on 6 machines.
Three controllers each run every API and network service, so any one of them can fail without stopping the cloud.

**HA switches on automatically** when the `controller` group has more than one host.
The rules:
- the number of controllers must be odd (3 recommended)
- the `network` and `swift_proxy` groups must contain exactly the controllers

The `common` role checks both rules.

| Host | IP | Groups | Runs |
|---|---|---|---|
| **VIP** `openstack.tekup.world` | **10.0.0.29** | — | Floating address that clients and services use. keepalived moves it |
| `controller01.tekup.world` | 10.0.0.31 | controller, network, swift_proxy | Every API and agent below, HAProxy, keepalived, Galera, RabbitMQ, Memcached, OVN NB/SB, BIND 9 |
| `controller02.tekup.world` | 10.0.0.32 | same | same |
| `controller03.tekup.world` | 10.0.0.33 | same | same |
| `node01` / `node02.tekup.world` | 10.0.0.51 / .52 | compute | nova-compute, ovn-controller, OVN metadata agent, ceilometer-compute |
| `storage.tekup.world` | 10.0.0.60 | storage, nfs, swift_storage | cinder-volume, cinder-backup, manila-share, Swift storage, NFS (Cinder, **Glance images**, **Gnocchi metrics**) |

```
                    clients / services
                           │
                  openstack.tekup.world  10.0.0.29  (VIP, keepalived)
                           │
          ┌────────────────┼────────────────┐
     ┌────┴─────┐     ┌────┴─────┐     ┌────┴─────┐
     │ HAProxy  │     │ HAProxy  │     │ HAProxy  │   TLS on the VIP, health checks
     ├──────────┤     ├──────────┤     ├──────────┤
     │ APIs     │     │ APIs     │     │ APIs     │   Keystone, Nova, Neutron, … on mgmt_ip
     │ Galera   │◀───▶│ Galera   │◀───▶│ Galera   │   MariaDB cluster
     │ RabbitMQ │◀───▶│ RabbitMQ │◀───▶│ RabbitMQ │   cluster, mirrored queues
     │ OVN RAFT │◀───▶│ OVN RAFT │◀───▶│ OVN RAFT │   NB/SB databases
     └──────────┘     └──────────┘     └──────────┘
    controller01      controller02      controller03
```

### How each part is made highly available

| Component | HA mechanism |
|---|---|
| Entry point | **keepalived** (VRRP, unicast) holds the VIP. controller01 is preferred, and the VIP moves if HAProxy dies or the node goes down |
| APIs | **HAProxy** on the VIP: TLS termination and health checks over all 3 controllers. Keystone (:5000) and Horizon (:443) pass TLS through to Apache. noVNC and Horizon are sticky (`balance source`) |
| Database | **Galera** 3-node cluster. HAProxy sends all traffic to one node and keeps the other two as `backup`, which avoids write conflicts |
| Messaging | **RabbitMQ** cluster (shared Erlang cookie) with an `ha-all` mirrored-queue policy. Every service gets all 3 nodes in `transport_url` |
| Cache | One **Memcached** per controller. Every service gets all 3 in `memcached_servers` |
| Keystone tokens | Fernet and credential keys are created on controller01 and copied to the others |
| Networking | **OVN NB/SB RAFT** cluster. `ovn-northd` is active/standby. Every controller and compute is a gateway chassis |
| DNS | BIND 9 on every controller with the same RNDC key. The Designate pool lists all 3 nameservers |
| Images / metrics | Glance images and Gnocchi metrics go on NFS shares from the storage node, owned by fixed UIDs (`glance_uid`, `gnocchi_uid`). Gnocchi and Ceilometer coordinate through MariaDB |
| One-time steps | DB syncs, Keystone bootstrap, Nova cells, pool loading, and creating images, flavors and networks all run on controller01 only |

### Hardware

| Node | CPU / RAM | NICs | Disks |
|---|---|---|---|
| controller01-03 | 4+ vCPU / 12 GB+ each | eth0 + **eth1 (no IP)** | system disk |
| node01, node02 | 4+ vCPU / 8 GB+, nested KVM | eth0 + **eth1 (no IP)** | system disk |
| storage | 2 vCPU / 4 GB+ | eth0 | system + `/dev/sdb` (Cinder) + `/dev/sdc` (Manila) + `/dev/sdd` (Swift) |

**Network requirements:**
- All nodes are on 10.0.0.0/24.
- The VIP address must be **free**.
- VRRP id `vip_router_id` (51) must be unused on that LAN.
- `openstack.tekup.world` must resolve to the VIP from your workstation.

### Run it

```bash
ansible-inventory -i inventory/hosts-ha.yml --graph
ansible-playbook  -i inventory/hosts-ha.yml site.yml --ask-vault-pass
ansible-playbook  -i inventory/hosts-ha.yml verify.yml --ask-vault-pass
```

- **Horizon:** `https://openstack.tekup.world/horizon`
- **APIs:** `https://openstack.tekup.world:<port>`
- **HAProxy stats:** `http://openstack.tekup.world:1936/`

Settings are in `inventory/group_vars/all/main.yml`, under "High availability":

| Variable | Default |
|---|---|
| `vip_address` | `10.0.0.29` |
| `vip_fqdn` | `openstack.tekup.world` |
| `vip_prefix` | `24` |
| `vip_interface` | the default-route NIC |
| `vip_router_id` | `51` |
| `glance_uid`, `gnocchi_uid` | `950`, `951` |

HA also uses extra secrets in `vault.yml`: `vault_rabbit_erlang_cookie`, `vault_keepalived_password` and `vault_db_passwords.tooz`.

### Test a failover

```bash
# on the controller holding the VIP (ip -4 addr show eth0 | grep 10.0.0.29)
sudo systemctl stop haproxy      # the VIP moves to another controller within seconds
openstack token issue            # still works through the VIP
sudo systemctl start haproxy
# or power off a whole controller: Galera, RabbitMQ and OVN keep a 2/3 majority
```

### Limits

- **Fresh deployments only.** There's no in-place migration from the all-in-one or 5-node layouts. Reinstall the servers, then deploy with `hosts-ha.yml`.
- **The storage node isn't redundant.** Cinder volumes, Manila shares, Swift data (1 replica), Glance images and Gnocchi metrics all live on it.
- **After a full outage** (all 3 controllers down), Galera doesn't restart by itself.
  1. On the node with `safe_to_bootstrap: 1` in `/var/lib/mysql/grastate.dat`, run `galera_new_cluster`.
  2. Start `mariadb` on the other two.
- **RabbitMQ mirroring** uses classic mirrored queues (`ha-all` policy). They work on Ubuntu 24.04's RabbitMQ 3.12 but are deprecated; RabbitMQ 4 needs quorum queues instead.
- **Live migration** isn't configured, as in the guide.
- **Not yet run on real servers.** The OVN RAFT bootstrap is the riskiest step, because it relies on how Ubuntu's `ovn-central` reads `OVN_CTL_OPTS`. Check it first with `ovs-appctl -t /var/run/ovn/ovnnb_db.ctl cluster/status OVN_Northbound`.

---

## Requirements

### Target server (all-in-one)

| Item | Requirement |
|---|---|
| OS | Ubuntu 24.04 LTS, freshly installed |
| CPU / RAM | 4+ vCPU, **16 GB+** RAM |
| Virtualization | Nested KVM (`/dev/kvm`). Without it Nova falls back to `virt_type=qemu`, which is slow but works |
| `eth0` | Management network, 10.0.0.30/24, with the default route |
| `eth1` | A second NIC with **no IP address**. It becomes `br-eth1` / `physnet1` for instance traffic |
| `/dev/sdb` | Empty disk for Cinder LVM |
| `/dev/sdc` | Empty disk for Manila LVM |
| Swift | Uses a 10 GB loop file by default, so no disk is needed |
| Access | SSH as `ubuntu` with passwordless sudo, or change `ansible_user` |

`dlp.tekup.world` must resolve to 10.0.0.30 from your workstation, through DNS or your `hosts` file.
You need that to reach Horizon and the APIs.

For multi-node hardware, see [Hardware per node](#hardware-per-node).

### Control machine (where you run Ansible)

- Linux, macOS, or WSL on Windows. **Ansible doesn't run natively on Windows.**
- `ansible-core` 2.15 or newer: `pip install ansible-core`
- Collections: `ansible-galaxy collection install -r requirements.yml`

You don't need `openstacksdk` on the control machine. All OpenStack API calls run on the controller.

> **WSL + OneDrive:** Ansible ignores `ansible.cfg` in world-writable directories, and `/mnt/c/...` is one.
> Copy the project into your WSL home first:
> ```bash
> cp -r "/mnt/c/Users/<you>/OneDrive/Documents/study/project/openstack-ansible" ~/
> cd ~/openstack-ansible
> ```
> Otherwise, run `export ANSIBLE_CONFIG=$PWD/ansible.cfg` first.

---

## Quick start

```bash
# 1. Install the collections
ansible-galaxy collection install -r requirements.yml

# 2. Check the inventory:
#    all-in-one: inventory/hosts.yml + inventory/host_vars/dlp.tekup.world.yml
#    multi-node: inventory/hosts-multinode.yml + all files in inventory/host_vars/

# 3. Encrypt the secrets (see the next section)
ansible-vault encrypt inventory/group_vars/all/vault.yml

# 4. Check connectivity and syntax
ansible all -m ping --ask-vault-pass
ansible-playbook site.yml --syntax-check

# 5. Deploy. The first run takes a long time
ansible-playbook site.yml --ask-vault-pass

# 6. Optional: create the test resources from the guide's "How to use" pages
ansible-playbook site.yml --ask-vault-pass --tags smoke_test -e create_test_resources=true

# 7. Status report
ansible-playbook verify.yml --ask-vault-pass
```

For multi-node, add `-i inventory/hosts-multinode.yml` to steps 4–7.

The playbook is **idempotent**, so running it again is safe. A second run should report few or no changes.

---

## Secrets and Ansible Vault

`inventory/group_vars/all/vault.yml` holds every secret:
- the admin password
- the RabbitMQ password
- all database passwords
- all service-user passwords
- the metadata secret
- the Barbican key-encryption key (KEK)
- the Swift hash prefix and suffix
- the Horizon `SECRET_KEY`
- the demo user passwords

> **Cloned this repository?** `vault.yml` is not in git (it is listed in `.gitignore`).
> Create it from the template, replace every `CHANGE_ME` value, then encrypt it:
> ```bash
> cp inventory/group_vars/all/vault.yml.example inventory/group_vars/all/vault.yml
> ```

Random values were generated when the project was created.
They're alphanumeric because they're embedded in database and RabbitMQ URLs.
Both inventories share the same vault.

> ⚠️ **The file is currently NOT encrypted.** Encrypt it before you commit or share the project.

**On Linux or WSL:**

```bash
ansible-vault encrypt inventory/group_vars/all/vault.yml
ansible-vault view    inventory/group_vars/all/vault.yml
ansible-vault edit    inventory/group_vars/all/vault.yml
```

**On Windows without Ansible:** `scripts/vault_encrypt.py` writes the same `$ANSIBLE_VAULT;1.1;AES256` format as `ansible-vault encrypt`.
It needs Python with the `cryptography` package.
Run it in your own terminal so you can type the password:

```powershell
python scripts\vault_encrypt.py inventory\group_vars\all\vault.yml
```

The script:
- asks for the password twice
- refuses files that are already encrypted
- decrypts its own output before it overwrites the file

Its settings were compared with Ansible's vault source code, but a real `ansible-vault` hasn't decrypted one of its files yet.
The first `--ask-vault-pass` run will confirm it.

If you don't want to type the password each time, keep it in a file readable only by you:

```bash
echo 'your-password' > ~/.ansible/openstack-vault-pass && chmod 600 ~/.ansible/openstack-vault-pass
```

Then uncomment `vault_password_file` in `ansible.cfg`.

> OneDrive keeps version history. A plain-text copy of `vault.yml` may already be stored there.
> After encrypting, delete the old versions, or generate new secrets.

---

## Configuration

Global settings are in `inventory/group_vars/all/main.yml`.
Per-host settings (IP, NIC, disks) go in `inventory/host_vars/<fqdn>.yml`, and those override the global values.
The settings you're most likely to change:

| Variable | Default | Meaning |
|---|---|---|
| `domain` | `tekup.world` | DNS domain, also used for NFSv4 idmapd |
| `timezone` | `Etc/UTC` | Server and Horizon timezone |
| `ntp_servers` | `[]` | Extra chrony servers; empty keeps Ubuntu's pool |
| `mgmt_network` | `10.0.0.0/24` | Allowed to query BIND and to mount NFS |
| `network_mode` | `geneve` | `flat` = guide item 12 (one shared network `sharednet1`). `geneve` = guide item 25 (`public` + `router01` + `private`, floating IPs) |
| `provider_net` | 10.0.0.0/24, .200–.254 | Addresses for instances (flat) or floating IPs (geneve) |
| `private_net` | 192.168.100.0/24 | Tenant network in geneve mode |
| `provider_interface` | `eth1` | NIC added to `br-eth1`. Set per host |
| `compute_is_gateway_chassis` | `true` | Computes also route external traffic, as in the guide |
| `cinder_lvm_device` | `/dev/sdb` | Disk for `vg_volume01` |
| `manila_lvm_device` | `/dev/sdc` | Disk for `manila-volumes` |
| `swift_devices` | 10 GB loop file | Or `- {name: device, disk: /dev/sdd}` per host |
| `nova_allow_qemu_fallback` | `true` | Use QEMU when `/dev/kvm` is missing |
| `glance_customize_image` | `false` | Enable SSH password login in the Ubuntu image (guide item 06) |
| `flavors` | m1.tiny … m2.medium | Flavors to create |
| `enable_*` | `true` | Turn services on or off |
| `create_test_resources` | `false` | Run the `smoke_test` role |

> Octavia and floating IPs need `network_mode: geneve`.
> Neutron can't have two flat networks on `physnet1`, so the two modes can't be combined.

---

## Running parts of the playbook

Every role has a tag. Related roles also share a group tag:

```bash
ansible-playbook site.yml --ask-vault-pass --tags keystone
ansible-playbook site.yml --ask-vault-pass --tags nova        # placement + nova_controller + nova_compute
ansible-playbook site.yml --ask-vault-pass --tags neutron     # server + chassis + network_setup
ansible-playbook site.yml --ask-vault-pass --tags cinder      # nfs_server + api + volume + backup
ansible-playbook site.yml --ask-vault-pass --tags swift
ansible-playbook site.yml --ask-vault-pass --tags telemetry   # gnocchi + ceilometer
ansible-playbook site.yml --ask-vault-pass --tags designate,octavia,heat,barbican,manila,cloudkitty,horizon
```

Tags skip the `common` and `tls` roles, which set up the hosts and certificates.
On a fresh host, run the full playbook once before you use tags.

To work on only some machines, use `--limit`, for example `--limit node02.tekup.world` after adding a new compute node.
Roles that register in Keystone always run their API calls on the controller.

---

## After the installation

| What | Where |
|---|---|
| Horizon | `https://dlp.tekup.world/horizon`. Log in as `admin`, domain `Default`, with the password in `vault_admin_password` |
| CA certificate | `./openstack-lab-ca.crt` on the control machine. Import it into your browser or OS to trust the endpoints |
| Admin CLI | On the controller: `sudo -i`, then `source ~/keystonerc` (added to root's `.bashrc`) |
| Demo user CLI | `source ~/keystonerc_serverworld` (project `hiroshima`) |
| Swift user CLI | `source ~/keystonerc_swift` (project `swiftservice`) |
| Ansible `clouds.yaml` | `/root/.config/openstack/clouds.yaml`, with clouds `admin`, `demo` and `swift`, used as `openstack --os-cloud demo …` |

Example session on the controller:

```bash
sudo -i
openstack server list --all-projects
openstack --os-cloud demo server create --flavor m1.small --image Ubuntu2404 \
  --network private --key-name mykey --security-group secgroup01 vm01
```

---

## Checking the deployment

`ansible-playbook verify.yml --ask-vault-pass` prints:
- endpoints and hypervisors
- compute services and network agents
- volume, share, orchestration and DNS services
- load balancer providers (`ovn` should be listed)
- Gnocchi status and CloudKitty modules
- Swift containers and Barbican secrets

**What to expect for multi-node:**
- two hypervisors, `node01` and `node02`
- network agents on `network`, `node01` and `node02`
- `cinder-volume` on `storage@lvm` and `storage@nfs`
- `manila-share` on `storage`
- endpoints on `network.tekup.world` for neutron, heat, dns, load-balancer, metric, rating and object-store; `dlp.tekup.world` for the rest

`-e create_test_resources=true --tags smoke_test` creates the guide's examples as the demo user:
- instance `Ubuntu-2404`, with a floating IP in geneve mode
- volumes `disk-lvm` and `disk-nfs`, attached to the instance
- Heat stack `Heat-Stack`
- Barbican secret `secret01`
- Swift container `test-container` with `testfile.txt`
- Manila share `share01`
- DNS zone `example.tekup.world.` with record `node01`
- OVN load balancer `lb01` → `listener01` → `pool01`, with the instance as a member

---

## Project layout

```
openstack-ansible/
├── ansible.cfg
├── requirements.yml            # openstack.cloud, community.{mysql,rabbitmq,general,crypto}, ansible.posix
├── site.yml                    # main playbook, one play per phase
├── verify.yml                  # read-only status report
├── inventory/
│   ├── hosts.yml               # all-in-one (default)
│   ├── hosts-multinode.yml     # 2 controllers, 2 computes, 1 storage
│   ├── hosts-ha.yml            # HA: 3 controllers + VIP, 2 computes, 1 storage
│   ├── host_vars/              # one file per host: IP, NIC, disks
│   │   ├── dlp.tekup.world.yml  network.tekup.world.yml
│   │   ├── node01.tekup.world.yml  node02.tekup.world.yml  storage.tekup.world.yml
│   │   ├── controller01/02/03.tekup.world.yml   (HA)
│   └── group_vars/all/
│       ├── main.yml            # all settings
│       └── vault.yml           # secrets (encrypt it!)
├── templates/                  # config files shared by several roles
│   ├── nova.conf.j2  neutron.conf.j2  ml2_conf.ini.j2  cinder.conf.j2
│   ├── manila.conf.j2  ceilometer.conf.j2  swift.conf.j2  keystonerc.j2
├── scripts/vault_encrypt.py    # vault encryption without Ansible (Windows)
└── roles/
    ├── os_common/              # shared tasks (db, keystone_register, apache_listen,
    │                           # nginx_stream, manage, ovs_external_ids, ...) + all handlers
    ├── common/ tls/ nginx/ mariadb/ rabbitmq/ memcached/
    ├── keystone/ glance/ placement/ nova_controller/ nova_compute/
    ├── neutron_server/ neutron_ovn_chassis/ network_setup/ bootstrap/
    ├── cinder_controller/ cinder_volume/ cinder_backup/ nfs_server/
    ├── barbican/ manila_controller/ manila_share/ heat/ designate/ octavia_ovn/
    ├── swift_proxy/ swift_storage/ gnocchi/ ceilometer_central/ ceilometer_compute/
    ├── cloudkitty/ horizon/ smoke_test/
```

**How the roles are built:**
- Every role depends on `os_common`, which provides the helper task files and the handlers.
- Service roles register in Keystone through `openstack.cloud` modules, which are idempotent, and create their database with `community.mysql`. Both run on the controller.
- Service roles move Apache-hosted APIs to `127.0.0.1` before publishing them through `/etc/nginx/stream.d/<service>.conf`.
- Config files used by several roles (`nova.conf`, `cinder.conf`, …) are one template each. Sections turn on based on the host's groups, so each node gets the right variant, and an all-in-one host gets one combined file.

---

## Differences from the Server World guide

| Topic | Guide | This playbook | Why |
|---|---|---|---|
| Hostnames | `*.srv.world` | `*.tekup.world` | Your domain |
| TLS | Let's Encrypt | Its own CA and one certificate per host, trusted system-wide | Works in a lab without public DNS. Services keep `insecure = false` |
| Nginx | Edits `nginx.conf` for each service | One file per service in `/etc/nginx/stream.d/` | Idempotent and easy to change |
| Config files | "Add to the end of the file" in many steps | One template per file, with sections based on groups | Same result, one source |
| Octavia | Amphora image, health-manager, housekeeping, worker, lb-mgmt network | OVN provider only | Much lighter. Pools must use `SOURCE_IP_PORT` |
| Swift proxy | Pipeline as printed on the page | `authtoken` and `keystoneauth` added (`operator_roles = admin,swiftoperator`) | Needed so Keystone users can log in |
| Swift replicas | 3 storage nodes | `min(3, number of devices)` | Works with 1 node or 1 disk |
| Swift ring zones | `r0z0`, `r1z1`, `r2z2` | `r1z1`, `r1z2`, … (one zone per storage host) | Standard layout |
| Nova metadata vhost | `WSGIProcessGroup nova-api` | Its own `nova-api-metadata` daemon | The daemon is defined in the same vhost |
| Nova telemetry option | `instance_usage_audit_audit_period` | `instance_usage_audit_period` | Typo in the guide |
| Compute iSCSI | Not mentioned | `open-iscsi` installed on computes | Needed to attach LVM volumes from a separate storage node |
| Ceilometer central | Authenticates as `gnocchi` | Authenticates as `ceilometer` | Consistent credentials |
| Barbican KEK | Sample key from the guide | Random value from the vault | Security |
| Designate | `chown -R bind:bind /etc/bind` | RNDC key kept `bind:designate 0640` | Otherwise Designate can't read the key |
| NFS server | Assumed to exist (`nfs.srv.world`) | `nfs_server` role sets it up (on stor1 in multi-node) | Self-contained |
| Horizon | No page in the series | Standard Ubuntu `openstack-dashboard` setup | — |

---

## Troubleshooting

| Symptom | Check |
|---|---|
| `ansible.cfg` ignored, roles not found | You're in a world-writable directory (WSL `/mnt/c`). Copy the project to `~` or set `ANSIBLE_CONFIG` |
| Multi-node or HA run only touches `dlp.tekup.world` | You forgot `-i inventory/hosts-multinode.yml` / `-i inventory/hosts-ha.yml` |
| HA: `Check the HA layout` fails | Use an odd number of controllers, and put exactly the controllers in `network` and `swift_proxy` |
| HA: VIP doesn't answer | `ip -4 addr` on each controller, `journalctl -u keepalived`. The VRRP id may clash, or VRRP traffic may be filtered |
| HA: an API is `DOWN` in HAProxy stats | `http://<vip>:1936/`. Check that the service listens on `mgmt_ip:<port>` (`ss -ltnp`) |
| HA: Galera won't start after a full outage | Run `galera_new_cluster` on the node with `safe_to_bootstrap: 1` in `/var/lib/mysql/grastate.dat`, then start the others |
| HA: `wsrep_cluster_size` less than 3 | `journalctl -u mariadb` on the missing node. Ports 4567, 4568 and 4444 must be open between controllers |
| HA: OVN cluster not formed | `ovs-appctl -t /var/run/ovn/ovnnb_db.ctl cluster/status OVN_Northbound`. Check `/etc/default/ovn-central` |
| `Decryption failed` | Wrong vault password, or the file was encrypted with another password |
| `network_setup` assertion fails | `provider_interface` carries the default route. Use a second NIC |
| `cinder_lvm_device … does not exist` | Attach the disk, or change `cinder_lvm_device` / `manila_lvm_device` in the storage node's host_vars |
| Instances in ERROR, `No valid host` | `openstack hypervisor list`, `journalctl -u nova-compute`. Check `/dev/kvm` or the QEMU fallback |
| Volume attach fails in multi-node | On the compute: `systemctl status iscsid`, `iscsiadm -m session`. Check that stor1 port 3260 is reachable |
| TLS or certificate errors in service logs | `/usr/local/share/ca-certificates/openstack-lab-ca.crt` exists and `update-ca-certificates` has run |
| An API port refuses connections | `ss -ltnp \| grep <port>`: the service should be on `127.0.0.1` and nginx on `mgmt_ip`. Run `nginx -t`, then check `/etc/nginx/stream.d/` |
| Network agents down | `openstack network agent list`, `ovs-vsctl show`, `ovn-sbctl show` (on the network node) |
| Swift `401` | The user needs the `swiftoperator` role. `journalctl -u swift-proxy` on the proxy node |

Service logs are in `/var/log/<service>/` on the node that runs the service. For Apache-hosted APIs, look in `/var/log/apache2/`.

---

**Source:** [server-world.info – OpenStack Flamingo on Ubuntu 24.04](https://www.server-world.info/en/note?os=Ubuntu_24.04&p=openstack_flamingo&f=1)
