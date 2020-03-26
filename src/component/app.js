import React from 'react';

import TrainRLAgent from './form/training';
import Game from './game';

import '../index.css'

class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      show: false
    }
  }

  showModal = () => {
    this.setState({
      ...this.state,
      show: true
    })
  }

  closeModal = () => {
    this.setState({
      ...this.state,
      show: false
    })
  }

  handleModal = () => {
    (this.state.show) ? this.closeModal() : this.showModal();
    return;
  }

  render(){
    const modalClassName = this.state.show ? "modal display-block" : "modal display-none";
    return (
      <div>
        <div className={modalClassName}>
          <section className="modal-main">
            <TrainRLAgent handleModal={this.handleModal}/>
          </section>
        </div>
        <div className="game">
          <Game handleModal={this.handleModal}/>
        </div>
      </div>
    );
  }
}

export default App