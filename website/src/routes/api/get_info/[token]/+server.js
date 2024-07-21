export function GET({ params }) {
    const { token } = params;

    return fetch(`http://backend:8000/api/oauth2/get_info/${token}`);
}