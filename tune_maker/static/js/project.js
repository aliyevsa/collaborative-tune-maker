const project_id = parseInt(
	document.getElementById("project-id").textContent
);

const songLength = parseInt(
	document.getElementById("project-length").textContent
);

let playButton = document.getElementById("play-button");

let projectLoaded = false;

const notes = [
	"C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A5", "A#5", "B5",
	"C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A6", "A#6", "B6",
];

let song = new Array(songLength);
for (let i = 0; i < songLength; i++) song[i] = new Set();

// Durations (seconds)
let blockDuration = 0.2;
let noteDuration = 0.17;

let rowInterval;
let currentRow = 0;

// Note volume (0 to 1)
let velocity = 0.5;

const margin = 3;
const cornerRadius = 6;

const blockHeight = 30;
let blockWidth;
let blockColours;
let activatedBlockColours;
let playingBlockColour;

let polySynth;
let playing = false;
let playingTimeout;

const projectSocket = new WebSocket(
    `ws://${window.location.host}/project_socket/${project_id}/`
);

projectSocket.onmessage = (e) => {
	data = JSON.parse(e.data);
	if (projectLoaded) {
		// Receive the latest block update
		const row = data.row;
		const note = data.note;
		const operation = data.operation;
	
	
		if (operation === "add") {
			song[row].add(notes[note]);
		}
		else if (operation === "delete") {
			song[row].delete(notes[note]);
		}
	}
	else {
		// Retrieve the latest state of the project
		const previous_notes = data.previous_notes;

		for (let i = 0; i < previous_notes.length; i++) {
			for (let j = 0; j < notes.length; j++) {
				if (previous_notes[i][j]) {
					song[i].add(notes[j]);
				}
			}
		}

		projectLoaded = true;
	}
};

function preload() {
	blockColours = [color(0, 0, 0, 30), color(0, 0, 0, 45), color(0, 0, 0, 60)];
	activatedBlockColours = [color(63, 165, 162), color(83, 185, 182), color(103, 205, 202)];
	playingBlockColour = color(175, 64, 64);
}

function playSong() {
	userStartAudio();
	polySynth = new p5.PolySynth();

	// Time tracker (seconds)
	let time = 0;

	// Iterate over the song
	for (let i = 0; i < song.length; i++) {
		// Notes can be played at the same time to create a chord
		song[i].forEach((note) => {
			polySynth.play(note, velocity, time, noteDuration);
		});

		// Progress through the time to get to the next section of the song
		time += blockDuration;
	}

	// Track which row is currently being played
    rowInterval = setInterval(() => {
        currentRow++;

		// Scroll down to follow the row being played
		window.scrollBy(0, blockHeight);

		if (currentRow == song.length) {
			stopSong();
		}
    }, blockDuration * 1000);

    playButton.innerText = "■ Stop";
}

function playNote(note) {
	userStartAudio();
	polySynth = new p5.PolySynth();
	const time = 0;
	polySynth.play(note, velocity, time, noteDuration);
}

function stopSong() {
	polySynth.dispose();
    clearInterval(rowInterval);
    currentRow = 0;
    playButton.innerText = "⏵ Play";
	window.scrollTo(0, 0);
}

function setup() {
	let canvas = createCanvas(blockHeight * 24, blockHeight * songLength);

	blockWidth = canvas.width / notes.length;

	noStroke();
}

function draw() {
	clear();

	// Draw the blocks
	for (let i = 0; i < song.length; i++) {
		for (let j = 0; j < notes.length; j++) {
			const x = j * blockWidth;
			const y = i * blockHeight;

			// Highlight the block if the song has the note
			if (song[i].has(notes[j])) {
				if (playing && currentRow == i) {
					fill(playingBlockColour);
				}
				else if (
					mouseX > x &&
					mouseX < x + blockWidth &&
					mouseY > y &&
					mouseY < y + blockHeight
				) {
					if (mouseIsPressed) {
						fill(activatedBlockColours[2]);
					}
					else {
						fill(activatedBlockColours[1]);
					}
				}
				else {
					fill(activatedBlockColours[0]);
				}
			}
			// Do not highlight the block if the song does not have the note
			else {
				if (
					mouseX > x &&
					mouseX < x + blockWidth &&
					mouseY > y &&
					mouseY < y + blockHeight
				) {
					if (mouseIsPressed) {
						fill(blockColours[2]);
					}
					else {
						fill(blockColours[1]);
					}
				}
				else {
					fill(blockColours[0]);
				}
			}
			rect(x + margin, y + margin, blockWidth - margin * 2, blockHeight - margin * 2, cornerRadius);
		}
	}
}

function mouseClicked() {
	for (let i = 0; i < song.length; i++) {
		for (let j = 0; j < notes.length; j++) {
			const x = j * blockWidth;
			const y = i * blockHeight;

			if (
				mouseX > x &&
				mouseX < x + blockWidth &&
				mouseY > y &&
				mouseY < y + blockHeight
			) {
				if (song[i].has(notes[j])) {
                    projectSocket.send(JSON.stringify({
                        "row": i,
                        "note": j,
                        "operation": "delete"
                    }));
				} else {
                    projectSocket.send(JSON.stringify({
                        "row": i,
                        "note": j,
                        "operation": "add"
                    }));

					if (!playing) {
						playNote(notes[j]);
					}
				}
			}
		}
	}
}

playButton.onclick = (e) => {
    if (playing) {
        playing = false;
        clearTimeout(playingTimeout);
        stopSong();
    }
    else {
        playing = true;
        playingTimeout = setTimeout(() => {
            playing = false;
        }, song.length * blockDuration * 1000);
        playSong();
    }
};
