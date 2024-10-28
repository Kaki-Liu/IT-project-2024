<template>
    <div class="admin-page">
      <header>
        <img src="@/assets/vit-logo.png" alt="VIT Logo" height="60">
        <nav>
          <button @click="goHome">Homepage</button>
          <button @click="logout">Logout</button>
        </nav>
      </header>
  
      <section class="grid-container">
        
        <div class="grid-item" @click="goToCourseManagement">
          Course Management
        </div>
        <div class="grid-item" @click="goToClassroomManagement">
          Classroom Management
        </div>
        <div class="grid-item" @click="goToScheduleView">
          Timetable Auto Generation
        </div>
        <div class="grid-item" @click="goToAdminTimetable">
          Admin Timetable view
        </div>
       
      </section>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      goHome() {
        this.$router.push('/');
      },
      logout() {
        // Handle logout
      },
      
      goToCourseManagement() {
        this.$router.push('/course-management');
      },
      goToClassroomManagement() {
        this.$router.push('/classroom-management');
      },
      goToScheduleView() {
        this.$router.push('/schedule-management');
      },
      goToAdminTimetable() {
        this.$router.push('/admin-timetable');
      },
      
    }
  }
  </script>
  
  <style scoped>
  .admin-page {
    text-align: center;
    padding: 40px;
    background: linear-gradient(135deg, #f77b55, #fca986); /* 加入背景颜色的渐变 */
    min-height: 80vh; /* 使背景填充整个页面 */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
    padding: 10px 20px;
    background-color: #ffffff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  nav button {
    margin-left: 10px;
    padding: 10px 20px;
    background-color: #f77b55;
    color: white;
    border: none;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  nav button:hover {
    background-color: #e6673e;
  }
  

  .grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 两列布局 */
  grid-template-rows: repeat(3, 1fr); /* 三行布局 */
  gap: 20px;
  height: 70vh; /* 占据页面的大部分高度 */
  margin-top: 50px;
  align-items: center;
}
  

  .grid-item {
    background-color: #ffffff;
    color: #333;
    padding: 40px; /* 增加内边距，使选项更大 */
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
    cursor: pointer;
    font-size: 24px; /* 增大字体 */
    font-weight: bold;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, background-color 0.3s ease;
  }
  
  .grid-item:hover {
    background-color: #f77b55;
    color: white;
    transform: translateY(-5px);
  }
  
  </style>
  