import React,{ Component } from 'react';
import { withRouter, Link } from 'react-router-dom';
import {connect} from 'react-redux';
import FontAwesome from "react-fontawesome";
import { Collapse, Navbar, NavbarToggler, 
         NavbarBrand, Nav, NavItem, NavLink,
        Button,Popover,PopoverBody,Form,FormGroup,FormText,Label,Input} from 'reactstrap';
import PropTypes from 'prop-types';
import moment from 'moment';

import {renderLeaderBoardFetchOverlay,renderLeaderBoard2FetchOverlay,renderLeaderBoard3FetchOverlay,renderLeaderBoardSelectedDateFetchOverlay} from './leaderboard_healpers';
import { getGarminToken,logoutUser} from '../network/auth';
import fetchLeaderBoard from '../network/leaderBoard';
import AllRank_Data from "./leaderboard_allrank";



var CalendarWidget = require('react-calendar-widget');  
var ReactDOM = require('react-dom');
const categoryMeta = {
	"Overall Health GPA":{
		short_name:"oh_gpa",
		url_name:"overall-health-gpa"
	},
	"Alcohol Drink":{
		short_name:"alcohol_drink",
		url_name:"alcohol-drink"
	},
	"Average Sleep":{ 
		short_name:"avg_sleep",
		url_name:"avg-sleep"
	},
	"Percent Unprocessed Food":{
		short_name:"prcnt_uf",
		url_name:"percent-unprocessed-food"
	},
	"Total Steps":{
		short_name:"total_steps",
		url_name:"total-steps"
	},
	"Movement Consistency":{
		short_name:"mc",
		url_name:"movement-consistency"
	},
	"Exercise Consistency":{
		short_name:"ec",
		url_name:"exercise-consistency"
	},
	"Awake Time":{
		short_name:"awake_time",
		url_name:"awake-time"
	},
	"Resting Heart Rate":{
		short_name:"resting_hr",
		url_name:"resting-heart-rate"
	},
	"Deep Sleep":{
		short_name:"deep_sleep",
		url_name:"deep-sleep" 
	},
	"Movement Non Exercise GPA":{
		short_name:"mne_gpa",
		url_name:"movement-non-exercise-gpa"
	},
	"Floor Climbed":{
		short_name:"floor_climbed",
		url_name:"floor-climbed"
	},
};
const catagory = ["oh_gpa","alcohol_drink","avg_sleep","prcnt_uf","total_steps","mc","ec","awake_time","resting_hr","deep_sleep","mne_gpa","floor_climbed",];
const duration = ["week","today","yesterday","year","month","custom_range"];
let durations_captilize = {"today":"Today","yesterday":"Yesterday","week":"Week","month":"Month","year":"Year",};
class LeaderBoard extends Component{
	constructor(props){
		super(props);
		let rankInitialState = {}
    for (let catg of catagory){
        let catInitialState = {}
        for(let dur of duration){
	          let userRank = {
	            'user_rank':{
	              category:'',
	              rank:'',
	              username:'', 
	              score:''
	            },
	            "all_rank":[
	            ]
	        };
         catInitialState[dur] = userRank;
        }
        rankInitialState[catg] = catInitialState;
    };
		this.state = {
			selectedDate:new Date(),
			lb1_start_date:'',
	        lb1_end_date:'',
	        lb2_start_date:'',
	        lb2_end_date:'',
	        lb3_start_date:'',
	        lb3_end_date:'',
	        fetching_lb1:false,
	        fetching_lb2:false,
	        fetching_lb3:false,
	        fetching_lb4:false,
	        dateRange1:false,
	        dateRange2:false,
	        dateRange3:false,
			calendarOpen:false,
			isOpen:false,
			ranking_data:rankInitialState,
			duration_date:{
				"week":"",
				"today":"",
				"yesterday":"",
				"year":"",
				"month":"",
			
			},
		}
		this.toggleCalendar = this.toggleCalendar.bind(this);
		this.handleLogout = this.handleLogout.bind(this);
		this.toggle = this.toggle.bind(this);
		this.successLeaderBoard = this.successLeaderBoard.bind(this);
		this.successLeaderBoard = this.successLeaderBoard.bind(this);
		this.processDate = this.processDate.bind(this);
		this.renderTablesTd = this.renderTablesTd.bind(this);
		this.onSubmitDate1 = this.onSubmitDate1.bind(this);
		this.onSubmitDate2 = this.onSubmitDate2.bind(this);
		this.onSubmitDate3 = this.onSubmitDate3.bind(this);
		this.toggleDate1 = this.toggleDate1.bind(this);
		this.toggleDate2 = this.toggleDate2.bind(this);
		this.toggleDate3 = this.toggleDate3.bind(this);
		this.handleChange = this.handleChange.bind(this);
		this.headerDates = this.headerDates.bind(this);
		this.renderLeaderBoardFetchOverlay = renderLeaderBoardFetchOverlay.bind(this);
		this.renderLeaderBoard2FetchOverlay = renderLeaderBoard2FetchOverlay.bind(this);
		this.renderLeaderBoard3FetchOverlay = renderLeaderBoard3FetchOverlay.bind(this);
		this.renderLeaderBoardSelectedDateFetchOverlay = renderLeaderBoardSelectedDateFetchOverlay.bind(this);
	}
	successLeaderBoard(data){
		this.setState({
			ranking_data:data.data,
			duration_date:data.data.duration_date,
			fetching_lb1:false,
	        fetching_lb2:false,
	        fetching_lb3:false,
	        fetching_lb4:false,
		});
	}

