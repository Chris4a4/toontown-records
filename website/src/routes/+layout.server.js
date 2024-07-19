export async function load() {
    const [recordResponse, leaderboardResponse, usersResponse] = await Promise.all([
        fetch(`http://backend:8000/api/records/get_all_records`),
        fetch(`http://backend:8000/api/leaderboards/get_leaderboard/ttr`),
		fetch(`http:backend:8000/api/accounts/get_all_users`)
    ]);

    const [recordData, leaderboardData, usersData] = await Promise.all([
        recordResponse.json(),
        leaderboardResponse.json(),
		usersResponse.json()
    ]);

	usersData.data = Object.entries(usersData.data).reduce((acc, [key, value]) => (acc[value] = key, acc), {})

    return {
        recordData: recordData.data,
        leaderboardData: leaderboardData.data,
		usersData: usersData.data
    };
}