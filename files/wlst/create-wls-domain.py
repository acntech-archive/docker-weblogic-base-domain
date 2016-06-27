# Copyright (c) 2014-2015 Oracle and/or its affiliates. All rights reserved.
#
# WebLogic on Docker Default Domain
#
# Domain, as defined in DOMAIN_NAME, will be created in this script. Name defaults to 'base_domain'.
#
# Since : October, 2014
# Author: bruno.borges@oracle.com
# ==============================================
oracle_home  = os.environ.get('ORACLE_HOME', '/u01/oracle')
domain_name  = os.environ.get("DOMAIN_NAME", "base_domain")
domain_home  = os.environ.get("DOMAIN_HOME", "%s/user_projects/domains/%s" % (oracle_home, domain_name))
admin_port   = int(os.environ.get("ADMIN_PORT", "7001"))
admin_pass   = os.environ.get("ADMIN_PASSWORD")
nm_port      = int(os.environ.get("NM_PORT", "5556"))
cluster_name = os.environ.get("CLUSTER_NAME", "DockerCluster")

print('domain_name : [%s]' % domain_name);
print('admin_port  : [%s]' % admin_port);
print('cluster_name: [%s]' % cluster_name);
print('domain_home : [%s]' % domain_home);

# Open default domain template
# ======================
readTemplate("%s/wlserver/common/templates/wls/wls.jar" % oracle_home)

set('Name', domain_name)
setOption('DomainName', domain_name)

# Disable Admin Console
# --------------------
# cmo.setConsoleEnabled(false)

# Configure the Administration Server and SSL port.
# =========================================================
cd('/Servers/AdminServer')
set('ListenAddress', '')
set('ListenPort', admin_port)

# Define the user password for weblogic
# =====================================
cd('/Security/%s/User/weblogic' % domain_name)
cmo.setPassword(admin_pass)

# Write the domain and close the domain template
# ==============================================
setOption('OverwriteDomain', 'true')
setOption('ServerStartMode','prod')

cd('/NMProperties')
set('ListenAddress', '')
set('ListenPort', nm_port)
set('CrashRecoveryEnabled', 'true')
set('NativeVersionEnabled', 'true')
set('StartScriptEnabled', 'false')
set('SecureListener', 'false')
set('LogLevel', 'FINEST')

# Set the Node Manager user name and password (domain name will change after writeDomain)
cd('/SecurityConfiguration/base_domain')
set('NodeManagerUsername', 'weblogic')
set('NodeManagerPasswordEncrypted', admin_pass)

# Define a WebLogic Cluster
# =========================
cd('/')
create(cluster_name, 'Cluster')

cd('/Clusters/%s' % cluster_name)
cmo.setClusterMessagingMode('unicast')

# Write Domain
# ============
writeDomain(domain_home)
closeTemplate()

# Exit WLST
# =========
exit()