	errorLeaderBoard(error){
		console.log(error.message);
		this.setState({
			fetching_lb1:false,
	        fetching_lb2:false,
	        fetching_lb3:false,
	        fetching_lb4:false,
    	});
	}
	processDate(selectedDate){
		this.setState({
			selectedDate:selectedDate,
			fetching_lb4:true,
			calendarOpen:!this.state.calendarOpen,
		},()=>{fetchLeaderBoard(this.successLeaderBoard,this.errorLeaderBoard,this.state.selectedDate);
		});
	}
	onSubmitDate1(event){
    event.preventDefault();
    this.setState({
      dateRange1:!this.state.dateRange1,
      fetching_lb1:true
    },()=>{
        let custom_ranges = [];
        if(this.state.lb2_start_date && this.state.lb2_end_date){
            custom_ranges.push(this.state.lb2_start_date);
            custom_ranges.push(this.state.lb2_end_date);
        }
         if(this.state.lb3_start_date && this.state.lb3_end_date){
            custom_ranges.push(this.state.lb3_start_date);
            custom_ranges.push(this.state.lb3_end_date);
        }
        custom_ranges.push(this.state.lb1_start_date);
        custom_ranges.push(this.state.lb1_end_date);
      fetchLeaderBoard(this.successLeaderBoard,this.errorLeaderBoard,this.state.selectedDate,custom_ranges);
    });
  }
   onSubmitDate2(event){
    event.preventDefault();
    this.setState({
      dateRange2:!this.state.dateRange2,
      fetching_lb2:true,
    },()=>{
         let custom_ranges = [];
        if(this.state.lb1_start_date && this.state.lb1_end_date){
            custom_ranges.push(this.state.lb1_start_date);
            custom_ranges.push(this.state.lb1_end_date);
        }
         if(this.state.lb3_start_date && this.state.lb3_end_date){
            custom_ranges.push(this.state.lb3_start_date);
            custom_ranges.push(this.state.lb3_end_date);
        }

        custom_ranges.push(this.state.lb2_start_date);
        custom_ranges.push(this.state.lb2_end_date);
      fetchLeaderBoard(this.successLeaderBoard,this.errorLeaderBoard,this.state.selectedDate,custom_ranges);
    });
  }
 onSubmitDate3(event){
    event.preventDefault();
    this.setState({
      dateRange3:!this.state.dateRange3,
      fetching_lb3:true,
    },()=>{
         let custom_ranges = [];
         if(this.state.lb1_start_date && this.state.lb1_end_date){
            custom_ranges.push(this.state.lb1_start_date);
            custom_ranges.push(this.state.lb1_end_date);
        }
        if(this.state.lb2_start_date && this.state.lb2_end_date){
            custom_ranges.push(this.state.lb2_start_date);
            custom_ranges.push(this.state.lb2_end_date);
        }
        custom_ranges.push(this.state.lb3_start_date);
        custom_ranges.push(this.state.lb3_end_date);
      fetchLeaderBoard(this.successLeaderBoard,this.errorLeaderBoard,this.state.selectedDate,custom_ranges);
    });
  }
	componentDidMount(){
		fetchLeaderBoard(this.successLeaderBoard,this.errorLeaderBoard,this.state.selectedDate);
	}
	toggle() {
	    this.setState({
	      isOpen: !this.state.isOpen,
	    });
  	}
	toggleCalendar(){
	    this.setState({
	      calendarOpen:!this.state.calendarOpen
	    });
    }
    toggleDate1(){
    this.setState({
      dateRange1:!this.state.dateRange1
    });
   }
 toggleDate2(){
    this.setState({
      dateRange2:!this.state.dateRange2
    });
   }
    toggleDate3(){
    this.setState({
      dateRange3:!this.state.dateRange3
    });
   }
    handleLogout(){
    	this.props.logoutUser(this.onLogoutSuccess);
  	}
  	handleChange(event){
      const target = event.target;
      const value = target.value;
      const name = target.name;
      this.setState({
        [name]: value
      });
    }
    headerDates(value){
    let str = value;
            let d = str.split(" ");
            let d1 = d[0];
            let date1 =moment(d1).format('MMM DD, YYYY');
            let d2 = d[2];
            let date2 =moment(d2).format('MMM DD, YYYY');
            let date = date1 + ' to ' + date2;
            return date;
	}
  	renderTablesTd(value,value5){
  		let category = "";
	  	let durations = [];
	  	let scores = [];
	  	let ranks = [];
	  	let tableRows = [];
	  	let durations_type = ["today","yesterday","week","month","year","custom_range"];
	  	for(let duration of durations_type){
	  		let val = value[duration];
	  		if(duration == "custom_range" && val){
	  			for(let [range,value1] of Object.entries(val)){
	  				durations.push(this.headerDates(range));
	  				for(let [c_key,c_rankData] of Object.entries(value1)){
		  				if(c_key == "user_rank"){
			  		 		if(!category)
			  		 			category = c_rankData.category;
			  		 		scores.push(c_rankData.score);
			  		 		ranks.push({'rank':c_rankData.rank,'duration':range,'isCustomRange':true});
		  		 		}
	  				}
	  			}
	  		}
	  		else{
	  			if (val){ 
			  		durations.push(duration);
			  		for (let [key,rankData] of Object.entries(val)){
			  		 	if(key == "user_rank"){
			  		 		if(!category){
			  		 			category = rankData.category;
			  		 		}
			  		 		scores.push(rankData.score);
			  		 		ranks.push({'rank':rankData.rank,'duration':duration,'isCustomRange':false});
			  		 	}
			  		}
			  	}
		  	}
	  	}

	  	// creating headers for table
	  	let tableHeaders = [<th className = "lb_table_style_rows">{category}</th>]
	  	for(let dur of durations){
	  		let capt = dur[0].toUpperCase() + dur.slice(1)
	  		let date;
	  		if(dur == "today"){
	  			date = moment(value5[dur]).format('MMM DD, YYYY');	
	  		}
	  		else if(dur == "yesterday"){
	  			date = moment(value5[dur]).format('MMM DD, YYYY');	
	  		}
	  		else if(dur == "week"){
		  		date = this.headerDates(value5[dur]);
	  		}
	  		else if(dur == "month"){
		  		date = this.headerDates(value5[dur]);
	  		}
	  		else if(dur == "year"){
		  		date = this.headerDates(value5[dur]);
	  		}
	  		else{
	  			date = value5[dur];
	  		}	
	  		tableHeaders.push(<th className = "lb_table_style_rows">{capt}<br/>{date}</th>);
	  	}
	 
	  	tableRows.push(<thead className = "lb_table_style_rows">{tableHeaders}</thead>);

	  	// creating table rows for ranks
	  	let rankTableData = [<td style={{fontWeight:"bold"}}
	  							 className = "lb_table_style_rows">
	  							 {"Ranks"}</td>]
	  	if (category){
		  	for(let rank of ranks){
		  		if(rank.isCustomRange){
		  			var state = {
			  					lbCatgData:this.state.ranking_data[
			  					categoryMeta[category]["short_name"]]['custom_range'][rank['duration']].all_rank}
			  	}
			  	else{
			  		var state = {
			  					lbCatgData:this.state.ranking_data[
			  					categoryMeta[category]["short_name"]][rank['duration']].all_rank}
			  	}
		  		rankTableData.push(
			  		<td className = "lb_table_style_rows">
			  			<Link to={{
			  				pathname:`/leaderboard/${categoryMeta[category]["url_name"]}`,
			  				state:state
			  				}}>{rank.rank}
			  			</Link>
			  		</td>
		  		);
		  	}
		 }else{
		 	for(let rank of ranks){
		  		rankTableData.push(
			  		<td className = "lb_table_style_rows">
			  			<Link to={{
			  				pathname:`/leaderboard}`
			  				}}>{rank?rank.rank:rank}
			  			</Link>
			  		</td>
		  		);
		  	}
		 }
	  	tableRows.push(<tr className = "lb_table_style_rows">{rankTableData}</tr>)

	  	let scoreTableData = [<td style={{fontWeight:"bold"}}
	  							  className = "lb_table_style_rows">
	  							  {"Scores"}</td>]
	  	for(let score of scores){
	  		if(category == "Total Steps"){
	  			var value = score;
	  		    if(value != undefined){
	                value += '';
	                var x = value.split('.');
	                var x1 = x[0];
	                var x2 = x.length > 1 ? '.' + x[1] : '';
	                var rgx = /(\d+)(\d{3})/;
	                while (rgx.test(x1)) {
	            			x1 = x1.replace(rgx, '$1' + ',' + '$2');
	          		}
	                scoreTableData.push(<td className="lb_table_style_rows">{x1 + x2}</td>);
    	        }
	  		}
	  		else{
	  		scoreTableData.push(<td className = "lb_table_style_rows">{score}</td>);
	  	    }
	  	}
	  	tableRows.push(<tbody><tr className = "lb_table_style_rows">{scoreTableData}</tr></tbody>)

	  	return  <table className = "table table-striped table-bordered">{tableRows}</table>;
  	};
  	
