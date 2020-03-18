import React from 'react';
import ReactDOM from 'react-dom';

import TrainRLAgent from './training_form';
import Game from './game';

import './index.css';

class App extends React.Component{
  render(){
    return (
      <div className="game">
        <TrainRLAgent/>
        <Game/>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
