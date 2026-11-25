// Turns a time sent by the server into a short date such as "25 Nov 2026".
export function formatDate(value) {
  // The server sends UTC times without a time zone marker, so add one before reading the date.
  const hasZone = value.endsWith("Z") || /[+-]\d\d:\d\d$/.test(value);
  const date = new Date(hasZone ? value : `${value}Z`);
  return date.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}
