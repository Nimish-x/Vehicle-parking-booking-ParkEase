import { defineStore } from "pinia";

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    userInfo: null,
  }),
  actions: {
    setToken(token) {
      this.token = token;
      localStorage.setItem('token', token); // persist token
    },
    setUserInfo(user) {
      this.userInfo = user;
    },
    logout() {
      this.token = null;
      this.userInfo = null;
      localStorage.removeItem('token');
    },
  },
});
