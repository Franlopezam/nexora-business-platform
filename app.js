const pages = ["dashboard", "products", "customers", "sales", "inventory"];

async function init() {
  if (!API.token) return showLogin();

  try {
    const user = await API.request("/api/auth/me");
    document.querySelector("#login").classList.add("hidden");
    document.querySelector("#user-badge").textContent = `${user.name} · ${user.role}`;
    bindNavigation();
    await showPage("dashboard");
  } catch {
    showLogin();
  }
}

function showLogin() {
  document.querySelector("#app").classList.add("hidden");
  document.querySelector("#login").classList.remove("hidden");
}

function bindNavigation() {
  document.querySelectorAll("[data-page]").forEach(button => {
    button.addEventListener("click", () => showPage(button.dataset.page));
  });
  document.querySelector("#logout").addEventListener("click", () => API.logout());

  document.querySelector("#login-form").addEventListener("submit", async event => {
    event.preventDefault();
    const error = document.querySelector("#login-error");
    error.textContent = "";
    try {
      await API.login(
        document.querySelector("#email").value,
        document.querySelector("#password").value
      );
      location.reload();
    } catch (err) {
      error.textContent = err.message;
    }
  });
}

async function showPage(page) {
  pages.forEach(name => document.querySelector(`#${name}-page`).classList.toggle("hidden", name !== page));
  document.querySelector("#page-title").textContent = page[0].toUpperCase() + page.slice(1);

  if (page === "dashboard") await renderDashboard();
  if (page === "products") await renderProducts();
  if (page === "customers") await renderCustomers();
  if (page === "sales") await renderSales();
  if (page === "inventory") await renderInventory();
}

async function renderDashboard() {
  const data = await API.request("/api/dashboard/summary");
  document.querySelector("#dashboard-page").innerHTML = `
    <div class="cards">
      <div class="card"><span>Revenue</span><strong>$${data.revenue.toFixed(2)}</strong></div>
      <div class="card"><span>Sales</span><strong>${data.sales}</strong></div>
      <div class="card"><span>Products</span><strong>${data.products}</strong></div>
      <div class="card"><span>Low stock</span><strong>${data.low_stock}</strong></div>
    </div>
    <div class="panel">
      <h3>Workspace overview</h3>
      <p>Manage products, inventory, customers and sales from one place.</p>
      <a href="/api/reports/sales.csv">Export sales CSV</a>
    </div>`;
}

async function renderProducts() {
  const products = await API.request("/api/products");
  document.querySelector("#products-page").innerHTML = `
    <div class="panel">
      <div class="toolbar">
        <input id="product-search" placeholder="Search by name or SKU">
        <button class="primary" id="search-products">Search</button>
      </div>
      <table><thead><tr><th>SKU</th><th>Name</th><th>Price</th><th>Stock</th><th>Min</th></tr></thead>
      <tbody>${products.map(p => `<tr><td>${p.sku}</td><td>${p.name}</td><td>$${p.price.toFixed(2)}</td><td>${p.stock}</td><td>${p.min_stock}</td></tr>`).join("")}</tbody>
      </table>
    </div>`;
  document.querySelector("#search-products").onclick = async () => {
    const q = document.querySelector("#product-search").value;
    const rows = await API.request(`/api/products?q=${encodeURIComponent(q)}`);
    const tbody = document.querySelector("#products-page tbody");
    tbody.innerHTML = rows.map(p => `<tr><td>${p.sku}</td><td>${p.name}</td><td>$${p.price.toFixed(2)}</td><td>${p.stock}</td><td>${p.min_stock}</td></tr>`).join("");
  };
}

async function renderCustomers() {
  const customers = await API.request("/api/customers");
  document.querySelector("#customers-page").innerHTML = `
    <div class="panel"><table><thead><tr><th>Name</th><th>Email</th><th>Phone</th></tr></thead>
    <tbody>${customers.map(c => `<tr><td>${c.name}</td><td>${c.email || "—"}</td><td>${c.phone || "—"}</td></tr>`).join("")}</tbody></table></div>`;
}

async function renderSales() {
  const sales = await API.request("/api/sales");
  document.querySelector("#sales-page").innerHTML = `
    <div class="panel"><table><thead><tr><th>ID</th><th>Total</th><th>Status</th><th>Date</th></tr></thead>
    <tbody>${sales.map(s => `<tr><td>#${s.id}</td><td>$${Number(s.total).toFixed(2)}</td><td>${s.status}</td><td>${new Date(s.created_at).toLocaleString()}</td></tr>`).join("")}</tbody></table></div>`;
}

async function renderInventory() {
  const movements = await API.request("/api/inventory");
  document.querySelector("#inventory-page").innerHTML = `
    <div class="panel"><table><thead><tr><th>Product</th><th>Type</th><th>Quantity</th><th>Note</th><th>Date</th></tr></thead>
    <tbody>${movements.map(m => `<tr><td>#${m.product_id}</td><td>${m.movement_type}</td><td>${m.quantity}</td><td>${m.note || "—"}</td><td>${new Date(m.created_at).toLocaleString()}</td></tr>`).join("")}</tbody></table></div>`;
}

init();
