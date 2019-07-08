# GCP Short Intro Demonstration For Tieto Specialists  <!-- omit in toc -->


# Table of Contents  <!-- omit in toc -->
- [WORK IN PROGRESS](#WORK-IN-PROGRESS)
- [Introduction](#Introduction)
- [GCP Solution](#GCP-Solution)
  - [Project](#Project)
  - [Vpc](#Vpc)
  - [VM](#VM)
- [Demonstration Manuscript](#Demonstration-Manuscript)
- [Suggestions How to Continue this Demonstration](#Suggestions-How-to-Continue-this-Demonstration)
- [Investigating Connectivity Issue](#Investigating-Connectivity-Issue)


# WORK IN PROGRESS

I'll delelete this chapter once this demonstration is ready.

# Introduction

This demonstration can be used in training new cloud specialists who don't need to have any prior knowledge of GCP (Google Cloud Platform) but who want to start working on GCP projects and building their GCP competence (well, a bit of GCP knowledge is required - GCP main concepts, how to use the GCP Portal and CLI).

This demonstration is basically the same as [gcp-intro-demo](https://github.com/tieto-pc/gcp-intro-demo) with one difference: gcp-intro-demo uses [Terraform](https://www.terraform.io/) as IaC tool, and gcp-intro-dp-demo uses [GCP Deployment Manager](https://cloud.google.com/deployment-manager/docs/). The idea is to introduce another way to create infrastructure code in GCP and let developers to compare Terraform and GCP Deployment Manager and make their own decision which tool to use in their future projects.

This project demonstrates basic aspects how to create cloud infrastructure as code. The actual infra is very simple: just one virtual machine instance. We create a virtual private cloud [vpc](https://cloud.google.com/vpc/) and an application subnet into which we create a [VM](https://cloud.google.com/compute/docs/instances/). There is also one [firewall](https://cloud.google.com/vpc/docs/firewalls) in the VPC that allows inbound traffic only using ssh port 22. The IaC also creates a ssh key pair - the public key gets stored in your workstation, the private key will be installed to the VM.

I tried to keep this demonstration as simple as possible. The main purpose is not to provide an example how to create a cloud system (e.g. not recommending VMs over containers) but to provide a very simple example of infrastructure code and tooling related creating the infra. I have provided some suggestions how to continue this demonstration at the end of this document - you can also send me email to my corporate email and suggest what kind of GCP or GCP POCs you need in your team - I can help you to create the POCs for your customer meetings.

There are two equivalent cloud native deployment demonstrations in other "Big three" cloud provider platforms: AWS demonstration - [aws-intro-cloudformation-demo](https://github.com/tieto-pc/aws-intro-cloudformation-demo), and Azure demonstration - [azure-intro-arm-demo](https://github.com/tieto-pc/azure-intro-arm-demo) - compare the terraform code between these GCP, AWS and Azure infra implementations.

There are a lot of [Terraform examples provided by Google](https://github.com/GoogleCloudPlatform/terraform-google-examples) - you should use these examples as a starting point for your own GCP Terraform IaC, I did too.


# GCP Solution

The diagram below depicts the main services / components of the solution.

![GCP Intro Demo Architecture](docs/gcp-intro-demo.png?raw=true "GCP Intro Demo Architecture")

So, the system is extremely simple (for demonstration purposes): Just one VPC, one application subnet and one Compute instance (VM) doing nothing in the subnet. One Firewall rule in the VPC which allows only ssh traffic to the Compute instance. 


## Project

The project definition creates the infra project that will host all resources in this demonstration. IaC also links this new project to the folder we are using (if you don't have a folder modify the code) and to a billing account (you must have a billing account in order to create resources). We also set auto-create-network to false since we don't want that GCP creates a default VPC for us which it would normally do.

We also turn on certain GCP APIs we need in this project (compute related).


## Vpc

The [vpc](https://cloud.google.com/vpc/) definition creates the VPC (virtual private cloud), subnet and the firewall rule to allow ssh traffic to this VPC. We set auto-create-subnetworks to false since we want to create the subnet using IaC in this demonstration.

Note that in GCP VPC is a global entity and you don't assign an address space ([cidr](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)) to it as in AWS and Azure. You assign the address space to subnet. You also need to provide the infra project id which is used to host subnet and firewall rule (and later compute instance).

Finally there is a [firewall rule](https://cloud.google.com/vpc/docs/firewalls) defintion which opens port 22 for ssh connections. NOTE: We do not restrict any source addresses - in real world system you should restrict the source ip addresses, of course. But don't worry - there is just one VM and we protect the VM with ssh keys (see VM chapter later).


## VM


The [vm](https://cloud.google.com/compute/docs/instances/) module is a also a bit more complex. But let's not be intimidated - let's see what kind of bits and pieces there are in this module. 

We first create the ssh keys to be used for both *nix and Windows workstations (client side). 

Then we create the external static ip for the compute instance. 

Finally there is the compute instance defitinion. We link this instance to the infra project, provide values for various parameters (zone...) and inject the public ssh key to the machine (to be used later when we use ssh to connect to the VM). We also provide a set of labels for the VM.



# Demonstration Manuscript

NOTE: These instructions are for Linux (most probably should work for Mac as well). If some Tieto employee is using Windows I would appreciate to get a merge request to provide instructions for a Windows workstation as well.

Let's finally give detailed demonstration manuscript how you are able to deploy the infra of this demonstration to your GCP account. You need a GCP account for this demonstration. You can order a private GCP account or you can contact your line manager if you are allowed to use Tieto's GCP account (contact the administrator in Tieto Yammer Google Cloud Platform group).  **NOTE**: Watch for costs! Always finally destroy your infrastructure once you are ready (never leave any resources to run indefinitely in your GCP account to generate costs).

1. Install [Terraform](https://www.terraform.io/). You might also like to add Terraform support for your favorite editor (e.g. there is a Terraform extension for VS Code).
2. Install [GCP command line interface](https://cloud.google.com/sdk/).
3. Clone this project: git clone https://github.com/tieto-pc/gcp-intro-demo.git
4. Create the environment variables file as described earlier. Use [gcp_env_template.sh](gcp_env_template.sh) as a template.
5. Open console and source the environment variable file (```source <FILE>```). Create the admin project and the terraform backend cloud storage bucket using the [create-admin-proj.sh](create-admin-proj.sh) script as described earlier.
6. Create project infra gcloud configuration:
   1. Source your environment variables file: ```source <FILE>```
   2. Use script [create-infra-configuration.sh](create-infra-configuration.sh).
7. Open console in [dev](terraform/envs/dev) folder. Give commands
   1. Source your environment variables file: ```source <FILE>```
   2. Check that you are using the right gcloud configuration: ```gcloud config configurations list```
   3. ```terraform init``` => Initializes the Terraform backend state.
   4. ```terraform get``` => Gets the terraform modules of this project.
   5. ```terraform plan``` => Gives the plan regarding the changes needed to make to your infra. **NOTE**: always read the plan carefully!
   6. ```terraform apply``` => Creates the delta between the current state in the infrastructure and your new state definition in the Terraform configuration files.
8. Open GCP Portal and browse different views to see what entities were created:
   1. Home => Select the project you created.
   2. Click the "VPC Network". Browse subnets etc.
   3. Click the "Compute Engine". Browse different information regarding the VM.
9.  Test to get ssh connection to the VM instance:
    1.  ```gcloud compute instances list``` => list VMs (should be only one) => check the external ip.
    2.  ssh -i terraform/modules/vm/.ssh/vm_id_rsa user@IP-NUMBER-HERE
10. Finally destroy the infra using ```terraform destroy``` command. Check manually also using Portal that terraform destroyed all resources. **NOTE**: It is utterly important that you always destroy your infrastructure when you don't need it anymore - otherwise the infra will generate costs to you or to your unit.

The official demo is over. Next you could do the equivalent [gcp-intro-dp-demo](https://github.com/tieto-pc/gcp-intro-dp-demo) that uses GCP Deployment Manager. Then compare the Terraform and Deployment Manager code and also the workflows. Evaluate the two tools - which pros and cons they have when compared to each other? Which one would you like to start using? And why?


# Suggestions How to Continue this Demonstration

We could add e.g. an instance group and a load balancer to this demonstration but let's keep this demonstration as short as possible so that it can be used as a GCP introduction demonstration. If there are some improvement suggestions that our Tieto developers would like to see in this demonstration let's create other small demonstrations for those purposes, e.g.:
- Create a custom Linux image that has the Java app baked in.
- An instance group (with CRM app baked in) + a load balancer.
- Logs to StackDriver.
- Use container instead of VM.


# Investigating Connectivity Issue

When I created the first version of VPC, subnetwork, firewall and VM I couldn't connect to the VM neither using Console SSH or ssh from my local workstation. The VM was not reachable using ping. I created another standard VM using GCP Console into the same subnetwork - same thing. GCP provided nice document for solving connectivity issues: [Troubleshooting SSH](https://cloud.google.com/compute/docs/troubleshooting/troubleshooting-ssh). That document didn't help though. A seasoned cloud developer has a best practice in situation like this. Create another version of the entities using either Portal or some tutorial instructions that should work. Verify that the tutorial version works. Then compare all entities (your not-working entity and equivalent tutorial working entity) - in some entity you should see some discrepancy which should give you either the culprit itself or at least some clues how to investivate the issue further. So, I created another custom VPC, subnetwork and firewall using instructions in [Using VPC](https://cloud.google.com/vpc/docs/using-vpc) and was able to pinpoint the issue and fix it. 

While investigating the issue I noticed that when choosing the instance in GCP Console and clicking Edit button and checking the ssh key it complains: ```Invalid key. Required format: <protocol> <key-blob> <username@example.com> or <protocol> <key-blob> google-ssh {"userName":"<username@example.com>", expireOn":"<date>"}``` ... but logging to instance using the key succeeds: ```ssh -i terraform/modules/vm/.ssh/vm_id_rsa user@<EXTERNAL-IP>```. I didn't bother to investigate reason for that error message since I could ssh to the instance using the key.