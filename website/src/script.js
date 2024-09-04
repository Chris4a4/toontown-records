window.addEventListener('load', () => {
    fetch('api/leaderboards/top3')
        .then(response => response.json())
        .then(data => {
            document.getElementById('rank1_name').textContent = `${data[0].username}`;
            document.getElementById('rank2_name').textContent = `${data[1].username}`;
            document.getElementById('rank3_name').textContent = `${data[2].username}`;

            document.getElementById('rank1_points').textContent = `${data[0].points}`;
            document.getElementById('rank2_points').textContent = `${data[1].points}`;
            document.getElementById('rank3_points').textContent = `${data[2].points}`;

            if (data[0].pfp != null){
                document.getElementById('rank1_pfp').src = `${data[0].pfp}`;
            }
            if (data[1].pfp != null){
                document.getElementById('rank2_pfp').src = `${data[1].pfp}`;
            }
            if (data[2].pfp != null){
                document.getElementById('rank3_pfp').src = `${data[2].pfp}`;
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
