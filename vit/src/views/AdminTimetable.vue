<template>
  <div>
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

    <div class="timetable-container">
      <div class="campus-list">
        <h2>Campuses</h2>
        <ul>
          <li 
            v-for="campus in campuses" 
            :key="campus.id"
            @click="selectCampus(campus.id)"
            :class="{ active: selectedCampusId === campus.id }"
          >
            {{ campus.name }}
            <div v-if="selectedCampusId === campus.id && rooms.length" class="room-list">
              <h4>Rooms</h4>
              <ul>
                <li 
                  v-for="room in rooms" 
                  :key="room.RoomID"
                  @click="selectRoom(room)"
                >
                  {{ room.RoomName }}
                </li>
              </ul>
            </div>
          </li>
        </ul>
      </div>

      <div class="week-timetable" v-if="schedule.length">
        <h3>{{ selectedCampusName }} Timetable</h3>
        <h4 v-if="selectedRoomAddress">Room Address: {{ selectedRoomAddress }}</h4>
        <table>
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
  <tr v-for="hour in 7" :key="hour">
    <td>{{ `${hour + 7}:00-${hour + 8}:00` }}</td>
    <td v-for="day in [1, 2, 3, 4, 5]" :key="day">
      <template v-if="!isMerged(hour + 7, day)">
        <div 
          v-for="course in getCoursesForTimeAndDay(hour + 7, day)" 
          :key="course.CourseName" 
          :rowspan="course.EndTime - course.StartTime" 
          class="course-cell"
        >
          {{ course.CourseName }} ({{ course.StartTime }}:00 - {{ course.EndTime }}:00)
        </div>
      </template>
    </td>
  </tr>
</tbody>


        </table>
      </div>
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
      selectedCampusId: null,
      selectedRoomAddress: '',
      rooms: [],
      schedule: [],
      timeSlots: Array.from({ length: 13 }, (_, i) => `${i + 7}:00-${i + 8}:00`),
    };
  },
  computed: {
    selectedCampusName() {
      const campus = this.campuses.find(campus => campus.id === this.selectedCampusId);
      return campus ? campus.name : '';
    },
  },
  methods: {
    isMerged(hour, day) {
      // Logic to check if the cell has already been rendered in a previous hour
      return this.schedule.some(course => 
        course.Day === day && 
        course.StartTime < hour && 
        course.EndTime > hour
      );
    },
    getCoursesForTimeAndDay(hour, day) {
      return this.schedule.filter(course => {
        return course.Day === day && course.StartTime === hour;
      })},
    goToPage(page) {
      this.$router.push(page);
    },
    logout() {
      // Handle logout logic
    },
    selectCampus(campusId) {
      this.selectedCampusId = campusId;
      this.sendCampusIdToServer(campusId);
    },
    selectRoom(room) {
      this.selectedRoomAddress = room.RoomAddress;
      this.sendRoomIdToServer(room.RoomID);
    },
    sendCampusIdToServer(campusId) {
      axios.post('http://127.0.0.1:5002/admin-timetable', {
        campusId: campusId
      })
      .then(response => {
        console.log('Campus ID sent successfully:', response.data);
        this.rooms = response.data.rooms;
      })
      .catch(error => {
        console.error('Error sending campus ID:', error);
      });
    },
    sendRoomIdToServer(roomId) {
      axios.post('http://127.0.0.1:5002/admin-timetable/room', {
        roomId: roomId
      })
      .then(response => {
        console.log('Room ID sent successfully:', response.data);
        this.schedule = response.data.schedule;
      })
      .catch(error => {
        console.error('Error sending room ID:', error);
      });
    },
    getCoursesForTimeAndDay(hour, day) {
      return this.schedule.filter(course => {
        return course.Day === day && course.StartTime <= hour && course.EndTime > hour;
      });
    }
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.logo {
  height: 60px;
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

/* 时间表样式 */
.timetable-container {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

.campus-list {
  width: 20%;
  background-color: #f5f5f5;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.campus-list h2 {
  margin-bottom: 10px;
  color: #ff7043;
}

.campus-list ul {
  list-style-type: none;
}

.campus-list li {
  margin: 5px 0;
  cursor: pointer;
  padding: 5px;
  transition: background-color 0.3s ease;
}

.campus-list li:hover {
  background-color: #eee;
}

.campus-list li.active {
  font-weight: bold;
  background-color: #ff7043;
  color: white;
}

.week-timetable {
  width: 75%;
  padding: 15px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: center;
  border: 1px solid #ddd;
}

th {
  background-color: #ff7043;
  color: white;
}

td {
  background-color: white;
  border-radius: 4px;
}

.course-cell {
  background-color: #FFECB3;
  border: 1px solid #FF7043;
  border-radius: 4px;
}
</style>