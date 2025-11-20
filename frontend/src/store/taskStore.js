import { defineStore } from 'pinia'
import api from '@/api'

export const useTaskStore = defineStore('task', {
  state: () => ({
    items: [],
    total: 0,
    page: 1,
    pageSize: 10,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchTasks(params = {}) {
      this.loading = true
      const query = {
        page: this.page,
        page_size: this.pageSize,
        ...params,
      }
      try {
        const data = await api.get('/api/v1/tasks/', { params: query })
        this.items = data.items ?? []
        this.total = data.total ?? 0
        this.error = null
      } catch (err) {
        console.error('Failed to fetch tasks:', err)
        this.error = err
      } finally {
        this.loading = false
      }
    },
    setPage(page) {
      this.page = page
    },
  },
})

