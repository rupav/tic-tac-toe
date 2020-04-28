# tic-tac-toe
A react Js based tic tac toe game

* Frontend is made using React, hosted on gh-pages: https://rupav.github.io/tic-tac-toe/.
* Backend is made using Flask, hosted on heroku: https://rupav-tic-tac-toe.herokuapp.com/api/.

**Implementation**

* Bot always plays the first move. User then plays against the bot in an alternate turns manner, aiming to fill any row, column or diagonal with its shape, ‘O’. First to do that wins the game, if there are no moves left, the game is declared a draw. 

* For its move, ReactJS sends the current state of the board to the server as a POST request, where a python script is run to choose the next move optimally, and then a 201 response is sent back along with the optimal move of the bot. 

* Frontend, then on receiving the response changes the view. But for the bot to play optimally, first we have to train it. 

* So to do that, the view provides a ‘form in a modal’ to train, in which the user has to set the different parameters - alpha (learning rate of the agent/bot), and episodes (how many epochs bot will play to get trained using Reinforcement Learning).

* On ‘form submit’, a POST request is sent to the server, and again a python script is run on the backend to train with given inputs.

* After training, a response with 201 code along with the value function array is sent over as the response. This Value function array is basically what used to decide the next optimal move.

* So this being important data has to be stored somewhere. This job is done by our model, redux store. Now for each subsequent request to the server, this data is sent along the request, to be used by the controller for the next optimal move in the way our bot is trained by the user. 

* Also the ‘view’ provides the option to revisit the previous state of the board, and then even rewrite the history (in short ‘Undo’ option).

So this way we can train the bot to play against us in an optimal manner, always trying to defeat us!


**Contributors**:

* [Rupav Jain](https://github.com/rupav/)
