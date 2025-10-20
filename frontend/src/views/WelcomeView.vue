<template>
  <div class="welcome-wrapper">
    <div class="floating-shapes">
      <div class="shape shape1"></div>
      <div class="shape shape2"></div>
      <div class="shape shape3"></div>
    </div>

    <div class="welcome-container">
      <div class="hero-section">
        <div class="logo">🏦</div>
        <h1>Bienvenido a BankSync</h1>
        <p class="subtitle">
          La solución inteligente para la conciliación bancaria automática.<br>
          Simplifica tu gestión financiera con tecnología de vanguardia.
        </p>

        <div class="features-grid">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="feature-card"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="feature-icon">{{ feature.icon }}</div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </div>
        </div>

        <div class="cta-section">
          <button class="btn btn-primary" @click="comenzar">Comenzar Ahora</button>
          <button class="btn btn-secondary" @click="verDemo">Ver Demo</button>
        </div>
      </div>

      <div class="stats-section">
        <div v-for="(stat, index) in stats" :key="index" class="stat-card">
          <div class="stat-number">{{ stat.number }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const features = ref([
  {
    icon: '⚡',
    title: 'Automatización Completa',
    description: 'Concilia tus transacciones bancarias de forma automática en segundos. Ahorra tiempo y elimina errores manuales.'
  },
  {
    icon: '📊',
    title: 'Reportes en Tiempo Real',
    description: 'Visualiza dashboards actualizados con métricas clave de tu gestión financiera en tiempo real.'
  },
  {
    icon: '🔒',
    title: 'Seguridad Garantizada',
    description: 'Protección de datos bancarios con encriptación de nivel empresarial y cumplimiento de estándares internacionales.'
  },
  {
    icon: '🤝',
    title: 'Integración Bancaria',
    description: 'Conecta múltiples cuentas bancarias en una sola plataforma. Compatible con los principales bancos.'
  },
  {
    icon: '📈',
    title: 'Análisis Predictivo',
    description: 'Detecta patrones y anomalías automáticamente con algoritmos de inteligencia artificial.'
  },
  {
    icon: '💼',
    title: 'Gestión Empresarial',
    description: 'Herramientas diseñadas para empresas de todos los tamaños. Escala según tus necesidades.'
  }
]);

const stats = ref([
  { number: '99.9%', label: 'Precisión en Conciliaciones' },
  { number: '10min', label: 'Tiempo Promedio de Proceso' },
  { number: '24/7', label: 'Soporte Disponible' },
  { number: '15+', label: 'Bancos Integrados' }
]);

const comenzar = () => {
  router.push('/upload');
};

const verDemo = () => {
  router.push('/demo');
};
</script>

<style scoped>
.welcome-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-x: hidden;
  position: relative;
}

.floating-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite ease-in-out;
}

.shape1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.shape3 {
  width: 100px;
  height: 100px;
  bottom: 10%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(180deg);
  }
}

.welcome-container {
  max-width: 1200px;
  width: 100%;
  padding: 40px 20px;
  position: relative;
  z-index: 1;
}

.hero-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 60px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
  margin-bottom: 40px;
  backdrop-filter: blur(10px);
}

.logo {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 30px;
  font-size: 40px;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

h1 {
  font-size: 48px;
  color: #2d3748;
  margin-bottom: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 20px;
  color: #4a5568;
  margin-bottom: 40px;
  line-height: 1.6;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.feature-card {
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-align: center;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.2);
}

.feature-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  font-size: 32px;
}

.feature-title {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 12px;
}

.feature-description {
  font-size: 14px;
  color: #718096;
  line-height: 1.6;
}

.cta-section {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 16px 40px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(102, 126, 234, 0.5);
}

.btn-secondary {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 40px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  color: white;
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

@media (max-width: 768px) {
  h1 {
    font-size: 32px;
  }

  .subtitle {
    font-size: 16px;
  }

  .hero-section {
    padding: 40px 24px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>