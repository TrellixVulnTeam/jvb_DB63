import React, {Component} from 'react'
import {Button,FormGroup, Label, Input, FormText, className, Modal,
		ModalHeader, ModalBody, ModalFooter, Collapse} from 'reactstrap';

export default class SmokedSubstance extends Component{

	constructor(props){
		super(props);
		let smoked_substance_list = this.props.smoked_substance_list;
		let pat = /^cigarettes/i;
		let isCigarettes = pat.test(smoked_substance_list);
		let cigarettes_count = '';

		if (isCigarettes){
			let pattern = /^cigarettes\((\d+)\)$/i;
			cigarettes_count = pattern.exec(smoked_substance_list)[1];
			smoked_substance_list = 'cigarettes';
		}

		this.state = {
		collapse:true,
			smoked_substance_list:smoked_substance_list,
			cigarettes_count:cigarettes_count,
			collapseOther: (smoked_substance_list !== '' && smoked_substance_list !== 'cigarettes')? true : false,
			collapseCigarettesCount: isCigarettes ? true : false
		};
		
		this.handleChange = this.handleChange.bind(this);
		this.handleChangeCigarettes = this.handleChangeCigarettes.bind(this);		

	}

	handleChange(event){
		const value = event.target.value;
		if (value === 'other'){
		    this.setState({
		    	collapseOther:true,
		    	collapseCigarettesCount:false
		    });
		}else if (value === 'cigarettes'){
			this.setState({
		    	smoked_substance_list: value,
		    	collapseCigarettesCount: true,
		    	collapseOther:false
		    });
		}else {
			this.setState({
				smoked_substance_list: value
			});
		}
	}

	handleChangeCigarettes(event){
		const value = event.target.value;
		const smoked_substance_list = this.state.smoked_substance_list+"("+value+")";

		this.setState({
			cigarettes_count: value,
			smoked_substance_list:smoked_substance_list
		});
	}
	

	createCigarettesDropdown(num){
		let elements = [];
		elements.push(<option value=''>select</option>);
		for(let i=1;i<=num;i++){
			elements.push(<option value={i}>{i}</option>);
		}
		elements.push(<option value={num+"+"}>{num+"+"}</option>);
		return elements;
	}

	render(){
		return(
			<div>
				
					<Collapse isOpen={this.state.collapse}>
						<FormGroup>   
                            <Label>17.1) What Did You Smoke Yesterday?</Label>
                            <Input 
                            type="select" 
                            className="custom-select form-control" 
                            value={this.state.smoked_substance_list}
                            onChange={this.handleChange}>
                            	<option value="">select</option>
                                <option value="other">Other</option>
                                <option value="cigarettes">Cigarettes</option>
                            </Input>  
                          </FormGroup> 

                        <Collapse isOpen={this.state.collapseCigarettesCount}>
							<FormGroup>
								<Label>17.2) How Many Cigarettes You Have Smoked?</Label>
								<Input 
		                            type="select" 
		                            className="custom-select form-control" 
		                            value={this.state.cigarettes_count}
		                            onChange={this.handleChangeCigarettes}>
	                            {this.createCigarettesDropdown(60)}
                            </Input> 
							</FormGroup>
						</Collapse>

						<Collapse isOpen={this.state.collapseOther}>
							<FormGroup>
								<Input 
	                            type="textarea" 
	                            className="form-control" 
	                            rows="5" columns="5"
	                            placeholder="Please type in..."
	                            value={this.state.smoked_substance_list}
	                            onChange={this.handleChange} />
							</FormGroup>
						</Collapse>

					
					</Collapse>
				
			</div>
		);
	}
}