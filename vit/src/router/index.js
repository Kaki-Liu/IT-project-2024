// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import AdminPage from '@/views/AdminPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import ClassroomManagement from '@/views/ClassroomManagement.vue';
import CourseManagement from '@/views/CourseManagement.vue';
import AdminTimetable from '@/views/AdminTimetable.vue';
import GenerateTimetable from '@/views/GenerateTimetable.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/admin-page',
    name: 'AdminPage',
    component: AdminPage
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/classroom-management',
    name: 'ClassroomManagement',
    component: ClassroomManagement
  },
  {
    path: '/course-management',
    name: 'CourseManagement',
    component: CourseManagement
  },
  {
    path: '/admin-timetable',
    name: 'AdminTimetable',
    component: AdminTimetable
  },
  {
    path: '/schedule-management',
    name: 'GenerateTimetable',
    component: GenerateTimetable
  },
 
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
