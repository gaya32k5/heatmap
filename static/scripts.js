document.getElementById('profileForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const profileUrl = document.getElementById('profileUrl').value;

    fetch('/analyze_profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `profile_url=${encodeURIComponent(profileUrl)}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('results').style.display = 'block';

            // Display the bio and images
            document.getElementById('paragraphs').innerText = data.data.paragraphs.join('\n');
            const deepfakeList = document.getElementById('deepfakeResults');
            deepfakeList.innerHTML = '';
            Object.keys(data.data.deepfake_results).forEach(image => {
                const li = document.createElement('li');
                li.textContent = `${image}: ${data.data.deepfake_results[image]}`;
                deepfakeList.appendChild(li);
            });

            // Apply the heatmap to bio and images
            applyHeatmap(data.data.suspicion_scores);
        }
    });
});

function applyHeatmap(suspicionScores) {
    // Example: Highlight the bio section
    const bioSection = document.getElementById('bioSection');
    if (suspicionScores.bio >= 0.8) {
        bioSection.style.backgroundColor = 'red';
    } else if (suspicionScores.bio >= 0.4) {
        bioSection.style.backgroundColor = 'yellow';
    } else {
        bioSection.style.backgroundColor = 'green';
    }

    // Similarly for images or other sections
    const imageSection = document.getElementById('imageSection');
    if (suspicionScores.images >= 0.8) {
        imageSection.style.backgroundColor = 'red';
    } else if (suspicionScores.images >= 0.4) {
        imageSection.style.backgroundColor = 'yellow';
    } else {
        imageSection.style.backgroundColor = 'green';
    }
}
