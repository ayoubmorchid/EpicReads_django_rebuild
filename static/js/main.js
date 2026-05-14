document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const navLinks = document.querySelector("[data-nav-links]");

  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      navLinks.classList.toggle("open");
    });
  }

  const scrollButton = document.querySelector("[data-scroll-top]");
  if (scrollButton) {
    const updateScrollButton = () => {
      scrollButton.hidden = window.scrollY <= 200;
    };
    window.addEventListener("scroll", updateScrollButton);
    updateScrollButton();
    scrollButton.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  document.querySelectorAll("[data-favorite]").forEach((button) => {
    button.addEventListener("click", () => {
      button.classList.toggle("liked");
    });
  });

  const favoritesToggle = document.querySelector("[data-favorites-toggle]");
  const favoritesPanel = document.querySelector("[data-favorites-panel]");
  const favoritesClose = document.querySelector("[data-favorites-close]");

  if (favoritesToggle && favoritesPanel) {
    favoritesToggle.addEventListener("click", () => {
      favoritesPanel.classList.toggle("is-open");
      favoritesToggle.textContent = favoritesPanel.classList.contains("is-open")
        ? "Close"
        : "♥ Favorites";
    });
  }

  if (favoritesClose && favoritesPanel && favoritesToggle) {
    favoritesClose.addEventListener("click", () => {
      favoritesPanel.classList.remove("is-open");
      favoritesToggle.textContent = "♥ Favorites";
    });
  }

  const shippingPopup = document.querySelector("[data-shipping-popup]");
  const openShipping = document.querySelector("[data-open-shipping]");
  const closeShipping = document.querySelector("[data-close-shipping]");

  if (shippingPopup && openShipping && closeShipping) {
    openShipping.addEventListener("click", () => {
      shippingPopup.hidden = false;
    });
    closeShipping.addEventListener("click", () => {
      shippingPopup.hidden = true;
    });
  }

  const paymentForm = document.querySelector("[data-payment-form]");
  if (paymentForm) {
    paymentForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const cardNumber = paymentForm.querySelector("[data-card-number]").value.replace(/\D/g, "");
      const expiry = paymentForm.querySelector("[data-expiry]").value;
      const cvv = paymentForm.querySelector("[data-cvv]").value.replace(/\D/g, "");
      const error = paymentForm.querySelector("[data-payment-error]");

      if (cardNumber.length !== 16 || cvv.length !== 3 || !/^(0[1-9]|1[0-2])\/\d{2}$/.test(expiry)) {
        error.textContent = "Invalid card details. Please check your information.";
        error.hidden = false;
        return;
      }

      error.hidden = true;
      alert("Payment Successful! Thank you for your purchase.");
      window.location.href = "/";
    });
  }
});
