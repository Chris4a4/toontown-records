// Converts ms to a time string
function toTime(ms) {
  // Compute hours, minutes, seconds, and milliseconds
  let s = Math.floor(ms / 1000);
  ms = ms % 1000;
  let m = Math.floor(s / 60);
  s = s % 60;
  let h = Math.floor(m / 60);
  m = m % 60;

  let msPart = ms === 0 ? '' : `.${ms.toString().padStart(3, '0')}`;

  // Format the string depending on what kind of time it is
  if (h !== 0) {
    return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}${msPart}`;
  } else if (m !== 0) {
    return `${m}:${s.toString().padStart(2, '0')}${msPart}`;
  }

  return `${s}${msPart}`;
}

// Using a record's tags, correctly formats its score
export function valueString(submission, tags = []) {
  let score = submission['value_score'];
  let time = submission['value_time'];

  // Check for null
  let timeString = time === null ? '???' : toTime(time);

  let scoreString;
  let scorePlural;
  if (score === null) {
    scoreString = '???';
    scorePlural = 's';
  } else {
    scoreString = score;
    scorePlural = score === 1 ? '' : 's';
  }

  // Format based on tags
  if (tags.includes('golf')) {
    return `${scoreString} swing${scorePlural}, ${timeString}`;
  }

  if (tags.includes('min_rewards')) {
    return `${scoreString} reward${scorePlural}, ${timeString}`;
  }

  if (tags.length > 0) {
      return timeString;
  }

  // Unknown record/no tags provided, use sensible default format
  return `${scoreString} score, ${timeString} time`;
}