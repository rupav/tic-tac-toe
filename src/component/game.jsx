import React from 'react';
import { connect } from 'react-redux'
import axios from 'axios';

import defaultParams from '../axiosConfig'

const lines = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

function calculateWinner(squares){
  for (let i=0; i<lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[b] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function isDraw(squares){
  for (let i=0; i<9; i++){
    if(!squares[i]) return false;
  }
  return true;
}

function cellStatus(squares){
  let table = Array(9).fill(null);
  if(calculateWinner(squares)){
    for (let i=0; i<lines.length; i++) {
      const [a, b, c] = lines[i];
      if (squares[a] && squares[a] === squares[b] && squares[b] === squares[c]) {
        table[a] = table[b] = table[c] = 1;
        break;
      }
    }
  } else if (isDraw(squares)) {
    for(let i=0; i<9; i++){
      table[i] = 0;
    }
  }
  return table;
}

function getSquareClass(status){
  switch(status){
    case 0: {
      return 'draw-square'
    }
    case 1: {
      return 'winning-square'
    }
    default: {
      return 'square'
    }
  }
}

function Square(props) {
  return (
    <button
      className={getSquareClass(props.status)}
      onClick={props.onClick}
      >
        {props.value}
    </button>
  );
}

class Board extends React.Component {

  renderSquare(i, status) {
    return(
     <Square 
      value={this.props.squares[i]}
      status={status}
      onClick = {()=>this.props.onClick(i)}
     />
   );
  }

  createTable  = () => {
    let z = cellStatus(this.props.squares);
    let table = [];
    let id_;
    for(let i=0; i<3; i++){
      let row = []
      for(let j=0; j<3; j++){
        id_ = 3*i + j;
        row.push(<td key={id_}>{this.renderSquare(id_, z[id_])}</td>)
      }
      table.push(<tr key={i} className="board-row">{row}</tr>)
    }
    return table
  }

  render() {
    return (
      <table>
        <tbody>
          {this.createTable()}
        </tbody>
      </table>
    );
  }
}

class Game extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      showOptions: false, 
      history: [{
        squares: Array(9).fill(null),
      }],
      xIsNext: true,
      stepNumber: 0,
    };
  }

  handleClick(i){
    const history = this.state.history.slice(0, this.state.stepNumber + 1);
    const current = history[history.length - 1];
    const squares = current.squares.slice();

    /* If game has been won or square if already filled */
    if (calculateWinner(squares) || squares[i]) {
      return ;
    }
    
    /// if x is next continue, since it is the chance of computer to play
    if(this.state.xIsNext){
      return;
    }

    squares[i] = this.state.xIsNext?'X':'O';
    this.setState({
      ...this.state,
      history: history.concat([{
        squares: squares,
      }]),
      stepNumber: history.length,
      xIsNext: !this.state.xIsNext,
    });
  }

  nextMove(){
    const history = this.state.history.slice(0, this.state.stepNumber + 1);
    const current = history[history.length - 1];
    const squares = current.squares.slice();    
    
    let mapped_squares = squares.map(square => {
      switch(square){
        case 'X': {
          return 1
        }
        case 'O': {
          return 2
        }
        default: {
          return 0
        }
      }
    });

    if (this.state.xIsNext) {
      const params = {
        board: mapped_squares,
        V: this.props.V
      }
      console.log(this.props.alpha)
      console.log(process.env.REACT_APP_API_URI)
      axios({
        ...defaultParams,
        url: '/next_move',
        data: params
      }).then((resp) => {
        console.log(resp.data.next_move);
        squares[resp.data.next_move] = this.state.xIsNext?'X':'O';
        this.setState({
          ...this.state,
          history: history.concat([{
            squares: squares,
          }]),
          stepNumber: history.length,
          xIsNext: !this.state.xIsNext,
        });        
        
      }).catch((error) => {
        console.log(error);
      });
    } else {
      return;
    }
  }  

  jumpTo(step) {
    this.setState({
      ...this.state,
      stepNumber: step,
      xIsNext: (step % 2) === 0,
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

  handleOptionsModal = () => {
    (!this.state.showOptions) ? this.showOptionModal() : this.closeOptionModal();
    return;
  }  

  render() {
    const history = this.state.history;
    const current = history[this.state.stepNumber];
    const winner = calculateWinner(current.squares);
    const modalClassName = this.state.showOptions ? "modal display-block" : "modal display-none";
    
    let status;
    if (winner) {
      status = 'Winner: ' + winner;
    } else if (isDraw(current.squares)) {
      status = 'Its a Draw!';
    } else {
      status = 'Next player: '+ (this.state.xIsNext?'X':'O');
      /// agent plays next move
      this.nextMove();
    }

    const moves = history.map((step, move) => {
      const desc = move ?
        'Move #' + move:
        'Restart';
      return (
        <li key={move}>
          <button className="options" onClick={() => this.jumpTo(move)}>{desc}</button>
        </li>
      );
    });

    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares = {current.squares}
            onClick = {(i) => this.handleClick(i)}
          />
        </div>
        <div className="game-info">
          <div className="center-align">
            <div className="game-status">{status}</div>
          </div>
          <div className="center-align">
            <button className="modal-open options-modal-open" onClick={this.handleOptionsModal}>Go to</button>
          </div>
          <div className={modalClassName}>
            <section className="modal-main">
              <ol>
                {moves}
              </ol>
              <button className="modal-close" type="button" onClick={this.handleOptionsModal}>Close</button>
            </section>
          </div>
          <div className="center-align">
            <button className="modal-open" onClick={this.props.handleModal}>
              Train
            </button>
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state, props) => {
  const app = state.app
  return app
}

export default connect(mapStateToProps)(Game)