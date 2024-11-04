<template>
    <div class="select-campus">
      <h1>Select Campus</h1>
      <div class="button-container">
        <button class="campus-button" @click="selectCampus(0)">Melbourne</button>
        <button class="campus-button" @click="selectCampus(1)">Geelong</button>
        <button class="campus-button" @click="selectCampus(2)">Sydney</button>
        <button class="campus-button" @click="selectCampus(3)">Adelaide</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'SelectCampus',
    methods: {
      selectCampus(campusId) {
        axios.get('http://127.0.0.1:5002/schedule-management', {
          params: {
            campusId: campusId
          }
        }).then(response => {
          console.log('Response:', response.data);
          alert(`New schedule generated for campus with ID ${campusId}`);
        }).catch(error => {
          console.error('Error:', error);
          alert('Failed to generate schedule. Please try again.');
        });
      }
    }
  }
  </script>
  
  
  <style scoped>
  .select-campus {
    text-align: center;
    margin-top: 50px;
  }
  
  .button-container {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
  }
  
  .campus-button {
    padding: 10px 1px;
    font-size: 14px;
    width: 100px;
    color: white;
    background-color: #ff6347;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .campus-button:hover {
    background-color: #e5533f;
  }
  </style>
  