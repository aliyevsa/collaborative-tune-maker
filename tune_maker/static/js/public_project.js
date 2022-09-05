const project_id = parseInt(
	document.getElementById("project-id").textContent
);

let playButton = document.getElementById("play-button");

let projectLoaded = false;

const notes = [
	"C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A5", "A#5", "B5",
	"C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A6", "A#6", "B6",
];
let song;

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
let blockColour;
let activatedBlockColour;
let playingBlockColour;

let polySynth;
let playing = false;
let playingTimeout;

function preload() {
    let tune_rows_request = new XMLHttpRequest();
    tune_rows_request.onreadystatechange = () => {
        if (tune_rows_request.readyState == 4 &&
            tune_rows_request.status >= 200 &&
            tune_rows_request.status < 400) {
            const tune_rows = JSON.parse(tune_rows_request.responseText);

            song = new Array(tune_rows.length);
            
            for (let i = 0; i < song.length; i++) song[i] = new Set();

            for (let i = 0; i < song.length; i++) {
                const notes_id = tune_rows[i]["notes"];
                let notes_request = new XMLHttpRequest();
                notes_request.onreadystatechange = () => {
                    if (notes_request.readyState == 4 &&
                        notes_request.status >= 200 &&
                        notes_request.status < 400) {
                        const tune_row_notes = JSON.parse(notes_request.responseText);

                        for (let j = 0; j < notes.length; j++) {
                            if (tune_row_notes[`note_${j + 1}`]) {
                                song[i].add(notes[j]);
                            }
                        }
                    }
                };
                notes_request.open("GET", `/api/notes/${notes_id}`, true);
                notes_request.send();
            }
        }
    };
    tune_rows_request.open("GET", `/api/tune_rows/${project_id}`, true);
    tune_rows_request.send();

    blockColour = color(0, 0, 0, 30);
    activatedBlockColour = color(63, 165, 162);
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

function stopSong() {
	polySynth.dispose();
    clearInterval(rowInterval);
    currentRow = 0;
    playButton.innerText = "⏵ Play";
    window.scrollTo(0, 0);
}

function setup() {
    if (song) {
        let canvas = createCanvas(blockHeight * 24, blockHeight * song.length);

        blockWidth = canvas.width / notes.length;
    
        noStroke();
    }
}

function draw() {
    if (!projectLoaded) {
        if (song) {
            projectLoaded = true;
            setup();
        }
    }

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
                else {
					fill(activatedBlockColour);
				}
			}
			// Do not highlight the block if the song does not have the note
			else {
				fill(blockColour);
			}
			rect(x + margin, y + margin, blockWidth - margin * 2, blockHeight - margin * 2, cornerRadius);
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
        playSong(song);
    }
};
