export function money(value) {
  return Number(value).toLocaleString("en-US", { style: "currency", currency: "USD" });
}
