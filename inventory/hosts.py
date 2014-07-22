#!/usr/bin/env python

from __future__ import print_function, generators

import json
import os
import re
import shlex
import subprocess
import yaml


def get_config(config_file):
    # Load config file
    with open(config_file, "r") as fp:
        return yaml.load(fp)


def get_hosts():
    # Get config dict
    config = get_config(".config.yml")

    # Add openstack creds to environment
    env = os.environ
    env.update(config["env"])

    # Get list of servers from nova by host prefix
    output = subprocess.check_output(
        shlex.split(
            "nova list --name {} --fields name,networks".format(
                config["host_prefix"]
            )
        ),
        env=env
    )

    # Ignore first three and last output lines
    lines = output.splitlines()[3:-1]

    # Initialize dynamic inventory output
    hosts = {"cluster": {"hosts": []}, "_meta": {"hostvars": {}}}

    # For each line
    for index, line in enumerate(lines):
        # Split lines into sections by "|" chars
        bits = re.findall("[|] ([^|]*) ", line)

        # Pickout IPv4 public addresses
        ips = re.findall("public=(?:(.*), )?(.*);", bits[2])[0]
        ipv4 = ips[0] if ":" not in ips[0] else ips[1]

        # Update hostvars metadata
        hosts["_meta"]["hostvars"].update(
            {
                bits[1].strip():
                {
                    "id": bits[0].strip(),
                    "ansible_ssh_host": ipv4.strip(),
                    "ansible_ssh_user": "root",
                    "container_ip":
                        config["container_cidr_prefix"] +
                        str(index + 1) + "/" +
                        config["container_cidr_mask"],
                    "tunnel_ip":
                        config["tunnel_cidr_prefix"] +
                        str(index + 1) + "/" +
                        config["tunnel_cidr_mask"]
                }
            }
        )

        # Append hostname to cluster group
        hosts["cluster"]["hosts"].append(bits[1].strip())

    return hosts

if __name__ == "__main__":
    print(json.dumps(get_hosts(), indent=2, sort_keys=True))
