export function GET({ params }) {
    const { token } = params;

    return fetch(`${import.meta.env.VITE_BACKEND_URL}/api/oauth2/get_info/${token}`);
}