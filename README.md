#Rackspace Cloud Server Provisioner

Use this to provision cloud servers you've already configured.

#Python Requirements

- PyYaml
- rackspace-novaclient

#Usage

This expects a .config.yml in the clone root formatted as follows:

```
---
# Rackspace OpenStack credentials
env:
  OS_USERNAME: "username"
  OS_TENANT_ID: "12345"
  OS_AUTH_SYSTEM: "rackspace"
  OS_PASSWORD: "reallylongapikeyhere"
  OS_AUTH_URL: "https://identity.api.rackspacecloud.com/v2.0/"
  OS_REGION_NAME: "IAD"
  OS_NO_CACHE: "1"
  NOVA_RAX_AUTH: "1"
# Prefix for nodes used by nova list --name
host_prefix: "my-node"
# Container network CIDR prefix/mask to reconfigure
container_cidr_prefix: "172.16.0."
container_cidr_mask: "24"
# VXLAN tunnel CIDR prefix/mask to configure
tunnel_cidr_prefix: "172.16.1."
tunnel_cidr_mask: "24"
```

Then just run `ansible-playbook site.yml` to prepare your cloud servers for RPC.
