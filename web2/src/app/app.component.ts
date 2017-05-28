import { Component } from '@angular/core';
import { Http, Response } from '@angular/http';

@Component({
  selector: 'my-app',
  templateUrl: 'templates/app.html',
})
export class AppComponent {

  name = 'Angular';

  x = 0;
  y = 0;
  scaledx = 0;
  scaledy = 0;
  thrust = 0;
  angle = 0;

  count = 0;
  local_status = "initialized";
  remote_status = "none";
  error = "";
  mode = "none";
  isError = false;
  lightsLight = false;

  hostname = "192.168.178.50";

  baseurl = "http://" + this.hostname + ":8087/car/";
  videourl = "http://" + this.hostname + ":8071/?action=stream";

  http: Http;

  constructor(http: Http) {
    this.http = http;
  }

  onPanStart(pan: any) {
    console.log('panstart');
    console.log(pan);
  }

  onPanMove(pan: any) {
    console.log(pan);
    this.x = pan.center.x;
    this.y = pan.center.y;

    this.scaledx = -1 + 2 * (pan.center.x - pan.target.offsetLeft) / pan.target.offsetWidth;
    this.scaledy = 1 - 2 * (pan.center.y - pan.target.offsetTop) / pan.target.offsetHeight;

    var len = Math.sqrt(this.scaledx * this.scaledx + this.scaledy * this.scaledy);

    this.thrust = Math.min(1, len);
    this.angle = Math.atan2(this.scaledx, this.scaledy);
  }

  move(thrust: number, angle: number) {
    this.http.get(this.baseurl + "f9/" + thrust + "/" + angle)
      .subscribe(data => {
        this.error = data.json();
        this.isError = false;
      }, error => {
        this.error = error;
        this.isError = true;
      });
  }


  lightsOn() {
    this.http.get(this.baseurl + "lightson")
      .subscribe(data => {
        this.error = data.json();
        this.isError = false;
      }, error => {
        this.error = error;
        this.isError = true;
      });
  };

  lightsOff() {
    this.http.get(this.baseurl + "lightsoff")
      .subscribe(data => {
        this.error = data.json();
        this.isError = false;
      }, error => {
        this.error = error;
        this.isError = true;
      });
  };

  switchLights() {
    if (this.lightsLight) {
      this.lightsLight = false;
      this.lightsOff();
    } else {
      this.lightsLight = true;
      this.lightsOn();
    }
  };


}
