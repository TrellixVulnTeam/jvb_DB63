import React, { Component } from 'react';
import { connect } from 'react-redux';
import {Field, reduxForm } from 'redux-form';
import {Table,Button} from "reactstrap";

 function renderTableRows(dateWiseData,category,field,classes=""){
	let elements = [];
	for(let [date,data] of Object.entries(dateWiseData)){
		if(field === "created_at"){
			elements.push(
				<th key={date} className={classes}>{date}</th>
			);	
		}else{
			elements.push(
				<td key={date} className={classes}>{data[category][field]}</td>
			);
		}
	}
	return elements;
}

export class Swim extends Component{
	constructor(props){
	super(props);
	this.swimScroll=this.swimScroll.bind(this);

}
componentDidMount() {
	document.getElementById('tBodySwim').addEventListener('scroll', this.swimScroll);
}


  swimScroll(e) { 
        var tbody = document.getElementById("tBodySwim");
        document.getElementById("tHeadSwim").style.left = '-'+tbody.scrollLeft+'px';
        document.querySelector('#tHeadSwim th:nth-child(1)').style.left = tbody.scrollLeft+'px';
        var trLength = document.querySelector('#tBodySwim').children;
        for (var i = 0; i < trLength.length; i++) {
        	trLength[i].querySelector('#tBodySwim td:nth-child(1)').style.left = tbody.scrollLeft+'px';
        }

    };
	render(){
	return(
	 <div className="quick3">
	
	     <table className="table table-responsive quick4">
	     
	     <thead id="tHeadSwim">
	          <tr className="quick8"> 
	         	<th>Swim Stats</th>
			    {renderTableRows(this.props.data,"swim_stats_ql","created_at")}
			  </tr>
			  </thead>
			<tbody id="tBodySwim" onScroll={this.swimScroll}>
			  <tr>
		       	<td>Overall Truth Grade</td>
		        {renderTableRows(this.props.data,"swim_stats_ql","pace_per_100_yard")}
	          </tr>

	          <tr className="quick9">
		        <td>Total Strokes</td>
		        {renderTableRows(this.props.data,"swim_stats_ql","total_strokes")}
	          </tr>
	          </tbody>
         </table>
         </div>
	);
}
}
export default Swim;