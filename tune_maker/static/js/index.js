document.getElementById("public-project-id-submit").onclick = (e) => {
    const public_project_id = document.getElementById("public-project-id").value;
    window.location.pathname = `/public/project/${public_project_id}/`;
};

// Pressing "Enter" sends the message
document.getElementById("public-project-id").focus();
document.getElementById("public-project-id").onkeyup = (e) => {
    if (e.key === "Enter") {
        document.getElementById("public-project-id-submit").click();
    }
};