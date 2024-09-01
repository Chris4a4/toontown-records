export async function load() {
    const [recordResponse, usersResponse] = await Promise.all([
        fetch(`${import.meta.env.VITE_BACKEND_URL}/api/records/get_all_records`),
		fetch(`${import.meta.env.VITE_BACKEND_URL}/api/accounts/get_all_users`)
    ]);

    const [recordData, usersData] = await Promise.all([
        recordResponse.json(),
		usersResponse.json()
    ]);

	usersData.data = Object.entries(usersData.data).reduce((acc, [key, value]) => (acc[value] = key, acc), {})

    return {
        recordData: recordData.data,
		usersData: usersData.data
    };
}