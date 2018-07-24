curl -sSL https://get.haskellstack.org/ | sh
apt-get install libgmp-dev libbz2-dev libreadline-dev
npm install -g solc
git clone https://github.com/trailofbits/echidna
cd echidna
stack upgrade
stack setup
stack install
