import {Component, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {CEServiceService} from "../../Services/ceservice.service";
import {Options} from "@angular-slider/ngx-slider";
import {CanvasJS} from "../../../assets/canvasjs.angular.component";
import { ViewChild } from '@angular/core'
import {WebSocketServiceService} from "../../Services/web-socket-service.service";
import {ContratService} from "../../Services/contrat.service";
import {Contrat} from "../../Modals/Contrat";
import {FormGroup} from "@angular/forms";
@Component({
  selector: 'app-cesimulator',
  templateUrl: './cesimulator.component.html',
  styleUrls: ['./cesimulator.component.scss']
})
export class CESimulatorComponent implements OnInit,OnChanges {
  u:Object
  p:Object
  contrat=new Contrat();
  w:any;
  test: string ;
  testamount: any;
  testage: any;
  testprime:any;
  testn: any;
  testi: any;
  vie: number;
  diff:string;



  constructor(private service:ContratService) {

  }

  ngOnInit(): void {

  }
  ngOnChanges(changes: SimpleChanges):void{

  }

  simulate() {


    this.u = null;
    this.p = null;
    this.test = null;
    this.testage = null;
    this.testamount = null;
    this.testprime = null;


    this.service.getfraud(this.contrat.claimamount, this.contrat.witenesses, this.contrat.injuries, this.contrat.vehicules_involved, this.contrat.umbrella,
      this.contrat.nb_police).subscribe(res => {
      console.log(res);
      this.u = res;
    });




  }
  clean(){};
}
