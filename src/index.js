import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

import TrainRLAgent from './training_form';


import './index.css';

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
        row.push(<td>{this.renderSquare(id_, z[id_])}</td>)
      }
      table.push(<tr className="board-row">{row}</tr>)
    }
    return table
  }

  render() {
    return (
      <div>
        {this.createTable()}
      </div>
    );
  }
}

class Game extends React.Component {
  constructor(props){
    super(props);
    this.state = {
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
    squares[i] = this.state.xIsNext?'X':'O';
    this.setState({
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
    
    const url = "/api/next_move";
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
      axios.post(url, {board: mapped_squares}).then((resp) => {
        console.log(resp.data.next_move);
        squares[resp.data.next_move] = this.state.xIsNext?'X':'O';
        this.setState({
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
      stepNumber: step,
      xIsNext: (step % 2) === 0,
    })
  }

  render() {
    const history = this.state.history;
    const current = history[this.state.stepNumber];
    const winner = calculateWinner(current.squares);
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
        'Go to move #' + move:
        'Restart';
      return (
        <option key={move} onClick={() => this.jumpTo(move)}>
          {desc}
        </option>
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
          <div className="game-status">{status}</div>
          <select>
            {moves}
          </select>
        </div>
      </div>
    );
  }
}

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
