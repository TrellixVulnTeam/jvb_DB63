import React from 'react';
import { Form, Label, Button, Input, FormText, FormGroup,
		 Row, Col, Container} from 'reactstrap';

export function renderFieldFormGroup(field){
	const { meta: {touched, error} } = field;
	const className = `${ touched && error ? 'has-danger' : '' }`;
	const label = field.label != "" ? <Label>{field.label}</Label> : ""
	return(
		<FormGroup className={className}>
			{label}
			<Input 
				type={field.type} 
				name={field.input.name} 
				placeholder={field.placeholder} 
				value={field.value}
				required
				{...field.input}
			/>
			<div style={{color:"red"}}className="form-control-feedback">
				{touched ? error : ''}
			</div>
		</FormGroup>
	);
}

function createDropdown(start_num , end_num, mins=false, step=1){
	let elements = [];
	let i = start_num;
	while(i<=end_num){
		let j = (mins && i < 10) ? "0"+i : i;
		elements.push(<option key={j} value={j}>{j}</option>);
		i=i+step;
	}
	return elements;
}

export function renderSelectFeet(field){
	console.log(field);
	const { meta: {touched, error} } = field;
	const className = `form-group ${ touched && error ? 'has-danger' : '' }`;
	return(
			<Input 
				type={field.type} 
				name={field.input.name} 
				required
				{...field.input}>
				<option value="feet">Feet</option> 
				{createDropdown(1,9)}
				{touched ? field.err_callback(error) : field.err_callback('')}
			</Input>
	);
}

export function renderSelectInches(field){
	const { meta: {touched, error} } = field;
	const className = `form-group ${ touched && error ? 'has-danger' : '' }`;
	return(
			<Input 
				type={field.type} 
				name={field.input.name}
				required 
				{...field.input}>
				<option value="inches">Inches</option> 
				{createDropdown(1,12)}
				{touched ? field.err_callback(error) : field.err_callback('')}
			</Input>
	);
}

export function renderSelectPounds(field){
	const { meta: {touched, error} } = field;
	const className = `form-group ${ touched && error ? 'has-danger' : '' }`;
	return(
			<Input 
				type={field.type} 
				name={field.input.name}
				required 
				{...field.input}>
				<option value="weight">weight</option> 
				{createDropdown(40,500)}
				{touched ? field.err_callback(error) : field.err_callback('')}
			</Input>
	);
}
export function renderSelectHours(field){
	const { meta: {touched, error} } = field;
	const className = `form-group ${ touched && error ? 'has-danger' : '' }`;
	return(
			<Input 
				type={field.type} 
				name={field.input.name}
				required 
				{...field.input}>
				<option value="Hours">Hours</option> 
				{createDropdown(0,24)}
				{touched ? field.err_callback(error) : field.err_callback('')}
			</Input>
	);
}
export function renderSelectMinutes(field){
	const { meta: {touched, error} } = field;
	const className = `form-group ${ touched && error ? 'has-danger' : '' }`;
	return(
			<Input 
				type={field.type} 
				name={field.input.name}
				required 
				{...field.input}>
				<option value="Minutes">Minutes</option> 
				{createDropdown(0,59,true)}
				{touched ? field.err_callback(error) : field.err_callback('')}
			</Input>
	);
}

export function renderSelectMonth(field){
	console.log(field);
	const { meta: {touched, error} } = field;
	const className = `form-group ${ touched && error ? 'has-danger' : '' }`;
	return(
			<Input 
				type={field.type} 
				name={field.input.name} 
				required
				{...field.input}>
				<option value="month">month</option> 
				{createDropdown(1,12)}
				{touched ? field.err_callback(error) : field.err_callback('')}
			</Input>
	);
}
export function renderSelectDate(field){
	console.log(field);
	const { meta: {touched, error} } = field;
	const className = `form-group ${ touched && error ? 'has-danger' : '' }`;
	return(
			<Input 
				type={field.type} 
				name={field.input.name} 
				required
				{...field.input}>
				<option value="date">date</option> 
				{createDropdown(1,31)}
				{touched ? field.err_callback(error) : field.err_callback('')}
			</Input>
	);
}
export function renderSelectYear(field){
	console.log(field);
	const { meta: {touched, error} } = field;
	const className = `form-group ${ touched && error ? 'has-danger' : '' }`;
	return(
			<Input 
				type={field.type} 
				name={field.input.name} 
				required
				{...field.input}>
				<option value="year">year</option> 
				{createDropdown(1930,2018)}
				{touched ? field.err_callback(error) : field.err_callback('')}
			</Input>
	);
}