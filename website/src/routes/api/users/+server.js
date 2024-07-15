export function GET({ params }) {
    return fetch(`http:backend:8000/api/accounts/get_all_users`);
}