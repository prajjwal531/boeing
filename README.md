# Boeing Assignment

This is the solution to create a fault tolerant, scalable and one click of a button solution to deploy a microservice to the cloud.

In this assignment technologies used are given below.

1. Java ( To Develope the MicroService )
2. Maven ( Build tool )
3. Python ( Automation Scripting language to automate build, deploy and AWS automation process)
4. AWS ( Used to host CPU and Storage power )
5. Ansible ( Used Ansible dynamic Inventory to do deployment on AWS Instances based on specific keys assosiated to environment)

This is a one click of a button solution. MicroService is developed in Java Using Jax-rs and it currently supports two operations, first one is get which returns the "Hello World" second post operation which takes name as query param and returns
"Hello {Name} World".

In-order to test the code Junits has been written for both of the methods, hence at buid time integration testing will happen.

# Working Flow.

data.py is the starting point of this solution and it requies various mode.

1. -m : This is used to define the mode of operation, supported operations are build and deployment.
2. -e : This represents the environment name where we want to deploy to eg. Dev, QA, UAT, Production etc.
3. -v : if we want to delpoy a specific version of webservice then we need to specify this version.
4. -b : This represents the build number and used to create new build version at each build. 

Example:

1. Build

Python data.py -m build -e dev -b 1

2. Deployment of an specific version

Python data.py -m deployment -e dev -v 1.0.0-SNASHOT-1

# Mode Build
Each time build happens it creates a new version based on build number passed to it and stores it in a seperate folder called storage with different version numbers. Sample folder structure has been given with the folder name storage. 
In real world all new versions will be deployed to Artifactory.

After putting the version in storage folder. AWS automation takes place. data.py internally calls aws.py and this scripts reads the data from data.yml and creates following resources in AWS.

1. SecutiryGroups.
2. LoadBalancers
3. AutoScaling
    3.1 Launch Configuration
    3.2 AutoScaling Policy
    
After AWS automation environment name is passed to Ansible playbook and version to deploy to, based on environment and version it does the deploys the webservice to tomcat instance of AWS ec2 instances.

Note: Each environment in AWS has been assosiated with different access key based on environment. For example the key for dev environment is going to be prajjwakey_dev. Based on the environment passed to ansible it knows which environment to delpy to and it forms a env key and use it for deployment.

# Mode Deployent

Many times we want to deploy specific version of a service to any environment without even building the code. This term is known as Continuus deployment.

To achieve this our deployment mode comes handy. In this we need to pass environment namee andd version name to data.py.
Once it receives these parameters it runs the AWS automation then it passes these parameters to ansible playbook.
Based on env name and version name, ansible pick the right artifact from the storage and starts deploying it to that environmnt.

To make service fault tolerant, Initial infrastructure has been given 2 ec2-instances for each env with a load balancer on top of them. In the cirumstances of exteme load autoscaling policy has been assigned to it and it will grow upto 1o instances to support high load. ( The condition for high load is when CPU usage goes above 80% ).

This is a one click of a button solution that will,
1. Build
2. Test
3. Build Infrastructure.
4. Deployment.

In case if you have any questions regarding this solution, Please let me know.
I can be reached on my email or phone.
Emal: prajjwal.gupta531@gmail.com
Ph: 587 938 7955.

