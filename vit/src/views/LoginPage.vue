<template>
  <div class="login-page">
    <div class="login-container">
      <img src="@/assets/vit-logo.png" alt="VIT Logo" class="logo">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="input-group">
          <input v-model="username" type="text" placeholder="Username" required class="input-box" @change="verifyName">
          <span class="msg">{{ nameError }}</span>
        </div>
        <div class="input-group">
          <input v-model="password" type="password" placeholder="Password" required class="input-box" @change="verifyPwd">
          <span class="msg">{{ passwordError }}</span>
        </div>
        <button type="submit" class="login-button">LOGIN</button>
      </form>
      <button @click="goToHome" class="home-button">Back to Homepage</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      nameError: '',
      passwordError: ''
    }
  },
  methods: {
    verifyName() {
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailRegex.test(this.username)) {
        this.nameError = "Invalid email format.";
        return false;
      }
      this.nameError = "";
      return true;
    },
    verifyPwd() {
      if (this.password.length < 8) {
        this.passwordError = "Password must be at least 8 characters long.";
        return false;
      }
      this.passwordError = "";
      return true;
    },
    login() {
      if (this.verifyName() && this.verifyPwd()) {
        // 跳转到 admin page
        this.$router.push("/admin-page"); // 改为 admin page 的路由
      }
    },
    goToHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(to right, #f2994a, #e74c3c); /* 添加背景渐变 */
}

.login-container {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 300px;
}

.logo {
  height: 60px;
  margin-bottom: 20px;
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

.input-group {
  margin-bottom: 15px;
}

.input-box {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

.login-button {
  width: 100%;
  padding: 10px;
  background-color: #f2994a;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #f2c94c;
}

.home-button {
  width: 100%;
  padding: 10px;
  background-color: transparent;
  color: #f2994a;
  border: 1px solid #f2994a;
  border-radius: 5px;
  font-size: 16px;
  margin-top: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.home-button:hover {
  background-color: #f2994a;
  color: white;
}

.msg {
  color: red;
  font-size: 12px;
  display: block;
  margin-top: 5px;
}
</style>

