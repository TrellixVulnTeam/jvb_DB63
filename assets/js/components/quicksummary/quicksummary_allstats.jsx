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
import User from './user_inputs';
import Dimensions from 'react-dimensions';

 class AllStats extends Component{
  constructor(props) {
    super(props);
    this.renderTableColumns = this.renderTableColumns.bind(this);
    // this.renderTableAttrColumn = this.renderTableAttrColumn.bind(this);

    this.state = {
      myTableData: [
        {name: 'Alcohol Per Day'},
        {name: 'Alcohol Per Week'},
        {name: 'Avg Cadence'}, 
        {name: 'Avg Power'},
        {name: 'Avg Speed'},        
        {name: 'Asvg Speed Per Mile'},
        {name: 'Average Heartrate'},
        {name: 'Avg Heart Rate Grade'},
        {name: 'Chia Seeds consumed during Workout'},
        {name: 'Dew Point'},
        {name: 'Distance'},
        {name: 'Drug'},
        {name: 'Drug Consumed'},
        {name: 'Effort Level'},
        {name: 'Elevation Gain'},
        {name: 'Elevation Loss'},
        {name: 'Exercise Consistency '},
        {name: 'Exercise Fifteen More'},        
        {name: 'Fast Before Workout'},
        {name: 'Heart Rate Variability Grade'},
        {name: 'HRR'},
        {name: 'HRR Beats Lowered'},
        {name: 'HRR Start Point'},
        {name: 'Humidity'},
        {name: 'Maximum Elevation Workout'},  
        {name: 'Medication'},
        {name: 'Minutes Walked Before Workout'},
        {name: 'Percent Breath through Nose During Workout'},
        {name: 'OverAll Workout Grade'},
        {name: 'Pace'},
        {name: 'Pain'},
        {name: 'Pain Area'},
        {name: 'Running Cadence'},
        {name: 'Sick '}, 
        {name: 'Sleep Resting Hr Last Night'},
        {name: 'Smoke Substance'},
        {name: 'Stress Level'},
        {name: 'Temperature'},          
        {name: 'Temperature Feels Like'},
        {name: 'TimeWatch Paused Workout'},
        {name: 'Vo2 Max'},              
        {name: 'Water Consumed during Workout'},
        {name: 'Wind'},
        {name: 'Workout Comment'},
        {name: 'Workout Duration'},
        {name: 'Workout Duration Grade'},
        {name: 'Workout Easy Hard'},
        {name: 'Workout Effort Level Grade'},
        {name: 'Workout Elapsed Time'},
        {name: 'Workout Location'},
        {name: 'Workout Time'},
        {name: 'Workout Type'},
        {name: 'Diet Type'},
        {name: 'Non Processed Food'}, 
        {name: 'percentage Non Processed Food'},
        {name: 'Percentage Non Processed Food Grade'},
        {name: 'Alcoholic Drink Per Week Grade'},
        {name: 'Avg Sleep Per Night Grade'},
        {name: 'Exercise Consistency Grade'},
        {name: 'Movement Consistency Grade'},
        {name: 'Movement Non Exercise steps Grade'},
        {name: 'Overall Truth Grade'},
        {name: 'Overall Truth Health Gpa'},
        {name: 'Overall Workout Grade'},
        {name: 'Penalty'},
        {name: 'percent NonProcessed Food Consumed Grade'},
        {name: 'Awake Time'},
        {name: 'Deep Sleep'},
        {name: 'Light Sleep'},
        {name: 'Sleep Aid'},
        {name: 'Sleep Awake Time'},
        {name: 'Sleep Bed Time'},
        {name: 'Sleep Per User Input'},
        {name: 'Sleep Per Wearable'},
        {name: 'Exercise Steps'},
        {name: 'Floor Climed'}, 
        {name: 'Floor Decended'},
        {name: 'Movement Consistency'},
        {name: 'Non Exercise Steps'},
        {name: 'Total Steps'},
        {name: 'pace per 100 yard'},
        {name: 'Total Strokes'},         
                      
      ],
    };
  }

  renderTableColumns(dateWiseData,category=undefined,classes=""){
    let columns = [];
    for(let [date,data] of Object.entries(dateWiseData)){
      let all_data = [];
      let keys = [];
      for(let cat of Object.keys(data).sort()){
        if (cat !== "created_at" &&
          cat !== "updated_at" &&
          cat !== "user"){
          for(let key of Object.keys(data[cat]).sort()){
            if(key !== 'id' && key !== 'user_ql'){
              all_data.push(data[cat][key]);
              keys.push(key);
            }
          }
        }
      }
      columns.push(
        <Column 
          header={<Cell>{date}</Cell>}
              cell={props => (
                    <Cell {...props}>
                      {all_data[props.rowIndex]}
                    </Cell>
                  )}
              width={132}
        />
      )
      console.log(keys);
    }
    return columns;
  }
  render(){
    let rowsCount = this.state.myTableData.length;
		return(
  

<div>
</div>
			);
	
}
}
export default AllStats;
