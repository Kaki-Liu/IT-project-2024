<template>
  <div class="classroom-management-page">
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

    <div class="classroom-container">
      <h2>Classroom Management</h2>

      <div class="campus-selection">
        <h3>Select Campus</h3>
        <ul>
          <li
            v-for="campus in campuses"
            :key="campus.id"
            @click="selectCampus(campus.id)"
            :class="{ active: selectedCampusId === campus.id }"
          >
            {{ campus.name }}
          </li>
        </ul>
      </div>

      <form v-if="selectedCampusId !== null" @submit.prevent="addClassroom" class="classroom-form">
        <input v-model="newClassroom.RoomName" type="text" placeholder="Classroom/Lab Name" required />
        <input v-model="newClassroom.RoomType" type="number" placeholder="Room Type (0 for Classroom, 1 for Lab)" required />
        <input v-model="newClassroom.RoomAddress" type="text" placeholder="Location (Building/Level)" required />
        <input v-model="newClassroom.RoomCapacity" type="number" placeholder="Capacity" required />
        <input v-model="newClassroom.RoomAvailableTimeStart" type="number" placeholder="Available Time Start (Hour)" required />
        <input v-model="newClassroom.RoomAvailableTimeEnd" type="number" placeholder="Available Time End (Hour)" required />
        <input v-model="newClassroom.RoomAvailableDays" type="number" placeholder="Available Days" required />
        <button type="submit" class="add-button">Add Classroom</button>
      </form>

      <div class="title" v-if="selectedCampusId !== null">Total Classrooms: <span>{{ filteredClassrooms.length }}</span></div>

      <table class="classroom-table" v-if="selectedCampusId !== null && filteredClassrooms.length > 0">
        <thead>
          <tr>
            <th>Classroom/Lab Name</th>
            <th>Room Type</th>
            <th>Location <br />Building/Level</th>
            <th>Capacity</th>
            <th>Available Time Start</th>
            <th>Available Time End</th>
            <th>Available Days</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(classroom, index) in filteredClassrooms" :key="index">
            <td>{{ classroom.RoomName }}</td>
            <td>{{ classroom.RoomType === 0 ? 'Classroom' : 'Lab' }}</td>
            <td>{{ classroom.RoomAddress }}</td>
            <td>{{ classroom.RoomCapacity }}</td>
            <td>{{ classroom.RoomAvailableTimeStart }}</td>
            <td>{{ classroom.RoomAvailableTimeEnd }}</td>
            <td>{{ classroom.RoomAvailableDays }}</td>
            <td>
              <button @click="deleteClassroom(index)" class="delete-button">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      campuses: [
        { id: 0, name: 'Melbourne' },
        { id: 1, name: 'Geelong' },
        { id: 2, name: 'Sydney' },
        { id: 3, name: 'Adelaide' },
      ],
      selectedCampusId: 0,
      newClassroom: {
        RoomName: '',
        RoomType: '',
        RoomAddress: '',
        RoomCapacity: '',
        RoomAvailableTimeStart: '',
        RoomAvailableTimeEnd: '',
        RoomAvailableDays: '',
      },
      classrooms: []  // 确保 classrooms 初始化为一个空数组
    };
  },
  computed: {
    filteredClassrooms() {
      console.log("过滤教室，选中校区 ID：", this.selectedCampusId);
      console.log("当前教室数据：", this.classrooms);
      // 确保 classrooms 是数组，避免调用 filter 时出现错误
      if (Array.isArray(this.classrooms)) {
        return this.classrooms.filter(classroom => classroom.CampusID === this.selectedCampusId);
      } else {
        console.warn("classrooms 不是一个数组，设置为空数组");
        return [];
      }
    }
  },
  methods: {
    goToPage(page) {
      console.log("跳转到页面：", page);
      this.$router.push(page);
    },
    logout() {
      console.log("用户登出");
      // Handle logout logic
    },
    selectCampus(campusId) {
      console.log("选中了校区 ID：", campusId);
      this.selectedCampusId = campusId;
      this.fetchClassrooms(); // Trigger data fetch for the selected campus
    },
    async addClassroom() {
      try {
        console.log("添加教室：", this.newClassroom, "校区 ID：", this.selectedCampusId);
        const response = await axios.post('http://127.0.0.1:5002/classroom-management', {
          ...this.newClassroom,
          CampusID: this.selectedCampusId
        });
        console.log("添加教室请求响应：", response);
        alert(response.data.message);
        this.fetchClassrooms(); // Refresh classrooms after adding
        this.resetForm();
      } catch (error) {
        console.error('添加教室时出错:', error);
        if (error.response) {
          console.error('服务器返回的错误响应:', error.response.data);
        } else if (error.request) {
          console.error('请求已发送，但没有收到响应:', error.request);
        } else {
          console.error('设置请求时出错:', error.message);
        }
        alert('Failed to add classroom. Please check the console for more details.');
      }
    },
    async deleteClassroom(index) {
      const classroomToDelete = this.filteredClassrooms[index];
      console.log("删除教室 ID：", classroomToDelete.RoomID);
      try {
        const response = await axios.delete(`http://127.0.0.1:5002/classroom-management/${classroomToDelete.RoomID}`);
        console.log("删除教室请求响应：", response);
        alert('Classroom deleted successfully!');
        this.fetchClassrooms(); // Refresh classrooms after deleting
      } catch (error) {
        console.error('删除教室时出错:', error);
        if (error.response) {
          console.error('服务器返回的错误响应:', error.response.data);
        } else if (error.request) {
          console.error('请求已发送，但没有收到响应:', error.request);
        } else {
          console.error('设置请求时出错:', error.message);
        }
        alert('Failed to delete classroom. Please check the console for more details.');
      }
    },
    async fetchClassrooms() {
      try {
        console.log("请求获取教室信息，选中校区 ID：", this.selectedCampusId);
        const response = await axios.get('http://127.0.0.1:5002/classroom-management', {
          params: { campusId: this.selectedCampusId },
          headers: { 'Accept': 'application/json' } 
        });
        console.log("获取到的教室数据：", response.data);
        // 确保 response.data 是一个数组
        if (Array.isArray(response.data)) {
          this.classrooms = response.data;
        } else {
          console.warn("获取的教室数据不是数组，重置 classrooms 为空数组");
          this.classrooms = [];
        }
      } catch (error) {
        console.error('获取教室信息时出错:', error);
        alert('Failed to load classrooms.');
        this.classrooms = []; // 如果请求失败，重置 classrooms
      }
    },
    resetForm() {
      console.log("重置表单");
      this.newClassroom = {
        RoomName: '',
        RoomType: '',
        RoomAddress: '',
        RoomCapacity: '',
        RoomAvailableTimeStart: '',
        RoomAvailableTimeEnd: '',
        RoomAvailableDays: '',
      };
    }
  },
  created() {
    console.log("Classroom Management 页面创建完成");
    this.fetchClassrooms();
  }
};
</script>





