const API_ROOT = "/api/v1";
const TOKEN_KEY = "tm_access_token";

const state = {
  token: localStorage.getItem(TOKEN_KEY) || "",
  toastTimer: null,
  activeView: "authentication",
};

const viewTitleMap = {
  authentication: "Authentication",
  tasks: "Tasks",
  users: "Users",
  departments: "Departments",
  projects: "Projects",
};

function setToken(token) {
  state.token = token || "";
  if (state.token) {
    localStorage.setItem(TOKEN_KEY, state.token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
  updateAuthBanner();
}

function updateAuthBanner() {
  const banner = document.getElementById("authBanner");
  if (!banner) {
    return;
  }

  if (!state.token) {
    banner.textContent = "Not authenticated";
    return;
  }

  const compact = `${state.token.slice(0, 24)}...`;
  banner.textContent = `Authenticated | token ${compact}`;
}

function switchView(viewName) {
  state.activeView = viewName;

  const title = document.getElementById("viewTitle");
  if (title && viewTitleMap[viewName]) {
    title.textContent = viewTitleMap[viewName];
  }

  document.querySelectorAll(".nav-btn").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === viewName);
  });

  document.querySelectorAll(".view-panel").forEach((panel) => {
    panel.classList.remove("active");
  });

  const nextView = document.getElementById(`view-${viewName}`);
  if (nextView) {
    nextView.classList.add("active");
  }

  if (!state.token) {
    return;
  }

  if (viewName === "tasks") {
    refreshTasks();
  }
  if (viewName === "users") {
    refreshUsers();
  }
  if (viewName === "departments") {
    refreshDepartments();
  }
  if (viewName === "projects") {
    refreshProjects();
  }
}

function setupNavigation() {
  const navButtons = document.querySelectorAll(".nav-btn");

  navButtons.forEach((button) => {
    button.addEventListener("click", () => {
      switchView(button.dataset.view);
    });
  });
}

