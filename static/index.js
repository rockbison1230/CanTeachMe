function submitText() {
    const inputText = document.getElementById('expression').value;

    fetch('/', {
        method: 'POST',
        body: JSON.stringify({ text: userInput }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    
    .then(response => response.json())
    .then(data => {
        const resultsContainer = document.getElementById('sentiment');
        resultsContainer.innerHTML += `<p>Sentiment: ${data.sentiment}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // Clear the input field after submission
    document.getElementById('textInput').value = '';
}

    