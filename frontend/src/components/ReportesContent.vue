<template>
    <div>
        <!-- Header -->
        <header class="bg-white border-b border-gray-200 px-8 py-6">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">Reportes y Auditorías</h1>
                    <p class="text-sm text-gray-600 mt-1">Genera informes financieros y revisa el historial de acciones</p>
                </div>
                <div class="flex items-center gap-3">
                    <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        Seleccionar periodo
                    </button>
                    <button class="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Generar reporte
                    </button>
                </div>
            </div>
        </header>

        <div class="p-8">
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Tasa de Automatización</p>
                    <p class="text-3xl font-bold text-gray-900">87%</p>
                    <p class="text-xs text-gray-600 mt-1">Matches automáticos</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Tiempo Promedio</p>
                    <p class="text-3xl font-bold text-gray-900">2.3 min</p>
                    <p class="text-xs text-gray-600 mt-1">Por conciliación</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Errores Corregidos</p>
                    <p class="text-3xl font-bold text-gray-900">34</p>
                    <p class="text-xs text-gray-600 mt-1">Este mes</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Ajustes Generados</p>
                    <p class="text-3xl font-bold text-gray-900">156</p>
                    <p class="text-xs text-gray-600 mt-1">Asientos contables</p>
                </div>
            </div>

            <!-- Tabs -->
            <div class="bg-white rounded-xl border border-gray-200 mb-8">
                <div class="border-b border-gray-200">
                    <nav class="flex -mb-px">
                        <button 
                            v-for="tab in tabs" 
                            :key="tab.id"
                            @click="activeTab = tab.id"
                            :class="activeTab === tab.id ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
                            class="px-6 py-4 border-b-2 font-medium text-sm transition-colors"
                        >
                            {{ tab.name }}
                        </button>
                    </nav>
                </div>

                <!-- Reports Tab -->
                <div v-if="activeTab === 'reportes'" class="p-6">
                    <div class="mb-6">
                        <h3 class="text-lg font-semibold text-gray-900">Reportes Disponibles</h3>
                        <p class="text-sm text-gray-600">Genera y descarga informes financieros</p>
                    </div>

                    <div class="flex items-center justify-between mb-4">
                        <div class="relative flex-1 max-w-md">
                            <input 
                                type="text" 
                                placeholder="Buscar reportes..."
                                class="w-full pl-4 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            >
                        </div>
                        <div class="flex items-center gap-3">
                            <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                                <option>Tipo</option>
                                <option>Mensual</option>
                                <option>Trimestral</option>
                                <option>Anual</option>
                            </select>
                            <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                                </svg>
                                Filtrar
                            </button>
                        </div>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gray-50 border-b border-gray-200">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre del Reporte</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Periodo</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha Generación</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Registros</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Conciliadas</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr v-for="report in reports" :key="report.id" class="hover:bg-gray-50">
                                    <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ report.name }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ report.type }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ report.period }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ report.date }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ report.records }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">{{ report.reconciled }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                                            {{ report.status }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm">
                                        <div class="flex items-center gap-2">
                                            <button class="text-gray-600 hover:text-gray-700">
                                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                                </svg>
                                            </button>
                                            <button class="text-blue-600 hover:text-blue-700">
                                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                                </svg>
                                            </button>
                                            <button class="text-green-600 hover:text-green-700">
                                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                                </svg>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Audits Tab -->
                <div v-if="activeTab === 'auditorias'" class="p-6">
                    <p class="text-gray-600">Vista de auditorías - En desarrollo</p>
                </div>

                <!-- Statistics Tab -->
                <div v-if="activeTab === 'estadisticas'" class="p-6">
                    <p class="text-gray-600">Vista de estadísticas - En desarrollo</p>
                </div>
            </div>

            <!-- Report Templates -->
            <div class="mb-8">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Plantillas de Reportes</h3>
                <p class="text-sm text-gray-600 mb-6">Genera reportes personalizados</p>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div v-for="template in templates" :key="template.id" class="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-shadow">
                        <div class="flex items-start gap-4 mb-4">
                            <div :class="`w-12 h-12 ${template.color} rounded-lg flex items-center justify-center`">
                                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                            <div class="flex-1">
                                <h4 class="font-semibold text-gray-900 mb-1">{{ template.name }}</h4>
                                <p class="text-sm text-gray-600">{{ template.description }}</p>
                            </div>
                        </div>
                        <button class="w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                            </svg>
                            Generar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const activeTab = ref('reportes');

const tabs = ref([
    { id: 'reportes', name: 'Reportes' },
    { id: 'auditorias', name: 'Auditorías' },
    { id: 'estadisticas', name: 'Estadísticas' }
]);

const reports = ref([
    { id: 1, name: 'Conciliaciones Octubre 2025', type: 'Mensual', period: 'Octubre 2025', date: '2025-10-13', records: 847, reconciled: 738, status: 'Completado' },
    { id: 2, name: 'Transacciones no conciliadas Q3', type: 'Trimestral', period: 'Q3 2025', date: '2025-10-01', records: 124, reconciled: 0, status: 'Completado' },
    { id: 3, name: 'Ajustes contables Septiembre', type: 'Ajustes', period: 'Septiembre 2025', date: '2025-09-30', records: 23, reconciled: 23, status: 'Completado' },
    { id: 4, name: 'Auditoría anual 2024', type: 'Auditoría', period: 'Año 2024', date: '2025-01-15', records: 9847, reconciled: 9734, status: 'Completado' }
]);

const templates = ref([
    { id: 1, name: 'Conciliación Mensual', description: 'Resumen completo de conciliaciones del mes', color: 'bg-blue-600' },
    { id: 2, name: 'Transacciones Pendientes', description: 'Lista de transacciones sin conciliar', color: 'bg-green-600' },
    { id: 3, name: 'Ajustes Contables', description: 'Asientos de ajuste generados', color: 'bg-purple-600' }
]);
</script>
