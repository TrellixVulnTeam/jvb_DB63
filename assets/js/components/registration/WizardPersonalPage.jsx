import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { connect } from 'react-redux';
import {Field, reduxForm } from 'redux-form';
import { Form, Label, Button, Input, FormText, FormGroup,
		 Row, Col, Container,InputGroup} from 'reactstrap';

import {renderFieldFormGroup,renderSelectFeet, renderSelectInches,renderSelectPounds,renderSelectMonth,renderSelectDate,renderSelectYear} from './fieldRenderer';
import { personal_validate } from './validation';

class WizardPersonalPage extends Component{

	constructor(props){
		super(props);
		this.state = {
			'feet_err':' ',
			'inches_error':' ',
            'weight_error':' ' ,
            'monthError':' ',
            'dateError':' ',
            'yearError':' '
		}
		this.FeetError = this.FeetError.bind(this);
		this.InchesError = this.InchesError.bind(this);
		this.WeightError = this.WeightError.bind(this);
		this.monthError = this.monthError.bind(this);
		this.dateError = this.dateError.bind(this);
		this.yearError = this.yearError.bind(this);

	}

	FeetError(err_msg){
		this.setState({
			feet_err:err_msg !== undefined ? err_msg : ' '
		});
	}

	InchesError(err_msg){
		this.setState({
			inches_error:err_msg !== undefined ? err_msg : ' '
		});
	}
	WeightError(err_msg){
		this.setState({
			weight_error:err_msg !== undefined ? err_msg : ' '
		});
	}
	monthError(err_msg){
		this.setState({
			monthError:err_msg !== undefined ? err_msg : ' '
		});
	}

	dateError(err_msg){
		this.setState({
			dateError:err_msg !== undefined ? err_msg : ' '
		});
	}
	yearError(err_msg){
		this.setState({
			yearError:err_msg !== undefined ? err_msg : ' '
		});
	}

	render(){
		const { handleSubmit, previousPage, onSubmit } = this.props;
		return(
			<Form  onSubmit={handleSubmit(onSubmit)}>
				<Row>
					<Col className="form-item">

						<Field
							name = "first_name"
							type = "input"
							label = "First Name"
							placeholder = "John"
							value=""
							component = {renderFieldFormGroup}
						/>

						<Field
							name = "last_name"
							type = "input"
							label = "Last Name"
							placeholder = "Doe"
							value=""
							component = {renderFieldFormGroup}
						/>

						
						<FormGroup>
							<Label>Date of Birth</Label>
							<InputGroup>
								<Field
									name = "dob_month"
									type = "select"
									component = {renderSelectMonth}
									err_callback = {this.monthError}	
								/>
								&nbsp;
								<Field
									name = "dob_day"
									type = "select"
									component = {renderSelectDate}	
									err_callback = {this.dateError}	
								/>
								&nbsp;
								<Field
									name = "dob_year"
									type = "select"
									component = {renderSelectYear}	
									err_callback = {this.yearError}	
								/>
							</InputGroup>
							<div style={{color:"red"}}>
								{this.state.monthError+" "+this.state.dateError+" "+this.state.yearError}
							</div>

						</FormGroup>

						<FormGroup>
							<Label>Height</Label>
							<InputGroup>
								<Field
									name = "feet"
									type = "select"
									component = {renderSelectFeet}
									err_callback = {this.FeetError}	
								/>
								&nbsp;&nbsp;
								<Field
									name = "inches"
									type = "select"
									component = {renderSelectInches}	
									err_callback = {this.InchesError}	
								/>
							</InputGroup>
							<div style={{color:"red"}}>
								{this.state.feet_err+" "+this.state.inches_error}
							</div>

						</FormGroup>
						<FormGroup>
						<label>Weight&nbsp;&nbsp;(in pounds)</label>
                           <Field
									name = "weight"
									type = "select"
									component = {renderSelectPounds}	
									err_callback = {this.WeightError}	
								/>
 
                            <div style={{color:"red"}}>
								{this.state.weight_error}
							</div>
                        </FormGroup>   
                           
						

						 <FormGroup>
					          <Label className="custom-control custom-radio">
					            	<Field 
					            		className="custom-control-input"
					            		name="gender" 
					            		component="input" 
					            		type="radio" 
					            		value="M"
					            	required 
					            	/>
					            	<span className="custom-control-indicator"></span>
					            	<span className="custom-control-description">Male</span>
					          </Label>
					          <Label className="custom-control custom-radio">
					            	<Field 
					            		className="custom-control-input"
					            		name="gender" 
					            		component="input" 
					            		type="radio" 
					            		value="F" 
					            	/>
					            	<span className="custom-control-indicator"></span>
					            	<span className="custom-control-description">Female</span>
					          </Label>
				        </FormGroup>
				        <div className="f-footer">
							<Button outline color="primary" onClick={previousPage}>
								Previous
							</Button>
							<Button type="submit" outline color="primary" style={{float:'right'}}>
								Next
							</Button>
						</div>
					</Col>
				</Row>
			</Form>
		);
	}
}

export default reduxForm({
	form: 'register',
	destroyOnUnmount: false,
	forceUnregisterOnUnmount: true,
	validate: personal_validate
})(
	connect(null,{})(WizardPersonalPage)
);