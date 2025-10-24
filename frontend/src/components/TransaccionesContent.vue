<template>
    <div>
        <!-- Header -->
        <header class="bg-white border-b border-gray-200 px-8 py-6">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">Transacciones Bancarias</h1>
                    <p class="text-sm text-gray-600 mt-1">Gestiona los movimientos importados desde tus cuentas bancarias</p>
                </div>
                <div class="flex items-center gap-3">
                    <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Sincronizar
                    </button>
                    <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                        </svg>
                        Importar extracto
                    </button>
                    <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        Exportar
                    </button>
                </div>
            </div>
        </header>

        <div class="p-8">
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Total transacciones</p>
                    <p class="text-2xl font-bold text-gray-900">847</p>
                    <p class="text-xs text-gray-500 mt-1">Este mes</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Ingresos</p>
                    <p class="text-2xl font-bold text-green-600">$185.5M</p>
                    <p class="text-xs text-gray-500 mt-1">342 transacciones</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Egresos</p>
                    <p class="text-2xl font-bold text-red-600">$142.8M</p>
                    <p class="text-xs text-gray-500 mt-1">505 transacciones</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Sin conciliar</p>
                    <p class="text-2xl font-bold text-orange-600">124</p>
                    <p class="text-xs text-gray-500 mt-1">14.6% del total</p>
                </div>
            </div>

            <!-- Filters -->
            <div class="bg-white rounded-xl border border-gray-200 p-6 mb-8">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="relative">
                        <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                        <input 
                            type="text" 
                            placeholder="Buscar transacciones..."
                            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                    </div>
                    <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option>Banco</option>
                        <option>Banco Nacional</option>
                        <option>Banco del País</option>
                        <option>Banco Internacional</option>
                    </select>
                    <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option>Tipo</option>
                        <option>Ingreso</option>
                        <option>Egreso</option>
                    </select>
                    <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option>Estado</option>
                        <option>Procesado</option>
                        <option>Pendiente</option>
                    </select>
                </div>
            </div>

            <!-- Transactions Table -->
            <div class="bg-white rounded-xl border border-gray-200 mb-8">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Lista de Transacciones</h3>
                    <p class="text-sm text-gray-600">Movimientos bancarios del último mes</p>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead class="bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID Transacción</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Banco</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Descripción</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Categoría IA</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Conciliación</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr v-for="transaction in transactions" :key="transaction.id" class="hover:bg-gray-50">
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ transaction.id }}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ transaction.date }}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ transaction.bank }}</td>
                                <td class="px-6 py-4 text-sm text-gray-900">{{ transaction.description }}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm">
                                    <div class="flex items-center gap-2">
                                        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                        </svg>
                                        <span class="text-gray-600">{{ transaction.category }}</span>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold" :class="transaction.amount > 0 ? 'text-green-600' : 'text-red-600'">
                                    {{ formatCurrency(transaction.amount) }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span :class="transaction.status === 'Procesado' ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800'" 
                                          class="px-2 py-1 text-xs font-medium rounded-full">
                                        {{ transaction.status }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span :class="getReconciliationClass(transaction.reconciliation)" 
                                          class="px-2 py-1 text-xs font-medium rounded-full">
                                        {{ transaction.reconciliation }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm">
                                    <div class="flex items-center gap-2">
                                        <button class="text-blue-600 hover:text-blue-700">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                            </svg>
                                        </button>
                                        <button class="text-red-600 hover:text-red-700">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
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
                <!-- Categorization -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Categorización Automática con IA</h3>
                    <p class="text-sm text-gray-600 mb-6">El sistema clasifica automáticamente tus transacciones</p>
                    
                    <div class="space-y-4">
                        <div v-for="cat in categories" :key="cat.name" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div class="flex items-center gap-3">
                                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                                </svg>
                                <span class="font-medium text-gray-900">{{ cat.name }}</span>
                            </div>
                            <span class="px-3 py-1 bg-gray-900 text-white text-sm font-medium rounded-full">
                                {{ cat.count }} transacciones
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Bank Sync -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Sincronización Bancaria</h3>
                    <p class="text-sm text-gray-600 mb-6">Estado de conexión con tus bancos</p>
                    
                    <div class="space-y-4">
                        <div v-for="bank in banks" :key="bank.name" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <p class="font-medium text-gray-900">{{ bank.name }}</p>
                                <p class="text-sm text-gray-600">Última sincronización: {{ bank.lastSync }}</p>
                            </div>
                            <span :class="bank.status === 'Activo' ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800'" 
                                  class="px-3 py-1 text-sm font-medium rounded-full">
                                {{ bank.status }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const transactions = ref([
    { id: 'TRX-2025-1001', date: '2025-10-13', bank: 'Banco Nacional', description: 'Transferencia recibida - Cliente ABC Corp', category: 'Ventas', amount: 15000000, status: 'Pendiente', reconciliation: 'Pendiente' },
    { id: 'TRX-2025-1002', date: '2025-10-13', bank: 'Banco del País', description: 'Pago a Proveedor XYZ S.A.', category: 'Proveedores', amount: -3500000, status: 'Procesado', reconciliation: 'Conciliada' },
    { id: 'TRX-2025-1003', date: '2025-10-12', bank: 'Banco Nacional', description: 'Depósito efectivo - Recaudo diario', category: 'Ventas', amount: 8750000, status: 'Procesado', reconciliation: 'Conciliada' },
    { id: 'TRX-2025-1004', date: '2025-10-12', bank: 'Banco Digital', description: 'Transferencia nómina empleados', category: 'Nómina', amount: -12500000, status: 'Procesado', reconciliation: 'Conciliada' },
    { id: 'TRX-2025-1005', date: '2025-10-11', bank: 'Banco Nacional', description: 'Pago servicios públicos - Sede principal', category: 'Gastos operativos', amount: -450000, status: 'Procesado', reconciliation: 'Conciliada' },
    { id: 'TRX-2025-1006', date: '2025-10-11', bank: 'Banco Nacional', description: 'Comisión bancaria', category: 'Gastos financieros', amount: -45000, status: 'Procesado', reconciliation: 'Conciliada' },
    { id: 'TRX-2025-1007', date: '2025-10-10', bank: 'Banco Internacional', description: 'Transferencia recibida - Contrato servicios', category: 'Ventas', amount: 25000000, status: 'Procesado', reconciliation: 'Pendiente' },
    { id: 'TRX-2025-1008', date: '2025-10-10', bank: 'Banco Nacional', description: 'Pago arrendamiento - Oficina central', category: 'Arrendamiento', amount: -5500000, status: 'Procesado', reconciliation: 'Conciliada' },
    { id: 'TRX-2025-1009', date: '2025-10-09', bank: 'Banco del País', description: 'Reembolso gastos operativos', category: 'Otros ingresos', amount: 1200000, status: 'Procesado', reconciliation: 'Conciliada' },
    { id: 'TRX-2025-1010', date: '2025-10-09', bank: 'Banco Digital', description: 'Compra suministros oficina', category: 'Gastos operativos', amount: -850000, status: 'Procesado', reconciliation: 'Pendiente' }
]);

const categories = ref([
    { name: 'Ventas', count: 245 },
    { name: 'Proveedores', count: 189 },
    { name: 'Nómina', count: 52 },
    { name: 'Gastos operativos', count: 124 }
]);

const banks = ref([
    { name: 'Banco Nacional', lastSync: 'Hace 5 min', status: 'Activo' },
    { name: 'Banco del País', lastSync: 'Hace 15 min', status: 'Activo' },
    { name: 'Banco Internacional', lastSync: 'Hace 2 horas', status: 'Retraso' }
]);

const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
};

const getReconciliationClass = (status) => {
    return status === 'Conciliada' ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800';
};
</script>
