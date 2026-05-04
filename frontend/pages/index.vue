<template>
  <div class="container">
    <h1>📝 Task Manager</h1>

    <div class="input-row">
      <input v-model="newTask" placeholder="Write task here ..." @keyup.enter="addTask" />
      <button @click="addTask">Add</button>
    </div>

    <ul>
      <li v-for="task in tasks" :key="task.id" :class="{ done: task.completed }">
        <span @click="toggleTask(task.id)">{{ task.title }}</span>
        <button class="del" @click="deleteTask(task.id)">🗑️</button>
      </li>
    </ul>

    <p v-if="tasks.length === 0" class="empty">No task available! 👆</p>
  </div>
</template>

<script setup>
const tasks = ref([])
const newTask = ref('')

async function loadTasks() {
  tasks.value = await $fetch('http://localhost:8000/tasks')
}

async function addTask() {
  if (!newTask.value.trim()) return
  await $fetch('http://localhost:8000/tasks', {
    method: 'POST',
    body: { title: newTask.value }
  })
  newTask.value = ''
  await loadTasks()
}

async function toggleTask(id) {
  await $fetch(`http://localhost:8000/tasks/${id}`, { method: 'PUT' })
  await loadTasks()
}

async function deleteTask(id) {
  await $fetch(`http://localhost:8000/tasks/${id}`, { method: 'DELETE' })
  await loadTasks()
}

onMounted(loadTasks)
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 60px auto;
  font-family: sans-serif;
  padding: 20px;
}
h1 { text-align: center; margin-bottom: 24px; }
.input-row {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}
input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
button {
  padding: 10px 16px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}
ul { list-style: none; padding: 0; }
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  margin-bottom: 8px;
  background: #f9f9f9;
  border-radius: 8px;
}
li span { cursor: pointer; flex: 1; }
li.done span {
  text-decoration: line-through;
  color: #aaa;
}
.del { background: #ef4444; padding: 6px 10px; }
.empty { text-align: center; color: #aaa; }
</style>