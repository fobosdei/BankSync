<template>
    <div>
        <!-- Header -->
        <header class="bg-white border-b border-gray-200 px-8 py-6">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">Reglas de IA y Automatización</h1>
                    <p class="text-sm text-gray-600 mt-1">Configura las reglas que el motor de IA usa para conciliar automáticamente</p>
                </div>
                <div class="flex items-center gap-3">
                    <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                        </svg>
                        Entrenar modelo
                    </button>
                    <button class="px-4 py-2 text-white bg-purple-600 rounded-lg hover:bg-purple-700 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                        </svg>
                        Nueva regla
                    </button>
                </div>
            </div>
        </header>

        <div class="p-8">
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <div class="flex items-center justify-between mb-2">
                        <p class="text-sm text-gray-600">Precisión Global</p>
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                        </svg>
                    </div>
                    <p class="text-3xl font-bold text-gray-900">94.5%</p>
                    <p class="text-xs text-green-600 font-medium mt-1">+2.3% vs mes anterior</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <div class="flex items-center justify-between mb-2">
                        <p class="text-sm text-gray-600">Tasa de Recall</p>
                        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <p class="text-3xl font-bold text-gray-900">92.8%</p>
                    <p class="text-xs text-green-600 font-medium mt-1">+1.8% vs mes anterior</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <div class="flex items-center justify-between mb-2">
                        <p class="text-sm text-gray-600">Reglas Activas</p>
                        <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                    </div>
                    <p class="text-3xl font-bold text-gray-900">28 de 32</p>
                    <p class="text-xs text-gray-600 mt-1">87.5% activas</p>
                    <p class="text-xs text-orange-600 font-medium">4 reglas en prueba</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <div class="flex items-center justify-between mb-2">
                        <p class="text-sm text-gray-600">Auto-conciliaciones</p>
                        <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                    </div>
                    <p class="text-3xl font-bold text-gray-900">2,847</p>
                    <p class="text-xs text-gray-600 mt-1">Este mes</p>
                    <p class="text-xs text-green-600 font-medium">↑ 34% vs anterior</p>
                </div>
            </div>

            <!-- Chart -->
            <div class="bg-white rounded-xl border border-gray-200 p-6 mb-8">
                <div class="mb-6">
                    <h3 class="text-lg font-semibold text-gray-900">Evolución del Modelo de IA</h3>
                    <p class="text-sm text-gray-600">Precisión y recall en los últimos 6 meses</p>
                </div>
                <div class="relative h-64 border-l border-b border-gray-200">
                    <!-- Y-axis labels -->
                    <div class="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-500 pr-2" style="width: 40px;">
                        <span>100</span>
                        <span>95</span>
                        <span>90</span>
                        <span>85</span>
                        <span>80</span>
                    </div>
                    
                    <!-- Chart area -->
                    <div class="ml-10 h-full flex items-end justify-around px-4">
                        <div v-for="month in chartData" :key="month.name" class="flex flex-col items-center gap-2 flex-1">
                            <div class="w-full flex justify-center items-end gap-1" style="height: 200px;">
                                <div class="w-3 bg-green-500 rounded-t" :style="`height: ${(month.precision - 80) * 10}px`"></div>
                                <div class="w-3 bg-blue-500 rounded-t" :style="`height: ${(month.recall - 80) * 10}px`"></div>
                            </div>
                            <span class="text-xs text-gray-600">{{ month.name }}</span>
                        </div>
                    </div>
                </div>
                <div class="flex items-center justify-center gap-6 mt-6">
                    <div class="flex items-center gap-2">
                        <div class="w-3 h-3 bg-green-500 rounded"></div>
                        <span class="text-sm text-gray-600">Precisión %</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <div class="w-3 h-3 bg-blue-500 rounded"></div>
                        <span class="text-sm text-gray-600">Recall %</span>
                    </div>
                </div>
            </div>

            <!-- Rules Table -->
            <div class="bg-white rounded-xl border border-gray-200 mb-8">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Reglas Configuradas</h3>
                    <p class="text-sm text-gray-600">Gestiona las reglas de automatización y sus prioridades</p>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead class="bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Prioridad</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Condición</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acción</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Aciertos</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Aplicaciones</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr v-for="rule in rules" :key="rule.id" class="hover:bg-gray-50">
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ rule.priority }}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ rule.name }}</td>
                                <td class="px-6 py-4 text-sm text-gray-600">{{ rule.condition }}</td>
                                <td class="px-6 py-4 text-sm text-gray-600">{{ rule.action }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center gap-2">
                                        <div class="flex-1 bg-gray-200 rounded-full h-2 w-20">
                                            <div class="bg-gray-900 h-2 rounded-full" :style="`width: ${rule.accuracy}%`"></div>
                                        </div>
                                        <span class="text-sm font-medium text-gray-900">{{ rule.accuracy }}%</span>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="px-2 py-1 bg-gray-900 text-white text-xs font-medium rounded-full">
                                        {{ rule.applications }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" :checked="rule.active" class="sr-only peer">
                                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
                                        <span class="ml-3 text-sm font-medium" :class="rule.active ? 'text-green-600' : 'text-gray-400'">
                                            {{ rule.active ? 'Activa' : 'Inactiva' }}
                                        </span>
                                    </label>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm">
                                    <div class="flex items-center gap-2">
                                        <button class="text-blue-600 hover:text-blue-700">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                            </svg>
                                        </button>
                                        <button class="text-gray-600 hover:text-gray-700">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                            </svg>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Bottom Section -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Model Training -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <div class="flex items-start gap-3 mb-6">
                        <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                            </svg>
                        </div>
                        <div class="flex-1">
                            <h3 class="text-lg font-semibold text-gray-900">Entrenamiento del Modelo</h3>
                            <p class="text-sm text-gray-600 mt-1">Mejora la precisión con nuevos datos</p>
                        </div>
                    </div>
                    
                    <div class="space-y-4">
                        <div class="p-4 bg-purple-50 rounded-lg">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-sm font-medium text-purple-900">Estado del modelo</span>
                                <span class="text-xs text-purple-600">Última actualización: Hace 2 días</span>
                            </div>
                            <p class="text-sm text-purple-800">Datos de entrenamiento: 15,847 transacciones</p>
                        </div>
                        <button class="w-full px-4 py-3 text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                            Entrenar con datos recientes
                        </button>
                    </div>
                </div>

                <!-- Performance by Category -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Rendimiento por Categoría</h3>
                    <p class="text-sm text-gray-600 mb-6">Precisión por tipo de transacción</p>
                    
                    <div class="space-y-4">
                        <div v-for="cat in categories" :key="cat.name" class="flex items-center justify-between">
                            <div class="flex-1">
                                <div class="flex items-center justify-between mb-1">
                                    <span class="text-sm font-medium text-gray-900">{{ cat.name }}</span>
                                    <span class="text-sm font-bold text-green-600">{{ cat.accuracy }}%</span>
                                </div>
                                <p class="text-xs text-gray-600">{{ cat.cases }} casos</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const chartData = ref([
    { name: 'Ene', precision: 85, recall: 83 },
    { name: 'Feb', precision: 87, recall: 85 },
    { name: 'Mar', precision: 90, recall: 88 },
    { name: 'Abr', precision: 92, recall: 90 },
    { name: 'May', precision: 93, recall: 91 },
    { name: 'Jun', precision: 95, recall: 93 }
]);

const rules = ref([
    { id: 1, priority: 1, name: 'Nómina mensual', condition: 'Descripción contiene "Nómina" Y Monto > $15,000,000', action: 'Auto-conciliar con cuenta 5105', accuracy: 98, applications: 124, active: true },
    { id: 2, priority: 2, name: 'Pagos proveedores', condition: 'Descripción contiene "Proveedor" O "Pago factura" Sugerir cuenta 2205 y marcar para revisión', action: '', accuracy: 94, applications: 189, active: true },
    { id: 3, priority: 3, name: 'Ingresos por ventas', condition: 'Tipo = Crédito Y Monto > $1,000,000', action: 'Clasificar como "Ventas" y auto-conciliar', accuracy: 91, applications: 287, active: true },
    { id: 4, priority: 4, name: 'Comisiones bancarias', condition: 'Descripción contiene "Comisión" Y Monto < $100,000', action: 'Auto-conciliar con cuenta 5305', accuracy: 99, applications: 52, active: true },
    { id: 5, priority: 5, name: 'Servicios públicos', condition: 'Descripción = "Energía" O "Agua" O "Gas"', action: 'Categorizar como gastos servicios', accuracy: 96, applications: 38, active: true },
    { id: 6, priority: 6, name: 'Arrendamiento', condition: 'Descripción = "Pago arrendamiento" Y Día = 10', action: 'Auto-conciliar con cuenta 5120', accuracy: 100, applications: 12, active: false }
]);

const categories = ref([
    { name: 'Nómina', accuracy: 98, cases: '124 casos' },
    { name: 'Pagos de personal', accuracy: 94, cases: '89 casos' },
    { name: 'Proveedores', accuracy: 94, cases: '156 casos' }
]);
</script>
