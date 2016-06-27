FROM acntech/weblogic-generic:12.2.1.1
MAINTAINER Thomas Johansen "thomas.johansen@accenture.com"


ARG ADMIN_PASSWORD


ENV DOMAIN_NAME base_domain
ENV DOMAIN_HOME /u01/oracle/user_projects/domains/$DOMAIN_NAME
ENV ADMIN_PORT 7001
ENV ADMIN_HOST wlsadmin
ENV NM_PORT 5556
ENV MS_PORT 8001
ENV CONFIG_JVM_ARGS -Dweblogic.security.SSL.ignoreHostnameVerification=true
ENV PATH=$PATH:$ORACLE_HOME/oracle_common/common/bin:$ORACLE_HOME/wlserver/common/bin:${DOMAIN_NAME}/bin:$ORACLE_HOME/wlst



RUN apt-get -y update

USER oracle

RUN mkdir -p $DOMAIN_HOME/wlst
COPY files/wlst $ORACLE_HOME/wlst


WORKDIR $ORACLE_HOME

RUN $ORACLE_HOME/wlst/wlst $ORACLE_HOME/wlst/create-wls-domain.py

RUN mkdir -p $DOMAIN_HOME/servers/AdminServer/security
RUN echo "username=weblogic" > $DOMAIN_HOME/servers/AdminServer/security/boot.properties
RUN echo "password=welcome1" >> $DOMAIN_HOME/servers/AdminServer/security/boot.properties

#RUN echo ". $DOMAIN_HOME/bin/setDomainEnv.sh" >> /u01/oracle/.bashrc
#RUN cp $ORACLE_HOME/commEnv.sh $ORACLE_HOME/wlserver/common/bin/commEnv.sh


EXPOSE $NM_PORT $ADMIN_PORT $MS_PORT

WORKDIR $DOMAIN_HOME 


CMD ["/bin/bash"]