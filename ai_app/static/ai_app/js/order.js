const countdownText = document.getElementById('countdown-text');
const countdownNumber = document.getElementById('countdown-number');
const redirectUrl = countdownText.getAttribute('data-url');

  let seconds = 5;
  countdownNumber.textContent = seconds;

  const interval = setInterval(() => {
    seconds--;
    if (seconds > 0) {
      countdownNumber.textContent = seconds;
    } else {
      clearInterval(interval);
      window.location.href = redirectUrl;
    }
  }, 1000);

