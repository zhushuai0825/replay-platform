<template>
  <div class="tasks">
    <header class="tasks__header">
      <div>
        <h2>任务管理</h2>
        <p>查看后端返回的任务列表（数据来自 /api/v1/tasks/）。</p>
      </div>
      <button class="tasks__button" @click="reload" :disabled="loading">
        {{ loading ? '加载中...' : '刷新' }}
      </button>
    </header>

    <section v-if="error" class="tasks__error">
      <strong>获取任务失败：</strong> {{ errorMessage }}
    </section>

    <section v-else>
      <table class="tasks__table">
        <thead>
          <tr>
            <th>ID</th>
            <th>名称</th>
            <th>状态</th>
            <th>进度</th>
            <th>创建时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <td>{{ task.id }}</td>
            <td>{{ task.name }}</td>
            <td>{{ task.status }}</td>
            <td>{{ task.progress ?? 0 }}%</td>
            <td>{{ formatTime(task.created_at) }}</td>
          </tr>
          <tr v-if="!loading && tasks.length === 0">
            <td colspan="5" class="tasks__empty">暂无数据</td>
          </tr>
        </tbody>
      </table>

      <div class="tasks__pagination">
        <button
          @click="changePage(taskStore.page - 1)"
          :disabled="taskStore.page === 1 || loading"
        >
          上一页
        </button>
        <span>第 {{ taskStore.page }} 页</span>
        <button
          @click="changePage(taskStore.page + 1)"
          :disabled="endOfList || loading"
        >
          下一页
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useTaskStore } from '@/store'

const taskStore = useTaskStore()

const tasks = computed(() => taskStore.items)
const loading = computed(() => taskStore.loading)
const error = computed(() => taskStore.error)
const errorMessage = computed(() => taskStore.error?.message ?? '未知错误')
const endOfList = computed(() => {
  return taskStore.page * taskStore.pageSize >= taskStore.total
})

const reload = () => {
  taskStore.fetchTasks()
}

const changePage = (page) => {
  if (page < 1) return
  taskStore.setPage(page)
  taskStore.fetchTasks()
}

const formatTime = (value) => {
  if (!value) return '-'
  return new Date(value).toLocaleString()
}

onMounted(() => {
  taskStore.fetchTasks()
})
</script>

<style scoped>
.tasks {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tasks__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tasks__button {
  padding: 8px 16px;
  border: none;
  background: #2563eb;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

.tasks__button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.tasks__table {
  width: 100%;
  border-collapse: collapse;
}

.tasks__table th,
.tasks__table td {
  border: 1px solid #e5e7eb;
  padding: 8px;
  text-align: left;
}

.tasks__empty {
  text-align: center;
  color: #9ca3af;
}

.tasks__pagination {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.tasks__error {
  padding: 12px;
  border: 1px solid #fca5a5;
  background: #fee2e2;
  color: #b91c1c;
}
</style>

