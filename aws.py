import boto3
import yaml
import sys
from botocore.exceptions import ClientError
import re

class AWSEC2:

    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.ec2_resource = boto3.resource('ec2')
        self.elb= boto3.client('elb')
        self.client = boto3.client('autoscaling')
        f=open('data.yml')
        self.yml=yaml.load(f)

    def checkExistance(self, securitygroup):
        print "-------------Checking to see if Security Group exists------------------"
        groupInfo = []
        for securityGroup in securitygroup:
            securityGroupName= securitygroup.get(securityGroup).get('name')
            #print self.VpcId
            try:
                a = self.ec2.describe_security_groups(
                    GroupNames=[
                        securityGroupName
                    ]
                )
                print a
                if (a is not None):
                    print "---------------- Group with name %s exists, ----------------" % (securityGroup)
                    continue
            except ClientError as e:
                print "This Group Does not exist %s"%(securityGroupName)
                GroupId = self.createSecurityGroup(securityGroupName)
                print GroupId
                groupData=[securityGroupName,GroupId]
                groupInfo.append(groupData)
                pass
        return groupInfo

    def createSecurityGroup(self,securityGroupName):
        print "-------This method is used to create Security Group---------------------"
        response = self.ec2.create_security_group(GroupName=securityGroupName,
                                  Description="This is a security group for %s"%(securityGroupName))
                                  #VpcId=self.VpcId)
        security_group_id = response['GroupId']
        return security_group_id

    def getSecurityGroupId(self,groupName):
        r = self.ec2.describe_security_groups(
            GroupNames=[
                groupName
            ]
        )
        t = r.get('SecurityGroups')[0]
        return t.get('GroupId')


    def attachRules(self, groupInfo):
        for group in groupInfo:
            securityGroupName=group[0]
            securityGroupId=group[1]
            securitygroup = self.yml.get('SecurityGroups')
            for sgroups in securitygroup:
                if (securitygroup.get(sgroups).get('name') == securityGroupName):
                    mappings=securitygroup.get(sgroups).get('mappings')
                    print "this method is used to attach the rules for seurity group"
                    for mapping in mappings:
                        if (mapping == "inBound_mapping"):
                            for mapdata in mappings[mapping]:
                                print mapdata
                                p = re.compile("([\d]+\.){3}\d*\/\d+")
                                print p.match(str(mappings[mapping][mapdata].get('IpRanges')))
                                if ((p.match(str(mappings[mapping][mapdata].get('IpRanges')))) is None):
                                    range='UserIdGroupPairs'
                                    ipType ='GroupId'
                                    ipRange = self.getSecurityGroupId(mappings[mapping][mapdata].get('IpRanges'))
                                else:
                                    range = 'IpRanges'
                                    ipType = 'CidrIp'
                                    ipRange = mappings[mapping][mapdata].get('IpRanges')
                                try:
                                    print ipRange
                                    data = (self.ec2).authorize_security_group_ingress(
                                        GroupId=securityGroupId,
                                        IpPermissions=[
                                            {'IpProtocol': mappings[mapping][mapdata].get('IpProtocol'),
                                             'FromPort': mappings[mapping][mapdata].get('FromPort'),
                                             'ToPort': mappings[mapping][mapdata].get('ToPort'),
                                             range: [{ipType: ipRange}]}

                                            ])
                                    print data
                                except ClientError as e:
                                    print (e)
                                    pass
                        elif (mapping == 'outBound_mapping'):
                            print "this is a set up for outbound mapping"
                            for mapdata in mappings[mapping]:
                                t=str(mappings[mapping][mapdata].get('IpRanges'))
                                p = re.compile("([\d]+\.){3}\d*\/\d+")
                                print mappings[mapping][mapdata].get('IprRanges')
                                print (p.match(str(mappings[mapping][mapdata].get('IpRanges'))))
                                a=mappings[mapping][mapdata]
                                print a
                                if ((p.match(str(mappings[mapping][mapdata].get('IpRanges')))) is None):
                                    range = 'UserIdGroupPairs'
                                    ipType = 'GroupId'
                                    ipRange = self.getSecurityGroupId(mappings[mapping][mapdata].get('IpRanges'))
                                else:
                                    range = 'IpRanges'
                                    ipType = 'CidrIp'
                                    ipRange = mappings[mapping][mapdata].get('IpRanges')
                                try:
                                    data = (self.ec2).authorize_security_group_egress(
                                        GroupId=securityGroupId,
                                        IpPermissions=[
                                            {'IpProtocol': mappings[mapping][mapdata].get('IpProtocol'),
                                             'FromPort': mappings[mapping][mapdata].get('FromPort'),
                                             'ToPort': mappings[mapping][mapdata].get('ToPort'),
                                             range: [{ipType: ipRange}]}

                                        ])
                                    print data
                                except ClientError as e:
                                    print (e)
                                    pass


    def checkIfLoadBalanceExists(self,balancerName):
        try:
            response = self.elb.describe_load_balancers(
                LoadBalancerNames=[
                    balancerName,
                ], )
            if (response is not None): return response
        except ClientError as e:
            print (e)
            return False
            pass

    def configureHealthcheck(self,loadBalancerName):
        print 'this method is  used to configure health check'
        response = self.elb.configure_health_check(
            LoadBalancerName=loadBalancerName['LoadBalancerName'],
            HealthCheck=loadBalancerName['HealthCheck']
        )
        print response


    def createLoadBalance(self):
        loadbalancer=self.yml.get('LoadBalancer')
        for balancer in loadbalancer:
            status=self.checkIfLoadBalanceExists(loadbalancer[balancer]['LoadBalancerName'])
            print status
            if(status):
                print "------ Load Balancer exists, Hence we are going to check if instance exist in load balancer or not   ------------"

            else:
                print "Creating the load balancer"
                d=[]
                securityGroupId=[]
                for sg in loadbalancer[balancer]['SecurityGroups']:
                    groupId=self.getSecurityGroupId(sg)
                    securityGroupId.append(groupId)
                for lnumber in loadbalancer[balancer]['Listeners']:
                    d.append(loadbalancer[balancer]['Listeners'][lnumber])
                    print d
                try:
                    response = self.elb.create_load_balancer(
                        LoadBalancerName=loadbalancer[balancer]['LoadBalancerName'],
                        Listeners= d,
                        AvailabilityZones=loadbalancer[balancer]['AvailabilityZone'],
                        SecurityGroups=securityGroupId,
                    )
                    print "---------- Configuring the health check -------------------"
                    self.configureHealthcheck(loadbalancer[balancer])
                except ClientError as e:
                    print (e)

    def createLaunchConfiguration(self,data):

        print data.get('DeviceName')
        SecurityGroup = []
        sg = data.get('SecurityGroups')
        for sgs in sg:
            SecurityGroup.append(self.getSecurityGroupId(sgs))

        try:
            response = self.client.describe_launch_configurations(
                    LaunchConfigurationNames=[
                        data.get("LaunchConfigurationName"),
                    ],
            )
            if (response is not None):
                print "Info:: LaunchConfiguration %s already exists, hence we are not creating it "%(data.get("LaunchConfigurationName"))
                return
        except ClientError as e:
            print "============== AutoScaling Group does not exist, hence creating it ==============="
            response = self.client.create_launch_configuration(
                ImageId=data.get("ImageId"),
                InstanceType=data.get("instanceType"),
                LaunchConfigurationName=data.get("LaunchConfigurationName"),
                SecurityGroups=SecurityGroup,
                BlockDeviceMappings=[
                    {
                        'DeviceName': data.get('DeviceName'),
                        'Ebs': {
                            'SnapshotId': data.get('SnapshotId'),
                            'VolumeSize': 10,
                            'VolumeType': data.get('VolumeType'),
                            'DeleteOnTermination': True,
                        },
                    },
                ],
                KeyName=data.get("KeyName"),

            )
            print response
            pass

    def createAutoScalingGroup(self,data, scalingGroup):
        try:
            response = self.client.describe_auto_scaling_groups(
                AutoScalingGroupNames=[
                    scalingGroup.get('GroupName'),
                ],
            )
            if (response is not None):
                print "Info:: AutoScalingGroup %s already exists, hence we are not creating it "%(scalingGroup.get('GroupName'))
                return

        except ClientError as e:
            print "============== AutoScaling Group does not exist, hence creating it ==============="
            response = self.client.create_auto_scaling_group(
                AutoScalingGroupName=scalingGroup.get('GroupName'),
                LaunchConfigurationName=data.get("LaunchConfigurationName"),
                MinSize=scalingGroup.get('MinSize'),
                MaxSize=scalingGroup.get('MaxSize'),
                DesiredCapacity=1,
                DefaultCooldown=300,
                AvailabilityZones=scalingGroup.get('AvailabilityZone'),
                LoadBalancerNames=scalingGroup.get('LoadBalancer'),
                VPCZoneIdentifier= scalingGroup.get('VPCZoneIdentifier')


            )

            print response
            pass

    def parseSecrity(self):
        securityGroupInstance = self.yml.get('SecurityGroups')
        groupInfo=self.checkExistance(securityGroupInstance)
        self.attachRules(groupInfo)
        self.createLoadBalance()
        print "=========-====================================="
        print "========= Creating AutoScaling ================"
        print "==============================================="
        for scaling in self.yml.get("AutoScaling"):
            data = self.yml.get("AutoScaling")[scaling].get("LaunchConfiguration")
            scalingGroup = self.yml.get("AutoScaling")[scaling].get("AutoScalingGroup")
            self.createLaunchConfiguration(data)
            self.createAutoScalingGroup(data, scalingGroup)

if __name__ == '__main__':
    aws = AWSEC2()
    aws.parseSecrity()
