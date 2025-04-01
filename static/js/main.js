// Mapping of original column names to new display names.
const columnMapping = {
    "area_code": "CEP",
    "built_area_sqm": "Area construída",
    "construction_year": "Ano de construção",
    "declared_transaction_value": "Valor da transação",
    "street_name": "Logradouro",
    "street_number": "Número",
    "transaction_date": "Data da transação"
};

const handleError = (fn) => {
    return async (...args) => {
        try {
            return await fn(...args);
        } catch (error) {
            console.error(`Error in ${fn.name}:`, error);
            // You can also return a default value or throw a custom error
            return { error: 'Something went wrong' };
        }
    };
};

const fetchRealEstateData = handleError(async (logradouroFilter = '', numeroFilter = '') => {
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
        // Rebuild table headers using the friendly names.
        const headerRow = document.getElementById('table-headers');
        headerRow.innerHTML = '';
        Object.keys(data[0]).forEach(key => {
            const th = document.createElement('th');
            // Use display name if available, otherwise use the key.
            th.textContent = columnMapping[key] || key;
            headerRow.appendChild(th);
        });
        // Build table body.
        data.forEach(item => {
            const row = document.createElement('tr');
            Object.entries(item).forEach(([key, value]) => {
                const td = document.createElement('td');
                if (key === 'area_code') {
                    // Ensure the CEP has 8 digits and format as 5 digits-3 digits.
                    let cepStr = value.toString().padStart(8, '0');
                    value = `${cepStr.slice(0, 5)}-${cepStr.slice(5)}`;
                } else if (key === 'declared_transaction_value') {
                    // Format the transaction value as R$ currency.
                    value = new Intl.NumberFormat('pt-BR', {
                        style: 'currency',
                        currency: 'BRL'
                    }).format(value);
                }
                td.textContent = value;
                row.appendChild(td);
            });
            tbody.appendChild(row);
        });
    }
});

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
