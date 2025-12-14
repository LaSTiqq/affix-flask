// Resize logo onscroll
const logoDefault = document.getElementById("logo_default");
const logoNovember = document.getElementById("logo_november");
const logoDecember = document.getElementById("logo_december");

const scrollFunction = () => {
  const scrolled =
    document.body.scrollTop > 50 || document.documentElement.scrollTop > 50;

  const setLogoSize = (logo, width) => {
    if (logo) {
      logo.style.width = width;
    }
  };

  if (scrolled) {
    setLogoSize(logoDefault, "130px");
    setLogoSize(logoNovember, "130px");
    setLogoSize(logoDecember, "130px");
  } else {
    setLogoSize(logoDefault, "160px");
    setLogoSize(logoNovember, "160px");
    setLogoSize(logoDecember, "160px");
  }
};

window.onscroll = () => {
  scrollFunction();
};

// Tooltip
document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((el) => {
  new bootstrap.Tooltip(el);
});

// Scroll to certificates
const scrollToAnchor = (aid) => {
  const aTag = document.querySelector("a[name='" + aid + "']");

  if (aTag) {
    window.scrollTo({
      top: aTag.offsetTop,
      behavior: "smooth",
    });
  }
};

document.getElementById("help").addEventListener("click", () => {
  const modal = document.getElementById("Modal6");
  const modalInstance = bootstrap.Modal.getInstance(modal);

  if (modalInstance) {
    modalInstance.hide();
  }

  setTimeout(() => {
    scrollToAnchor("certificates");
  }, 200);
});

// Hide navbar after click when navbar collapsed
const navbarLinks = document.querySelectorAll(".navbar-collapse a");

navbarLinks.forEach((link) => {
  link.addEventListener("click", () => {
    const navbarCollapse = document.querySelector(".navbar-collapse");
    if (navbarCollapse.classList.contains("show")) {
      navbarCollapse.classList.remove("show");
    }
  });
});

// AOS animation
AOS.init({
  disable: window.innerWidth < 1399,
  startEvent: "DOMContentLoaded",
  once: true,
  duration: 800,
});

//AJAX form submission
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  const loader = document.getElementById("loader");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    loader.classList.remove("d-none");
    const formData = new FormData(form);

    try {
      const response = await fetch("/send-ajax", {
        method: "POST",
        headers: {
          "X-CSRFToken": formData.get("csrf_token"),
        },
        body: formData,
      });

      const result = await response.json();
      showAlert(result.message, result.status);

      if (result.status !== "info") {
        form.reset();
        grecaptcha.reset();
      }
    } catch (err) {
      showAlert("Radās kļūda! Mēģiniet vēlreiz.", "danger");
    } finally {
      loader.classList.add("d-none");
    }
  });

  function showAlert(message, type) {
    const alert = document.getElementById("alert");

    alert.className = `alert alert-${type} alert-dismissible rounded-pill fw-bold d-block`;
    alert.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Aizvērt"></button>
  `;

    setTimeout(() => {
      alert.classList.add("d-none");
      alert.className = "alert d-none";
    }, 4000);
  }
});
