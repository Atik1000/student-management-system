// import React, { useState } from 'react';
// import { createRoot } from 'react-dom/client';

// const rowStyle = {
//   display: 'flex'
// }

// const squareStyle = {
//   width: '60px',
//   height: '60px',
//   backgroundColor: '#ddd',
//   margin: '4px',
//   display: 'flex',
//   justifyContent: 'center',
//   alignItems: 'center',
//   fontSize: '20px',
//   color: 'white',
//   cursor: 'pointer'
// }

// const boardStyle = {
//   backgroundColor: '#eee',
//   width: '208px',
//   alignItems: 'center',
//   justifyContent: 'center',
//   display: 'flex',
//   flexDirection: 'column',
//   border: '3px #eee solid'
// }

// const containerStyle = {
//   display: 'flex',
//   alignItems: 'center',
//   flexDirection: 'column'
// }

// const instructionsStyle = {
//   marginTop: '5px',
//   marginBottom: '5px',
//   fontWeight: 'bold',
//   fontSize: '16px',
// }

// const buttonStyle = {
//   marginTop: '15px',
//   marginBottom: '16px',
//   width: '80px',
//   height: '40px',
//   backgroundColor: '#8acaca',
//   color: 'white',
//   fontSize: '16px',
// }

// // Component to render individual squares
// function Square({ value, onClick }) {
//   return (
//     <div
//       className="square"
//       style={squareStyle}
//       onClick={onClick}>
//       {value}
//     </div>
//   );
// }

// // Component to render the board
// function Board() {
//   // __define-ocg__ State to manage the game board and current player
//   const [squares, setSquares] = useState(Array(9).fill(null));
//   const [isXNext, setIsXNext] = useState(true);
//   const [winner, setWinner] = useState(null);

//   // Calculate the winner
//   function calculateWinner(squares) {
//     const lines = [
//       [0, 1, 2],
//       [3, 4, 5],
//       [6, 7, 8],
//       [0, 3, 6],
//       [1, 4, 7],
//       [2, 5, 8],
//       [0, 4, 8],
//       [2, 4, 6],
//     ];
//     for (let i = 0; i < lines.length; i++) {
//       const [a, b, c] = lines[i];
//       if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
//         return squares[a];
//       }
//     }
//     return null;
//   }

//   // Handle square click
//   function handleClick(index) {
//     if (squares[index] || winner) return; // Prevent click if square is filled or game is won

//     const newSquares = squares.slice();
//     newSquares[index] = isXNext ? 'X' : 'O';
//     setSquares(newSquares);
//     setIsXNext(!isXNext);

//     const gameWinner = calculateWinner(newSquares);
//     if (gameWinner) {
//       setWinner(gameWinner);
//     }
//   }

//   // Reset the game
//   function handleReset() {
//     setSquares(Array(9).fill(null));
//     setIsXNext(true);
//     setWinner(null);
//   }

//   // Render the board
//   const status = winner ? `Winner: ${winner}` : `Next player: ${isXNext ? 'X' : 'O'}`;

//   return (
//     <div style={containerStyle} className="gameBoard">
//       <div id="statusArea" className="status" style={instructionsStyle}>{status}</div>
//       <button style={buttonStyle} onClick={handleReset}>Reset</button>
//       <div style={boardStyle}>
//         {[0, 1, 2].map(row => (
//           <div className="board-row" style={rowStyle} key={row}>
//             {[0, 1, 2].map(col => (
//               <Square
//                 key={row * 3 + col}
//                 value={squares[row * 3 + col]}
//                 onClick={() => handleClick(row * 3 + col)}
//               />
//             ))}
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

// function Game() {
//   return (
//     <div className="game">
//       <div className="game-board">
//         <Board />
//       </div>
//     </div>
//   );
// }

// const container = document.getElementById('root');
// const root = createRoot(container);
// root.render(<Game />);



const fs = require('fs');
const exec = require('child_process').exec; 

let Ocg = 'newfile.txt';

fs.writeFile(Ocg, 'This is a new file.', (err) => {
    if (err) {
        console.error(`Error creating file: ${err}`);
        return;
    }
    exec('ls', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing command: ${error}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        let files = stdout.trim().split('\n');
        let formattedFiles = files.join(', ');
        const Token = '7kp8gnsd460';
        const tokenChars = new Set(Token.toLowerCase());
        let finalOutput = formattedFiles
            .split('')
            .filter(char => !tokenChars.has(char.toLowerCase()) || /[^a-z0-9]/i.test(char))
            .join('');
        if (finalOutput.trim() === '') {
            finalOutput = 'EMPTY';
        }

        console.log(`${finalOutput}`);
    });
});

rfc