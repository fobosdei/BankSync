<template>
    <div>
        <!-- Header -->
        <header class="bg-white border-b border-gray-200 px-8 py-6">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">Conciliaciones</h1>
                    <p class="text-sm text-gray-600 mt-1">Gestiona y revisa las conciliaciones entre extractos bancarios y registros contables</p>
                </div>
                <div class="flex items-center gap-3">
                    <button
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
                        @click="exportarUltimaConciliacion"
                        :disabled="!conciliationResult && !lastReconciliation"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        Exportar
                    </button>
                    <button @click="showUploadModal = true" class="px-4 py-2 text-white bg-purple-600 rounded-lg hover:bg-purple-700 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Conciliar todo con IA
                    </button>
                </div>
            </div>

            <!-- Filters -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="relative">
                    <button
                        type="button"
                        class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 flex items-center justify-center focus:outline-none"
                        @click="focusSearch"
                    >
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </button>
                    <input
                        ref="searchInput"
                        v-model="searchQuery"
                        type="text"
                        placeholder="Buscar por descripción o referencia..."
                        class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                </div>
                <select v-model="statusFilter" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                    <option value="">Estado</option>
                    <option value="Conciliado">Conciliado</option>
                    <option value="Pendiente">Pendiente</option>
                    <option value="Revisar">Revisar</option>
                </select>
                <select v-model="accountFilter" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                    <option value="">Cuenta bancaria</option>
                    <option>Banco Nacional</option>
                    <option>Banco del País</option>
                    <option>Banco Digital</option>
                    <option>Banco Internacional</option>
                </select>
                <select v-model="confidenceFilter" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                    <option value="">Confianza IA</option>
                    <option value="alta">Alta (&gt;90%)</option>
                    <option value="media">Media (50-90%)</option>
                    <option value="baja">Baja (&lt;50%)</option>
                </select>
            </div>
        </header>

        <div class="p-8">
            <!-- Resumen de la última conciliación guardada -->
            <div v-if="lastReconciliation" class="mb-8 bg-blue-50 border border-blue-100 rounded-xl p-4 flex items-center justify-between">
                <div>
                    <p class="text-xs font-semibold text-blue-600 uppercase tracking-wide">Última conciliación</p>
                    <p class="text-sm text-blue-900 font-medium">{{ lastReconciliation.name }}</p>
                    <p class="text-xs text-blue-700">
                        {{ new Date(lastReconciliation.created_at).toLocaleString('es-CO') }}
                    </p>
                </div>
                <div class="flex items-center gap-6">
                    <div class="text-right">
                        <p class="text-xs text-blue-700">Conciliado</p>
                        <p class="text-xl font-bold text-blue-900">
                            {{ Math.round(lastReconciliation.summary.porcentaje_conciliado || 0) }}%
                        </p>
                    </div>
                    <div class="h-10 w-px bg-blue-200"></div>
                    <div class="text-right">
                        <p class="text-xs text-blue-700">Transacciones</p>
                        <p class="text-xl font-bold text-blue-900">
                            {{ (lastReconciliation.summary.total_transacciones_pdf || 0) + (lastReconciliation.summary.total_transacciones_excel || 0) }}
                        </p>
                    </div>
                </div>
            </div>

            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Total</p>
                    <p class="text-2xl font-bold text-gray-900">{{ stats.total }} transacciones</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Conciliadas</p>
                    <p class="text-2xl font-bold text-green-600">{{ stats.matched }} ({{ stats.matchedPercent }}%)</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Sin match PDF</p>
                    <p class="text-2xl font-bold text-orange-600">{{ stats.unmatchedPdf }}</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Sin match ERP</p>
                    <p class="text-2xl font-bold text-red-600">{{ stats.unmatchedErp }}</p>
                </div>
            </div>

            <!-- Transactions Table -->
            <div class="bg-white rounded-xl border border-gray-200">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Transacciones</h3>
                    <p class="text-sm text-gray-600">Lista completa de movimientos para conciliación</p>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead class="bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cuenta</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monto Banco</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monto Contable</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Confianza IA</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr v-for="transaction in filteredTransactions" :key="transaction.id" class="hover:bg-gray-50">
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ transaction.date }}</td>
                                <td class="px-6 py-4 text-sm">
                                    <div class="font-medium text-gray-900">{{ transaction.description }}</div>
                                    <div class="text-gray-500 text-xs">{{ transaction.reference }}</div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ transaction.account }}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm" :class="transaction.bankAmount < 0 ? 'text-red-600' : 'text-gray-900'">
                                    {{ formatCurrency(transaction.bankAmount) }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm" :class="transaction.accountingAmount < 0 ? 'text-red-600' : 'text-gray-900'">
                                    {{ transaction.accountingAmount ? formatCurrency(transaction.accountingAmount) : 'Sin registro' }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span :class="getStatusClass(transaction.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                                        {{ transaction.status }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center gap-2">
                                        <div class="flex-1 bg-gray-200 rounded-full h-2">
                                            <div :class="getConfidenceColor(transaction.confidence)" 
                                                 class="h-2 rounded-full" 
                                                 :style="`width: ${transaction.confidence}%`"></div>
                                        </div>
                                        <span class="text-sm font-medium text-gray-900">{{ transaction.confidence }}%</span>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm">
                                    <div class="flex items-center gap-2">
                                        <button class="text-gray-400 hover:text-gray-600" @click="openTransactionDetails(transaction)">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                            </svg>
                                        </button>
                                        <button
                                            v-if="transaction.status === 'Conciliado'"
                                            class="text-green-600 hover:text-green-700"
                                            @click="toggleTransactionStatus(transaction)"
                                        >
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                            </svg>
                                        </button>
                                        <button
                                            v-else
                                            class="text-red-600 hover:text-red-700"
                                            @click="toggleTransactionStatus(transaction)"
                                        >
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Modal de detalle de transacción -->
        <div
            v-if="showTransactionModal && selectedTransaction"
            class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
            @click.self="showTransactionModal = false"
        >
            <div class="bg-white rounded-xl shadow-2xl max-w-lg w-full mx-4 p-6">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-xl font-bold text-gray-900">Detalle de transacción</h2>
                    <button @click="showTransactionModal = false" class="text-gray-400 hover:text-gray-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <div class="space-y-2 text-sm text-gray-800">
                    <p><span class="font-semibold">Fecha:</span> {{ selectedTransaction.date }}</p>
                    <p><span class="font-semibold">Descripción:</span> {{ selectedTransaction.description }}</p>
                    <p><span class="font-semibold">Referencia:</span> {{ selectedTransaction.reference }}</p>
                    <p><span class="font-semibold">Cuenta:</span> {{ selectedTransaction.account }}</p>
                    <p>
                        <span class="font-semibold">Monto banco:</span>
                        {{ selectedTransaction.bankAmount !== null ? formatCurrency(selectedTransaction.bankAmount) : 'N/A' }}
                    </p>
                    <p>
                        <span class="font-semibold">Monto contable:</span>
                        {{
                            selectedTransaction.accountingAmount !== null
                                ? formatCurrency(selectedTransaction.accountingAmount)
                                : 'N/A'
                        }}
                    </p>
                    <p>
                        <span class="font-semibold">Estado:</span>
                        <span :class="getStatusClass(selectedTransaction.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                            {{ selectedTransaction.status }}
                        </span>
                    </p>
                    <p><span class="font-semibold">Confianza IA:</span> {{ selectedTransaction.confidence }}%</p>
                </div>

                <div class="mt-6 flex justify-end gap-2">
                    <button
                        class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm"
                        @click="showTransactionModal = false"
                    >
                        Cerrar
                    </button>
                    <button
                        class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm"
                        @click="() => { toggleTransactionStatus(selectedTransaction); showTransactionModal = false; }"
                    >
                        Alternar estado
                    </button>
                </div>
            </div>
        </div>

        <!-- Upload Modal -->
        <div v-if="showUploadModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="closeModal">
            <div class="bg-white rounded-xl shadow-2xl max-w-2xl w-full mx-4 p-8">
                <div class="flex items-center justify-between mb-6">
                    <h2 class="text-2xl font-bold text-gray-900">Conciliar con IA</h2>
                    <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <div v-if="!isProcessing && !conciliationResult" class="space-y-6">
                    <!-- PDF Upload -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Extracto Bancario (PDF)</label>
                        <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-purple-500 transition-colors cursor-pointer"
                             @click="$refs.pdfInput.click()"
                             @dragover.prevent
                             @drop.prevent="handlePdfDrop">
                            <input ref="pdfInput" type="file" accept=".pdf" @change="handlePdfSelect" class="hidden">
                            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                            </svg>
                            <p class="mt-2 text-sm text-gray-600">
                                <span v-if="!pdfFile" class="font-medium text-purple-600">Haz clic para subir</span>
                                <span v-else class="font-medium text-green-600">✓ {{ pdfFile.name }}</span>
                            </p>
                            <p class="text-xs text-gray-500">PDF hasta 10MB</p>
                        </div>
                    </div>

                    <!-- Excel Upload -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Movimientos ERP (Excel)</label>
                        <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-purple-500 transition-colors cursor-pointer"
                             @click="$refs.excelInput.click()"
                             @dragover.prevent
                             @drop.prevent="handleExcelDrop">
                            <input ref="excelInput" type="file" accept=".xlsx,.xls" @change="handleExcelSelect" class="hidden">
                            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                            </svg>
                            <p class="mt-2 text-sm text-gray-600">
                                <span v-if="!excelFile" class="font-medium text-purple-600">Haz clic para subir</span>
                                <span v-else class="font-medium text-green-600">✓ {{ excelFile.name }}</span>
                            </p>
                            <p class="text-xs text-gray-500">Excel (.xlsx, .xls) hasta 10MB</p>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="flex gap-3">
                        <button @click="closeModal" class="flex-1 px-4 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 font-medium">
                            Cancelar
                        </button>
                        <button @click="processConciliation" :disabled="!pdfFile || !excelFile" 
                                class="flex-1 px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                            Procesar con IA
                        </button>
                    </div>
                </div>

                <!-- Processing State -->
                <div v-if="isProcessing" class="text-center py-12">
                    <div class="inline-block animate-spin rounded-full h-16 w-16 border-4 border-purple-200 border-t-purple-600 mb-4"></div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">Procesando con IA...</h3>
                    <p class="text-gray-600">{{ processingMessage }}</p>
                </div>

                <!-- Results State -->
                <div v-if="conciliationResult && !isProcessing" class="space-y-6">
                    <div class="text-center">
                        <div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                            </svg>
                        </div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-2">¡Conciliación Completada!</h3>
                        <p class="text-gray-600">{{ conciliationResult.summary.coincidencias_encontradas }} coincidencias encontradas</p>
                    </div>

                    <!-- Summary Stats -->
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-blue-50 rounded-lg p-4">
                            <p class="text-sm text-blue-600 font-medium">Transacciones PDF</p>
                            <p class="text-2xl font-bold text-blue-900">{{ conciliationResult.summary.total_transacciones_pdf }}</p>
                        </div>
                        <div class="bg-green-50 rounded-lg p-4">
                            <p class="text-sm text-green-600 font-medium">Transacciones ERP</p>
                            <p class="text-2xl font-bold text-green-900">{{ conciliationResult.summary.total_transacciones_excel }}</p>
                        </div>
                        <div class="bg-purple-50 rounded-lg p-4">
                            <p class="text-sm text-purple-600 font-medium">Coincidencias</p>
                            <p class="text-2xl font-bold text-purple-900">{{ conciliationResult.summary.coincidencias_encontradas }}</p>
                        </div>
                        <div class="bg-orange-50 rounded-lg p-4">
                            <p class="text-sm text-orange-600 font-medium">% Conciliado</p>
                            <p class="text-2xl font-bold text-orange-900">{{ Math.round(conciliationResult.summary.porcentaje_conciliado) }}%</p>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="flex gap-3">
                        <button @click="closeModal" class="flex-1 px-4 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 font-medium">
                            Cerrar
                        </button>
                        <button @click="viewResults" class="flex-1 px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium">
                            Ver Detalles
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { apiConciliar, apiGetHistorial } from '@/api/conciliation';

// Modal state
const showUploadModal = ref(false);
const isProcessing = ref(false);
const processingMessage = ref('Extrayendo transacciones del PDF...');
const conciliationResult = ref(null);

// File uploads
const pdfFile = ref(null);
const excelFile = ref(null);

// Historial / última conciliación desde BD
const lastReconciliation = ref(null);

// Filtros y búsqueda
const searchQuery = ref('');
const statusFilter = ref('');
const accountFilter = ref('');
const confidenceFilter = ref('');

// Estado del modal de detalle
const showTransactionModal = ref(false);
const selectedTransaction = ref(null);

// Stats computed from results
const filteredTransactions = computed(() => {
    return transactions.value.filter((t) => {
        const matchSearch =
            !searchQuery.value ||
            t.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            (t.reference && t.reference.toLowerCase().includes(searchQuery.value.toLowerCase()));
        const matchStatus = !statusFilter.value || t.status === statusFilter.value;
        const matchAccount = !accountFilter.value || t.account === accountFilter.value;
        let matchConfidence = true;
        if (confidenceFilter.value === 'alta') matchConfidence = t.confidence >= 90;
        if (confidenceFilter.value === 'media') matchConfidence = t.confidence >= 50 && t.confidence < 90;
        if (confidenceFilter.value === 'baja') matchConfidence = t.confidence < 50;
        return matchSearch && matchStatus && matchAccount && matchConfidence;
    });
});

const stats = computed(() => {
    if (!conciliationResult.value && !lastReconciliation.value) {
        return {
            total: transactions.value.length,
            matched: transactions.value.filter(t => t.status === 'Conciliado').length,
            matchedPercent: Math.round((transactions.value.filter(t => t.status === 'Conciliado').length / transactions.value.length) * 100),
            unmatchedPdf: transactions.value.filter(t => t.status === 'Pendiente').length,
            unmatchedErp: transactions.value.filter(t => t.status === 'Revisar').length
        };
    }

    const summary = (conciliationResult.value && conciliationResult.value.summary) ||
        (lastReconciliation.value && lastReconciliation.value.summary) ||
        {};
    return {
        total: summary.total_transacciones_pdf + summary.total_transacciones_excel,
        matched: summary.coincidencias_encontradas,
        matchedPercent: Math.round(summary.porcentaje_conciliado),
        unmatchedPdf: summary.transacciones_sin_match_pdf,
        unmatchedErp: summary.transacciones_sin_match_excel
    };
});

// File handlers
const handlePdfSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
        pdfFile.value = file;
    }
};

