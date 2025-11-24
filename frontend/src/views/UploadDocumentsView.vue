<template>
  <div class="upload-wrapper">
    <div class="upload-container">
      <!-- Header -->
      <div class="page-header">
        <button class="back-button" @click="volver">
          <span>←</span>
        </button>
        <div class="header-content">
          <h1>Carga de Documentos</h1>
          <p>Sube los archivos para la conciliación bancaria automática</p>
        </div>
      </div>

      <!-- Progress Steps -->
      <div class="progress-steps">
        <div class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
          <div class="step-number">1</div>
          <div class="step-label">Banco</div>
        </div>
        <div class="step-line" :class="{ active: currentStep > 1 }"></div>
        <div class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
          <div class="step-number">2</div>
          <div class="step-label">Sistema</div>
        </div>
        <div class="step-line" :class="{ active: currentStep > 2 }"></div>
        <div class="step" :class="{ active: currentStep >= 3 }">
          <div class="step-number">3</div>
          <div class="step-label">Confirmar</div>
        </div>
      </div>

      <!-- Formulario -->
      <form @submit.prevent="procesarConciliacion" class="upload-form">
        
        <!-- Card 1: Extracto Bancario -->
        <div class="upload-card">
          <div class="card-header">
            <div class="card-icon bank">🏦</div>
            <div class="card-title">
              <h3>Extracto Bancario</h3>
              <p>Documento del banco (PDF, Excel, CSV)</p>
            </div>
          </div>

          <div class="form-group">
            <label for="banco">Seleccionar Banco *</label>
            <select id="banco" v-model="formulario.banco" required>
              <option value="">Elige un banco</option>
              <option value="bancolombia">Bancolombia</option>
              <option value="davivienda">Davivienda</option>
              <option value="bbva">BBVA</option>
              <option value="banco-bogota">Banco de Bogotá</option>
              <option value="otro">Otro</option>
            </select>
          </div>

          <div class="form-group">
            <label>Fecha del Extracto *</label>
            <div class="date-range">
              <input type="date" v-model="formulario.fechaInicioBanco" required>
              <span>hasta</span>
              <input type="date" v-model="formulario.fechaFinBanco" required>
            </div>
          </div>

          <div class="upload-area" :class="{ 'has-file': archivoBanco, 'dragover': isDraggingBanco }" 
               @dragover.prevent="isDraggingBanco = true"
               @dragleave.prevent="isDraggingBanco = false"
               @drop.prevent="handleDropBanco">
            <input type="file" id="file-banco" ref="fileBancoInput" @change="handleFileBanco" accept=".pdf,.xlsx,.xls,.csv" hidden>
            <label for="file-banco" class="upload-label">
              <div v-if="!archivoBanco" class="upload-placeholder">
                <div class="upload-icon">📤</div>
                <p class="upload-text">Arrastra el archivo aquí o haz clic para seleccionar</p>
                <p class="upload-hint">PDF, Excel o CSV (Máx. 10MB)</p>
              </div>
              <div v-else class="file-preview">
                <div class="file-icon">📄</div>
                <div class="file-info">
                  <p class="file-name">{{ archivoBanco.name }}</p>
                  <p class="file-size">{{ formatFileSize(archivoBanco.size) }}</p>
                </div>
                <button type="button" class="remove-file" @click.stop="removeFileBanco">✕</button>
              </div>
            </label>
          </div>
        </div>

        <!-- Card 2: Archivo del Sistema -->
        <div class="upload-card">
          <div class="card-header">
            <div class="card-icon system">📊</div>
            <div class="card-title">
              <h3>Archivo del Sistema</h3>
              <p>Reporte de transacciones (Excel, CSV)</p>
            </div>
          </div>

          <div class="form-group">
            <label>Fecha del Reporte *</label>
            <div class="date-range">
              <input type="date" v-model="formulario.fechaInicioSistema" required>
              <span>hasta</span>
              <input type="date" v-model="formulario.fechaFinSistema" required>
            </div>
          </div>

          <div class="upload-area" :class="{ 'has-file': archivoSistema, 'dragover': isDraggingSistema }"
               @dragover.prevent="isDraggingSistema = true"
               @dragleave.prevent="isDraggingSistema = false"
               @drop.prevent="handleDropSistema">
            <input type="file" id="file-sistema" ref="fileSistemaInput" @change="handleFileSistema" accept=".xlsx,.xls,.csv" hidden>
            <label for="file-sistema" class="upload-label">
              <div v-if="!archivoSistema" class="upload-placeholder">
                <div class="upload-icon">📤</div>
                <p class="upload-text">Arrastra el archivo aquí o haz clic para seleccionar</p>
                <p class="upload-hint">Excel o CSV (Máx. 10MB)</p>
              </div>
              <div v-else class="file-preview">
                <div class="file-icon">📊</div>
                <div class="file-info">
                  <p class="file-name">{{ archivoSistema.name }}</p>
                  <p class="file-size">{{ formatFileSize(archivoSistema.size) }}</p>
                </div>
                <button type="button" class="remove-file" @click.stop="removeFileSistema">✕</button>
              </div>
            </label>
          </div>
        </div>

        <!-- Card 3: Opciones adicionales -->
        <div class="upload-card options-card">
          <h4>Opciones de Conciliación</h4>
          
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formulario.conciliarAutomatico">
              <span class="checkbox-custom"></span>
              <div class="checkbox-text">
                <strong>Conciliación Automática</strong>
                <small>El sistema intentará emparejar las transacciones automáticamente</small>
              </div>
            </label>

            <label class="checkbox-label">
              <input type="checkbox" v-model="formulario.notificarResultados">
              <span class="checkbox-custom"></span>
              <div class="checkbox-text">
                <strong>Notificar Resultados</strong>
                <small>Recibir un email cuando termine el proceso</small>
              </div>
            </label>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="form-actions">
          <button type="button" class="btn btn-secondary" @click="limpiarFormulario">Limpiar Todo</button>
          <button type="submit" class="btn btn-primary" :disabled="!formularioValido || procesando">
            <span v-if="!procesando">✓ Iniciar Conciliación</span>
            <span v-else class="loading">
              <span class="spinner"></span>
              Procesando...
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useNotifications } from '@/composables/useNotifications';

