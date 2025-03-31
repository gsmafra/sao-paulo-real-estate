async function fetchRealEstateData() {
    try {
        const response = await fetch('/real-estate'); // Replace with your actual endpoint
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const table = document.getElementById('real-estate-listings');
        table.innerHTML = ''; // Clear existing table content

        if (data.length > 0) {
            // Create table headers dynamically
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            Object.keys(data[0]).forEach(key => {
                const th = document.createElement('th');
                th.textContent = key;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            // Create table body dynamically
            const tbody = document.createElement('tbody');
            data.forEach(item => {
                const row = document.createElement('tr');
                Object.values(item).forEach(value => {
                    const td = document.createElement('td');
                    td.textContent = value;
                    row.appendChild(td);
                });
                tbody.appendChild(row);
            });
            table.appendChild(tbody);
        }
    } catch (error) {
        console.error('Error fetching real estate data:', error);
    }
}

// Fetch data when the page loads
window.onload = fetchRealEstateData;
