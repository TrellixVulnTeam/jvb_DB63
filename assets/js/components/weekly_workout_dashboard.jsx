import React, { Component } from 'react';
import { withRouter, Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import {Field, reduxForm } from 'redux-form';
import axios from 'axios';
import axiosRetry from 'axios-retry';
import moment from 'moment';
import FontAwesome from "react-fontawesome";
import { Collapse, Navbar, NavbarToggler, 
         NavbarBrand, Nav, NavItem, NavLink,
        Button,Popover,PopoverBody,Form,FormGroup,FormText,Label,Input} from 'reactstrap';
import NavbarMenu from './navbar';
import fetchWeeklyWorkoutData from '../network/weekly_workout';


axiosRetry(axios, { retries: 3});
var CalendarWidget = require('react-calendar-widget');
var ReactDOM = require('react-dom');

class WorkoutDashboard extends Component{
	constructor(props) {
    super(props);
	    this.state = {
	    	calendarOpen:false,
		   	selectedDate:new Date(),
		   	weekly_data:{},
	    }
	    this.toggleCalendar = this.toggleCalendar.bind(this);
	    this.renderAddDate = this.renderAddDate.bind(this);
		this.renderRemoveDate = this.renderRemoveDate.bind(this);
		this.toggleCalendar = this.toggleCalendar.bind(this);
		this.successWeeklyWorkoutData = this.successWeeklyWorkoutData.bind(this);
		this.errorWeeklyWorkoutData = this.errorWeeklyWorkoutData.bind(this);
		this.processDate = this.processDate.bind(this);
		this.renderTable = this.renderTable.bind(this);
		this.gpascoreDecimal = this.gpascoreDecimal.bind(this);
		this.renderTime = this.renderTime.bind(this);
	}
	successWeeklyWorkoutData(data){
		this.setState({
			weekly_data:data.data
		});
  	}
  	errorWeeklyWorkoutData(error){
		console.log(error.message);
  	}
	renderAddDate(){
		/*It is forward arrow button for the calender getting the next day date*/
		var today = this.state.selectedDate;
		var tomorrow = moment(today).add(1, 'days');
		this.setState({
			selectedDate:tomorrow.toDate()
		},()=>{
			fetchWeeklyWorkoutData(this.successWeeklyWorkoutData,this.errorWeeklyWorkoutData,this.state.selectedDate);
		});
	}
	renderRemoveDate(){
		/*It is backward arrow button for the calender getting the last day date*/
		var today = this.state.selectedDate;
		var tomorrow = moment(today).subtract(1, 'days');
		this.setState({
			selectedDate:tomorrow.toDate()
		},()=>{
			fetchWeeklyWorkoutData(this.successWeeklyWorkoutData,this.errorWeeklyWorkoutData,this.state.selectedDate);
		});
	}
	toggleCalendar(){
		//Toggle of calander icon.
	    this.setState({
	      calendarOpen:!this.state.calendarOpen
	    });
    }
     processDate(selectedDate){
		this.setState({
			selectedDate:selectedDate,
			calendarOpen:!this.state.calendarOpen,
		},()=>{
			fetchWeeklyWorkoutData(this.successWeeklyWorkoutData,this.errorWeeklyWorkoutData,this.state.selectedDate);
		});
	}
	componentDidMount(){
		fetchWeeklyWorkoutData(this.successWeeklyWorkoutData,this.errorWeeklyWorkoutData,this.state.selectedDate);
	}
	gpascoreDecimal(gpa){
		let value;
		let x = gpa;
		if( x !=  null && x != undefined){
		    value =parseFloat(x).toFixed(2) + " %";
		 }
		 else{
		  value = "";
		 }
		return value;
	}
	renderTime(value){
		// This function will devide the seconds to hh:mm:ss format.
		var time;
		if(value){
			if(value>0){
				var sec_num = parseInt(value); 
			    var hours   = Math.floor(sec_num / 3600);
			    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
			    var seconds = sec_num - (hours * 3600) - (minutes * 60);

			    if (hours   < 10) {hours   = "0"+hours;}
			    if (minutes < 10) {minutes = "0"+minutes;}
			    if (seconds < 10) {seconds = "0"+seconds;}
			    time = hours+':'+minutes;
			}
		}
		else if(value == 0 || value == null){
			time = "00:00";
		}
		return time;
	}
	renderTable(weekly_data){
		let tr_values = [];
		let td_keys = ["workout_type","days_with_activity","percent_of_days","duration","workout_duration_percent","average_heart_rate","duration_in_aerobic_range",
		"percent_aerobic","duration_in_anaerobic_range","percent_anaerobic","duration_below_aerobic_range","percent_below_aerobic",
		"duration_hrr_not_recorded","percent_hrr_not_recorded","distance_meters"];
		let td_keys1 = ["no_activity","days_no_activity","percent_days_no_activity","","","","","","","","","","","","",];
		for(let [key,value] of Object.entries(weekly_data)){
			let td_values = [];
			if(key != "extra"){
				for(let key1 of td_keys){
					if(key1 == "percent_of_days" || key1 == "workout_duration_percent" ||
					 key1 == "percent_aerobic" || key1 == "percent_anaerobic" ||
					  key1 == "percent_below_aerobic" || key1 == "percent_hrr_not_recorded"){
						td_values.push(<td>{this.gpascoreDecimal(value[key1])}</td>)
					}
					else if(key1 == "duration" || key1 == "duration_in_aerobic_range" ||
					 key1 == "duration_in_anaerobic_range" || key1 == "duration_below_aerobic_range" ||
					  key1 == "duration_hrr_not_recorded"){
						td_values.push(<td>{this.renderTime(value[key1])}</td>)
					}
					else{
						td_values.push(<td>{value[key1]}</td>)
					}
				}
			}
			else{
				for(let key2 of td_keys1){
					if(key2 == "percent_days_no_activity"){
						td_values.push(<td>{this.gpascoreDecimal(value[key2])}</td>)
					}
					else if(key2 == "no_activity"){
						td_values.push(<td>No Activity</td>)
					}
					else{
						td_values.push(<td>{value[key2]}</td>)
					}
				}
			}
			tr_values.push(<tr>{td_values}</tr>)
		}
		return tr_values;
	}
	render(){
		return(
				<div className = "container-fluid">
					<NavbarMenu title = {<span style = {{fontSize:"22px"}}>
					Weekly Workout Summary Report
					</span>} />

					<div className = "cla_center">
						<span>
							<span onClick = {this.renderRemoveDate} style = {{marginLeft:"30px",marginRight:"14px"}}>
								<FontAwesome
			                        name = "angle-left"
			                        size = "2x"
				                />
							</span> 
			            	<span id="navlink" onClick={this.toggleCalendar} id="gd_progress">
			                    <FontAwesome
			                        name = "calendar"
			                        size = "2x"
			                    />
			                    <span style = {{marginLeft:"20px",fontWeight:"bold",paddingTop:"7px"}}>{moment(this.state.selectedDate).format('MMM DD, YYYY')}</span>  
		                	</span>
		                	<span onClick = {this.renderAddDate} style = {{marginLeft:"14px"}}>
								<FontAwesome
			                        name = "angle-right"
			                        size = "2x"
				                />
							</span> 
			            	<Popover
					            placement="bottom"
					            isOpen={this.state.calendarOpen}
					            target="gd_progress"
					            toggle={this.toggleCalendar}>
				                <PopoverBody className="calendar2">
				                <CalendarWidget  onDaySelect={this.processDate}/>
				                </PopoverBody>
			                </Popover>
	                	</span>
		        	</div>
					 <div className = "row justify-content-center hr_table_padd">
							<div className = "table table-responsive">
				          	    <table className = "table table-striped table-bordered ">
									<tr>
										<th>Workout Type</th>
										<th>Avg # Of Days With Activity</th>
										<th>% of Days</th>
										<th>Avg. Workout Duration (hh:mm)</th>
										<th>% of Total Duration</th>
										<th>Avg Heart Rate</th>
										<th>Avg Aerobic Duration (hh:mm)</th>
										<th>Avg % Aerobic</th>
										<th>Avg Anaerobic Duration (hh:mm)</th>
										<th>Avg % Anaerobic</th>
										<th>Avg Below Aerobic Duration (hh:mm)</th>
										<th>Avg % Below Aerobic</th>
										<th>Avg HR Not Recorded Duration (hh:mm)</th>
										<th>Avg % HR Not Recorded</th>
										<th>Avg Distance (In Miles)</th>
									</tr>
									<tbody>
									{this.renderTable(this.state.weekly_data)}	
									</tbody>
								</table>
							</div>
						</div>
					
				</div>
			);
	}
}
export default WorkoutDashboard;