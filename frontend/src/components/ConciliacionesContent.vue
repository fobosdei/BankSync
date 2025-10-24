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
                    <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        Exportar
                    </button>
                    <button class="px-4 py-2 text-white bg-purple-600 rounded-lg hover:bg-purple-700 flex items-center gap-2">
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
                    <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <input 
                        type="text" 
                        placeholder="Buscar por descripción o referencia..."
                        class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                </div>
                <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                    <option>Estado</option>
                    <option>Conciliado</option>
                    <option>Pendiente</option>
                    <option>Revisar</option>
                </select>
                <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                    <option>Cuenta bancaria</option>
                    <option>Banco Nacional</option>
                    <option>Banco del País</option>
                    <option>Banco Internacional</option>
                </select>
                <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                    <option>Confianza IA</option>
                    <option>Alta (&gt;90%)</option>
                    <option>Media (50-90%)</option>
                    <option>Baja (&lt;50%)</option>
                </select>
            </div>
        </header>

        <div class="p-8">
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Total</p>
                    <p class="text-2xl font-bold text-gray-900">285 transacciones</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Conciliadas</p>
                    <p class="text-2xl font-bold text-green-600">248 (87%)</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Pendientes</p>
                    <p class="text-2xl font-bold text-orange-600">24 (8%)</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Requieren revisión</p>
                    <p class="text-2xl font-bold text-red-600">13 (5%)</p>
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
                            <tr v-for="transaction in transactions" :key="transaction.id" class="hover:bg-gray-50">
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
                                        <button class="text-gray-400 hover:text-gray-600">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                            </svg>
                                        </button>
                                        <button v-if="transaction.status === 'Conciliado'" class="text-green-600 hover:text-green-700">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                            </svg>
                                        </button>
                                        <button v-else class="text-red-600 hover:text-red-700">
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
    </div>
</template>

<script setup>
import { ref } from 'vue';

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
</script>
