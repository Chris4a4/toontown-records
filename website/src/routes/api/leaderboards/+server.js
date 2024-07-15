export function GET({ params }) {
  return fetch(`http:backend:8000/api/leaderboards/get_leaderboard/ttr`);
}