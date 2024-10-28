<template>
  <div class="timetable-page">
    <!-- 头部部分 -->
    <header>
      <div class="header-left">
        <img src="@/assets/vit-logo.png" alt="VIT Logo" height="60" />
      </div>
      <div class="header-right">
        <button @click="goToPage('/admin-page')">Back to Admin Page</button>
        <button @click="goToPage('/')">Homepage</button>
        <button @click="logout">Logout</button>
      </div>
    </header>

    <!-- 页面主体布局 -->
    <div class="main-content">
      <!-- 左侧部分：学生姓名和建筑物 -->
      <div class="left-section">
        <div class="student-name-section">
          <h2>Student Name</h2>
          <ul>
            <li>Student 1</li>
            <li>Student 2</li>
            <li>Student 3</li>
            <li>Student 4</li>
          </ul>
        </div>

        <div class="building-section">
          <h2>Building</h2>
          <ul>
            <li>Building 1</li>
            <li>Building 2</li>
            <li>Building 3</li>
          </ul>
        </div>

        <div class="chat-section">
          <h2>Chat with your Peers</h2>
          <textarea v-model="message" placeholder="Type your message..."></textarea>
          <button @click="sendMessage">Send</button>
        </div>
      </div>

      <!-- 右侧部分：时间表 -->
      <div class="right-section">
        <h2>Timetable Weeks</h2>
        <table class="timetable">
          <thead>
            <tr>
              <th>Time</th>
              <th>Monday</th>
              <th>Tuesday</th>
              <th>Wednesday</th>
              <th>Thursday</th>
              <th>Friday</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>9:00-10:00</td>
              <td class="course-block">Math</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td>10:00-11:00</td>
              <td></td>
              <td class="course-block">Physics</td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td>11:00-12:00</td>
              <td></td>
              <td></td>
              <td class="course-block">Chemistry</td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td>12:00-13:00</td>
              <td></td>
              <td></td>
              <td></td>
              <td class="course-block">Biology</td>
              <td></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: ''
    };
  },
  methods: {
    goToPage(page) {
      this.$router.push(page);
    },
    logout() {
      // Handle logout logic
    },
    sendMessage() {
      console.log(this.message);
      this.message = '';
    }
  }
};
</script>

<style scoped>

/* 全局样式调整 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.timetable-page {
  display: flex;
  flex-direction: column;
}

header {
  background-color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.header-left img {
  height: 60px;
}

.header-right {
  display: flex;
  gap: 10px;
}

.logo {
  height: 60px;
}


header button {
  background-color: #FF7043;
  border: none;
  padding: 10px 20px;
  color: white;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

header button:hover {
  background-color: #FF8A65;
}

.main-content {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

.left-section {
  width: 25%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-section {
  width: 70%;
}

.student-name-section, .building-section, .chat-section {
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.student-name-section ul, .building-section ul {
  list-style: none;
}

.student-name-section li, .building-section li {
  padding: 10px;
  background-color: #ff7043;
  color: white;
  margin: 5px 0;
  text-align: center;
}

.chat-section textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
}

.chat-section button {
  width: 100%;
  background-color: #ff7043;
  color: white;
  padding: 10px;
  margin-top: 10px;
}

.timetable {
  width: 100%;
  border-collapse: collapse;
}

.timetable th, .timetable td {
  padding: 15px;
  border: 1px solid #ddd;
  text-align: center;
}

.course-block {
  background-color: #ffcccb;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 5px;
}
</style>