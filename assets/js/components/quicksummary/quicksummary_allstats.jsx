import React, { Component } from 'react';
import { connect } from 'react-redux';
import {Field, reduxForm } from 'redux-form';
import {Table,Button} from "reactstrap";
import Grades from './quicksummary_grades';
import Swim from './quicksummary_swim';
import Bike from './quicksummary_bike';
import Steps from './quicksummary_steps';
import Sleep from './quicksummary_sleep';
import Food from './quicksummary_food';  
import Alcohol from './quicksummary_alocohol';
import Exercise from './quicksummary_exercise';

 const AllStats =(props)=>{
		return(


 <div>
                   <Grades data={props.data}/>
                   <Swim data={props.data}/>
                   <Bike data={props.data}/>
                   <Steps data={props.data}/>
                   <Sleep data={props.data}/>
                   <Food data={props.data}/>
                   <Alcohol data={props.data}/>
                   <Exercise data={props.data}/>
                  
</div>

			);
	
}
export default AllStats;
