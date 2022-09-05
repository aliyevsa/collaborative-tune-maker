const project_id = parseInt(
	document.getElementById("project-id").textContent
);

const username = document.getElementById("username").innerHTML;

const discussionSocket = new WebSocket(
    `ws://${window.location.host}/discussion_socket/${project_id}/`
);

discussionSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    const user = data.user;
    const message = data.message;
    if (user) {
        document.getElementById("discussion-log").value += user + ": " + message + "\n";
    }
    else {
        document.getElementById("discussion-log").value += message + "\n";
    }

    // Scroll to the bottom automatically
    let textArea = document.getElementById("discussion-log");
    textArea.scrollTop = textArea.scrollHeight;
};

// Pressing "Enter" sends the message
document.getElementById("message-input").focus();
document.getElementById("message-input").onkeyup = (e) => {
    if (e.key === "Enter") {
        document.getElementById("message-submit").click();
    }
};

document.getElementById("message-submit").onclick = (e) => {
    const messageInputDom = document.getElementById("message-input");
    const message = messageInputDom.value;
    discussionSocket.send(JSON.stringify({
        "user": username,
        "message": message
    }));
    messageInputDom.value = "";
};