	render(){
		 const {fix} = this.props;
		return(
			<div className="container-fluid">
		         <Navbar toggleable
		         fixed={fix ? 'top' : ''}
		          className="navbar navbar-expand-sm navbar-inverse nav6">
		          <NavbarToggler className="navbar-toggler hidden-sm-up" onClick={this.toggle}>
		           <FontAwesome
		                 name = "bars"
		                 size = "1x"
		             />
		          </NavbarToggler>
		          <Link to='/' >
		            <NavbarBrand
		              className="navbar-brand float-sm-left"
		              id="navbarTogglerDemo" style={{fontSize:"16px",marginLeft:"-4px"}}>
		              <img className="img-fluid"
		               style={{maxWidth:"200px"}}
		               src="//static1.squarespace.com/static/535dc0f7e4b0ab57db48c65c/t/5942be8b893fc0b88882a5fb/1504135828049/?format=1500w"/>
		            </NavbarBrand>
		          </Link>
		            <span id="header">
		            <h2 className="head" id="head">Leader Board
		            </h2>
		            </span>
		          <Collapse className="navbar-toggleable-xs" isOpen={this.state.isOpen} navbar>
		            <Nav className="nav navbar-nav float-xs-right ml-auto" navbar>
		              <NavItem className="float-sm-right">
		                <Link id="logout"className="nav-link" to='/'>Home</Link>
		              </NavItem>
		               <NavItem className="float-sm-right">
		                   <NavLink
		                   className="nav-link"
		                   id="logout"
		                   onClick={this.handleLogout}>Log Out
		                    </NavLink>
		              </NavItem>
		            </Nav>
		          </Collapse>
		        </Navbar>

      		<div className = "row justify-content-center"> 
                <span id="navlink" onClick={this.toggleCalendar} id="progress">
                    <FontAwesome
                        name = "calendar"
                        size = "2x"
                    />
                </span>               
                <span  onClick={this.toggleDate1} id="daterange1" style={{color:"white"}}>
                    <span className="date_range_btn">
                        <Button
                            className="daterange-btn btn"                            
                            id="daterange"
                            onClick={this.toggleDate1} >Custom Date Range1
                        </Button>
                    </span>
                </span>
                <span  onClick={this.toggleDate2} id="daterange2" style={{color:"white"}}>
                    <span className="date_range_btn">
                        <Button
                            className="daterange-btn btn"                            
                            id="daterange"
                            onClick={this.toggleDate2} >Custom Date Range2
                        </Button>
                    </span>
                </span>
                <span  onClick={this.toggleDate3} id="daterange3" style={{color:"white"}}>
                    <span className="date_range_btn">
                        <Button
                            className="daterange-btn btn"                            
                            id="daterange"
                            onClick={this.toggleDate3} >Custom Date Range3
                        </Button>
                    </span>
                </span>
            </div>
            <Popover
            placement="bottom"
            isOpen={this.state.calendarOpen}
            target="progress"
            toggle={this.toggleCalendar}>
	              <PopoverBody className="calendar2">
	                <CalendarWidget  onDaySelect={this.processDate}/>
	              </PopoverBody>
	        </Popover>

	        <Popover
            placement="bottom"
            isOpen={this.state.dateRange1}
            target="daterange1"
            toggle={this.toggleDate1}>
                    <PopoverBody>
                        <div >
                            <Form>
	                            <div style={{paddingBottom:"12px"}} className="justify-content-center">
	                                <Label>Start Date</Label>&nbsp;<b style={{fontWeight:"bold"}}>:</b>&nbsp;
	                                <Input type="date"
	                                name="lb1_start_date"
	                                value={this.state.lb1_start_date}
	                                onChange={this.handleChange} style={{height:"35px",borderRadius:"7px"}}/>
	                            </div>
	                            <div id="date" className="justify-content-center">
	                                <Label>End date</Label>&nbsp;<b style={{fontWeight:"bold"}}>:</b>&nbsp;
	                                <Input type="date"
	                                name="lb1_end_date"
	                                value={this.state.lb1_end_date}
	                                onChange={this.handleChange} style={{height:"35px",borderRadius:"7px"}}/>
	                            </div>
	                            <div id="date" style={{marginTop:"12px"}} className="justify-content-center">
		                            <button
		                            id="nav-btn"
		                            style={{backgroundColor:"#ed9507"}}
		                            type="submit"
		                            className="btn btn-block-lg"
		                            onClick={this.onSubmitDate1} style={{width:"175px"}}>SUBMIT</button>
	                            </div>
                            </Form>
                        </div>
                    </PopoverBody>
                </Popover>
                 <Popover
            placement="bottom"
            isOpen={this.state.dateRange2}
            target="daterange2"
            toggle={this.toggleDate2}>
                    <PopoverBody>
                        <div >
                            <Form>
	                            <div style={{paddingBottom:"12px"}} className="justify-content-center">
	                                <Label>Start Date</Label>&nbsp;<b style={{fontWeight:"bold"}}>:</b>&nbsp;
	                                <Input type="date"
	                                name="lb2_start_date"
	                                value={this.state.lb2_start_date}
	                                onChange={this.handleChange} style={{height:"35px",borderRadius:"7px"}}/>
	                            </div>
	                            <div id="date" className="justify-content-center">
	                                <Label>End date</Label>&nbsp;<b style={{fontWeight:"bold"}}>:</b>&nbsp;
	                                <Input type="date"
	                                name="lb2_end_date"
	                                value={this.state.lb2_end_date}
	                                onChange={this.handleChange} style={{height:"35px",borderRadius:"7px"}}/>
	                            </div>
	                            <div id="date" style={{marginTop:"12px"}} className="justify-content-center">
		                            <button
		                            id="nav-btn"
		                            style={{backgroundColor:"#ed9507"}}
		                            type="submit"
		                            className="btn btn-block-lg"
		                            onClick={this.onSubmitDate2} style={{width:"175px"}}>SUBMIT</button>
	                            </div>
                            </Form>
                        </div>
                    </PopoverBody>
                </Popover>
                 <Popover
            placement="bottom"
            isOpen={this.state.dateRange3}
            target="daterange3"
            toggle={this.toggleDate3}>
                    <PopoverBody>
                        <div >
                            <Form>
	                            <div style={{paddingBottom:"12px"}} className="justify-content-center">
	                                <Label>Start Date</Label>&nbsp;<b style={{fontWeight:"bold"}}>:</b>&nbsp;
	                                <Input type="date"
	                                name="lb3_start_date"
	                                value={this.state.lb3_start_date}
	                                onChange={this.handleChange} style={{height:"35px",borderRadius:"7px"}}/>
	                            </div>
	                            <div id="date" className="justify-content-center">
	                                <Label>End date</Label>&nbsp;<b style={{fontWeight:"bold"}}>:</b>&nbsp;
	                                <Input type="date"
	                                name="lb3_end_date"
	                                value={this.state.lb3_end_date}
	                                onChange={this.handleChange} style={{height:"35px",borderRadius:"7px"}}/>
	                            </div>
	                            <div id="date" style={{marginTop:"12px"}} className="justify-content-center">
		                            <button
		                            id="nav-btn"
		                            style={{backgroundColor:"#ed9507"}}
		                            type="submit"
		                            className="btn btn-block-lg"
		                            onClick={this.onSubmitDate3} style={{width:"175px"}}>SUBMIT</button>
	                            </div>
                            </Form>
                        </div>
                    </PopoverBody>
                </Popover>
            <div className="col-sm-12 col-md-12 col-lg-12">
		        <div className = "row justify-content-center lb_table_style" style = {{paddingTop:"25px"}}>
		        	<div className = "table table-responsive">
			        	{this.renderTablesTd(this.state.ranking_data.oh_gpa,this.state.duration_date)}
			        </div>
		        </div>
		       <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.alcohol_drink,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.avg_sleep,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.prcnt_uf,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.total_steps,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.mc,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.ec,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.awake_time,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.resting_hr,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.deep_sleep,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
		        	<div className = "table table-responsive">
		        		{this.renderTablesTd(this.state.ranking_data.mne_gpa,this.state.duration_date)}
		        	</div>
		        </div>
		        <div className = "row justify-content-center lb_table_style">
			        <div className = "table table-responsive">
			        	{this.renderTablesTd(this.state.ranking_data.floor_climbed,this.state.duration_date)}
			        </div>
		        </div>
	        </div>
	        {this.renderLeaderBoardFetchOverlay()}
			{this.renderLeaderBoard2FetchOverlay()}
			{this.renderLeaderBoard3FetchOverlay()}
			{this.renderLeaderBoardSelectedDateFetchOverlay()}
	        </div>
		)
	}
	
}
function mapStateToProps(state){
  return {
    errorMessage: state.garmin_auth.error,
    message : state.garmin_auth.message
  };
}
export default connect(mapStateToProps,{getGarminToken,logoutUser})(withRouter(LeaderBoard));
Navbar.propTypes={
    fixed: PropTypes.string,
    color: PropTypes.string,
} 