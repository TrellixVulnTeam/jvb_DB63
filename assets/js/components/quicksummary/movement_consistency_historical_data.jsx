import React, { Component } from 'react';
import { connect } from 'react-redux';
import {Field, reduxForm } from 'redux-form';
import {Button} from "reactstrap";
import {Table, Column, Cell} from 'fixed-data-table-2';
import 'fixed-data-table-2/dist/fixed-data-table.css';
import Dimensions from 'react-dimensions';
import { StyleSheet, css } from 'aphrodite';
import moment from 'moment';

class MovementHistorical extends Component{
	constructor(props){
    super(props);
    this.renderTableColumns = this.renderTableColumns.bind(this);
    this.mcHistoricalData = this.mcHistoricalData.bind(this);
    this.dailyMC = this.dailyMC.bind(this);
    this.state = {
      myTableData: [{name:"% of Days User Get 300 Steps in the Hour"}]
    }

    var p = this.props.data;

    for(var key in p) {
      this.state.myTableData.push({name: key})
    }
  }

mcHistoricalData(score,status){
      if(status == "sleeping")
        return {background:'rgb(0,176,240)',color:'white'}
      else if(status == "inactive")
         return {background:'red',color:'white'}
      else if(status == "strength")
        return {background:"rgb(255,0,255)",color:'white'}
      else if (score >= 300 )
        return {background:'green', color:'white'};
}
dailyMC(score,status){
      if (score <= 5 )
        return {background:'green', color:'white'};
      else if (score > 5 && score <= 10)
        return {background:'yellow', color:'black'};
      else if (score > 10 )
        return {background:'red', color:'white'};
}
renderTableColumns(dateWiseData,category,classes="",start_date,end_date){
    let columns = [];
    let obj ={ 
            "dmc" :[],
            "total_steps" : [],
            "12:00 AM to 12:59 AM" : [],
            "01:00 AM to 01:59 AM" : [],
            "02:00 AM to 02:59 AM" : [],
            "03:00 AM to 03:59 AM" : [],
            "04:00 AM to 04:59 AM" : [],
            "05:00 AM to 05:59 AM" : [],
            "06:00 AM to 06:59 AM" : [],
            "07:00 AM to 07:59 AM" : [],
            "08:00 AM to 08:59 AM" : [],
            "09:00 AM to 09:59 AM" : [],
            "10:00 AM to 10:59 AM" : [],
            "11:00 AM to 11:59 AM" : [],
            "12:00 PM to 12:59 PM" : [],
            "01:00 PM to 01:59 PM" : [],
            "02:00 PM to 02:59 PM" : [],
            "03:00 PM to 03:59 PM" : [],
            "04:00 PM to 04:59 PM" : [],
            "05:00 PM to 05:59 PM" : [],
            "06:00 PM to 06:59 PM" : [],
            "07:00 PM to 07:59 PM" : [],
            "08:00 PM to 08:59 PM" : [],
            "09:00 PM to 09:59 PM" : [],
            "10:00 PM to 10:59 PM" : [],
            "11:00 PM to 11:59 PM" : [],
            "active_hours" : [],
            "inactive_hours" : [],
            "sleeping_hours" : [],
            "strength_hours" : [],
            "total_steps" : []
          };
        
        let start_dt = moment(this.props.start_date);
        let end_dt = moment(this.props.end_date);
        let duration = end_dt.diff(start_dt,'days');

    for(let [date,data] of Object.entries(dateWiseData)){
       for(let [key,value] of Object.entries(data[category])){
            if(key !== 'id' && key !== 'user_ql'){  
                if (key == 'movement_consistency'){
                            let mc = value;
                            if( mc != undefined && mc != "" && mc != "-"){
                                mc = JSON.parse(mc);                       
                                for(let [time,mCdata] of Object.entries(mc)){
                                  console.log('=====',mCdata);
                                      if(time == "inactive_hours"){
                                        obj[time].push({value:mc.inactive_hours,
                                                        style:this.dailyMC(value)});
                                        obj["dmc"].push({value:mc.inactive_hours,
                                                          style:this.dailyMC(mc.inactive_hours)});
                                      }
                                      else if (time == "active_hours")
                                        obj[time].push({value:mc.active_hours,
                                                        style:this.mcHistoricalData(value)});
                                      else if (time == "strength_hours")
                                        obj[time].push({value:mc.strength_hours,
                                                        style:this.mcHistoricalData(value)});
                                      else if (time == "sleeping_hours")
                                        obj[time].push({value:mc.sleeping_hours,
                                                        style:this.mcHistoricalData(value)});
                                      else if (time == "total_steps")
                                        obj[time].push({value:mc.total_steps,
                                                        style:this.mcHistoricalData(value)});
                                      else                                                                                       
                                        obj[time].push({value:mCdata.steps,
                                                        style:this.mcHistoricalData(mCdata.steps,mCdata.status)});                                    
                                }
                            }else{
                              for(let [time,mCdata] of Object.entries(obj)){
                                obj[time].push({value:'-',
                                                style:""});
                              }
                            }
                }        
            }
       }
    }

    let verbose_name = {
        "12:00 AM to 12:59 AM" : "12:00 AM to 12:59 AM",
        "01:00 AM to 01:59 AM" : "01:00 AM to 01:59 AM",
        "02:00 AM to 02:59 AM" : "02:00 AM to 02:59 AM",
        "03:00 AM to 03:59 AM" : "03:00 AM to 03:59 AM",
        "04:00 AM to 04:59 AM" : "04:00 AM to 04:59 AM",
        "05:00 AM to 05:59 AM" : "05:00 AM to 05:59 AM",
        "06:00 AM to 06:59 AM" : "06:00 AM to 06:59 AM",
        "07:00 AM to 07:59 AM" : "07:00 AM to 07:59 AM",
        "08:00 AM to 08:59 AM" : "08:00 AM to 08:59 AM",
        "09:00 AM to 09:59 AM" : "09:00 AM to 09:59 AM",
        "10:00 AM to 10:59 AM" : "10:00 AM to 10:59 AM",
        "11:00 AM to 11:59 AM" : "11:00 AM to 11:59 AM",
        "12:00 PM to 12:59 PM" : "12:00 PM to 12:59 PM",
        "01:00 PM to 01:59 PM" : "01:00 PM to 01:59 PM",
        "02:00 PM to 02:59 PM" : "02:00 PM to 02:59 PM",
        "03:00 PM to 03:59 PM" : "03:00 PM to 03:59 PM",
        "04:00 PM to 04:59 PM" : "04:00 PM to 04:59 PM",
        "05:00 PM to 05:59 PM" : "05:00 PM to 05:59 PM",
        "06:00 PM to 06:59 PM" : "06:00 PM to 06:59 PM",
        "07:00 PM to 07:59 PM" : "07:00 PM to 07:59 PM",
        "08:00 PM to 08:59 PM" : "08:00 PM to 08:59 PM",
        "09:00 PM to 09:59 PM" : "09:00 PM to 09:59 PM",
        "10:00 PM to 10:59 PM" : "10:00 PM to 10:59 PM",
        "11:00 PM to 11:59 PM" : "11:00 PM to 11:59 PM",
        "active_hours" : "Active Hours",
        "inactive_hours" : "Inactive Hours",
        "sleeping_hours" : "Sleeping Hours",
        "strength_hours" : "Strength Hours",
        "total_steps" : "Total Steps",
        "dmc":"Daily Movement consistency"
      }

    for(let [key,col] of Object.entries(obj)){
      let prcnt_active_steps = '';
      if(key != "active_hours" && key != "inactive_hours" &&
         key != "sleeping_hours" && key != "strength_hours" &&
         key != "total_steps" && key != "dmc"){
        let active_days = 0;
        for(let step of col){
          if(step.value >= 300)
            active_days += 1;
        }
        prcnt_active_steps = parseFloat((active_days / duration) * 100).toFixed(2) +"%";
      }
      col.splice(0, 0,{value:prcnt_active_steps,
                       style:""});
      console.log('++++++',col[0]);
       columns.push(
        <Column 
          header={<Cell className={css(styles.newTableHeader)}>{verbose_name[key]}</Cell>}
           cell={props => (
                    <Cell style={col[props.rowIndex].style} {...{'title':col[props.rowIndex]}} {...props} className={css(styles.newTableBody)}>
                      {col[props.rowIndex].value}
                    </Cell>
                  )}
          width ={128}
          
        />
      )
    }
  return columns;

}

