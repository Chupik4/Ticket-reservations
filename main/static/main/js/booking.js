const bookingPage = document.querySelector(".booking-page");
const seatMap = document.getElementById("seat-map");
const list = document.getElementById("ticket-list");
const emptyState = document.getElementById("empty-state");
const countLabel = document.getElementById("ticket-count");
const totalLabel = document.getElementById("total-label");
const selectedInput = document.getElementById("selected_seats");
const totalInput = document.getElementById("total_price");
const continueBtn = document.getElementById("continue-btn");
const timer = document.getElementById("timer");
const successMessage = document.getElementById("booking-success");
const ageposter = document.querySelector(".session-card .poster .age"); 


const occupied = new Set(
  bookingPage.dataset.occupied
    .split(",")
    .map((seat) => seat.trim())
    .filter(Boolean)
);
const selected = new Map();
const rows = ["A", "B", "C", "D", "E", "F", "G", "L"];

rows.forEach((row, rowIndex) => {
  const rowEl = document.createElement("div");
  rowEl.className = row === "L" ? "seat-row lux-row" : "seat-row";
  const seatCount = row === "L" ? 16 : 18;

  for (let index = 1; index <= seatCount; index += 1) {
    if (row === "L" && index % 2 === 1) {
      const gap = document.createElement("span");
      gap.className = "pair-gap";
      rowEl.appendChild(gap);
    }

    const id = `${row}${index}`;
    const seat = document.createElement("button");
    seat.type = "button";
    seat.className = row === "L" ? "seat lux-seat" : "seat";
    seat.dataset.id = id;
    seat.dataset.row = row;
    seat.dataset.number = index;
    seat.dataset.price = row === "L" ? "330" : "210";
    seat.title = occupied.has(id) ? `${id} вже заброньовано` : `Місце ${id}`;

    if (occupied.has(id)) {
      seat.classList.add("occupied");
      seat.textContent = "×";
      seat.disabled = true;
    }

    if (rowIndex < 7 && (index === 5 || index === 14)) {
      seat.classList.add("aisle-after");
    }

    seat.addEventListener("click", () => toggleSeat(seat));
    rowEl.appendChild(seat);
  }

  seatMap.appendChild(rowEl);
});

function toggleSeat(seat) {
  const id = seat.dataset.id;
  if (selected.has(id)) {
    selected.delete(id);
    seat.classList.remove("selected");
  } else {
    selected.set(id, {
      id,
      row: seat.dataset.row,
      number: seat.dataset.number,
      price: Number(seat.dataset.price),
      type: seat.classList.contains("lux-seat") ? "SUPER LUX" : "GOOD",
    });
    seat.classList.add("selected");
  }
  renderSummary();
}

function renderSummary() {
  const tickets = Array.from(selected.values());
  const total = tickets.reduce((sum, ticket) => sum + ticket.price, 0);
  list.innerHTML = "";

  tickets.forEach((ticket) => {
    const item = document.createElement("article");
    item.className = "ticket-item";
    item.innerHTML = `
      <div>
        <strong>${ticket.type}</strong>
        <span>Ряд ${ticket.row}, місце ${ticket.number}</span>
      </div>
      <b>${ticket.price} грн</b>
    `;
    list.appendChild(item);
  });

  emptyState.hidden = tickets.length > 0;
  countLabel.textContent = tickets.length;
  totalLabel.textContent = total;
  selectedInput.value = tickets.map((ticket) => ticket.id).join(", ");
  totalInput.value = total;
  continueBtn.disabled = tickets.length === 0;
}

if (successMessage) {
  setTimeout(() => {
    window.location.href = "/";
  }, 5000);
}

let secondsLeft = 419;
const timerInterval = setInterval(() => {
  secondsLeft = Math.max(0, secondsLeft - 1);
  const minutes = String(Math.floor(secondsLeft / 60)).padStart(2, "0");
  const seconds = String(secondsLeft % 60).padStart(2, "0");
  timer.textContent = `${minutes}:${seconds}`;
  if (secondsLeft === 0) {
    clearInterval(timerInterval);
    window.location.href = "/";
  }
}, 1000);
