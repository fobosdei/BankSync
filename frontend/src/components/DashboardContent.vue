<template>
    <div>
        <!-- Header -->
        <header class="bg-white border-b border-gray-200 px-8 py-6">
            <div class="flex items-center justify-end gap-3">
                <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                    Exportar
                </button>
                <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                    Importar extracto
                </button>
                <button class="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 flex items-center gap-2">
                    Nueva conciliación
                </button>
            </div>
        </header>

        <div class="p-8">
        <!-- Stats Cards -->
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Card 1 -->
            <div class="bg-white rounded-xl p-6 border border-gray-200">
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
                <p class="text-xs text-green-600 font-medium">+5% vs mes anterior</p>
            </div>

            <!-- Card 2 -->
            <div class="bg-white rounded-xl p-6 border border-gray-200">
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
            <div class="bg-white rounded-xl p-6 border border-gray-200">
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
                <a href="#" class="text-xs text-blue-600 font-medium hover:underline">Ver detalles →</a>
            </div>

            <!-- Card 4 -->
            <div class="bg-white rounded-xl p-6 border border-gray-200">
                <div class="flex items-start justify-between mb-4">
                    <div>
                        <p class="text-sm text-gray-600 mb-1">Precisión IA</p>
                        <h3 class="text-3xl font-bold text-gray-900">
                            {{ Math.round(resumen.promedio_porcentaje_conciliado || 0) }}%
                        </h3>
                    </div>
                    <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                        ⚡
                    </div>
                </div>
                <p class="text-sm text-gray-600 mb-2">Matches automáticos</p>
                <p class="text-xs text-green-600 font-medium">+2.3% esta semana</p>
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
                <div class="h-64 flex items-end justify-between gap-4">
                    <div v-for="month in chartData" :key="month.name" class="flex-1 flex flex-col items-center gap-2">
                        <div class="w-full bg-green-500 rounded-t-lg" :style="`height: ${month.conciliado}%`"></div>
                        <div class="w-full bg-orange-400 rounded-t-lg" :style="`height: ${month.pendiente}%`"></div>
                        <span class="text-xs text-gray-600">{{ month.name }}</span>
                    </div>
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
            <div class="bg-white rounded-xl p-6 border border-gray-200">
                <div class="mb-6">
                    <h3 class="text-lg font-semibold text-gray-900">Estado Global</h3>
                    <p class="text-sm text-gray-600">Distribución actual</p>
                </div>
                <div class="flex items-center justify-center h-64">
                    <div class="relative w-48 h-48 rounded-full bg-gradient-to-br from-green-500 via-orange-400 to-red-500"></div>
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
        <div class="bg-white rounded-xl p-6 border border-gray-200">
            <div class="mb-6">
                <h3 class="text-lg font-semibold text-gray-900">Cuentas Bancarias</h3>
                <p class="text-sm text-gray-600">Estado de sincronización y conciliación</p>
            </div>
            <div class="space-y-4">
                <div v-for="account in bankAccounts" :key="account.id" 
                     class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
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
import { ref, computed, onMounted } from 'vue';
import { apiGetDashboardResumen } from '@/api/conciliation';

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

const pendientesTotales = computed(
    () => resumen.value.total_pendientes_pdf + resumen.value.total_pendientes_erp
);

const chartData = computed(() => {
    const base = Math.round(resumen.value.promedio_porcentaje_conciliado || 0);
    const pendiente = 100 - base;
    const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'];
    return meses.map((name) => ({
        name,
        conciliado: base,
        pendiente
    }));
});

// De momento las cuentas bancarias son estáticas; más adelante se pueden
// alimentar desde Supabase cuando exista el modelo correspondiente.
const bankAccounts = ref([
    {
        id: 1,
        name: 'Banco Nacional - Cuenta Corriente',
        number: '****4321',
        balance: '$1,250,000',
        updated: 'Hoy 08:30',
        percentage: 95
    },
    {
        id: 2,
        name: 'Banco del País - Ahorros',
        number: '****7832',
        balance: '$850,000',
        updated: 'Hoy 08:45',
        percentage: 100
    },
    {
        id: 3,
        name: 'Banco Internacional - USD',
        number: '****2109',
        balance: '$2,100,000',
        updated: 'Ayer 16:20',
        percentage: 78
    },
    {
        id: 4,
        name: 'Banco Digital - Nómina',
        number: '****9854',
        balance: '$3,450,000',
        updated: 'Hoy 09:15',
        percentage: 93
    }
]);

onMounted(async () => {
    loading.value = true;
    error.value = null;
    try {
        const { data } = await apiGetDashboardResumen();
        resumen.value = data;
    } catch (e) {
        console.error('Error cargando resumen de dashboard:', e);
        error.value = 'No se pudo cargar el resumen de conciliaciones';
    } finally {
        loading.value = false;
    }
});
</script>
