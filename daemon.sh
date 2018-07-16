while true; do
  source activate daemon
  python /home/blueblood/daemon.py >> /home/blueblood/log/log.log &
  sleep 60*60
  kill $!
  source deactivate daemon
done