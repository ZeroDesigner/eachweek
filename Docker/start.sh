#!/binb/bash
cp /etc/crontab /etc/crontab.bak
tee /etc/crontab << 'EOF'
0 0     0 0 1   root    /root/miniconda3/bin/conda/env/eachweek/bin/python /root/eachweek.py 2&>1
EOF
cat /etc/crontab.bak >> /etc/crontab
systemctl start crontab
systemctl reload crontab
systemctl restart crontab
/usr/local/nginx/sbin/nginx && hexo g --watch