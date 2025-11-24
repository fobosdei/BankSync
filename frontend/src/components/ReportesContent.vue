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
                    <button
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
                        @click="showPeriodModal = true"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        Seleccionar periodo
                    </button>
                    <button
                        class="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 flex items-center gap-2"
                        @click="handleGenerateReport"
                    >
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
                    <p class="text-3xl font-bold text-gray-900">{{ Math.round(dashboardStats.promedio_porcentaje_conciliado || 0) }}%</p>
                    <p class="text-xs text-gray-600 mt-1">Matches automáticos</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Tiempo Promedio</p>
                    <p class="text-3xl font-bold text-gray-900">2.3 min</p>
                    <p class="text-xs text-gray-600 mt-1">Por conciliación</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Errores Corregidos</p>
                    <p class="text-3xl font-bold text-gray-900">{{ dashboardStats.total_discrepancias || 0 }}</p>
                    <p class="text-xs text-gray-600 mt-1">Este mes</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Ajustes Generados</p>
                    <p class="text-3xl font-bold text-gray-900">{{ dashboardStats.total_pendientes_erp || 0 }}</p>
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
                                v-model="searchQuery"
                                type="text" 
                                placeholder="Buscar reportes..."
                                class="w-full pl-4 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            >
                        </div>
                        <div class="flex items-center gap-3">
                            <select
                                v-model="typeFilter"
                                class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            >
                                <option value="">Tipo</option>
                                <option value="Mensual">Mensual</option>
                                <option value="Trimestral">Trimestral</option>
                                <option value="Anual">Anual</option>
                            </select>
                            <button
                                class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
                                @click="resetFilters"
                            >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                                </svg>
                                Filtrar
                            </button>
                        </div>
                    </div>

                    <div v-if="loading" class="text-center py-12">
                        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                        <p class="mt-4 text-gray-600">Cargando reportes...</p>
                    </div>
                    <div v-else-if="filteredReports.length === 0" class="text-center py-12">
                        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <p class="mt-4 text-gray-600">No hay reportes disponibles</p>
                        <p class="text-sm text-gray-500 mt-2">Realiza conciliaciones para generar reportes</p>
                    </div>
                    <div v-else class="overflow-x-auto">
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
                                <tr v-for="report in filteredReports" :key="report.id" class="hover:bg-gray-50">
                                    <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ report.name }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ report.type }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ report.period }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ formatDate(report.date) }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ report.records }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">{{ report.reconciled }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span :class="getStatusClass(report.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                                            {{ report.status }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm">
                                        <div class="flex items-center gap-2">
                                            <button class="text-gray-600 hover:text-gray-700" @click="openReportDetails(report)" title="Ver detalles">
                                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                                </svg>
                                            </button>
                                            <button class="text-blue-600 hover:text-blue-700" @click="downloadSingleReport(report)" title="Descargar CSV">
                                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                                                </svg>
                                            </button>
                                            <button class="text-green-600 hover:text-green-700" @click="exportReportJson(report)" title="Descargar JSON">
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
                        <button
                            class="w-full px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
                            @click="generateFromTemplate(template)"
                        >
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

    <!-- Modal seleccionar periodo -->
    <div
        v-if="showPeriodModal"
        class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
        @click.self="showPeriodModal = false"
    >
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-md p-6 space-y-4">
            <div class="flex items-center justify-between mb-2">
                <h3 class="text-lg font-semibold text-gray-900">Seleccionar periodo</h3>
                <button class="text-gray-400 hover:text-gray-600" @click="showPeriodModal = false">✕</button>
            </div>

            <div class="space-y-4 text-sm">
                <div class="space-y-1">
                    <label class="font-medium text-gray-700">Desde</label>
                    <input
                        v-model="dateFrom"
                        type="date"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                </div>
                <div class="space-y-1">
                    <label class="font-medium text-gray-700">Hasta</label>
                    <input
                        v-model="dateTo"
                        type="date"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                </div>
            </div>

            <div class="flex justify-end gap-2 mt-4">
                <button
                    class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm"
                    @click="clearPeriod"
                >
                    Limpiar
                </button>
                <button
                    class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
                    @click="applyPeriodFilter"
                >
                    Aplicar
                </button>
            </div>
        </div>
    </div>

    <!-- Modal detalle de reporte -->
    <div
        v-if="showReportModal && selectedReport"
        class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
        @click.self="showReportModal = false"
    >
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-lg p-6 space-y-4">
            <div class="flex items-center justify-between mb-2">
                <h3 class="text-lg font-semibold text-gray-900">Detalle de reporte</h3>
                <button class="text-gray-400 hover:text-gray-600" @click="showReportModal = false">✕</button>
            </div>

            <div class="space-y-2 text-sm text-gray-800">
                <p><span class="font-semibold">Nombre:</span> {{ selectedReport.name }}</p>
                <p><span class="font-semibold">Tipo:</span> {{ selectedReport.type }}</p>
                <p><span class="font-semibold">Periodo:</span> {{ selectedReport.period }}</p>
                <p><span class="font-semibold">Fecha generación:</span> {{ selectedReport.date }}</p>
                <p><span class="font-semibold">Registros:</span> {{ selectedReport.records }}</p>
                <p><span class="font-semibold">Conciliadas:</span> {{ selectedReport.reconciled }}</p>
                <p><span class="font-semibold">Estado:</span> {{ selectedReport.status }}</p>
            </div>

            <div class="flex justify-end gap-2 mt-4">
                <button
                    class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm"
                    @click="showReportModal = false"
                >
                    Cerrar
                </button>
                <button
                    class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
                    @click="downloadSingleReport(selectedReport)"
                >
                    Descargar CSV
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { apiGetHistorial, apiGetDashboardResumen } from '@/api/conciliation';
import { useNotifications } from '@/composables/useNotifications';

const { showSuccess, showError, showWarning, showInfo } = useNotifications();

const activeTab = ref('reportes');

const tabs = ref([
    { id: 'reportes', name: 'Reportes' },
    { id: 'auditorias', name: 'Auditorías' },
    { id: 'estadisticas', name: 'Estadísticas' }
]);

const loading = ref(false);
const error = ref(null);
const reports = ref([]);
const dashboardStats = ref({
    total_conciliaciones: 0,
    promedio_porcentaje_conciliado: 0,
    total_transacciones_pdf: 0,
    total_transacciones_excel: 0,
    total_discrepancias: 0,
    total_pendientes_pdf: 0,
    total_pendientes_erp: 0
});

// filtros y estado de UI
const searchQuery = ref('');
const typeFilter = ref('');
const dateFrom = ref('');
const dateTo = ref('');
const showPeriodModal = ref(false);
const showReportModal = ref(false);
const selectedReport = ref(null);

const templates = ref([
    { id: 1, name: 'Conciliación Mensual', description: 'Resumen completo de conciliaciones del mes', color: 'bg-blue-600' },
    { id: 2, name: 'Transacciones Pendientes', description: 'Lista de transacciones sin conciliar', color: 'bg-green-600' },
    { id: 3, name: 'Ajustes Contables', description: 'Asientos de ajuste generados', color: 'bg-purple-600' }
]);

const filteredReports = computed(() => {
    return reports.value.filter((r) => {
        const matchSearch =
            !searchQuery.value ||
            r.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            r.period.toLowerCase().includes(searchQuery.value.toLowerCase());

        const matchType = !typeFilter.value || r.type === typeFilter.value;

        let matchDate = true;
        if (dateFrom.value) matchDate = matchDate && r.date >= dateFrom.value;
        if (dateTo.value) matchDate = matchDate && r.date <= dateTo.value;

        return matchSearch && matchType && matchDate;
    });
});

const mapHistorialToReports = (items) => {
    return items.map((item) => {
        const summary = item.summary || {};
        const total =
            (summary.total_transacciones_pdf || 0) +
            (summary.total_transacciones_excel || 0);
        const conciliadas = summary.coincidencias_encontradas || 0;

        const created = item.created_at ? new Date(item.created_at) : null;
        const dateStr = created
            ? created.toISOString().slice(0, 10)
            : '';

        const periodStr = created
            ? created.toLocaleDateString('es-CO', {
                  year: 'numeric',
                  month: 'long'
              })
            : 'N/A';

        return {
            id: item.id,
            name: item.name,
            type: 'Conciliación',
            period: periodStr,
            date: dateStr,
            records: total,
            reconciled: conciliadas,
            status: item.status || 'Completado'
        };
    });
};

const resetFilters = () => {
    searchQuery.value = '';
    typeFilter.value = '';
    dateFrom.value = '';
    dateTo.value = '';
};

const clearPeriod = () => {
    dateFrom.value = '';
    dateTo.value = '';
};

const openReportDetails = (report) => {
    selectedReport.value = { ...report };
    showReportModal.value = true;
};

const buildCsvFromReports = (list) => {
    if (!list || list.length === 0) return '';
    
    // Obtener los headers desde el primer objeto o usar los predeterminados
    const firstItem = list[0];
    const headers = Object.keys(firstItem);
    const headerRow = headers.join(',');
    
    const rows = list.map((r) => {
        return headers.map(h => {
            let value = r[h] || '';
            // Escapar comillas y envolver en comillas si contiene coma
            if (typeof value === 'string') {
                value = value.replace(/"/g, '""');
                if (value.includes(',') || value.includes('"') || value.includes('\n')) {
                    value = `"${value}"`;
                }
            }
            return value;
        }).join(',');
    });
    
    return [headerRow, ...rows].join('\n');
};

const triggerDownload = (csv, filename) => {
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
};

const exportFilteredReports = () => {
    const data = filteredReports.value;
    
    // Si no hay reportes filtrados, intentar generar desde las conciliaciones guardadas
    if (!data.length) {
        // Intentar generar reporte desde localStorage
        try {
            const savedConciliation = localStorage.getItem('bankSync_last_conciliation');
            if (savedConciliation) {
                const parsedData = JSON.parse(savedConciliation);
                generateReportFromConciliation(parsedData, 'reporte_general');
                return;
            }
        } catch (e) {
            console.warn('Error generando reporte desde localStorage:', e);
        }
        
        showWarning('No hay reportes para exportar con los filtros actuales. Realiza una conciliación primero.', 'Sin Datos');
        return;
    }
    
    // Generar reporte detallado desde los datos de las conciliaciones
    const detailedReport = generateDetailedReport(data);
    
    // Generar nombre de archivo con periodo si está filtrado
    let filename = 'reportes_conciliacion';
    if (dateFrom.value || dateTo.value) {
        const fromStr = dateFrom.value ? dateFrom.value.replace(/-/g, '') : 'inicio';
        const toStr = dateTo.value ? dateTo.value.replace(/-/g, '') : 'hoy';
        filename = `reportes_conciliacion_${fromStr}_${toStr}`;
    } else {
        filename = `reportes_conciliacion_${new Date().toISOString().slice(0, 10).replace(/-/g, '')}`;
    }
    
    const csv = buildCsvFromReports(detailedReport);
    triggerDownload(csv, `${filename}.csv`);
    showSuccess(`Se exportaron ${data.length} reporte(s) correctamente.`, 'Exportación Exitosa');
};

// Generar reporte detallado desde los datos de conciliaciones
const generateDetailedReport = (reports) => {
    const detailedReports = [];
    
    for (const report of reports) {
        // Si tiene rawData (datos completos de conciliación), usar esos
        if (report.rawData) {
            const summary = report.rawData.summary || {};
            detailedReports.push({
                id: report.id,
                nombre: report.name,
                tipo: report.type,
                periodo: report.period,
                fecha: report.date,
                total_registros: report.records,
                conciliadas: report.reconciled,
                pendientes_pdf: summary.transacciones_sin_match_pdf || 0,
                pendientes_erp: summary.transacciones_sin_match_excel || 0,
                discrepancias: summary.discrepancies || 0,
                porcentaje_conciliado: summary.porcentaje_conciliado || 0,
                estado: report.status
            });
        } else {
            // Usar datos básicos del reporte
            detailedReports.push({
                id: report.id,
                nombre: report.name,
                tipo: report.type,
                periodo: report.period,
                fecha: report.date,
                total_registros: report.records,
                conciliadas: report.reconciled,
                pendientes: report.records - report.reconciled,
                porcentaje: report.records > 0 ? Math.round((report.reconciled / report.records) * 100) : 0,
                estado: report.status
            });
        }
    }
    
    return detailedReports;
};

// Generar reporte completo desde una conciliación guardada
const generateReportFromConciliation = (conciliationData, reportType = 'general') => {
    if (!conciliationData || !conciliationData.summary) {
        showWarning('No hay datos de conciliación para generar el reporte.', 'Sin Datos');
        return;
    }
    
    const summary = conciliationData.summary || {};
    const now = new Date();
    const filename = `reporte_conciliacion_${now.toISOString().slice(0, 10).replace(/-/g, '')}.csv`;
    
    // Crear reporte detallado
    const reportData = [{
        fecha: now.toISOString().slice(0, 10),
        nombre: `Conciliación ${now.toLocaleDateString('es-CO')}`,
        total_registros: (summary.total_transacciones_pdf || 0) + (summary.total_transacciones_excel || 0),
        conciliadas: summary.coincidencias_encontradas || 0,
        pendientes_pdf: summary.transacciones_sin_match_pdf || 0,
        pendientes_erp: summary.transacciones_sin_match_excel || 0,
        discrepancias: summary.discrepancies || 0,
        porcentaje_conciliado: summary.porcentaje_conciliado || 0
    }];
    
    const csv = buildCsvFromReports(reportData);
    triggerDownload(csv, filename);
    showSuccess('Reporte generado correctamente desde la conciliación actual.', 'Reporte Generado');
};

// Manejar el botón "Generar reporte"
const handleGenerateReport = () => {
    // Si hay reportes filtrados, exportarlos
    if (filteredReports.value.length > 0) {
        exportFilteredReports();
        return;
    }
    
    // Si no hay reportes, intentar generar desde la conciliación guardada
    try {
        const savedConciliation = localStorage.getItem('bankSync_last_conciliation');
        if (savedConciliation) {
            const parsedData = JSON.parse(savedConciliation);
            generateReportFromConciliation(parsedData, 'reporte_general');
            return;
        }
    } catch (e) {
        console.warn('Error generando reporte desde localStorage:', e);
    }
    
    // Si no hay nada, mostrar mensaje
    showWarning('No hay conciliaciones disponibles para generar el reporte. Realiza una conciliación primero.', 'Sin Datos');
};

const applyPeriodFilter = () => {
    showPeriodModal.value = false;
    // Los filtros ya están aplicados por el computed filteredReports
    // Solo cerramos el modal
    showInfo('Filtro de periodo aplicado. Los reportes se han filtrado según el rango seleccionado.', 'Filtro Aplicado');
};

const downloadSingleReport = (report) => {
    if (!report) return;
    const csv = buildCsvFromReports([report]);
    triggerDownload(csv, `reporte_${report.id}.csv`);
    showSuccess('Reporte descargado correctamente.', 'Descarga Exitosa');
};

const exportReportJson = (report) => {
    if (!report) return;
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `reporte_${report.id}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    showSuccess('Reporte JSON descargado correctamente.', 'Descarga Exitosa');
};

const generateFromTemplate = (template) => {
    // Generar reporte basado en la plantilla seleccionada
    const filteredData = filteredReports.value;
    
    if (!filteredData.length) {
        showWarning('No hay reportes disponibles para generar desde esta plantilla.', 'Sin Datos');
        return;
    }
    
    let reportData = [];
    const periodStr = dateFrom.value && dateTo.value 
        ? `${dateFrom.value} - ${dateTo.value}`
        : 'Período completo';
    
    switch (template.id) {
        case 1: // Conciliación Mensual
            reportData = filteredData.map(r => ({
                nombre: r.name,
                periodo: r.period,
                fecha: r.date,
                total_registros: r.records,
                conciliadas: r.reconciled,
                pendientes: r.records - r.reconciled,
                porcentaje: r.records > 0 ? Math.round((r.reconciled / r.records) * 100) : 0
            }));
            break;
        case 2: // Transacciones Pendientes
            reportData = filteredData.filter(r => r.records - r.reconciled > 0).map(r => ({
                nombre: r.name,
                periodo: r.period,
                fecha: r.date,
                pendientes: r.records - r.reconciled,
                conciliadas: r.reconciled
            }));
            break;
        case 3: // Ajustes Contables
            reportData = filteredData.map(r => ({
                nombre: r.name,
                periodo: r.period,
                fecha: r.date,
                total_registros: r.records,
                ajustes_necesarios: r.records - r.reconciled,
                estado: r.status
            }));
            break;
    }
    
    if (!reportData.length) {
        showWarning('No hay datos para generar este tipo de reporte.', 'Sin Datos');
        return;
    }
    
    const csv = buildCsvFromReports(reportData);
    const filename = `${template.name.toLowerCase().replace(/\s+/g, '_')}_${periodStr.replace(/\s+/g, '_')}.csv`;
    triggerDownload(csv, filename);
    showSuccess(`Reporte "${template.name}" generado correctamente.`, 'Reporte Generado');
};

const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleDateString('es-CO', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
};

const getStatusClass = (status) => {
    const statusLower = (status || '').toLowerCase();
    if (statusLower.includes('completado') || statusLower.includes('completada')) {
        return 'bg-green-100 text-green-800';
    } else if (statusLower.includes('proceso') || statusLower.includes('procesando')) {
        return 'bg-yellow-100 text-yellow-800';
    } else if (statusLower.includes('error') || statusLower.includes('fallido')) {
        return 'bg-red-100 text-red-800';
    }
    return 'bg-gray-100 text-gray-800';
};

const loadReports = async () => {
    loading.value = true;
    error.value = null;
    
    // Primero intentar cargar desde localStorage (datos de conciliación guardada)
    try {
        const savedConciliation = localStorage.getItem('bankSync_last_conciliation');
        if (savedConciliation) {
            const parsedData = JSON.parse(savedConciliation);
            // Crear un reporte desde la conciliación guardada
            const reportFromLocalStorage = createReportFromConciliation(parsedData);
            if (reportFromLocalStorage) {
                reports.value = [reportFromLocalStorage];
            }
        }
    } catch (e) {
        console.warn('Error cargando conciliación desde localStorage:', e);
    }
    
    // Luego intentar cargar desde el backend
    try {
        const { data } = await apiGetHistorial();
        if (data && Array.isArray(data) && data.length > 0) {
            const reportsFromBackend = mapHistorialToReports(data);
            // Combinar reportes del backend con los de localStorage (evitando duplicados)
            const existingIds = new Set(reports.value.map(r => r.id));
            const newReports = reportsFromBackend.filter(r => !existingIds.has(r.id));
            reports.value = [...reports.value, ...newReports];
            // Ordenar por fecha (más reciente primero)
            reports.value.sort((a, b) => new Date(b.date) - new Date(a.date));
        }
    } catch (e) {
        console.error('Error cargando historial de conciliaciones:', e);
        // Solo mostrar error si realmente es un error del servidor y no hay datos locales
        if (e.response && e.response.status >= 500) {
            if (reports.value.length === 0) {
                // Solo mostrar error si no hay datos locales
                error.value = 'No se pudieron cargar los reportes';
                showError('Error del servidor al cargar los reportes. Mostrando datos locales si están disponibles.', 'Error al Cargar');
            }
        }
        // Si hay errores de red o 404, simplemente no mostrar error (puede ser normal)
    } finally {
        loading.value = false;
    }
};

// Función para crear un reporte desde una conciliación completa
const createReportFromConciliation = (conciliationData) => {
    if (!conciliationData || !conciliationData.summary) {
        return null;
    }
    
    const summary = conciliationData.summary || {};
    const total = (summary.total_transacciones_pdf || 0) + (summary.total_transacciones_excel || 0);
    const conciliadas = summary.coincidencias_encontradas || 0;
    
    // Usar la fecha actual si no hay fecha en los datos
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10);
    const periodStr = now.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long'
    });
    
    return {
        id: conciliationData.reconciliation_id || `local-${Date.now()}`,
        name: `Conciliación - ${dateStr}`,
        type: 'Conciliación',
        period: periodStr,
        date: dateStr,
        records: total,
        reconciled: conciliadas,
        status: 'Completado',
        // Guardar los datos completos para poder generar reportes detallados
        rawData: conciliationData
    };
};

const loadDashboardStats = async () => {
    try {
        const { data } = await apiGetDashboardResumen();
        if (data) {
            dashboardStats.value = data;
        }
    } catch (e) {
        console.error('Error cargando estadísticas del dashboard:', e);
        // No mostrar error si falla, solo usar valores por defecto
    }
};

onMounted(async () => {
    // Cargar reportes primero (puede usar datos locales rápidos)
    await loadReports();
    // Luego cargar estadísticas (puede fallar silenciosamente)
    loadDashboardStats().catch(e => {
        console.warn('Error cargando estadísticas:', e);
    });
});

// Recargar reportes cuando cambie el periodo (opcional: podrías hacer polling o eventos)
watch([dateFrom, dateTo], () => {
    // Los filtros se aplican automáticamente por el computed filteredReports
});
</script>
