/**
 * Vuex/Pinia Store
 * 用于状态管理
 */

// 如果使用 Pinia
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    // 应用状态
  }),
  actions: {
    // 应用操作
  },
})

// 如果使用 Vuex，取消注释以下代码
/*
import { createStore } from 'vuex'

export default createStore({
  state: {
    // 应用状态
  },
  mutations: {
    // 状态变更
  },
  actions: {
    // 异步操作
  },
})
*/

