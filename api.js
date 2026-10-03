const API = {
  token: localStorage.getItem("nexora_token"),

  async request(path, options = {}) {
    const headers = new Headers(options.headers || {});
    if (this.token) headers.set("Authorization", `Bearer ${this.token}`);
    if (options.body && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }

    const response = await fetch(path, { ...options, headers });
    if (response.status === 401) {
      this.logout();
      throw new Error("Session expired");
    }

    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "Request failed");
    return data;
  },

  async login(email, password) {
    const data = await this.request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
    this.token = data.access_token;
    localStorage.setItem("nexora_token", this.token);
    return data;
  },

  logout() {
    this.token = null;
    localStorage.removeItem("nexora_token");
    location.reload();
  }
};
