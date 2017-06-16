Install debian dependencies

    sudo apt-get install git supervisor python3 python3-pip nginx libjpeg-dev

Install python dependencies

    sudo pip3 install gunicorn falcon wiringpi

Install npm dependencies

    curl -sL https://deb.nodesource.com/setup_6.x | sudo bash -
    sudo apt-get install nodejs
    npm install bower -g
    
    cd web
    bower install ngtouch --save

Create symlinks

    $PR = /home/pi/raspi-car
    ln -sf $PR/conf/nginx/default /etc/nginx/sites-enabled/default
    ln -s $PR/conf/systemd/carweb.service /etc/systemd/system/carweb.service
    ln -s $PR/conf/systemd/livestream.service /etc/systemd/system/livestream.service
