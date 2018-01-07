#!/usr/bin/env bash
echo "Restarting the tomcat"
chmod +x /home/ubuntu/apache-tomcat-7.0.81/bin/s*
/home/ubuntu/apache-tomcat-7.0.81/bin/shutdown.sh
/home/ubuntu/apache-tomcat-7.0.81/bin/startup.sh