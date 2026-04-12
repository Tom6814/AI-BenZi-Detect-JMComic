import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    message: 'Hello from Pinia with Material 3 Expressive & Aurora Neon!'
  }),
  actions: {
    updateMessage(newMessage) {
      this.message = newMessage
    }
  }
})
