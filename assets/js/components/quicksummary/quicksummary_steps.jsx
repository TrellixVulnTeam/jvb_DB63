import React, { Component } from 'react';
import moment from 'moment';
import { connect } from 'react-redux';
import {Field, reduxForm } from 'redux-form';
import {Button} from "reactstrap";
import {Table, Column, Cell} from 'fixed-data-table-2';
import 'fixed-data-table-2/dist/fixed-data-table.css';
import Dimensions from 'react-dimensions';
import { StyleSheet, css } from 'aphrodite';

class Steps extends Component{

	constructor(props){
	super(props);
	 this.renderTableColumns = this.renderTableColumns.bind(this);
	 this.getDayWithDate = this.getDayWithDate.bind(this);

	 this.state = {
      myTableData: [
	    {name: 'Movement Consistency'},
        {name: 'Non Exercise Steps'},
        {name: 'Exercise Steps'},  
        {name: 'Total Steps'},
        {name: 'Floors Climed'}
      ],
    };
  }
getDayWithDate(date){
   let d = moment(date,'M-D-YY');
   let days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
   let dayName = days[d.day()] ;
   return date +"\n"+ dayName;
  }
renderTableColumns(dateWiseData,category,classes=""){
		let columns = [];
		for(let [date,data] of Object.entries(dateWiseData)){
			let all_data = [];

			for(let [key,value] of Object.entries(data[category])){
				if(key !== 'id' && key !== 'user_ql'){  
					if (key == 'movement_consistency'){
	                    let mc = value;
	                    if( mc != undefined && mc != "" && mc != "-"){
	                        mc = JSON.parse(mc);
	                        all_data.push(mc.inactive_hours);
	                	}else{
	                		all_data.push('-')
	                	}
	            	}
	                else{
						value += '';
		             	var x = value.split('.');
		            	var x1 = x[0];
			            var x2 = x.length > 1 ? '.' + x[1] : '';
			            var rgx = /(\d+)(\d{3})/;
			            while (rgx.test(x1)) {
				        x1 = x1.replace(rgx, '$1' + ',' + '$2');
			            }
					    all_data.push(x1 + x2);                  
					}
				}
			}

			columns.push(
				<Column 
					header={<Cell className={css(styles.newTableHeader)}>{this.getDayWithDate(date)}</Cell>}
			        cell={props => (
				            <Cell {...{'title':all_data[props.rowIndex]}} {...props} className={css(styles.newTableBody)}>
				              {all_data[props.rowIndex]}
				            </Cell>
				          )}
			        width={100}
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
		        rowHeight={50}
		        headerHeight={60}
		        width={containerWidth}
        		height={containerHeight}
        		touchScrollEnabled={true}
        		{...props}>
		        <Column
		          header={<Cell className={css(styles.newTableHeader)}>Steps</Cell>}
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
    color: '#111111',   
    border: 'none',
    fontFamily:'Proxima-Nova',
    fontStyle:'normal'
  },
  newTableBody:{
  	textAlign:'center',
    color: '#5e5e5e',
    fontSize: '16px', 
    border: 'none',
    fontFamily:'Proxima-Nova',
    fontStyle:'normal'
  }
});

export default Dimensions({
  getHeight: function(element) {
    return window.innerHeight - 172;
  },
  getWidth: function(element) {
    var widthOffset = window.innerWidth < 1024 ? 0 : 3;
    return window.innerWidth - widthOffset;
  }
})(Steps);