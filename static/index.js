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

        
$(function() {
    $('nav').each(function() {
        var $active, $content, $links = $(this).find('a');

        $active = $($links.filter('[href="' + location.hash + '"]')[0] || $links[0]);
        $active.addClass('active');

        $content = $($active[0].hash);

        $links.not($active).each(function() {
            $(this.hash).hide();
        });

        $(this).on('click', 'a', function(e) {
            $active.removeClass('active');
            $content.hide();

            $active = $(this);
            $content = $(this.hash);

            $active.addClass('active');
            $content.show();

            e.preventDefault();
        });
    });
});
    
    
  

    