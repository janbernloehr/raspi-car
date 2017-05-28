# Installation

Install debian dependencies

    sudo apt-get install git supervisor python3 python3-pip nginx libjpeg-dev

Install python dependencies

    sudo pip3 install gunicorn falcon wiringpi

To use wiringpi on kernel 4.9 one needs to apply a patch - see [here](https://github.com/WiringPi/WiringPi-Python/issues/47)

Install npm dependencies

    curl -sL https://deb.nodesource.com/setup_6.x | sudo bash -
    sudo apt-get install nodejs
    npm install bower -g
    
    cd web
    bower install ngtouch --save

Create symlinks

    $PR = /home/pi/raspi-car
    ln -sf $PR/conf/nginx/default /etc/nginx/sites-enabled/default
    ln -s $PR/conf/supervisor/carweb.conf /etc/supervisor/conf.d/carweb.conf
    ln -s $PR/conf/supervisor/livestream.conf /etc/supervisor/conf.d/livestream.conf