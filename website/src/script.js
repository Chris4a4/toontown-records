// Update Leaderboard Info
window.addEventListener('load', () => {
    fetch('api/leaderboards/top3')
        .then(response => response.json())
        .then(data => {
            if (data.length >= 1){
                document.getElementById('rank1_name').textContent = `${data[0].username}`;
                document.getElementById('rank1_points').textContent = `${data[0].points}`;
                if (data[0].pfp != null){
                    document.getElementById('rank1_pfp').src = `${data[0].pfp}`;
                }
            }

            if (data.length >= 2){
                document.getElementById('rank2_name').textContent = `${data[1].username}`;
                document.getElementById('rank2_points').textContent = `${data[1].points}`;
                if (data[1].pfp != null){
                    document.getElementById('rank2_pfp').src = `${data[1].pfp}`;
                }
            }

            if (data.length >= 3){
                document.getElementById('rank3_name').textContent = `${data[2].username}`;
                document.getElementById('rank3_points').textContent = `${data[2].points}`;
                if (data[2].pfp != null){
                    document.getElementById('rank3_pfp').src = `${data[2].pfp}`;
                }
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});

// Update Recent Records
window.addEventListener('load', () => {
    fetch('api/leaderboards/recent')
        .then(response => response.json())
        .then(data => {
            if (data.length >= 1){
                document.getElementById('recent-1-title').textContent = `${data[0].record_name}`;
                document.getElementById('recent-1-score').textContent = `${data[0].score_string}`;
                document.getElementById('recent-1-submitters').textContent = `${data[0].usernames}`;
                if (data[0].thumbnail_url != null){
                    document.getElementById('recent-1-thumbnail').src = `${data[0].thumbnail_url}`;
                }
            }

            if (data.length >= 2){
                document.getElementById('recent-2-title').textContent = `${data[1].record_name}`;
                document.getElementById('recent-2-score').textContent = `${data[1].score_string}`;
                document.getElementById('recent-2-submitters').textContent = `${data[1].usernames}`;
                if (data[1].thumbnail_url != null){
                    document.getElementById('recent-2-thumbnail').src = `${data[1].thumbnail_url}`;
                }
            }

            if (data.length >= 3){
                document.getElementById('recent-3-title').textContent = `${data[2].record_name}`;
                document.getElementById('recent-3-score').textContent = `${data[2].score_string}`;
                document.getElementById('recent-3-submitters').textContent = `${data[2].usernames}`;
                if (data[2].thumbnail_url != null){
                    document.getElementById('recent-3-thumbnail').src = `${data[2].thumbnail_url}`;
                }
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
