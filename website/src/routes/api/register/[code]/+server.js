export function GET({ params }) {
    const { code } = params;

    return fetch(`http://backend:8000/api/oauth2/register/${code}`);
}