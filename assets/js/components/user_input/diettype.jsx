import React, {Component} from 'react'
import {Button,FormGroup, Label, Input, FormText, className, Collapse} from 'reactstrap';

export default class DietType extends Component{

	constructor(props){
		super(props);
		const diet_type = this.props.diet_type;
		this.state = {
			diet_type:diet_type,
			collapse:diet_type ? true : false,	
		}

		this.handleChangeDiet = this.handleChangeDiet.bind(this);
		
	}

	handleChangeDiet(event){
		const value = event.target.value;  
		this.setState({
			diet_type:value
		},()=>{
			this.props.updateState(this.state.diet_type);
		});
	}

	render(){
		return(
			<div>
				<Collapse isOpen={this.state.collapse}>
				
							<FormGroup>
							    <Label>23.1) Hi, What Did You Take?</Label>
								<Input 
	                            type="FormText" 
	                            className="form-control" 
	                            value={this.state.diet_type}
	                          onChange={this.handleChangeDiet} >	                      
	                            </Input>	                        
							</FormGroup>	

				</Collapse>
			</div>
		);
	}
}