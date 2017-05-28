import { Component, Inject } from '@angular/core';
import { Http, Response } from '@angular/http';
import { DOCUMENT } from '@angular/platform-browser';

@Component({
  selector: 'my-app',
  templateUrl: 'templates/app.html',
})
export class AppComponent {

  name = 'Angular';

  scaledx: number = 0;
  scaledy: number = 0;
  thrust: number = 0;
  angle: number = 0;

  count: number = 0;
  local_status = "initialized";
  remote_status = "none";
  error = "";
  mode = "none";
  isError = false;
  lightsLight = false;

  hostname = "";
  baseurl = "";
  videourl = "";

  http: Http;

  constructor(http: Http, @Inject(DOCUMENT) private document: any) {
    this.http = http;
    this.hostname = document.location.hostname;

    this.baseurl = "http://" + this.hostname + ":8087/car/";
    this.videourl = "http://" + this.hostname + ":8071/?action=stream";

  }

  onPanStart(pan: any) {
    console.log('panstart');
  }

  onPanStop(touch: any) {
    console.log('panstop');
    this.halt();
  }

  halt() {
    this.local_status = "stop";
    this.http.get(this.baseurl + "st")
      .subscribe(data => {
        this.remote_status = "" + data.status;
        this.isError = false;
      }, error => {
        this.error = error;
        this.isError = true;
      });
    this.count = this.count - 1;
  };

  onPanMove(pan: any) {
    let x = pan.center.x;
    let y = pan.center.y;

    // map the center of the pan action to the interval [-1,1]x[-1,1]
    this.scaledx = -1 + 2 * (pan.center.x - pan.target.offsetLeft) / pan.target.offsetWidth;
    this.scaledy = 1 - 2 * (pan.center.y - pan.target.offsetTop) / pan.target.offsetHeight;

    let length = Math.sqrt(this.scaledx * this.scaledx + this.scaledy * this.scaledy);

    this.thrust = Math.min(1, length);
    this.angle = Math.atan2(this.scaledx, this.scaledy);

    console.log("panmove ${this.thrust} ${this.angle}");

    this.move(this.thrust, this.angle);
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
