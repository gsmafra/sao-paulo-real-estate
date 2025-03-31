async function fetchRealEstateData(logradouroFilter = '', numeroFilter = '') {
    try {
        let url = '/real-estate';
        const params = new URLSearchParams();
        if (logradouroFilter) {
            params.append('search', logradouroFilter);
        }
        if (numeroFilter) {
            params.append('numero', numeroFilter);
        }
        if ([...params].length > 0) {
            url += '?' + params.toString();
        }
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const tbody = document.getElementById('real-estate-listings');
        tbody.innerHTML = ''; // Clear table content

        if (data.length > 0) {
            // Rebuild table headers.
            const headerRow = document.getElementById('table-headers');
            headerRow.innerHTML = '';
            Object.keys(data[0]).forEach(key => {
                const th = document.createElement('th');
                th.textContent = key;
                headerRow.appendChild(th);
            });
            // Build table body.
            data.forEach(item => {
                const row = document.createElement('tr');
                Object.values(item).forEach(value => {
                    const td = document.createElement('td');
                    td.textContent = value;
                    row.appendChild(td);
                });
                tbody.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error fetching real estate data:', error);
    }
}

// When the page loads, fetch without filters.
window.onload = () => fetchRealEstateData();

// Filter button event listener.
document.getElementById('filter-btn').addEventListener('click', () => {
    const logradouroFilter = document.getElementById('logradouro-filter').value;
    const numeroFilter = document.getElementById('numero-filter').value;
    fetchRealEstateData(logradouroFilter, numeroFilter);
});

// Add event listeners to inputs for Enter key.
const logradouroInput = document.getElementById('logradouro-filter');
const numeroInput = document.getElementById('numero-filter');

[logradouroInput, numeroInput].forEach(input => {
    input.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            const logradouroFilter = logradouroInput.value;
            const numeroFilter = numeroInput.value;
            fetchRealEstateData(logradouroFilter, numeroFilter);
        }
    });
});
