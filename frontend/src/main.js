import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

import Profile from './components/Profile.vue'
import Login from './components/Login.vue'

const routes = [
    { path: '/', component: Login },
    { path: '/profile', component: Profile },
    
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// app.component('MyNewComponent', MyNewComponent);
// app.mount('#app');

createApp(App).use(router).mount('#app')