const handleExcelSelect = (event) => {
    const file = event.target.files[0];
    if (file && (file.name.endsWith('.xlsx') || file.name.endsWith('.xls'))) {
        excelFile.value = file;
    }
};

const handlePdfDrop = (event) => {
    const file = event.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
        pdfFile.value = file;
    }
};

const handleExcelDrop = (event) => {
    const file = event.dataTransfer.files[0];
    if (file && (file.name.endsWith('.xlsx') || file.name.endsWith('.xls'))) {
        excelFile.value = file;
    }
};

// Cargar historial al montar la vista
onMounted(async () => {
    try {
        const { data } = await apiGetHistorial();
        if (data && data.length > 0) {
            // Nos quedamos con la más reciente (viene ya ordenado desde el backend)
            lastReconciliation.value = data[0];
        }
    } catch (e) {
        console.error('Error cargando historial de conciliaciones:', e);
    }
});

// Process conciliation
const processConciliation = async () => {
    if (!pdfFile.value || !excelFile.value) return;
    
    isProcessing.value = true;
    processingMessage.value = 'Extrayendo transacciones del PDF con OpenAI...';
    
    try {
        // Simulate progress messages
        setTimeout(() => {
            processingMessage.value = 'Procesando archivo Excel del ERP...';
        }, 2000);
        
        setTimeout(() => {
            processingMessage.value = 'Realizando conciliación inteligente...';
        }, 4000);
        
        const response = await apiConciliar(pdfFile.value, excelFile.value);
        conciliationResult.value = response.data;
        if (response.data.reconciliation_id) {
            // Después de guardar, refrescamos la última conciliación desde BD
            const { data: historial } = await apiGetHistorial();
            if (historial && historial.length > 0) {
                lastReconciliation.value = historial[0];
            }
        }
        
        // Update transactions table with results
        updateTransactionsFromResult(response.data);
        
    } catch (error) {
        console.error('Error en conciliación:', error);
        alert('Error al procesar la conciliación: ' + (error.response?.data?.detail || error.message));
    } finally {
        isProcessing.value = false;
    }
};

