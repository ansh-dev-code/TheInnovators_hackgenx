
document.getElementById("loginBtn").addEventListener("click", () => {
    document.getElementById("loginForm").classList.remove("hidden");
    document.getElementById("signupForm").classList.add("hidden");
  });
  
  document.getElementById("signupBtn").addEventListener("click", () => {
    document.getElementById("signupForm").classList.remove("hidden");
    document.getElementById("loginForm").classList.add("hidden");
  });
  
  
  function redirectToLanding() {
    window.location.href = "landingpage2.html"; 
  }
  
  
  document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
  
    const response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
  
    const result = await response.json();
    alert(result.message);
  
    if (response.status === 200) {
      redirectToLanding();
    }
  });
  
  
  document.getElementById("signupForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
  
    if (password !== confirmPassword) {
      return alert("Passwords do not match!");
    }
  
    const response = await fetch("/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
  
    const result = await response.json();
    alert(result.message);
  
    if (response.status === 200) {
      redirectToLanding();
    }
  });