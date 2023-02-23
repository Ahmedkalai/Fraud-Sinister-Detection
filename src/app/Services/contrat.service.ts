import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {Contrat} from "../Modals/Contrat";

@Injectable({
  providedIn: 'root'
})
export class ContratService {

  url : string = 'http://localhost:5000';
  constructor(private http: HttpClient) { }

  getfraud(claimamount:number, witenesses:number, injuries:number, vehicules_involved:number, umbrella:number,
  nb_police:number){
    return this.http.get(`${this.url}/fraud/${nb_police}/${umbrella}/${vehicules_involved}/${injuries}/${witenesses}/${claimamount}`)
  }




}
