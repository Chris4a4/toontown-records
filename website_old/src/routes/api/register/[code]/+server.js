export function GET({ params }) {
    const { code } = params;

    return fetch(`${import.meta.env.VITE_BACKEND_URL}/api/oauth2/register/${code}`);
}