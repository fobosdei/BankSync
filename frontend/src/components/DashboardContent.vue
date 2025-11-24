<template>
    <div>
        <!-- Header -->
        <header class="sticky top-0 z-20 bg-white/70 backdrop-blur-md border-b border-white/60 px-8 py-4 shadow-sm">
            <div class="flex items-center justify-end gap-3">
                <button
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white/80 border border-gray-200 rounded-lg shadow-sm flex items-center gap-2 transition-all duration-200 hover:bg-white hover:-translate-y-0.5 hover:shadow-md"
                    @click="exportDashboardResumen"
                >
                    Exportar
                </button>
                <button
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white/80 border border-gray-200 rounded-lg shadow-sm flex items-center gap-2 transition-all duration-200 hover:bg-white hover:-translate-y-0.5 hover:shadow-md"
                    @click="scrollToBankAccounts"
                >
                    Importar extracto
                </button>
                <button
                    class="px-4 py-2 text-sm font-semibold text-white bg-purple-700 rounded-lg shadow-md flex items-center gap-2 transition-all duration-200 hover:bg-purple-800 hover:-translate-y-0.5 hover:shadow-lg active:scale-95"
                    @click="$emit('open-conciliation-modal')"
                >
                    Nueva conciliación
                </button>
            </div>
        </header>

        <div class="p-8">
        <!-- Stats Cards -->
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <!-- Card 1 -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <p class="text-sm text-gray-600 mb-1">Conciliación Total</p>
                        <h3 class="text-3xl font-bold text-gray-900">
                            {{ Math.round(resumen.promedio_porcentaje_conciliado || 0) }}%
                        </h3>
                    </div>
                    <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        ✓
                    </div>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2 mb-2">
                    <div
                        class="bg-green-600 h-2 rounded-full"
                        :style="`width: ${Math.round(resumen.promedio_porcentaje_conciliado || 0)}%`"
                    ></div>
                </div>
                <p class="text-xs text-green-600 font-medium" v-if="resumen.total_conciliaciones > 0">
                    {{ resumen.total_conciliaciones }} conciliación{{ resumen.total_conciliaciones !== 1 ? 'es' : '' }}
                </p>
                <p class="text-xs text-gray-500 font-medium" v-else>
                    Sin conciliaciones aún
                </p>
            </div>

            <!-- Card 2 -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <p class="text-sm text-gray-600 mb-1">Tiempo Promedio</p>
                        <h3 class="text-3xl font-bold text-gray-900">2.3 min</h3>
                    </div>
                    <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                        ⏱
                    </div>
                </div>
                <p class="text-sm text-gray-600 mb-2">Por transacción</p>
                <p class="text-xs text-green-600 font-medium">↓ 46% con IA</p>
            </div>

            <!-- Card 3 -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <p class="text-sm text-gray-600 mb-1">Pendientes</p>
                        <h3 class="text-3xl font-bold text-gray-900">
                            {{ pendientesTotales }}
                        </h3>
                    </div>
                    <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                        ⚠
                    </div>
                </div>
                <p class="text-sm text-gray-600 mb-2">Transacciones</p>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <!-- Tendencia Chart -->
            <div class="lg:col-span-2 bg-white rounded-xl p-6 border border-gray-200">
                <div class="mb-6">
                    <h3 class="text-lg font-semibold text-gray-900">Tendencia de Conciliación</h3>
                    <p class="text-sm text-gray-600">Últimos 6 meses</p>
                </div>
                <div v-if="chartData.length > 0" class="h-64 flex items-end justify-between gap-4">
                    <div v-for="month in chartData" :key="month.name" class="flex-1 flex flex-col items-center gap-2" style="min-height: 0;">
                        <div class="w-full flex flex-col items-center justify-end gap-1" style="height: 100%;">
                            <div class="w-full flex flex-col-reverse gap-1" style="height: 100%;">
                                <div 
                                    class="w-full bg-green-500 rounded-t-lg transition-all duration-500 hover:bg-green-600" 
                                    :style="`height: ${Math.max(month.conciliado, 2)}%`"
                                    :title="`${month.conciliadas} conciliadas de ${month.total}`"
                                ></div>
                                <div 
                                    class="w-full bg-orange-400 rounded-t-lg transition-all duration-500 hover:bg-orange-500" 
                                    :style="`height: ${Math.max(month.pendiente, 2)}%`"
                                    :title="`${month.total - month.conciliadas} pendientes`"
                                ></div>
                            </div>
                        </div>
                        <span class="text-xs text-gray-600 font-medium">{{ month.name }}</span>
                        <span v-if="month.total > 0" class="text-xs text-gray-500">{{ month.total }}</span>
                    </div>
                </div>
                <div v-else class="h-64 flex items-center justify-center">
                    <p class="text-gray-500 text-sm">No hay datos de tendencia disponibles</p>
                </div>
                <div class="flex items-center justify-center gap-6 mt-6">
                    <div class="flex items-center gap-2">
                        <div class="w-3 h-3 bg-green-500 rounded"></div>
                        <span class="text-sm text-gray-600">Conciliado %</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <div class="w-3 h-3 bg-orange-400 rounded"></div>
                        <span class="text-sm text-gray-600">Pendiente %</span>
                    </div>
                </div>
            </div>

            <!-- Pie Chart -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
                <div class="mb-6">
                    <h3 class="text-lg font-semibold text-gray-900">Estado Global</h3>
                    <p class="text-sm text-gray-600">Distribución actual</p>
                </div>
                <div class="flex items-center justify-center h-64">
                    <div class="relative w-48 h-48">
                        <!-- Gráfico circular basado en datos reales -->
                        <svg viewBox="0 0 200 200" class="transform -rotate-90">
                            <!-- Círculo de fondo -->
                            <circle cx="100" cy="100" r="80" fill="#e5e7eb" stroke="none" />
                            
                            <!-- Porcentaje conciliado (verde) -->
                            <circle
                                v-if="pieChartData.conciliado > 0"
                                cx="100"
                                cy="100"
                                r="80"
                                fill="none"
                                :stroke="'#10b981'"
                                :stroke-width="40"
                                :stroke-dasharray="`${(pieChartData.conciliado / 100) * 502.65} 502.65`"
                                stroke-linecap="round"
                                transform="rotate(0 100 100)"
                                class="transition-all duration-500"
                            />
                            
                            <!-- Porcentaje pendiente (naranja) -->
                            <circle
                                v-if="pieChartData.pendiente > 0"
                                cx="100"
                                cy="100"
                                r="80"
                                fill="none"
                                :stroke="'#f97316'"
                                :stroke-width="40"
                                :stroke-dasharray="`${(pieChartData.pendiente / 100) * 502.65} 502.65`"
                                :stroke-dashoffset="`-${(pieChartData.conciliado / 100) * 502.65}`"
                                stroke-linecap="round"
                                class="transition-all duration-500"
                            />
                            
                            <!-- Porcentaje con error (rojo) -->
                            <circle
                                v-if="pieChartData.error > 0"
                                cx="100"
                                cy="100"
                                r="80"
                                fill="none"
                                :stroke="'#ef4444'"
                                :stroke-width="40"
                                :stroke-dasharray="`${(pieChartData.error / 100) * 502.65} 502.65`"
                                :stroke-dashoffset="`-${((pieChartData.conciliado + pieChartData.pendiente) / 100) * 502.65}`"
                                stroke-linecap="round"
                                class="transition-all duration-500"
                            />
                        </svg>
                        
                        <!-- Texto central -->
                        <div class="absolute inset-0 flex items-center justify-center">
                            <div class="text-center">
                                <div class="text-2xl font-bold text-gray-900">
                                    {{ Math.round(resumen.promedio_porcentaje_conciliado || 0) }}%
                                </div>
                                <div class="text-xs text-gray-500">Conciliado</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="space-y-3 mt-4">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <div class="w-3 h-3 bg-green-500 rounded"></div>
                            <span class="text-sm text-gray-600">Conciliado</span>
                        </div>
                        <span class="text-sm font-semibold text-gray-900">
                            {{ Math.round(resumen.promedio_porcentaje_conciliado || 0) }}%
                        </span>
                    </div>
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <div class="w-3 h-3 bg-orange-400 rounded"></div>
                            <span class="text-sm text-gray-600">Pendiente</span>
                        </div>
                        <span class="text-sm font-semibold text-gray-900">
                            {{ pendientesTotales }}
                        </span>
                    </div>
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <div class="w-3 h-3 bg-red-500 rounded"></div>
                            <span class="text-sm text-gray-600">Con Error</span>
                        </div>
                        <span class="text-sm font-semibold text-gray-900">
                            {{ resumen.total_discrepancias }}
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Bank Accounts -->
        <div ref="bankAccountsSection" class="bg-white rounded-xl p-6 border border-gray-200 transition-all duration-300 hover:shadow-lg">
            <div class="mb-6">
                <h3 class="text-lg font-semibold text-gray-900">Cuentas Bancarias</h3>
                <p class="text-sm text-gray-600">Estado de sincronización y conciliación</p>
            </div>
            <div class="space-y-4">
                <div v-for="account in bankAccounts" :key="account.id" 
                     class="flex items-center justify-between p-4 bg-gray-50 rounded-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-md hover:bg-white">
                    <div class="flex-1">
                        <div class="flex items-center gap-3 mb-2">
                            <h4 class="font-semibold text-gray-900">{{ account.name }}</h4>
                            <span class="text-sm text-gray-600">{{ account.number }}</span>
                        </div>
                        <div class="flex items-center gap-4 text-sm text-gray-600">
                            <span>Saldo: {{ account.balance }}</span>
                            <span>•</span>
                            <span>Actualizado: {{ account.updated }}</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="text-right">
                            <div class="text-2xl font-bold text-gray-900">{{ account.percentage }}%</div>
                            <div class="w-32 bg-gray-200 rounded-full h-2 mt-1">
                                <div :class="account.percentage >= 90 ? 'bg-green-600' : 'bg-orange-500'" 
                                     class="h-2 rounded-full" :style="`width: ${account.percentage}%`"></div>
                            </div>
                        </div>
                        <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 text-sm">
                            Gestionar
                        </button>
                    </div>
                </div>
            </div>
        </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { apiGetDashboardResumen, apiGetBanks, apiGetHistorial } from '@/api/conciliation';
