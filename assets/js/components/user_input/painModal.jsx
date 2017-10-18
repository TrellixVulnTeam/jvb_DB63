import React, {Component} from 'react';
import Select from 'react-select';
import 'react-select/dist/react-select.css';

import {Button,FormGroup, Label, Input, FormText, className, Collapse} from 'reactstrap';
	

const option=[
                { value:"right knee",label:'Right knee'},
                { value:'left knee',label:'Light knee'},
                { value:"right ankle",label:'Right ankle'},
                { value:"left ankle",label:'Left ankle'},
                { value:"right foot",label:'Right foot'},
                { value:"left foot",label:'Left foot'},
                { value:"right shins",label:'Right shins'},
                { value:"left shins",label:'Left shins'},
                { value:"right hip",label:'Right hip'},
                { value:"left hip",label:'Left hip'},
                { value:"right achilles",label:'Right achilles'},
                { value:"left achilles",label:'Left achilles'},
                { value:"right calf",label:'Right calf'},
                { value:"left calf",label:'Left calf'},
                { value:"right toes",label:'Right toes'},
                { value:"left toes",label:'Left toes'},
                { value:"neck",label:'Neck'},
                { value:"upper back",label:'Upper back'},
                { value:"mid back",label:'Mid back'},
                { value:"lower back",label:'Lower back'},
                { value:"other",label:'Other'}

		];

export default class PainModal extends Component{

	constructor(props){
		super(props);
		let other = true;
		const area = this.props.pain_area;
		const area_list = area.split(',');

		if(area === ""){
			other = false;
		}else{
			for(let item of option){
				for(let a of area_list){
					if(item.value === a){
						other = false;
						break;
					}
				}
			}
		}

		let pain_area_to_show = area;
		if(other)
			pain_area_to_show = 'other'


		this.state = {
			collapse:other ? true : false,	
			disabled: false,
			stayOpen: true,
			pain_area: area,
			pain_area_to_show: pain_area_to_show
		};
		this.handleSelectChange = this.handleSelectChange.bind(this);
		this.handleChange = this.handleChange.bind(this);
	}
	handleChange(event){
		const value = event.target.value;
		this.setState({
			pain_area:value
		},() => {
		    	this.props.updateState(this.state.pain_area);
		 });
	}
	handleSelectChange(value) {

		if (value === 'other'){
		    this.setState({
		    	pain_area_to_show: value,
		    	collapse:true
		    });
		}else if(value === ''){
			this.setState({
				pain_area:'',
				pain_area_to_show:'',
				collapse:false				
			});
		}
		else{
			this.setState({
		    	pain_area:value,
		    	pain_area_to_show:value
		    },()=>{
		    	this.props.updateState(this.state.pain_area)
		    });
		}
	}

	render(){
		return(
			<div>
				<FormGroup>   

                    <Label>5.1) Where Did You Have Pain/Twinges?</Label>
					<div className="input1">
	                    <Select
								closeOnSelect={!this.state.stayOpen}
								disabled={this.state.disabled}
								multi
								onChange={this.handleSelectChange}
								options={option}
								simpleValue
								value={this.state.pain_area_to_show}
						/> 
					</div>
                  </FormGroup> 

				<Collapse isOpen={this.state.collapse}>
					<FormGroup>
						<Label>5.2 Please Write Where You Have Pain/Twinges</Label>
							<div className="input1">
								<Input
								type="text"
								className="form-control"
								placeholder="Write where you have pain here.."
								value={this.state.pain_area}
								onChange={this.handleChange} />
							</div>
					</FormGroup>
				</Collapse>
			</div>
		);
	}
}