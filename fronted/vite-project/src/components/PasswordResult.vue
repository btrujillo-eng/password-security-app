<template>
  <div v-if="result" class="result-card" :style="{ borderColor: result.safety_color }">
    
    <h2 :style="{ color: result.safety_color }">
      Contraseña: {{ result.security_status }}
    </h2>

    <div v-if="result.vulnerabilities.length > 0">
      <h3>Vulnerabilidades detectadas</h3>
      <ul>
        <li v-for="(vuln, index) in result.vulnerabilities" :key="index">
          {{ vuln }}
        </li>
      </ul>
    </div>

    <div v-if="result.feedback.length > 0">
      <h3>Sugerencias</h3>
      <ul>
        <li v-for="(tip, index) in result.feedback" :key="index">
          {{ tip }}
        </li>
      </ul>
    </div>

  </div>
</template>

<script setup>
defineProps({
  result: {
    type: Object,
    default: null
  }
})
</script>

<style scoped>
.result-card {
  margin-top: 24px;
  padding: 20px;
  border: 2px solid;
  border-radius: 8px;
}

h2 {
  margin-bottom: 12px;
}

h3 {
  margin-top: 16px;
  margin-bottom: 8px;
}

ul {
  padding-left: 20px;
}

li {
  margin-bottom: 6px;
}
</style>