#!/usr/bin/env bash

NODE=$1
MEMORY=$2
CPU=$3
USERNAME=$4
PASSWORD=$5

TMPFILE=$(mktemp)

lxc-info -n ${NODE} 2>&1 >/dev/null | if grep -q "doesn't exist"; then
    lxc-clone -o template -n ${NODE}
    echo "# ELASTIQ" >> /var/lib/lxc/${NODE}/config
    echo "lxc.start.auto = 1" >> /var/lib/lxc/${NODE}/config
    echo "lxc.cgroup.memory.limit_in_bytes = ${MEMORY}G" >> /var/lib/lxc/${NODE}/config
    echo "lxc.cgroup.cpu.shares  = $CPU" >> /var/lib/lxc/${NODE}/config
    lxc-start -d -n ${NODE}
    sleep 10
    IP=$(lxc-ls --fancy | grep "^${NODE} " | awk '{print $3}')
    cat devops/etc/nginx/site-enabled/template | sed "s/{name}/${NODE}/g" | sed "s/{ip}/${IP}/g" > /etc/nginx/sites-enabled/${NODE}
    cat devops/etc/default/elasticsearch | sed "s/{memory}/${MEMORY}/g" > /var/lib/lxc/${NODE}/rootfs/etc/default/elasticsearch
    htpasswd -b -c /etc/nginx/${NODE}.passwd  ${USERNAME} "${PASSWORD}"
    service nginx reload

else
    grep -B100 ELASTIQ /var/lib/lxc/${NODE}/config > ${TMPFILE}
    cp ${TMPFILE} /var/lib/lxc/${NODE}/config
    echo "lxc.start.auto = 1" >> /var/lib/lxc/${NODE}/config
    echo "lxc.cgroup.memory.limit_in_bytes = ${MEMORY}G" >> /var/lib/lxc/${NODE}/config
    echo "lxc.cgroup.cpu.shares  = $CPU" >> /var/lib/lxc/${NODE}/config
    cat devops/etc/default/elasticsearch | sed "s/{memory}/${MEMORY}/g" > /var/lib/lxc/${NODE}/rootfs/etc/default/elasticsearch
    lxc-stop -n ${NODE}
    lxc-start -d -n ${NODE}
fi

rm ${TMPFILE}