import { useNotifications } from '@/composables/useNotifications';
import { useDialogStore } from '@/store/dialog';

const { showSuccess, showError, showWarning, showInfo } = useNotifications();
const dialogStore = useDialogStore();

const loading = ref(false);
const error = ref(null);
const resumen = ref({
    total_conciliaciones: 0,
    promedio_porcentaje_conciliado: 0,
    total_transacciones_pdf: 0,
    total_transacciones_excel: 0,
    total_discrepancias: 0,
    total_pendientes_pdf: 0,
    total_pendientes_erp: 0
});

const historial = ref([]);

// Calcular pendientes totales
const pendientesTotales = computed(
    () => resumen.value.total_pendientes_pdf + resumen.value.total_pendientes_erp
);

// Calcular datos del gráfico de tendencias basados en historial real
const chartData = computed(() => {
    if (!historial.value || historial.value.length === 0) {
        // Si no hay historial, mostrar datos vacíos
        const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'];
        return meses.map((name) => ({
            name,
            conciliado: 0,
            pendiente: 100
        }));
    }
    
    // Agrupar conciliaciones por mes
    const mesesData = {};
    historial.value.forEach(item => {
        if (!item.created_at) return;
        const fecha = new Date(item.created_at);
        const mesKey = `${fecha.getFullYear()}-${fecha.getMonth()}`;
        
        if (!mesesData[mesKey]) {
            mesesData[mesKey] = {
                mes: fecha.getMonth(),
                año: fecha.getFullYear(),
                total: 0,
                conciliadas: 0
            };
        }
        
        const summary = item.summary || {};
        const total = (summary.total_transacciones_pdf || 0) + (summary.total_transacciones_excel || 0);
        const conciliadas = summary.coincidencias_encontradas || 0;
        
        mesesData[mesKey].total += total;
        mesesData[mesKey].conciliadas += conciliadas;
    });
    
    // Obtener últimos 6 meses
    const now = new Date();
    const meses = [];
    const nombresMeses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    
    for (let i = 5; i >= 0; i--) {
        const fecha = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const mesKey = `${fecha.getFullYear()}-${fecha.getMonth()}`;
        const data = mesesData[mesKey];
        
        let porcentajeConciliado = 0;
        let porcentajePendiente = 100;
        
        if (data && data.total > 0) {
            porcentajeConciliado = Math.round((data.conciliadas / data.total) * 100);
            porcentajePendiente = 100 - porcentajeConciliado;
        }
        
        meses.push({
            name: nombresMeses[fecha.getMonth()],
            conciliado: porcentajeConciliado,
            pendiente: porcentajePendiente,
            total: data ? data.total : 0,
            conciliadas: data ? data.conciliadas : 0
        });
    }
    
    return meses;
});

