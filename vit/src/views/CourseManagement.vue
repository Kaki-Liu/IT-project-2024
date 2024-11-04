<template>
  <div class="course-management-page">
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

    <h1>Course Unit Management</h1>

    <div class="campus-selection">
      <h3>Select Campus</h3>
      <ul>
        <li 
          v-for="(name, id) in campuses" 
          :key="id"
          @click="selectCampus(id)"
          :class="{ active: selectedCampusId === id }"
        >
          {{ name }}
        </li>
      </ul>
    </div>

    <div class="instructions">
      <p>Please fill in the details for each course task:</p>
      <ul>
        <li>Course Task Type: Specify the type of course task (e.g., Lecture, Training, Lab, Practice). Use numbers (1: Lecture, 2: Training, 3: Lab, 4: Practice).</li>
        <li>Time Per Week: Enter the number of hours per week for the course task.</li>
        <li>Coherence Requirement: Specify if the course requires continuous sessions (true or false).</li>
        <li>Teacher ID: Enter the teacher's ID responsible for the course task.</li>
        <li>Course ID: Enter the ID of the course this task belongs to.</li>
        <li>Room Type: Enter the type of room needed (1: Classroom, 2: Lab, etc.).</li>
      </ul>
    </div>

    <form v-if="selectedCampusId !== null" @submit.prevent="addCourseTask">
      <input v-model="newCourseTask.courseTaskType" type="number" placeholder="Course Task Type (1: Lecture, 2: Training, etc.)" required />
      <input v-model="newCourseTask.timePerWeek" type="number" placeholder="Time Per Week (hours)" required />
      <input v-model="newCourseTask.coherenceRequirement" type="text" placeholder="Coherence Requirement (true/false)" required />
      <input v-model="newCourseTask.teacherId" type="number" placeholder="Teacher ID" required />
      <input v-model="newCourseTask.courseId" type="number" placeholder="Course ID" required />
      <input v-model="newCourseTask.roomType" type="number" placeholder="Room Type (1: Classroom, 2: Lab, etc.)" required />
      <button type="submit">Add Course Task</button>
    </form>

    <table v-if="selectedCampusId !== null">
      <thead>
        <tr>
          <th>Course Task Type</th>
          <th>Time Per Week</th>
          <th>Coherence Requirement</th>
          <th>Teacher ID</th>
          <th>Course ID</th>
          <th>Room Type</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(courseTask, index) in filteredCourseTasks" :key="index">
          <td>{{ courseTask.CourseTaskType }}</td>
          <td>{{ courseTask.TimePerWeek }}</td>
          <td>{{ courseTask.CoherenceRequirement }}</td>
          <td>{{ courseTask.TeacherID }}</td>
          <td>{{ courseTask.CourseID }}</td>
          <td>{{ courseTask.RoomType }}</td>
          <td>
            <button @click="deleteCourseTask(index)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      campuses: {
        0: 'Melbourne',
        1: 'Geelong',
        2: 'Sydney',
        3: 'Adelaide'
      },
      selectedCampusId: null,
      newCourseTask: {
        courseTaskType: '',
        timePerWeek: '',
        coherenceRequirement: '',
        teacherId: '',
        courseId: '',
        roomType: ''
      },
      courseTasks: []
    };
  },
  computed: {
    filteredCourseTasks() {
      return Array.isArray(this.courseTasks) ? this.courseTasks.filter(courseTask => courseTask.CampusID == this.selectedCampusId) : [];
    }
  },
  methods: {
    goToPage(page) {
      this.$router.push(page);
    },
    selectCampus(campusId) {
      this.selectedCampusId = campusId;
      this.fetchCourseTasks();
    },
    addCourseTask() {
      if (
        !this.newCourseTask.courseTaskType ||
        !this.newCourseTask.timePerWeek ||
        !this.newCourseTask.coherenceRequirement ||
        !this.newCourseTask.teacherId ||
        !this.newCourseTask.courseId ||
        !this.newCourseTask.roomType
      ) {
        alert('The input cannot be empty.');
        return;
      }

      // 添加campusId到newCourseTask中
      this.newCourseTask.campusId = this.selectedCampusId;

      axios.post('http://127.0.0.1:5002/course-management', this.newCourseTask, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then(response => {
        console.log(response.data.message);
        this.fetchCourseTasks();
        this.resetForm();
      })
      .catch(error => {
        console.error('Failed to add course task:', error.response?.data?.message);
      });
    },
    deleteCourseTask(index) {
      if (confirm('Confirm to delete')) {
        const globalIndex = this.courseTasks.findIndex((courseTask, i) => courseTask.CampusID == this.selectedCampusId && i === index);
        if (globalIndex !== -1) {
          this.courseTasks.splice(globalIndex, 1);
        }
        this.saveToLocalStorage();
      }
    },
    fetchCourseTasks() {
      axios.get('http://127.0.0.1:5002/course-management', {
        headers: {
          'Accept': 'application/json'
        },
        params: {
          campusId: this.selectedCampusId
        }
      })
      .then(response => {
        this.courseTasks = Array.isArray(response.data) ? response.data : [];
      })
      .catch(error => {
        console.error('Failed to fetch course tasks:', error);
      });
    },
    resetForm() {
      this.newCourseTask = {
        courseTaskType: '',
        timePerWeek: '',
        coherenceRequirement: '',
        teacherId: '',
        courseId: '',
        roomType: '',
        campusId: null
      };
    },
    logout() {
      // Add your logout logic here
    }
  },
  mounted() {
    this.fetchCourseTasks();
  }
};
</script>

<style>
/* Add necessary styling here */
</style>


<style scoped>
* {
  box-sizing: border-box;
}

body {
  font-family: 'Roboto', sans-serif;
}

.course-management-page {
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

h1 {
  margin-top: 30px;
  text-align: center;
  color: #333;
  font-size: 36px;
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

.instructions {
  text-align: center;
  margin: 20px;
  font-size: 16px;
  color: #666;
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

