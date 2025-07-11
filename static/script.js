document.addEventListener('DOMContentLoaded', () => {
    const listingsTbody = document.getElementById('listings-tbody');
    const searchButton = document.getElementById('search-button');
    const promptInput = document.getElementById('prompt-input');
    const resultsList = document.getElementById('search-results-list');
    const chatbotResponseEl = document.getElementById('chatbot-response');

    // --- 1. Fetch and display all listings on page load ---
    fetch('/listings')
        .then(response => response.json())
        .then(data => {
            if (!data || data.length === 0) {
                listingsTbody.innerHTML = '<tr><td colspan="7">No listings found.</td></tr>';
                return;
            }
            data.forEach(car => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${car.Year}</td>
                    <td>${car.Make}</td>
                    <td>${car.Model}</td>
                    <td>${car.Mileage.toLocaleString()}</td>
                    <td>$${car.Price.toLocaleString()}</td>
                    <td>${car.City}</td>
                    <td>${car.State}</td>
                `;
                listingsTbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching listings:', error);
            listingsTbody.innerHTML = '<tr><td colspan="7">Failed to load listings.</td></tr>';
        });

    // --- 2. Handle search button click ---
    const performSearch = () => {
        const prompt = promptInput.value;
        if (!prompt) {
            alert('Please enter a search prompt.');
            return;
        }

        resultsList.innerHTML = '<li>Searching...</li>';
        chatbotResponseEl.style.display = 'none'; // Hide old response

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt }),
        })
        .then(response => response.json())
        .then(data => {
            resultsList.innerHTML = ''; // Clear "Searching..." message
            
            // Display the chatbot response text
            if (data && data.response_text) {
                chatbotResponseEl.textContent = data.response_text;
                chatbotResponseEl.style.display = 'block'; // Make it visible
            }

            const results = data.results;
            if (!results || results.length === 0) {
                resultsList.innerHTML = '<li>No matching cars found.</li>';
                return;
            }
            
            results.forEach(result => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span class="match-score">${result.match_percentage.toFixed(2)}% Match:</span>
                    ${result.description} (ID: ${result.listing_id})
                `;
                resultsList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error performing search:', error);
            resultsList.innerHTML = '<li>An error occurred during search.</li>';
            chatbotResponseEl.style.display = 'none';
        });
    };

    searchButton.addEventListener('click', performSearch);
    
    // Allow pressing Enter to search
    promptInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            performSearch();
        }
    });
}); 