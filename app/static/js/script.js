function updateCountdown() {
    const countdowns = document.querySelectorAll('.countdown');
    countdowns.forEach(el => {
        const deadline = new Date(el.dataset.deadline);
        const now = new Date();
        const diff = deadline - now;
        if(diff <= 0){
            el.innerText = "Deadline passed";
        } else {
            const days = Math.floor(diff / (1000*60*60*24));
            const hours = Math.floor((diff / (1000*60*60)) % 24);
            const minutes = Math.floor((diff / (1000*60)) % 60);
            const seconds = Math.floor((diff / 1000) % 60);
            el.innerText = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }
    });
}
setInterval(updateCountdown, 1000);
updateCountdown();

function toggleTask(taskId) {
    fetch(`/toggle/${taskId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            alert("Error updating task!");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}