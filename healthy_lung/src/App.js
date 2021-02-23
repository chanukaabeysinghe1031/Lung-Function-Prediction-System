import logo from './logo.svg';
import './App.css';
import React,{useReducer} from 'react';

const stateManager = {
  initial:'initial',
  states : {
    initial : {on : {next : 'loadingModel'}},
    loadingModel : {on : {next : 'awaitingUpload'}},
    awaitingUpload : {on : {next : 'ready'}},
    ready : {on : {next : 'predicitng'},showImage:true},
    predicitng : {on : {next : 'complete'}},
    complete : {on : {next : 'awaitingUpload'},showImage:true}
  }
}

const reducer = (currentState,event) => stateManager.states[currentState].on[event] || stateManager.initial;

function App() {
  const [state,dispatch] = useReducer(reducer,stateManager.initial);
  const next = ()=>dispatch('next');
  const buttonProps = {
    initial:{text:'Load Model',action:()=>{}},
    loadingModel:{text:'Loading Model',action:()=>{}},
    awaitingUpload:{text:'Upload the CT scan',action:()=>{}},
    ready:{text:'Predict FVC',action:()=>{}},
    predicting:{text:'Predicting',action:()=>{}},
    complete:{text:'Reset',action:()=>{}}
  }

  return (
    <div className="App">
        <button onClick={buttonProps[state].action}>{buttonProps[state].text}</button>
    </div>
  );
}

export default App;
