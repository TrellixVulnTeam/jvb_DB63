import React, { Component } from 'react';
import { Container, Row, Col, Card,CardTitle, 
		 CardHeader, CardBody, CardText, Progress } from 'reactstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.min.css';

import RegisterNetwork from '../../network/register';

import WizardAccountPage from './WizardAccountPage';
import WizardPersonalPage from './WizardPersonalPage';
import WizardGoalsPage from './WizardGoalsPage';

class Register extends Component {

	constructor(props){
		super(props);
		this.nextPage = this.nextPage.bind(this);
		this.previousPage = this.previousPage.bind(this);
		this.onSubmit = this.onSubmit.bind(this);
		this.onRegisterSuccess = this.onRegisterSuccess.bind(this);
		this.state = {
			page:1,
			progress:20
		};
	}

	onRegisterSuccess(response){
		this.setState({
			progress: this.state.progress + 33.33
		});

		//redirect to user newly created profile
		toast.info(
		"User Account created successfully!",{
          className:"dark"
        });
	}

	onRegisterFailure(error){
		console.log('Error: ',error);
	}

	onSubmit(values){
		var reg = new RegisterNetwork();
		reg.register(values,this.onRegisterSuccess,this.onRegisterFailure);
	}

	nextPage() {
		this.setState({
			page: this.state.page + 1,
			progress: this.state.progress + 33.33
		});
	}

	previousPage(){
		this.setState({
			page: this.state.page - 1,
			progress: this.state.progress - 33.33
		});
	}

	render(){
		const { page } = this.state;
		const class_account = `f-cp-icon ${page === 1 ? 'active':''}`;
		const class_personal = `f-cp-icon ${page === 2 ? 'active':''}`;
		const class_goals = `f-cp-icon ${page === 3 ? 'active':''}`;

		return(
			<div className="form-container">
				<Container className="h-100" id="reg-form">
					<Row className="justify-content-center align-items-center h-100">
						<Col md="6" className="h-100">
							<Card className="form-card">
								<CardHeader className="text-center">
									<div className="img-fluid">
										<img src="https://static1.squarespace.com/static/535dc0f7e4b0ab57db48c65c/t/591e1eb0414fb533af1850a6/1495146161157"
											 alt="jvb-logo"
											 height="100"
											 width="100" 
										/>
									</div>
									<div className="f-progress">
										<Progress 
											className="f-progress-bar" 
											value={this.state.progress}
										/>
										<div className="f-cp">
											<div className={class_account}>
												<i className="fa fa-key" aria-hidden="true"></i>
											</div>
											<p>Account</p>
										</div>
										<div className="f-cp">
											<div className={class_personal}>
												<i className="fa fa-user" aria-hidden="true"></i>
											</div>
											<p>Personal</p>
										</div>
										<div className="f-cp">
											<div className={class_goals}>
												<i className="fa fa-check-circle" aria-hidden="true"></i>
											</div>
											<p>Goals</p>
										</div>
									</div>
								</CardHeader>
								<CardBody>
									{page === 1 && <WizardAccountPage onSubmit = {this.nextPage} />}
									{page === 2 &&
									 <WizardPersonalPage 
											onSubmit = {this.nextPage}
											previousPage = {this.previousPage}
									 />}
									 {page === 3 &&
									 <WizardGoalsPage 
											onSubmit = {this.onSubmit}
											previousPage = {this.previousPage}
									 />}
								</CardBody>
							</Card>
						</Col>
					</Row>
				</Container>
				<ToastContainer 
					position="top-center"
					type="success"
					autoClose={5000}
					hideProgressBar={true}
					newestOnTop={false}
					closeOnClick
				/>
			</div>
		);
	}
}

export default Register;