const router = useRouter();
const { showSuccess, showError, showWarning, showInfo } = useNotifications();

const currentStep = ref(1);
const procesando = ref(false);
const isDraggingBanco = ref(false);
const isDraggingSistema = ref(false);

const archivoBanco = ref(null);
const archivoSistema = ref(null);
const fileBancoInput = ref(null);
const fileSistemaInput = ref(null);

const formulario = ref({
  banco: '',
  fechaInicioBanco: '',
  fechaFinBanco: '',
  fechaInicioSistema: '',
  fechaFinSistema: '',
  conciliarAutomatico: true,
  notificarResultados: true
});

const formularioValido = computed(() => {
  return formulario.value.banco &&
         formulario.value.fechaInicioBanco &&
         formulario.value.fechaFinBanco &&
         formulario.value.fechaInicioSistema &&
         formulario.value.fechaFinSistema &&
         archivoBanco.value &&
         archivoSistema.value;
});

const volver = () => {
  router.push('/');
};

const handleFileBanco = (event) => {
  const file = event.target.files[0];
  if (file && validarArchivo(file, 10)) {
    archivoBanco.value = file;
    currentStep.value = Math.max(currentStep.value, 2);
  }
  isDraggingBanco.value = false;
};

const handleFileSistema = (event) => {
  const file = event.target.files[0];
  if (file && validarArchivo(file, 10)) {
    archivoSistema.value = file;
    currentStep.value = 3;
  }
  isDraggingSistema.value = false;
};

const handleDropBanco = (event) => {
  const file = event.dataTransfer.files[0];
  if (file && validarArchivo(file, 10)) {
    archivoBanco.value = file;
    currentStep.value = Math.max(currentStep.value, 2);
  }
  isDraggingBanco.value = false;
};

const handleDropSistema = (event) => {
  const file = event.dataTransfer.files[0];
  if (file && validarArchivo(file, 10)) {
    archivoSistema.value = file;
    currentStep.value = 3;
  }
  isDraggingSistema.value = false;
};

const removeFileBanco = () => {
  archivoBanco.value = null;
  if (fileBancoInput.value) {
    fileBancoInput.value.value = '';
  }
};

const removeFileSistema = () => {
  archivoSistema.value = null;
  if (fileSistemaInput.value) {
    fileSistemaInput.value.value = '';
  }
};

const validarArchivo = (file, maxSizeMB) => {
  const maxSize = maxSizeMB * 1024 * 1024;
  if (file.size > maxSize) {
    showError(`El archivo es muy grande. Tamaño máximo: ${maxSizeMB}MB`, 'Archivo Demasiado Grande');
    return false;
  }
  return true;
};

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

