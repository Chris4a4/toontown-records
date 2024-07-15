export function GET({ params }) {
    return fetch(`http:backend:8000/api/records/get_all_records`);
}