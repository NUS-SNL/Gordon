sudo apt-get install -y python
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
python3 -m pip install numpy
#sudo python3-pip install numpy
sudo add-apt-repository ppa:keithw/mahimahi -y
sudo apt-get update
sudo apt-get install -y mahimahi
sudo dpkg-reconfigure -p critical dash
sudo sysctl -w net.ipv4.ip_forward=1
sudo apt-get install -y libnetfilter-queue-dev
sudo apt-get install tmux

# apt-get install sudo -y   # for Docker
sudo apt-get install -y iputils-ping
sudo apt-get install -y wget
sudo apt-get install -y psmisc
sudo apt install -y net-tools

