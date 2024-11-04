// main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';

const app = createApp(App);

// 设置全局 Axios 实例
app.config.globalProperties.$axios = axios;

// 如果需要，可以设置默认的 Axios 配置
axios.defaults.baseURL = 'http://127.0.0.1:5002/api'; // 设置默认的 API 路径
axios.defaults.headers.common['Content-Type'] = 'application/json';

app.use(router);
app.mount('#app');