// Calcular porcentajes para el gráfico circular (pie chart)
const pieChartData = computed(() => {
    const conciliado = Math.round(resumen.value.promedio_porcentaje_conciliado || 0);
    const pendientePorcentaje = Math.min(100 - conciliado, 100);
    const errorPorcentaje = Math.min(
        resumen.value.total_discrepancias > 0 ? 10 : 0,
        100 - conciliado - pendientePorcentaje
    );
    
    return {
        conciliado: Math.max(0, conciliado),
        pendiente: Math.max(0, pendientePorcentaje),
        error: Math.max(0, errorPorcentaje)
    };
});

// Cuentas bancarias cargadas desde el backend
const bankAccounts = ref([]);
const loadBankAccounts = async () => {
    try {
        const { data } = await apiGetBanks();
        // Formatear bancos como cuentas bancarias
        bankAccounts.value = (data || []).map((bank, index) => ({
            id: index + 1,
            name: bank.name,
            number: '****' + (Math.floor(Math.random() * 9000) + 1000), // Temporal, se puede mejorar
            balance: 'N/A', // Se puede calcular desde transacciones si es necesario
            updated: bank.lastSync || 'N/A',
            percentage: bank.status === 'Activo' ? 100 : 0
        }));
    } catch (error) {
        console.error('Error cargando cuentas bancarias:', error);
        bankAccounts.value = [];
    }
};