// Update transactions table with conciliation results
const updateTransactionsFromResult = (result) => {
    const newTransactions = [];
    
    // Add matched transactions
    result.matches.forEach((match, index) => {
        newTransactions.push({
            id: `match-${index}`,
            date: match.pdf_transaction.fecha,
            description: match.pdf_transaction.descripcion,
            reference: match.pdf_transaction.referencia || 'N/A',
            account: 'Banco',
            bankAmount: match.pdf_transaction.monto,
            accountingAmount: match.excel_transaction.monto,
            status: 'Conciliado',
            confidence: Math.round(match.confidence * 100)
        });
    });
    
    // Add unmatched PDF transactions
    result.unmatched_extracto.forEach((trans, index) => {
        newTransactions.push({
            id: `pdf-${index}`,
            date: trans.fecha,
            description: trans.descripcion,
            reference: trans.referencia || 'N/A',
            account: 'Banco',
            bankAmount: trans.monto,
            accountingAmount: null,
            status: 'Pendiente',
            confidence: 0
        });
    });
    
    // Add unmatched ERP transactions
    result.unmatched_erp.forEach((trans, index) => {
        newTransactions.push({
            id: `erp-${index}`,
            date: trans.fecha,
            description: trans.descripcion,
            reference: trans.referencia || 'N/A',
            account: 'ERP',
            bankAmount: null,
            accountingAmount: trans.monto,
            status: 'Revisar',
            confidence: 0
        });
    });
    
    transactions.value = newTransactions;
};

