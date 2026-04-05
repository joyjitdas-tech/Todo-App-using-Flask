    // Toggle Task Status
function toggleTask(taskId, checkboxEl) {
    fetch(`/task/toggle/${taskId}`, { method: 'POST' })
    .then(res => {
        if (res.ok) {
            const taskCard = checkboxEl.closest('.task-card');
            if (checkboxEl.checked) {
                taskCard.classList.add('completed'); // Turns green
            } else {
                taskCard.classList.remove('completed');
            }
        } else {
            alert('Error updating task status');
        }
    })
    .catch(err => console.error(err));
}

document.addEventListener("DOMContentLoaded", function () {
    // ✅ Select all tasks after DOM is loaded
    const tasks = document.querySelectorAll('.task-card');

    // Tabs
    const tabs = document.querySelectorAll('.tab-btn');



    // Countdown Timer
    function updateCountdown() {
        tasks.forEach(el => {
            const countdownEl = el.querySelector('.countdown');
            if (!countdownEl) return;
            const deadlineStr = countdownEl.dataset.deadline;
            if (!deadlineStr) return;

            const deadline = new Date(deadlineStr);
            const now = new Date();
            const diff = deadline - now;
            if (diff <= 0) countdownEl.innerText = "Deadline passed";
            else {
                const days = Math.floor(diff / (1000*60*60*24));
                const hours = Math.floor((diff / (1000*60*60)) % 24);
                const minutes = Math.floor((diff / (1000*60)) % 60);
                const seconds = Math.floor((diff / 1000) % 60);
                countdownEl.innerText = `${days}d ${hours}h ${minutes}m ${seconds}s`;
            }
        });
    }
    setInterval(updateCountdown, 1000);
    updateCountdown();

    // Filter Tasks by Tab
    function filterTasks(type) {
        const now = new Date();
        const today = new Date();
        today.setHours(0,0,0,0);
        const tomorrow = new Date(today);
        tomorrow.setDate(today.getDate()+1);

        tasks.forEach(task => {
            const status = task.dataset.status;
            const deadlineStr = task.dataset.deadline;
            if (!deadlineStr) { task.style.display = 'none'; return; }
            const deadline = new Date(deadlineStr);

            if (type === 'today') task.style.display = (deadline >= today && deadline < tomorrow) ? 'block' : 'none';
            else if (type === 'upcoming') task.style.display = (deadline >= tomorrow) ? 'block' : 'none';
            else if (type === 'overdue') task.style.display = (deadline < now && status !== 'completed') ? 'block' : 'none';
        });
    }

    // Default Tab → Today
    filterTasks('today');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            filterTasks(tab.dataset.tab);
        });
    });

    // Highlight overdue tasks
    tasks.forEach(task => {
        const status = task.dataset.status;
        const deadlineStr = task.dataset.deadline;

        if (!deadlineStr) return;

        const deadline = new Date(deadlineStr);
        const now = new Date();

        // ❗ If completed → always green
        if (status === 'completed') {
            task.classList.add('completed');
            return;
        }

        // ❗ If not completed and overdue → red
        if (deadline < now) {
            task.classList.add('overdue');
        }
    });

    // Graph (Chart.js)
    const completedTasks = [...tasks].filter(t => t.dataset.status === 'completed').length;
    const pendingTasks = [...tasks].filter(t => t.dataset.status !== 'completed').length;
    const ctx = document.getElementById('progressChart')?.getContext('2d');
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Pending'],
                datasets: [{ data: [completedTasks, pendingTasks], backgroundColor: ['#4CAF50', '#FF9800'] }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });
    }
});