function showToast(message, type = "success") {
  const toast = document.getElementById("toast");
  if (!toast) {
    return;
  }

  toast.textContent = message;
  toast.className = `toast ${type} show`;

  if (state.toastTimer) {
    clearTimeout(state.toastTimer);
  }

  state.toastTimer = setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

async function apiRequest(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (state.token) {
    headers.Authorization = `Bearer ${state.token}`;
  }

  const response = await fetch(`${API_ROOT}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    return null;
  }

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    const message = payload.message || payload.error || `Request failed (${response.status})`;
    throw new Error(message);
  }

  return payload;
}

function formToObject(formElement) {
  const data = new FormData(formElement);
  const output = {};

  for (const [key, value] of data.entries()) {
    output[key] = value;
  }

  return output;
}

function clearTableBody(tbodyId) {
  const tbody = document.getElementById(tbodyId);
  if (tbody) {
    tbody.innerHTML = "";
  }
}

function addCell(row, value) {
  const cell = document.createElement("td");
  cell.textContent = value == null || value === "" ? "-" : String(value);
  row.appendChild(cell);
}

async function refreshTasks() {
  clearTableBody("tasksTableBody");
  const tbody = document.getElementById("tasksTableBody");

  try {
    const tasks = await apiRequest("/tasks/");
    tasks.forEach((task) => {
      const row = document.createElement("tr");
      addCell(row, task.id);
      addCell(row, task.title);
      addCell(row, task.status);
      addCell(row, task.priority);
      addCell(row, task.due_date);
      addCell(row, task.project_id);
      tbody.appendChild(row);
    });
  } catch (error) {
    showToast(`Tasks: ${error.message}`, "error");
  }
}

async function refreshDepartments() {
  const list = document.getElementById("departmentsList");
  list.innerHTML = "";

  try {
    const departments = await apiRequest("/departments/");
    departments.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = `${item.id}: ${item.name}`;
      list.appendChild(li);
    });
  } catch (error) {
    showToast(`Departments: ${error.message}`, "error");
  }
}

async function refreshProjects() {
  const list = document.getElementById("projectsList");
  list.innerHTML = "";

  try {
    const projects = await apiRequest("/projects/");
    projects.forEach((item) => {
      const li = document.createElement("li");
      if (item.department_id == null) {
        li.textContent = `${item.id}: ${item.name}`;
      } else {
        li.textContent = `${item.id}: ${item.name} [dept ${item.department_id}]`;
      }
      list.appendChild(li);
    });
  } catch (error) {
    showToast(`Projects: ${error.message}`, "error");
  }
}

async function refreshUsers() {
  clearTableBody("usersTableBody");
  const tbody = document.getElementById("usersTableBody");

  try {
    const users = await apiRequest("/users/");
    users.forEach((user) => {
      const row = document.createElement("tr");
      addCell(row, user.id);
      addCell(row, user.name);
      addCell(row, user.email);
      addCell(row, user.role);
      addCell(row, user.department_id);
      tbody.appendChild(row);
    });
  } catch (error) {
    showToast(`Users: ${error.message}`, "error");
  }
}

async function refreshAllData() {
  if (!state.token) {
    return;
  }

  await Promise.allSettled([
    refreshTasks(),
    refreshDepartments(),
    refreshProjects(),
    refreshUsers(),
  ]);
}

function setupAuthHandlers() {
  const loginForm = document.getElementById("loginForm");
  const logoutBtn = document.getElementById("logoutBtn");

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = formToObject(loginForm);

    try {
      const result = await apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setToken(result.access_token);
      showToast("Login successful", "success");
      await refreshAllData();
      switchView("tasks");
    } catch (error) {
      showToast(`Login failed: ${error.message}`, "error");
    }
  });

  logoutBtn.addEventListener("click", () => {
    const loginForm = document.getElementById("loginForm");
    setToken("");
    clearTableBody("tasksTableBody");
    clearTableBody("usersTableBody");
    document.getElementById("departmentsList").innerHTML = "";
    document.getElementById("projectsList").innerHTML = "";
    if (loginForm) {
      loginForm.reset();
    }
    switchView("authentication");
    showToast("Signed out", "success");
  });
}

function setupTaskHandlers() {
  document.getElementById("refreshTasksBtn").addEventListener("click", refreshTasks);

  document.getElementById("taskForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = formToObject(form);

    payload.project_id = Number(payload.project_id);
    payload.description = payload.description || null;
    payload.priority = payload.priority || null;
    payload.due_date = payload.due_date || null;

    try {
      await apiRequest("/tasks/", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      form.reset();
      showToast("Task created", "success");
      await refreshTasks();
    } catch (error) {
      showToast(`Create task failed: ${error.message}`, "error");
    }
  });

  document.getElementById("taskUpdateForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = formToObject(form);
    const taskId = Number(payload.task_id);

    delete payload.task_id;

    const updatePayload = {};
    if (payload.title) {
      updatePayload.title = payload.title;
    }
    if (payload.status) {
      updatePayload.status = payload.status;
    }
    if (payload.priority) {
      updatePayload.priority = payload.priority;
    }
    if (payload.due_date) {
      updatePayload.due_date = payload.due_date;
    }
    if (payload.description) {
      updatePayload.description = payload.description;
    }

    if (!Object.keys(updatePayload).length) {
      showToast("Provide at least one field to update", "error");
      return;
    }

    try {
      await apiRequest(`/tasks/${taskId}`, {
        method: "PUT",
        body: JSON.stringify(updatePayload),
      });
      form.reset();
      showToast("Task updated", "success");
      await refreshTasks();
    } catch (error) {
      showToast(`Update task failed: ${error.message}`, "error");
    }
  });

  document.getElementById("taskDeleteForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = formToObject(form);

    try {
      await apiRequest(`/tasks/${Number(payload.task_id)}`, {
        method: "DELETE",
      });
      form.reset();
      showToast("Task deleted", "success");
      await refreshTasks();
    } catch (error) {
      showToast(`Delete task failed: ${error.message}`, "error");
    }
  });

  document.getElementById("taskAssignForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = formToObject(form);

    const userIds = payload.user_ids
      .split(",")
      .map((value) => Number(value.trim()))
      .filter((value) => Number.isInteger(value) && value > 0);

    if (!userIds.length) {
      showToast("Provide valid user IDs, ex: 1,2", "error");
      return;
    }

    try {
      await apiRequest(`/tasks/${Number(payload.task_id)}/assign`, {
        method: "POST",
        body: JSON.stringify({ user_ids: userIds }),
      });
      form.reset();
      showToast("Users assigned to task", "success");
      await refreshTasks();
    } catch (error) {
      showToast(`Assign failed: ${error.message}`, "error");
    }
  });
}

function setupDepartmentHandlers() {
  document.getElementById("refreshDepartmentsBtn").addEventListener("click", refreshDepartments);

  document.getElementById("departmentForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = formToObject(form);

    try {
      await apiRequest("/departments/", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      form.reset();
      showToast("Department created", "success");
      await refreshDepartments();
    } catch (error) {
      showToast(`Create department failed: ${error.message}`, "error");
    }
  });
}

function setupProjectHandlers() {
  document.getElementById("refreshProjectsBtn").addEventListener("click", refreshProjects);

  document.getElementById("projectForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = formToObject(form);
    payload.department_id = Number(payload.department_id);

    try {
      await apiRequest("/projects/", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      form.reset();
      showToast("Project created", "success");
      await refreshProjects();
    } catch (error) {
      showToast(`Create project failed: ${error.message}`, "error");
    }
  });
}

function setupUserHandlers() {
  document.getElementById("refreshUsersBtn").addEventListener("click", refreshUsers);

  document.getElementById("userForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = formToObject(form);
    payload.department_id = Number(payload.department_id);

    try {
      await apiRequest("/users/", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      form.reset();
      showToast("User created", "success");
      await refreshUsers();
    } catch (error) {
      showToast(`Create user failed: ${error.message}`, "error");
    }
  });
}

function init() {
  setupNavigation();
  updateAuthBanner();
  setupAuthHandlers();
  setupTaskHandlers();
  setupDepartmentHandlers();
  setupProjectHandlers();
  setupUserHandlers();
  switchView(state.activeView);
  refreshAllData();
}

document.addEventListener("DOMContentLoaded", init);
