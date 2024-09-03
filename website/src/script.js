window.addEventListener('load', () => {
    // URL of the data you want to fetch
    const url = 'api/leaderboards/top3'; // Example API

    // Fetch data from the URL
    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById('rank1_name').textContent = `${data[0].username}`;
            document.getElementById('rank2_name').textContent = `${data[1].username}`;
            document.getElementById('rank3_name').textContent = `${data[2].username}`;

            document.getElementById('rank1_points').textContent = `${data[0].points}`;
            document.getElementById('rank2_points').textContent = `${data[1].points}`;
            document.getElementById('rank3_points').textContent = `${data[2].points}`;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});