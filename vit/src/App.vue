<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/login">Login</router-link>
      <router-link to="/admin-timetable">Admin Timetable</router-link>
      <router-link to="/course-management">Course Management</router-link>
      <router-link to="/classroom-management">Classroom Management</router-link>
      <router-link to="/admin-page">Admin Page</router-link>
    </nav>

    <router-view></router-view>
  </div>
</template>


<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  margin: 20px 0;
}

nav a {
  margin-right: 15px;
  text-decoration: none;
  color: #000;
}

nav a:hover {
  color: #007BFF;
}

</style>
