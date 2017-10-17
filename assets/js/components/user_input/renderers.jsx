export function renderWorkoutEffortModal(){
  if(this.state.workout_effort !== "no workout today" && 
	 this.state.workout_effort !== ""){
	const updateState = function(val){
						  this.setState({
							workout_effort_hard_portion:val
						  })}.bind(this);

	return(
	  <WorkoutEffortModal
		workout_effort_hard_portion={this.state.workout_effort_hard_portion}
		updateState={updateState}
	  />
	);
}
  }

export function renderPainModal(){
  if(this.state.pain === 'yes'){
	const updateState = function(val){
						  this.setState({
							pain_area: val
						  })}.bind(this);
	return(
	  <PainModal
		pain_area={this.state.pain_area}
		updateState={updateState}
	  />
	);
  }
}

export function renderDietType(){
	if(this.state.diet_type === 'other'){
	   const updateState = function(val){
						  this.setState({
							diet_type: val
						  })}.bind(this);
	   return(           
		<DietType
		  diet_type={this.state.diet_type}
		  updateState={updateState}
		/>
		);
	}
}

export function renderUnprocessedFoodModal(){
  
	if(this.state. prcnt_unprocessed_food > 0 ){
	  const updateState = function(val){
						  this.setState({
						  unprocessed_food_list: val
						  })}.bind(this);

		  return(
		<UnprocesedFoodModal
		unprocessed_food_list={this.state.unprocessed_food_list}
		updateState={updateState}
	  />
	  );
	}
}

export function renderFasted(){ 
 if(this.state. fasted === 'no'){
   const updateState = function(val){
						  this.setState({
					   food_ate_before_workout: val
						  })}.bind(this);
	   return(
			<FastedModal
			  food_ate_before_workout={this.state.food_ate_before_workout}
			  updateState={updateState}
			/>
  );
 }  
}


export function renderPrescriptionMedication(){
	if(this.state. medications === 'yes'){
	 const updateState = function(val){
							  this.setState({
						   medications_taken_list: val
							  })}.bind(this);         
	  return(
		  <PrescriptionMedication
		  sleep_aid_taken={this.state.medications_taken_list}
		  updateState={updateState}
		  />
		);
	  }
}

export function renderPrescriptionSleepAids(){
	if(this.state.prescription_sleep_aids === 'yes'){
	 const updateState = function(val){
							  this.setState({
						  sleep_aid_taken: val
							  })}.bind(this); 
		 return(
			<PrescriptionSleepAids
			sleep_aid_taken={this.state.sleep_aid_taken}
			updateState={updateState}
			/>
		);
	  }
 
}

export function renderPainSick(){
  if(this.state.sick === 'yes'){
	 const updateState = function(val){
						  this.setState({
						  sickness: val
						  })}.bind(this); 

	 return(
		  <SickModal
			sickness={this.state.sickness}
			updateState={updateState}
		  />
		 );
  }
}

export function renderSmokeSubstance(callback){
  if (this.state.smoke_substances === 'yes'){

	const updateState = function(val){
		this.setState({
		 smoked_substance_list: val
		});
	  }.bind(this);

	return(
	  <SmokedSubstance
		smoked_substance_list={this.state.smoked_substance_list}
		updateState={updateState}
	  />
	);
  }
}

export function renderUpdateButton(){
  if(this.state.update_form){
	return(
	  <Button 
		color="info" 
		className="btn btn-block btn-primary"
		onClick={this.onUpdate}>
		  Update
	  </Button>
	);
  }
}
