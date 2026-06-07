const carousel = document.querySelector("[data-movie-carousel]");

if (carousel) {
  const movies = [
    {
      title: "Дуже страшне кіно",
      kicker: "Прем'єра тижня",
      description: "Відкрийте для себе нову комедію жахів, яка вже підкорила серця глядачів. Ідеальний вибір для вечірнього перегляду з друзями.",
      rating: "18+",
      format: "2D",
      subtitle: "SDH",
      hall: "Зал №3",
      posterClass: "",
    },
    {
      title: "Нічний рейс",
      kicker: "Новинка",
      description: "Напружений трилер про подорож, де кожна хвилина змінює правила гри. Темна атмосфера, швидкий темп і фінал без пауз.",
      rating: "16+",
      format: "2D",
      subtitle: "UA",
      hall: "Зал №2",
      posterClass: "action",
    },
    {
      title: "Місто світла",
      kicker: "Вибір глядачів",
      description: "Тепла історія про дружбу, мрії та вечір, який може змінити все. Фільм для спокійного кіносеансу з красивою музикою.",
      rating: "12+",
      format: "2D",
      subtitle: "SDH",
      hall: "Зал №5",
      posterClass: "drama",
    },
    {
      title: "Космічна пригода",
      kicker: "Для всієї родини",
      description: "Яскрава пригода для сімейного перегляду: багато гумору, швидких сцен і герої, за яких хочеться вболівати.",
      rating: "6+",
      format: "3D",
      subtitle: "UA",
      hall: "Зал №1",
      posterClass: "family",
    },
  ];

  const heroSection = document.querySelector(".home-hero");
  const title = document.querySelector("[data-movie-title]");
  const cardTitle = document.querySelector("[data-movie-card-title]");
  const kicker = document.querySelector("[data-movie-kicker]");
  const description = document.querySelector("[data-movie-description]");
  const rating = document.querySelector("[data-movie-rating]");
  const format = document.querySelector("[data-movie-format]");
  const subtitle = document.querySelector("[data-movie-subtitle]");
  const hall = document.querySelector("[data-movie-hall]");
  const poster = document.querySelector("[data-movie-poster]");
  const bookingLink = document.querySelector("[data-booking-link]");
  const prev = document.querySelector("[data-carousel-prev]");
  const next = document.querySelector("[data-carousel-next]");
  const dots = document.querySelector("[data-carousel-dots]");
  let activeMovie = 0;
  let locked = false;

  movies.forEach((movie, index) => {
    const dot = document.createElement("button");
    dot.className = index === activeMovie ? "carousel-dot active" : "carousel-dot";
    dot.type = "button";
    dot.setAttribute("aria-label", movie.title);
    dot.addEventListener("click", () => showMovie(index));
    dots.appendChild(dot);
  });

  function showMovie(index) {
    if (locked || index === activeMovie) return;
    locked = true;
    activeMovie = (index + movies.length) % movies.length;

    heroSection.classList.add("is-changing");

    setTimeout(() => {
      renderMovie();
      heroSection.classList.remove("is-changing");
      setTimeout(() => { locked = false; }, 320);
    }, 320);
  }

  function renderMovie() {
    const movie = movies[activeMovie];
    title.textContent = movie.title;
    cardTitle.textContent = movie.title;
    kicker.textContent = movie.kicker;
    description.textContent = movie.description;
    rating.textContent = movie.rating;
    format.textContent = movie.format;
    subtitle.textContent = movie.subtitle;
    hall.textContent = movie.hall;
    poster.className = movie.posterClass
      ? `show-poster ${movie.posterClass}`
      : "show-poster";
    bookingLink.href = `/booking/?movie=${encodeURIComponent(movie.title)}`;

    document.querySelectorAll(".carousel-dot").forEach((d, i) => {
      d.classList.toggle("active", i === activeMovie);
    });
  }

  prev.addEventListener("click", () => showMovie(activeMovie - 1));
  next.addEventListener("click", () => showMovie(activeMovie + 1));
}