<style scoped>
* {
  box-sizing: border-box;
}

body {
  font-family: 'Roboto', sans-serif;
}

.classroom-management-page {
  background-color: #f5f5f5;
  padding-bottom: 50px;
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

.campus-selection {
  text-align: center;
  margin-bottom: 20px;
}

.campus-selection ul {
  list-style-type: none;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.campus-selection li {
  cursor: pointer;
  padding: 10px 20px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.campus-selection li:hover {
  background-color: #eee;
}

.campus-selection li.active {
  background-color: #FF7043;
  color: white;
}

form {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
  padding: 20px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  width: 80%;
  margin: 0 auto;
}

form input {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  width: 180px;
}

form button {
  background-color: #FF7043;
  border: none;
  padding: 15px 30px;
  color: white;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

form button:hover {
  background-color: #FF8A65;
}

.title {
  text-align: center;
  font-size: 20px;
  color: #333;
  margin-bottom: 20px;
}

table {
  width: 90%;
  margin: 0 auto;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

th, td {
  padding: 20px;
  border: 1px solid #ddd;
  text-align: center;
  font-size: 16px;
}

th {
  background-color: #FF7043;
  color: white;
  font-weight: bold;
}

td button {
  background-color: #FF7043;
  border: none;
  padding: 10px 20px;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

td button:hover {
  background-color: #FF8A65;
}
</style>


