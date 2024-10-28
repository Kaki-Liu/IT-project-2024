<template>
  <div class="student-information-page">
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

    <h1>Student Information</h1>

    <form @submit.prevent="addStudent">
      <input v-model="newStudent.studentId" type="text" placeholder="Student ID" required />
      <input v-model="newStudent.studentName" type="text" placeholder="Student Name" required />
      <input v-model="newStudent.personalEmail" type="email" placeholder="Personal Email" required />
      <input v-model="newStudent.universityEmail" type="email" placeholder="University Email" required />
      <input v-model="newStudent.studentType" type="text" placeholder="Student Type" required />
      <input v-model="newStudent.offerType" type="text" placeholder="Offer Type" required />
      <input v-model="newStudent.courseName" type="text" placeholder="Course Name" required />
      <input v-model="newStudent.campus" type="text" placeholder="Campus" required />
      
      <!-- Updated Date Fields with Placeholders -->
      <input v-model="newStudent.originalCOEStartDate" type="date" placeholder="Original COE Start Date" required />
      <input v-model="newStudent.courseStartDate" type="date" placeholder="Course Start Date" required />
      <input v-model="newStudent.courseEndDate" type="date" placeholder="Course End Date" required />

      <input v-model="newStudent.coeStatus" type="text" placeholder="COE Status" required />
      <input v-model="newStudent.specialisation" type="text" placeholder="Specialisation" />
      <input v-model="newStudent.pathwayIndicator" type="text" placeholder="Pathway Indicator" />
      <button type="submit">Add Student</button>
    </form>

    <div class="title">Total Students: <span>{{ students.length }}</span></div>

    <table>
      <thead>
        <tr>
          <th>Student ID</th>
          <th>Student Name</th>
          <th>Personal Email</th>
          <th>University Email</th>
          <th>Student Type</th>
          <th>Offer Type</th>
          <th>Course Name</th>
          <th>Campus</th>
          <th>Original COE Start Date</th>
          <th>Course Start Date</th>
          <th>Course End Date</th>
          <th>COE Status</th>
          <th>Specialisation</th>
          <th>Pathway Indicator</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(student, index) in students" :key="index">
          <td>{{ student.studentId }}</td>
          <td>{{ student.studentName }}</td>
          <td>{{ student.personalEmail }}</td>
          <td>{{ student.universityEmail }}</td>
          <td>{{ student.studentType }}</td>
          <td>{{ student.offerType }}</td>
          <td>{{ student.courseName }}</td>
          <td>{{ student.campus }}</td>
          <td>{{ student.originalCOEStartDate }}</td>
          <td>{{ student.courseStartDate }}</td>
          <td>{{ student.courseEndDate }}</td>
          <td>{{ student.coeStatus }}</td>
          <td>{{ student.specialisation }}</td>
          <td>{{ student.pathwayIndicator }}</td>
          <td>
            <button @click="deleteStudent(index)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newStudent: {
        studentId: '',
        studentName: '',
        personalEmail: '',
        universityEmail: '',
        studentType: '',
        offerType: '',
        courseName: '',
        campus: '',
        originalCOEStartDate: '',
        courseStartDate: '',
        courseEndDate: '',
        coeStatus: '',
        specialisation: '',
        pathwayIndicator: ''
      },
      students: JSON.parse(localStorage.getItem('students')) || []
    };
  },
  methods: {
    goToPage(page) {
      this.$router.push(page);
    },
    addStudent() {
      if (
        !this.newStudent.studentId ||
        !this.newStudent.studentName ||
        !this.newStudent.personalEmail ||
        !this.newStudent.universityEmail ||
        !this.newStudent.studentType ||
        !this.newStudent.offerType ||
        !this.newStudent.courseName ||
        !this.newStudent.campus ||
        !this.newStudent.originalCOEStartDate ||
        !this.newStudent.courseStartDate ||
        !this.newStudent.courseEndDate ||
        !this.newStudent.coeStatus
      ) {
        alert('All required fields must be filled.');
        return;
      }

      this.students.push({ ...this.newStudent });
      this.saveToLocalStorage();
      this.resetForm();
    },
    deleteStudent(index) {
      if (confirm('Are you sure you want to delete this student?')) {
        this.students.splice(index, 1);
        this.saveToLocalStorage();
      }
    },
    saveToLocalStorage() {
      localStorage.setItem('students', JSON.stringify(this.students));
    },
    resetForm() {
      this.newStudent = {
        studentId: '',
        studentName: '',
        personalEmail: '',
        universityEmail: '',
        studentType: '',
        offerType: '',
        courseName: '',
        campus: '',
        originalCOEStartDate: '',
        courseStartDate: '',
        courseEndDate: '',
        coeStatus: '',
        specialisation: '',
        pathwayIndicator: ''
      };
    },
    logout() {
      // Add your logout logic here
    }
  }
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #f87c51;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  gap: 10px;
}

button {
  padding: 10px;
  background-color: #f87c51;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #e66a3f;
}

.student-information-page {
  max-width: 1200px;
  margin: 30px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

form {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

form input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  border: 1px solid #ddd;
}

th {
  background-color: #f87c51;
  color: white;
}

button.delete {
  background-color: #ff4d4d;
}

button.delete:hover {
  background-color: #e63939;
}
</style>
