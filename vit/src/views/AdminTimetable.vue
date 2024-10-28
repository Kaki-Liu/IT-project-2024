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
          </li>
        </ul>
      </div>

      <div class="week-timetable">
        <h3>{{ selectedCampusName }} Timetable</h3>
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
            <tr v-for="time in timeSlots" :key="time">
              <td>{{ time }}</td>
              <td>
                <div v-for="course in filteredCourses('Monday', time)" :key="course.id">
                  {{ course.name }}
                </div>
              </td>
              <td>
                <div v-for="course in filteredCourses('Tuesday', time)" :key="course.id">
                  {{ course.name }}
                </div>
              </td>
              <td>
                <div v-for="course in filteredCourses('Wednesday', time)" :key="course.id">
                  {{ course.name }}
                </div>
              </td>
              <td>
                <div v-for="course in filteredCourses('Thursday', time)" :key="course.id">
                  {{ course.name }}
                </div>
              </td>
              <td>
                <div v-for="course in filteredCourses('Friday', time)" :key="course.id">
                  {{ course.name }}
                </div>
              </td>
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
      campuses: [
        { id: 1, name: 'Sydney' },
        { id: 2, name: 'Melbourne' },
        { id: 3, name: 'Geelong' },
        { id: 4, name: 'Adelaide' },
      ],
      selectedCampusId: 1,
      courses: {
        1: [
          { id: 1, name: 'Math', day: 'Monday', time: '9:00-10:00' },
          { id: 2, name: 'Physics', day: 'Tuesday', time: '10:00-11:00' },
        ],
        2: [
          { id: 3, name: 'Chemistry', day: 'Wednesday', time: '9:00-10:00' },
          { id: 4, name: 'Biology', day: 'Thursday', time: '11:00-12:00' },
        ],
        3: [
          { id: 5, name: 'English', day: 'Monday', time: '13:00-14:00' },
          { id: 6, name: 'History', day: 'Friday', time: '14:00-15:00' },
        ],
        4: [
          { id: 7, name: 'Art', day: 'Tuesday', time: '15:00-16:00' },
          { id: 8, name: 'Music', day: 'Thursday', time: '16:00-17:00' },
        ],
      },
      timeSlots: [
        '7:00-8:00', '8:00-9:00', '9:00-10:00', '10:00-11:00', 
        '11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00', 
        '15:00-16:00', '16:00-17:00', '17:00-18:00', '18:00-19:00', '19:00-20:00'
      ],
    };
  },
  computed: {
    selectedCampusName() {
      const campus = this.campuses.find(campus => campus.id === this.selectedCampusId);
      return campus ? campus.name : '';
    },
  },
  methods: {
    goToPage(page) {
      this.$router.push(page);
    },
    logout() {
      // Handle logout logic
    },
    filteredCourses(day, time) {
      return this.courses[this.selectedCampusId].filter(course => course.day === day && course.time === time);
    },
    selectCampus(campusId) {
      this.selectedCampusId = campusId;
    },
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
</style>
