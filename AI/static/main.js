let reset = false;

function display_result(win){
    let result = document.getElementById('result')
    if (win){
        result.innerHTML = 'WIN'
    } else {
        result.innerHTML = 'LOSE'
    };
};

function display_board(board, uncovered, flagged) {
    // Clear the previous content of the board
    document.getElementById('board_div').innerHTML = "";
    document.getElementById('result').innerHTML = "";

    let content = "";

    // Loop through each cell in the board
    for (let i = 0; i < board.length; i++) {
        for (let j = 0; j < board[i].length; j++) {
            let value = board[i][j];
            let coords = [i, j];
            let isUncovered = uncovered.some(arr => arr[0] === coords[0] && arr[1] === coords[1]);

            // Check if the current cell is uncovered
            if (isUncovered) {
                if (value == -1) {
                    content += `<button id='${i} ${j}' class='board_button'>X</button>`;
                } else if (value == 0) {
                    content += `<button id='${i} ${j}' class='board_button button_uncovered'></button>`;
                } else {
                    content += `<button id='${i} ${j}' class='board_button button_uncovered'>${value}</button>`;
                }
            }
            // If the cell is flagged
            else if (flagged.some(arr => arr[0] === coords[0] && arr[1] === coords[1])) {
                content += `<button id='${i} ${j}' class='board_button button_flagged' oncontextmenu='flag(this)'></button>`;
            } 
            // If the cell is not uncovered or flagged
            else {
                content += `<button id='${i} ${j}' class='board_button' onclick='dig(this)' oncontextmenu='flag(this)'></button>`;
            }
        }
        content += "<br>"; // New row
    }

    // Add the constructed content to the board_div element
    document.getElementById('board_div').innerHTML = content;
};



function initialise(size) {
    reset = true;

	fetch('/initialise', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({size: size})
        })
    .then(response => response.json())
    .then(data => {
    	display_board(data.board, [], []);

    });
};

function flag(button) {
    if (button.classList.contains('button_flagged')) {
        button.classList.remove("button_flagged");
        button.setAttribute('onclick', 'dig(this)');
    } else {
        button.classList.add('button_flagged');
    };

    let coords = button.id;

    fetch('/flag', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({coords: coords})
        })
    .then(response => response.json())
    .then(data => {
        console.log(data.flagged)
    });
};

function dig(button) {
    let coords = button.id;

    fetch('/dig', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({coords: coords})
        })
    .then(response => response.json())
    .then(data => {
        display_board(data.board, data.uncovered, data.flagged);

        if (data.result == 1) {
            display_result(true)
        } else if (data.result == -1) {
            display_result(false)
        };
    });
};

async function dig_one() {
    const response = await fetch('/dig_ai', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    });

    const data = await response.json();
    
    display_board(data.board, data.uncovered, data.flagged);

    if (data.result === 1) {
        display_result(true);
        return true;
    } else if (data.result === -1) {
        display_result(false);
        return true;
    } else {
        return false;
    }
};

async function dig_all() {
    if (!reset) {
        return
    };

    let end = await dig_one();
    while (!end) {
        end = await dig_one();
    };
    reset = false;
};


document.addEventListener('contextmenu', function(event) {
    event.preventDefault(); // This will prevent the context menu from appearing
});