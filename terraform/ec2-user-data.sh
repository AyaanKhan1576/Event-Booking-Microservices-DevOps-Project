#!/bin/bash
# Minimal bootstrap so Ansible can log in

yum update -y
# Amazon Linux 2 already has python3. If it didn't:
# yum install -y python3

# That’s it – Docker, git, code-clone, and compose
# will be handled by Ansible after the instance comes up.
