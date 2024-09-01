export async function load({ fetch }) {
    const [leaderboardResponse, usersResponse] = await Promise.all([
        fetch(`${import.meta.env.VITE_BACKEND_URL}/api/leaderboards/get_leaderboard/ttr`),
		fetch(`${import.meta.env.VITE_BACKEND_URL}/api/accounts/get_all_users`)
    ]);

    const [leaderboardData, usersData] = await Promise.all([
        leaderboardResponse.json(),
		usersResponse.json()
    ]);

	usersData.data = Object.entries(usersData.data).reduce((acc, [key, value]) => (acc[value] = key, acc), {})

    return {
        leaderboardData: leaderboardData.data,
		usersData: usersData.data
    };
  }