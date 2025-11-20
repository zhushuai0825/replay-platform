<template>
  <div id="app">
    <nav>
      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/tasks">Tasks</router-link>
      <router-link to="/traffic">Traffic</router-link>
      <router-link to="/environments">Environments</router-link>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

nav {
  padding: 20px;
  background-color: #f0f0f0;
  border-bottom: 1px solid #ddd;
}

nav a {
  margin-right: 20px;
  text-decoration: none;
  color: #2c3e50;
  font-weight: bold;
}

nav a.router-link-active {
  color: #42b983;
}

main {
  padding: 20px;
}
</style>
