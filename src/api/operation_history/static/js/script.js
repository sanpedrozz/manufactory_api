async function fetchOperationHistory() {
    try {
        const response = await fetch('/operation_history/list?limit=100');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const tableBody = document.querySelector('#operation-history-table tbody');
        tableBody.innerHTML = ''; // Clear existing rows

        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.place}</td>
                <td>${item.program}</td>
                <td>${item.data}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching operation history:', error);
    }
}

// Fetch and display operation history when the page loads
window.onload = function() {
    fetchOperationHistory();
    // Set interval to refresh data every second
    setInterval(fetchOperationHistory, 1000);

};
