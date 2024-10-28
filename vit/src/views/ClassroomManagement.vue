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

      <form v-if="selectedCampusId" @submit.prevent="addClassroom" class="classroom-form">
        <input v-model="newClassroom.name" type="text" placeholder="Classroom/Lab Name" required />
        <input v-model="newClassroom.type" type="number" placeholder="Room Type (0 for Classroom, 1 for Lab)" required />
        <input v-model="newClassroom.number" type="text" placeholder="Classroom Number" required />
        <input v-model="newClassroom.location" type="text" placeholder="Location (Building/Level)" required />
        <input v-model="newClassroom.capacity" type="number" placeholder="Capacity" required />
        <input v-model="newClassroom.availableTimeStart" type="number" placeholder="Available Time Start (Hour)" required />
        <input v-model="newClassroom.availableTimeEnd" type="number" placeholder="Available Time End (Hour)" required />
        <input v-model="newClassroom.availableDays" type="number" placeholder="Available Days" required />
        <button type="submit" class="add-button">Add Classroom</button>
      </form>

      <div class="title" v-if="selectedCampusId">Total Classrooms: <span>{{ filteredClassrooms.length }}</span></div>
      
      <table class="classroom-table" v-if="selectedCampusId">
        <thead>
          <tr>
            <th>Classroom/Lab Name</th>
            <th>Room Type</th>
            <th>Classroom Number</th>
            <th>Location <br>Building/Level</th>
            <th>Capacity</th>
            <th>Available Time Start</th>
            <th>Available Time End</th>
            <th>Available Days</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(classroom, index) in filteredClassrooms" :key="index">
            <td>{{ classroom.name }}</td>
            <td>{{ classroom.type === 0 ? 'Classroom' : 'Lab' }}</td>
            <td>{{ classroom.number }}</td>
            <td>{{ classroom.location }}</td>
            <td>{{ classroom.capacity }}</td>
            <td>{{ classroom.availableTimeStart }}</td>
            <td>{{ classroom.availableTimeEnd }}</td>
            <td>{{ classroom.availableDays }}</td>
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
        { id: 1, name: 'Sydney' },
        { id: 2, name: 'Melbourne' },
        { id: 3, name: 'Geelong' },
        { id: 4, name: 'Adelaide' },
      ],
      selectedCampusId: null,
      newClassroom: {
        name: '',
        type: '',
        number: '',
        location: '',
        capacity: '',
        availableTimeStart: '',
        availableTimeEnd: '',
        availableDays: '',
      },
      classrooms: []
    };
  },
  computed: {
    filteredClassrooms() {
      return this.classrooms.filter(classroom => classroom.campusId === this.selectedCampusId);
    }
  },
  methods: {
    goToPage(page) {
      this.$router.push(page);
    },
    logout() {
      // Handle logout logic
    },
    selectCampus(campusId) {
      this.selectedCampusId = campusId;
      this.fetchClassrooms();
    },
    async addClassroom() {
      try {
        const response = await axios.post('http://127.0.0.1:5002/api/classrooms', {
          ...this.newClassroom,
          campusId: this.selectedCampusId
        });
        alert(response.data.message);
        this.fetchClassrooms();
        this.resetForm();
      } catch (error) {
        console.error('Error adding classroom:', error);
        alert('Failed to add classroom.');
      }
    },
    async deleteClassroom(index) {
      const classroomToDelete = this.filteredClassrooms[index];
      try {
        await axios.delete(`http://127.0.0.1:5002/api/classrooms/${classroomToDelete.id}`);
        alert('Classroom deleted successfully!');
        this.fetchClassrooms();
      } catch (error) {
        console.error('Error deleting classroom:', error);
        alert('Failed to delete classroom.');
      }
    },
    async fetchClassrooms() {
      try {
        const response = await axios.get('http://127.0.0.1:5002/api/classrooms');
        this.classrooms = response.data;
      } catch (error) {
        console.error('Error fetching classrooms:', error);
        alert('Failed to load classrooms.');
      }
    },
    resetForm() {
      this.newClassroom = {
        name: '',
        type: '',
        number: '',
        location: '',
        capacity: '',
        availableTimeStart: '',
        availableTimeEnd: '',
        availableDays: '',
      };
    }
  },
  created() {
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

