import React from 'react';

import TrainRLAgent from './form/training';
import Game from './game';

import '../index.css'

class App extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      show: false,
      showOptions: false
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

  showOptionModal = () => {
    this.setState({
      ...this.state,
      showOptions: true
    })
  }

  closeOptionModal = () => {
    this.setState({
      ...this.state,
      showOptions: false
    })
  }

  handleModal = () => {
    (this.state.show) ? this.closeModal() : this.showModal();
    return;
  }

  handleOptionsModal = () => {
    (this.state.showOptions) ? this.showOptionModal() : this.closeOptionModal();
    return;
  }

  render(){
    const modalClassName = this.state.show ? "modal display-block" : "modal display-none";
    const optionsModalClassName = this.state.showOptions ? "modal display-block" : "modal display-none";
    return (
      <div>
        <div className={modalClassName}>
          <section className="modal-main">
            <TrainRLAgent handleModal={this.handleModal}/>
          </section>
        </div>
        <div className="game">
          <Game handleModal={this.handleModal} handleOptionsModal={this.handleOptionsModal} modalClassName={optionsModalClassName}/>
        </div>
      </div>
    );
  }
}

export default App