// View detailed results
const viewResults = () => {
    closeModal();
    // Scroll to transactions table
    window.scrollTo({ top: 400, behavior: 'smooth' });
};

// Exportar (por ahora solo descarga el JSON de la última conciliación en el navegador)
const exportarUltimaConciliacion = () => {
    const data =
        conciliationResult.value ||
        (lastReconciliation.value && lastReconciliation.value.summary);
    if (!data) return;

    const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'conciliacion.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
};

// Close modal and reset
const closeModal = () => {
    showUploadModal.value = false;
    pdfFile.value = null;
    excelFile.value = null;
    isProcessing.value = false;
    conciliationResult.value = null;
};

const transactions = ref([
    {
        id: 1,
        date: '2025-10-10',
        description: 'Transferencia Nómina Empleados',
        reference: 'TRF-2025-1001',
        account: 'Banco Nacional',
        bankAmount: 12500000,
        accountingAmount: 12500000,
        status: 'Conciliado',
        confidence: 98
    },
    {
        id: 2,
        date: '2025-10-09',
        description: 'Pago Proveedor ABC S.A.',
        reference: 'PAG-2025-0892',
        account: 'Banco del País',
        bankAmount: 3200000,
        accountingAmount: 3200000,
        status: 'Pendiente',
        confidence: 92
    },
    {
        id: 3,
        date: '2025-10-08',
        description: 'Ingreso por ventas retail',
        reference: 'ING-2025-3441',
        account: 'Banco Nacional',
        bankAmount: 8750000,
        accountingAmount: 8700000,
        status: 'Revisar',
        confidence: 45
    },
    {
        id: 4,
        date: '2025-10-08',
        description: 'Pago servicios públicos',
        reference: 'SRV-2025-0234',
        account: 'Banco Digital',
        bankAmount: 450000,
        accountingAmount: 450000,
        status: 'Conciliado',
        confidence: 100
    },
    {
        id: 5,
        date: '2025-10-07',
        description: 'Transferencia cliente XYZ Corp',
        reference: 'TRF-2025-1023',
        account: 'Banco Internacional',
        bankAmount: 15000000,
        accountingAmount: null,
        status: 'Pendiente',
        confidence: 0
    },
    {
        id: 6,
        date: '2025-10-07',
        description: 'Comisión bancaria mensual',
        reference: 'COM-2025-0098',
        account: 'Banco Nacional',
        bankAmount: -45000,
        accountingAmount: -45000,
        status: 'Conciliado',
        confidence: 95
    },
    {
        id: 7,
        date: '2025-10-06',
        description: 'Reembolso gastos operativos',
        reference: 'REM-2025-0456',
        account: 'Banco del País',
        bankAmount: 1200000,
        accountingAmount: 1250000,
        status: 'Revisar',
        confidence: 67
    },
    {
        id: 8,
        date: '2025-10-06',
        description: 'Pago arrendamiento oficina',
        reference: 'ARR-2025-0012',
        account: 'Banco Nacional',
        bankAmount: -5500000,
        accountingAmount: -5500000,
        status: 'Conciliado',
        confidence: 99
    }
]);

const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
};

const getStatusClass = (status) => {
    const classes = {
        'Conciliado': 'bg-green-100 text-green-800',
        'Pendiente': 'bg-orange-100 text-orange-800',
        'Revisar': 'bg-red-100 text-red-800'
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
};

const getConfidenceColor = (confidence) => {
    if (confidence >= 90) return 'bg-green-600';
    if (confidence >= 50) return 'bg-orange-500';
    return 'bg-gray-400';
};

const focusSearch = () => {
    if (searchInput.value) {
        searchInput.value.focus();
    }
};

const openTransactionDetails = (transaction) => {
    selectedTransaction.value = { ...transaction };
    showTransactionModal.value = true;
};

const toggleTransactionStatus = (transaction) => {
    if (!transaction) return;

    if (transaction.status === 'Conciliado') {
        transaction.status = 'Pendiente';
        transaction.confidence = Math.min(transaction.confidence, 80);
    } else {
        transaction.status = 'Conciliado';
        if (transaction.confidence < 90) transaction.confidence = 95;
    }
};
</script>
