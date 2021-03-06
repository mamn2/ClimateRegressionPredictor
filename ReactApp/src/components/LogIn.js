import React from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import {Link, withRouter } from 'react-router-dom'
import * as ROUTES from './Routes.js'
import ls from 'local-storage'
import {BrowserRouter, Route, Redirect} from 'react-router-dom'
import Simulation from './Simulation'
import SignUp from './SignUp'
import Switch from 'react-bootstrap/esm/Switch';
import '../App.css'

class LogIn extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username:"",
            password:"",
            validLogin:""
        }
    }

    // componentDidMount = () => {
    //     ls.set("validLogin", false);
    // }

    changeUsername =(e) => {
        this.setState({username: e.target.value })
        ls.set('username', e.target.value)
    }

    changePassword =(e) => {
        this.setState({password: e.target.value })
        ls.set('password', e.target.value)
    }
    logIn = () => {
        var data = {
            "username":this.state.username,
            "password":this.state.password
        }
        fetch('http://127.0.0.1:5000/logIn' , {
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST",
            body: JSON.stringify(data)
        })
        .then(response => response.text())
        .then((data) => {
                console.log(data)
                if (data === "1") {
                    ls.set("validLogin", true)
                    this.setState({validLogin: "true"})
                } else {
                    ls.set("validLogin", false)
                    this.setState({validLogin: "false"})
                }   
        })
        .catch((error) => {
            console.log(error)
        })
    }

    render() {
        console.log(ls.get("validLogin"))
        return (
            <div className="Main-Background">
                <Card style={{marginTop:"17%", marginLeft: "35%", width: '25rem'}}>
                    <Card.Body>
                        <h3>Modeling Climate Change</h3>
                        <Card.Title>Log In</Card.Title>
                        <Card.Text>
                            <Form>
                                <Form.Label>User ID</Form.Label>
                                <Form.Control type="username" placeholder = "Enter UserID" value = {this.state.username} onChange={this.changeUsername}/>
                                <Form.Label style={{marginTop:"20px"}}>Password</Form.Label>
                                <Form.Control type="password" placeholder = "Enter Password" value = {this.state.password} onChange={this.changePassword}/>
                                {this.state.validLogin == "true" && 
                                        <Redirect to = {ROUTES.SIMULATIONS} />
                                }
                                {this.state.validLogin == "false" && 
                                    <div>
                                        <Button style={{marginTop:"20px"}} variant="primary" value = {this.state.username} onClick={this.logIn}>LogIn</Button>
                                        <Form.Text style={{marginTop:"20px"}}>Wrong Username and/or Password</Form.Text>
                                    </div>
                                }
                                {this.state.validLogin == "" && 
                                    <div>
                                        <Button style={{marginTop:"20px"}} variant="danger" value = {this.state.username} onClick={this.logIn}>LogIn</Button>
                                    </div>
                                }
                                <Form.Text style={{marginTop:"20px"}} >
                                    <Link to={ROUTES.SIGN_UP}> Don't Have an Account. Sign Up </Link>
                                </Form.Text>
                            </Form>
                        </Card.Text>
                    </Card.Body>
                </Card>
            </div>
        )
    }


}


export default LogIn;
