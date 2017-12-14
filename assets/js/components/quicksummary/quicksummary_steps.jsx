import React, { Component } from 'react';
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

	 this.state = {
      myTableData: [
        {name: 'Non Exercise Steps'},
        {name: 'Exercise Steps'},
        {name: 'Total Steps'},
        {name: 'Floor Climed'}, 
        {name: 'Floor Decended'},
        {name: 'Movement Consistency'}                     
      ],
    };
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
                        }
                    }
                    else{
						all_data.push(value);
                    }
				}
			}

			columns.push(
				<Column 
					header={<Cell className={css(styles.newTableHeader)}>{date}</Cell>}
			        cell={props => (
				            <Cell {...props} className={css(styles.newTableBody)}>
				              {all_data[props.rowIndex]}
				            </Cell>
				          )}
			        width={200}
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
			 <div className="quick3"
			  >
			 <Table
		        rowsCount={rowsCount}
		        rowHeight={100}
		        headerHeight={50}
		        width={containerWidth}
        		height={containerHeight}
        		touchScrollEnabled={true}
        		{...props}>
		        <Column
		          header={<Cell className={css(styles.newTableHeader)}>Steps</Cell>}
		          cell={props => (
		            <Cell {...props} className={css(styles.newTableBody)}>
		              {this.state.myTableData[props.rowIndex].name}
		            </Cell>
		          )}
		          width={167}
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
    color: '#111111',
    fontSize: '18px',   
    border: 'none',
    fontFamily:'Proxima-Nova',
    fontStyle:'normal'
  },
  newTableBody:{
    color: '#5e5e5e',
    fontSize: '16px', 
    border: 'none',
    fontFamily:'Proxima-Nova',
    fontStyle:'normal'
  }
});

export default Dimensions({
  getHeight: function(element) {
    return window.innerHeight - 235;
  },
  getWidth: function(element) {
    var widthOffset = window.innerWidth < 1024 ? 0 : 3;
    return window.innerWidth - widthOffset;
  }
})(Steps);