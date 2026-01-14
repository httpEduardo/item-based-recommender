const userSelect = document.getElementById("userSelect") as HTMLSelectElement;
const recommendButton = document.getElementById("recommendButton") as HTMLButtonElement;
const seedButton = document.getElementById("seedButton") as HTMLButtonElement;
const resultsList = document.getElementById("results") as HTMLUListElement;

type Recommendation = { item: string; score: number };

function loadUsers(): void {
  fetch("/api/users")
    .then((res) => res.json())
    .then((data) => {
      userSelect.innerHTML = "";
      (data.users || []).forEach((user: string) => {
        const option = document.createElement("option");
        option.value = user;
        option.textContent = user;
        userSelect.appendChild(option);
      });
    });
}

function renderResults(results: Recommendation[]): void {
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
