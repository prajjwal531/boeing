import os
from subprocess import Popen,PIPE
import sys
import argparse

class automation:

    def runShellCommand(self,cmd):
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        print out
        return p.returncode

    def getVersion(self,target):
        os.chdir(target)
        p = Popen("find . -type f -name *.war", shell=True, stdout=PIPE, stderr=PIPE)
        (out, err) = p.communicate()
        outwithoutreturn = out.rstrip('\n')
        outwithoutreturn = out.strip("./")
        a = 1
        for i in outwithoutreturn:
            if (i == "-"):
                z = outwithoutreturn[10:-1].split(".wa")
                return z[0]
            a = a + 1

    # This Method is used as we do not have artifactory.
    def createStorage(self,target):
        storagePath="/Users/prajjavalgupta/Desktop/boeing/storage"
        if not os.path.exists(storagePath):
            os.mkdir(storagePath)
        version=self.getVersion(target)
        dataPath="%s/%s"%(storagePath, version)
        if not os.path.exists(dataPath):
            os.mkdir(dataPath)
        else:
            os.chdir(dataPath)
            os.system("rm -rf *")
        print "Copying the war into this location"
        command = "cp %s/*.war %s"%(target, dataPath)
        self.runShellCommand(command)
        return version

    def deployment(self,version, environment):
        print "========= This is Deployment using Ansible Dynamic Inventory =============="
        command = 'ansible-playbook deployment.yml  --extra-vars "ENVR=%s Version=%s"'%(environment,version)
        print command
        returnCode = self.runShellCommand(command)
        if returnCode is not 0:
            print "Error:: There is some error running the ansible playbook for deployment"
            sys.exit(1)

    def awsAutomation(self):
        print "===== Running the AWS Automation =========="

        command = "python aws.py"
        returnCode=self.runShellCommand(command)
        if returnCode is not 0:
            print "Error:: There are some issue while running AWS automation, hence exiting the system ======="
            sys.exit(1)

    # This Method is used to build the project.
    def build(self,buildNumber):
        print "==== This method is used to build the project ====="
        cwd=os.getcwd()
        path='%s/transactions'%(cwd)
        os.chdir(path)
        buildCommand="~/Downloads/apache-maven-3.5.2/bin/mvn clean install -Dbuild=%s"%(buildNumber)
        status=self.runShellCommand(buildCommand)
        if (status != 0):
            print "====== There is some issue building this project, please check the logs and we are exiting the system ===="
            sys.exit(1)
        else:
            print " =========== doing something ===================="
            target="%s/target"%(path)
            version= self.createStorage(target)
            return version

    def __init__(self):
        print "This is main constructor"

    def getData(self):
        print "this method is to get  data %s" %(self.i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Arguments')
    requiredNamed.add_argument('-m', '--mode', dest="mode",
                               help="Input the Environment Name for Env Config file")
    requiredNamed.add_argument('-e', '--environment', dest="environment",
                               help="Input the Environment Name for Env Config file")
    requiredNamed.add_argument('-v', '--version', dest="version",
                               help="Please input application specific paramters")
    requiredNamed.add_argument('-b', '--buildNumber', dest="buildNumber",
                               help="Please input application specific paramters")

    parentDirectory = os.getcwd()
    results = parser.parse_args()
    d = automation()

    print "========================================"
    print " Info:: Runnning AWS Automation ========"
    print "========================================"

    d.awsAutomation()
    if (results.mode == "build"):

                    homepath=os.getcwd()
                    version = d.build(results.buildNumber)
                    environment = results.environment
                    os.chdir(parentDirectory)
                    d.deployment(version,environment)
    elif (results.mode == "deployment"):
                    version = results.version
                    environment = results.environment
                    environment = results.environment
                    d.deployment(version,environment)