const limpiarFormulario = () => {
  formulario.value = {
    banco: '',
    fechaInicioBanco: '',
    fechaFinBanco: '',
    fechaInicioSistema: '',
    fechaFinSistema: '',
    conciliarAutomatico: true,
    notificarResultados: true
  };
  archivoBanco.value = null;
  archivoSistema.value = null;
  currentStep.value = 1;
};

const procesarConciliacion = async () => {
  if (!formularioValido.value) return;

  procesando.value = true;

  const formData = new FormData();
  formData.append('archivoBanco', archivoBanco.value);
  formData.append('archivoSistema', archivoSistema.value);
  formData.append('banco', formulario.value.banco);
  formData.append('fechaInicioBanco', formulario.value.fechaInicioBanco);
  formData.append('fechaFinBanco', formulario.value.fechaFinBanco);
  formData.append('fechaInicioSistema', formulario.value.fechaInicioSistema);
  formData.append('fechaFinSistema', formulario.value.fechaFinSistema);
  formData.append('conciliarAutomatico', formulario.value.conciliarAutomatico);
  formData.append('notificarResultados', formulario.value.notificarResultados);

  setTimeout(() => {
    procesando.value = false;
    showSuccess('¡Conciliación iniciada con éxito!', 'Proceso Iniciado');
    // Redirigir a la vista de conciliaciones después de un breve delay
    setTimeout(() => {
      router.push('/home');
    }, 1500);
  }, 2000);
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.upload-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.upload-container {
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.back-button {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: none;
  background: #f3f4f6;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: #e5e7eb;
  transform: translateX(-3px);
}

.header-content h1 {
  font-size: 28px;
  color: #1f2937;
  margin-bottom: 8px;
}

.header-content p {
  color: #6b7280;
  font-size: 15px;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 40px;
  padding: 0 20px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: white;
  color: #667eea;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
}

.step.completed .step-number {
  background: #10b981;
  color: white;
}

.step-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.step.active .step-label {
  color: white;
}

.step-line {
  width: 80px;
  height: 2px;
  background: rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.step-line.active {
  background: white;
}

.upload-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.upload-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
}

.card-icon.bank {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.card-icon.system {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.card-title h3 {
  font-size: 20px;
  color: #1f2937;
  margin-bottom: 4px;
}

.card-title p {
  font-size: 14px;
  color: #6b7280;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
  font-size: 14px;
}

.form-group select,
.form-group input[type="date"] {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
}

.form-group select:focus,
.form-group input[type="date"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.date-range {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 12px;
}

.date-range span {
  color: #6b7280;
  font-size: 14px;
  text-align: center;
}

.upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  transition: all 0.3s ease;
  background: #f9fafb;
}

.upload-area:hover {
  border-color: #667eea;
  background: #f3f4f6;
}

.upload-area.dragover {
  border-color: #667eea;
  background: #eef2ff;
}

.upload-area.has-file {
  border-style: solid;
  border-color: #10b981;
  background: #f0fdf4;
}

.upload-label {
  cursor: pointer;
  display: block;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.upload-text {
  font-size: 15px;
  color: #374151;
  font-weight: 500;
  margin-bottom: 8px;
}

.upload-hint {
  font-size: 13px;
  color: #6b7280;
}

.file-preview {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 10px;
}

.file-icon {
  font-size: 40px;
}

.file-info {
  flex: 1;
  text-align: left;
}

.file-name {
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 4px;
}

.file-size {
  font-size: 13px;
  color: #6b7280;
}

.remove-file {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: #fee2e2;
  color: #ef4444;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s ease;
}

.remove-file:hover {
  background: #fecaca;
}

.options-card h4 {
  font-size: 18px;
  color: #1f2937;
  margin-bottom: 20px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  padding: 16px;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.checkbox-label:hover {
  background: #f9fafb;
}

.checkbox-label input[type="checkbox"] {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  flex-shrink: 0;
  position: relative;
  transition: all 0.2s ease;
}

.checkbox-label input[type="checkbox"]:checked + .checkbox-custom {
  background: #667eea;
  border-color: #667eea;
}

.checkbox-label input[type="checkbox"]:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 14px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.checkbox-text {
  flex: 1;
}

.checkbox-text strong {
  display: block;
  color: #1f2937;
  margin-bottom: 4px;
  font-size: 14px;
}

.checkbox-text small {
  color: #6b7280;
  font-size: 13px;
}

.form-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}

.btn {
  padding: 14px 32px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(102, 126, 234, 0.5);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .date-range {
    grid-template-columns: 1fr;
  }
  
  .date-range span {
    display: none;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>