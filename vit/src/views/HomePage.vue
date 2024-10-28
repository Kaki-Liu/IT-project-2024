<template>
  <div class="homepage">
    <header>
      <div class="logo">
        <img src="@/assets/vit-logo.png" alt="VIT Logo" height="60">
      </div>
      <nav>
        <ul>
          <li><router-link to="/course">Course</router-link></li>
          <li><router-link to="/campus">Campus</router-link></li>
          <li><router-link to="/about">About</router-link></li>
          <li><router-link to="/profile">My profile</router-link></li>
        </ul>
      </nav>
      <button class="login-button" @click="login">LOGIN</button>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <h1>Welcome to the Victorian Institute of Technology</h1>
      <p>Explore our courses, campuses, and who we are.</p>
      <button class="cta-button">Get Started</button>
    </section>
  </div>
</template>

<script>
export default {
  methods: {
    login() {
      this.$router.push('/login');
      // Add login logic here
    }
  }
}
</script>

<style scoped>
/* Reset some styles for a clean layout */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.homepage {
  font-family: 'Roboto', sans-serif;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #ff7f50;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo img {
  height: 60px;
}

nav ul {
  list-style: none;
  display: flex;
  gap: 20px;
}

nav ul li a {
  text-decoration: none;
  font-size: 18px;
  color: white;
  padding: 10px 15px;
  transition: background-color 0.3s;
}

nav ul li a:hover {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
}

.login-button {
  padding: 10px 1px;
  font-size: 14px;
  width: 100px;
  color: white;
  background-color: #ff6347;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #ff4500;
}

/* Hero Section */
.hero {
  text-align: center;
  padding: 100px 20px;
  height:80vh;
  background-image: linear-gradient(to bottom right, #ff7f50, #ff6347);
  color: white;
}

.hero h1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.hero p {
  font-size: 20px;
  margin-bottom: 40px;
}

.cta-button {
  padding: 10px 25px;
  font-size: 16px;
  width: 400px;
  color: #ff6347;
  background-color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.cta-button:hover {
  background-color: #ff4500;
  color: white;
}
</style>