const bankAccountsSection = ref(null);

const exportDashboardResumen = () => {
    const blob = new Blob([JSON.stringify(resumen.value, null, 2)], {
        type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'dashboard_resumen.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    showSuccess('Resumen del dashboard exportado correctamente.', 'Exportación Exitosa');
};

const scrollToBankAccounts = () => {
    if (bankAccountsSection.value) {
        bankAccountsSection.value.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
};

// Cargar datos desde localStorage también (para consistencia con otras pantallas)
const loadFromLocalStorage = () => {
    try {
        const savedConciliation = localStorage.getItem('bankSync_last_conciliation');
        if (savedConciliation) {
            const parsedData = JSON.parse(savedConciliation);
            const summary = parsedData.summary || {};
            
            // Actualizar resumen con datos locales si no hay datos del backend
            if (resumen.value.total_conciliaciones === 0) {
                resumen.value = {
                    total_conciliaciones: 1,
                    promedio_porcentaje_conciliado: summary.porcentaje_conciliado || 0,
                    total_transacciones_pdf: summary.total_transacciones_pdf || 0,
                    total_transacciones_excel: summary.total_transacciones_excel || 0,
                    total_discrepancias: summary.discrepancies || 0,
                    total_pendientes_pdf: summary.transacciones_sin_match_pdf || 0,
                    total_pendientes_erp: summary.transacciones_sin_match_excel || 0
                };
                
                // Agregar al historial para el gráfico
                historial.value = [{
                    id: parsedData.reconciliation_id || 'local',
                    created_at: new Date().toISOString(),
                    summary: summary
                }];
            }
        }
    } catch (e) {
        console.warn('Error cargando datos desde localStorage:', e);
    }
};

const loadDashboardData = async () => {
    loading.value = true;
    error.value = null;
    
    // Primero cargar desde localStorage (rápido)
    loadFromLocalStorage();
    
    // Luego cargar desde el backend
    try {
        const [resumenData, historialData] = await Promise.all([
            apiGetDashboardResumen().catch(() => ({ data: resumen.value })),
            apiGetHistorial().catch(() => ({ data: [] }))
        ]);
        
        // Actualizar resumen solo si hay datos del backend
        if (resumenData && resumenData.data && resumenData.data.total_conciliaciones > 0) {
            resumen.value = resumenData.data;
        }
        
        // Actualizar historial
        if (historialData && historialData.data && Array.isArray(historialData.data)) {
            historial.value = historialData.data;
        }
    } catch (e) {
        console.error('Error cargando datos del dashboard:', e);
        // No mostrar error si hay datos locales, solo loguear
        if (resumen.value.total_conciliaciones === 0) {
            error.value = 'No se pudo cargar el resumen de conciliaciones';
            // No mostrar warning si simplemente no hay datos
        }
    } finally {
        loading.value = false;
    }
};

onMounted(async () => {
    // Limpiar alertas persistentes al cargar
    dialogStore.reset();
    
    await Promise.all([
        loadDashboardData(),
        loadBankAccounts()
    ]);
});
</script>
