const userSelect = document.getElementById("userSelect");
const recommendButton = document.getElementById("recommendButton");
const seedButton = document.getElementById("seedButton");
const resultsList = document.getElementById("results");

function loadUsers() {
  fetch("/api/users")
    .then((res) => res.json())
    .then((data) => {
      userSelect.innerHTML = "";
      (data.users || []).forEach((user) => {
        const option = document.createElement("option");
        option.value = user;
        option.textContent = user;
        userSelect.appendChild(option);
      });
    });
}

function renderResults(results) {
  resultsList.innerHTML = "";
  if (!results.length) {
    resultsList.innerHTML = "<li>No recommendations yet.</li>";
    return;
  }
  results.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.item}: ${item.score}`;
    resultsList.appendChild(li);
  });
}

recommendButton.addEventListener("click", () => {
  const userId = userSelect.value;
  fetch(`/api/recommend?user_id=${encodeURIComponent(userId)}`)
    .then((res) => res.json())
    .then((data) => renderResults(data.results || []));
});

seedButton.addEventListener("click", () => {
  fetch("/api/seed", { method: "POST" })
    .then((res) => res.json())
    .then(() => {
      alert("Sample data loaded.");
      loadUsers();
    });
});

loadUsers();
