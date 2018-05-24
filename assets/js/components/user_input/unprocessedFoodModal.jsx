import React, {Component} from 'react'
import {Button,FormGroup, Label, Input, FormText, className, Collapse} from 'reactstrap';
import Textarea from 'react-textarea-autosize';

export default class UnprocesedFoodModal extends Component{

	constructor(props){
		super(props);
		const unprocessed_food_list = this.props.unprocessed_food_list;
		const processed_food_list = this.props.processed_food_list;

		this.state = {
			collapse:true,
			enter_food:(unprocessed_food_list !== '') ? true : false,
			unprocessed_food_list:unprocessed_food_list,
			processed_food_list:processed_food_list,
			enter_process_food:(processed_food_list !== '') ? true : false,
		};
		
		this.handleChange = this.handleChange.bind(this);
		this.onClickFoodList=this.onClickFoodList.bind(this);
		this.onClickProcessFoodList =this.onClickProcessFoodList.bind(this);
	}

	componentWillReceiveProps(nextProps) {
  	  if((nextProps.unprocessed_food_list !== this.props.unprocessed_food_list) ||
  	  	 (nextProps.processed_food_list !== this.props.processed_food_list)) {
    	  	this.setState({
    	  		enter_food:(nextProps.unprocessed_food_list !== '') ? true : false,
    	  		enter_process_food:(nextProps.processed_food_list !== '') ? true : false,
    	  		unprocessed_food_list:nextProps.unprocessed_food_list,
    	  		processed_food_list:nextProps.processed_food_list
    	  	});
    	}
  	}

	handleChange(event){
		const value = event.target.value;
		const name = event.target.name;
	    this.setState({
	    	[name]: value,
	    },()=>{
	    	this.props.updateState(this.state[name],name)
	    });
	}

	onClickFoodList(event){
			this.setState({
				enter_food:!this.state.enter_food
			});
	}
	onClickProcessFoodList(event){
			this.setState({
				enter_process_food:!this.state.enter_process_food
			});
	}

	render(){
		return(
			<div>
				<Collapse isOpen={this.state.collapse}>				
						<FormGroup>   
                            	{this.props.editable && 
                            		<div>
                            		 <div className="unprocess_food">
						                        <Input type="checkbox"
						                        id="unprocess_check"
					                           	onClick={this.onClickProcessFoodList}
					                           	checked={this.state.enter_process_food ? 'checked':''}
					                           	/>                           		  
		                            			<Label id="text" className="LAbel">I Want to enter in the processed foods I consumed yesterday</Label>
	                            			</div>
	                            	<Collapse isOpen={this.state.enter_process_food}>
                            		 <Label className="LAbel">5.1 What Processed Food were Consumed?</Label>
											<div className="input1">	
					                            <Textarea 
					                            id="placeholder"						                           
						                            className="form-control" 
						                            value={this.state.processed_food_list}
						                            name="processed_food_list"
						                            rows="5" cols="5"
						                            onChange={this.handleChange}
						                             />
					                        </div>
					                </Collapse>
					                        {(this.props.report_type == "full") &&
					                        <div className="unprocess_food">
						                        <Input type="checkbox"
						                        id="unprocess_check"
					                           	onClick={this.onClickFoodList}
					                           	checked={this.state.enter_food ? 'checked':''}
					                           	/>                           		  
		                            			<Label id="text" className="LAbel">I Want To Enter A List Of &nbsp;
			                            			 <span style={{fontWeight:"bold"}}>
						                             	<span style={{textDecoration:"underline"}}>Un</span>processed?
						                             </span> Foods I Consumed</Label>
	                            			</div>
	                            		}
                            			<div>
										<Collapse isOpen={this.state.enter_food}>

										<Label className="LAbel">5.2 What &nbsp;
										 <span style={{fontWeight:"bold"}}>
			                              	<span style={{textDecoration:"underline"}}>Un</span>processed?
			                             </span> Food Were Consumed?</Label>
											<div className="input1">	
					                            <Textarea
					                            id="placeholder" 						                           
						                            className="form-control" 
						                            value={this.state.unprocessed_food_list}
						                            name = "unprocessed_food_list"
						                            rows="5" cols="5"
						                            onChange={this.handleChange}
						                            />
					                        </div>
					                       
					                        
					                    </Collapse>
					                    </div> 
					                    </div>
			                    }
			                    {!this.props.editable &&
	                             <div>
	                              <div className="input">
	                              	<Label className="LAbel">5.1 What Processed Food Were Consumed?</Label><br/>
	                              	
	                                <p>{this.state.processed_food_list}</p>
	                                </div>
	                                {(this.props.report_type == "full") &&
	                                <div className="input">
	                                
	                                <Label>5.2 What &nbsp;
	                                <span style={{fontWeight:"bold"}}>
		                             	<span style={{textDecoration:"underline"}}>Un</span>processed?
		                             </span> Food Were Consumed?</Label>
	                                <p >{this.state.unprocessed_food_list}</p>
	                           		
	                              </div>
	                             }
	                             </div>
	                            }
                          </FormGroup> 			
				</Collapse>
			</div>
		);
	}
}