 render(){
    const {height, width, containerHeight, containerWidth, ...props} = this.props;
    let rowsCount = this.state.myTableData.length;
    return(
      <div>
       <div>
       <Table
            rowsCount={rowsCount}
            rowHeight={65}
            headerHeight={90}
            width={containerWidth}
            height={containerHeight}
            touchScrollEnabled={true}
            {...props}>
            <Column
              header={<Cell className={css(styles.newTableHeader)}>Movement Consistency Historical Data</Cell>}

              cell={props => (
                <Cell {...{'title':this.state.myTableData[props.rowIndex].name}} {...props} className={css(styles.newTableBody)}>
                  {this.state.myTableData[props.rowIndex].name}
                </Cell>
                )}

              width={150}
              fixed={true}
            />
            {this.renderTableColumns(this.props.data,"steps_ql")}
         
          </Table>
      </div>
      </div>

      );
  }

}

const styles = StyleSheet.create({
  newTableHeader: {
  	textAlign:'center', 
    border: 'none',
    fontFamily:'Proxima-Nova',
    fontStyle:'normal',
    fontSize:'15px'
  },
  newTableBody:{
  	textAlign:'center',
    fontSize: '16px', 
    border: 'none',
    fontFamily:'Proxima-Nova',
    fontStyle:'normal'
  }
});

export default Dimensions({
  getHeight: function(element) {
    return window.innerHeight - 200;
  },
  getWidth: function(element) {
    var widthOffset = window.innerWidth < 1024 ? 0 : 3;
    return window.innerWidth - widthOffset;
  }
})(MovementHistorical);