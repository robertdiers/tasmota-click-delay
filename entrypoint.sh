printenv | grep -v "no_proxy" >> /etc/environment
echo 'environment stored'
python3 -V
echo 'run web app...'
python3 clickdelay.py &
echo 'starting cron'
cd /app
cron -f