<template>
    <div>
        <!-- Header -->
        <header class="bg-white border-b border-gray-200 px-8 py-6">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">Registros Contables</h1>
                    <p class="text-sm text-gray-600 mt-1">Gestiona los asientos contables para emparejar con transacciones bancarias</p>
                </div>
                <div class="flex items-center gap-3">
                    <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        Exportar
                    </button>
                    <button class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                        </svg>
                        Importar desde ERP
                    </button>
                    <button class="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Vincular pendientes
                    </button>
                </div>
            </div>

            <!-- Alert -->
            <div class="bg-purple-50 border border-purple-200 rounded-lg p-4 flex items-start gap-3">
                <svg class="w-5 h-5 text-purple-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <div class="flex-1">
                    <p class="font-semibold text-purple-900">La IA ha detectado</p>
                    <p class="text-sm text-purple-800 mt-1">
                        <span class="font-bold">3 registros contables</span> que podrían vincularse automáticamente con transacciones bancarias pendientes.
                    </p>
                    <button class="text-sm text-purple-600 font-medium hover:text-purple-700 mt-2">Ver sugerencias →</button>
                </div>
            </div>
        </header>

        <div class="p-8">
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Total registros</p>
                    <p class="text-2xl font-bold text-gray-900">1,847</p>
                    <p class="text-xs text-gray-500 mt-1">Este mes</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Vinculados</p>
                    <p class="text-2xl font-bold text-green-600">1,623 (88%)</p>
                    <p class="text-xs text-gray-500 mt-1">Con transacciones</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Pendientes</p>
                    <p class="text-2xl font-bold text-orange-600">224 (12%)</p>
                    <p class="text-xs text-gray-500 mt-1">Sin vincular</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Sugerencias IA</p>
                    <p class="text-2xl font-bold text-purple-600">156</p>
                    <p class="text-xs text-gray-500 mt-1">Matches posibles</p>
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
                            placeholder="Buscar por cuenta o descripción..."
                            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                    </div>
                    <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option>Cuenta contable</option>
                        <option>1105 - Bancos</option>
                        <option>2205 - Proveedores</option>
                        <option>4135 - Ingresos</option>
                    </select>
                    <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option>Tipo</option>
                        <option>Asiento automático</option>
                        <option>Asiento manual</option>
                    </select>
                    <select class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                        <option>Estado</option>
                        <option>Vinculado</option>
                        <option>Pendiente</option>
                    </select>
                </div>
            </div>

            <!-- Records Table -->
            <div class="bg-white rounded-xl border border-gray-200 mb-8">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Asientos Contables</h3>
                    <p class="text-sm text-gray-600">Registros contables del último mes</p>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead class="bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Asiento</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cuenta</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Descripción</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Débito</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Crédito</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sugerencia IA</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr v-for="record in records" :key="record.id" class="hover:bg-gray-50">
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ record.id }}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ record.date }}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm">
                                    <div class="font-medium text-gray-900">{{ record.account }}</div>
                                    <div class="text-gray-500 text-xs">{{ record.accountName }}</div>
                                </td>
                                <td class="px-6 py-4 text-sm text-gray-900">{{ record.description }}</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    {{ record.debit ? formatCurrency(record.debit) : '-' }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    {{ record.credit ? formatCurrency(record.credit) : '-' }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ record.type }}</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span :class="record.status === 'Vinculado' ? 'bg-green-100 text-green-800' : 'bg-orange-100 text-orange-800'" 
                                          class="px-2 py-1 text-xs font-medium rounded-full">
                                        {{ record.status }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div v-if="record.suggestion" class="flex items-center gap-2">
                                        <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                        </svg>
                                        <span class="text-sm text-purple-600 font-medium">{{ record.suggestion }}</span>
                                    </div>
                                    <span v-else class="text-sm text-gray-400">-</span>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm">
                                    <div class="flex items-center gap-2">
                                        <button v-if="record.suggestion" class="text-purple-600 hover:text-purple-700">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                                            </svg>
                                        </button>
                                        <button class="text-blue-600 hover:text-blue-700">
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
                <!-- ERP Integration -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Integración ERP</h3>
                    <p class="text-sm text-gray-600 mb-6">Sincronización con sistemas contables</p>
                    
                    <div class="space-y-4">
                        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <p class="font-medium text-gray-900">SAP Business One</p>
                                <p class="text-sm text-gray-600">Última sincronización: Hace 30 min</p>
                            </div>
                            <span class="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
                                Conectado
                            </span>
                        </div>
                        <button class="w-full px-4 py-3 text-gray-700 bg-white border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 hover:bg-gray-50 transition-colors flex items-center justify-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                            Sincronizar ahora
                        </button>
                    </div>
                </div>

                <!-- Distribution by Account -->
                <div class="bg-white rounded-xl border border-gray-200 p-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">Distribución por Cuenta</h3>
                    <p class="text-sm text-gray-600 mb-6">Registros por categoría contable</p>
                    
                    <div class="space-y-4">
                        <div v-for="account in accountDistribution" :key="account.code" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                            <div>
                                <p class="font-medium text-gray-900">{{ account.code }} - {{ account.name }}</p>
                                <p class="text-sm text-gray-600">{{ account.description }}</p>
                            </div>
                            <span class="px-3 py-1 bg-gray-900 text-white text-sm font-medium rounded-full">
                                {{ account.count }} registros
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

const records = ref([
    { id: 'AS-2025-3421', date: '2025-10-13', account: '1105', accountName: 'Bancos - Cuenta Corriente', description: 'Transferencia recibida Cliente ABC', debit: 15000000, credit: null, type: 'Asiento automático', status: 'Vinculado', suggestion: 'TRX-2025-1001 - 95% match' },
    { id: 'AS-2025-3420', date: '2025-10-13', account: '2205', accountName: 'Proveedores nacionales', description: 'Pago Proveedor XYZ S.A.', debit: null, credit: 3500000, type: 'Asiento manual', status: 'Vinculado', suggestion: null },
    { id: 'AS-2025-3419', date: '2025-10-12', account: '1105', accountName: 'Bancos - Cuenta Corriente', description: 'Depósito efectivo ventas diarias', debit: 8700000, credit: null, type: 'Asiento automático', status: 'Pendiente', suggestion: 'TRX-2025-1003 - 78% match' },
    { id: 'AS-2025-3418', date: '2025-10-12', account: '5105', accountName: 'Gastos de personal', description: 'Nómina mensual empleados', debit: null, credit: 12500000, type: 'Asiento automático', status: 'Vinculado', suggestion: null },
    { id: 'AS-2025-3417', date: '2025-10-11', account: '5135', accountName: 'Servicios públicos', description: 'Pago servicios públicos octubre', debit: null, credit: 450000, type: 'Asiento manual', status: 'Vinculado', suggestion: null },
    { id: 'AS-2025-3416', date: '2025-10-11', account: '5305', accountName: 'Gastos bancarios', description: 'Comisión bancaria mensual', debit: null, credit: 45000, type: 'Asiento automático', status: 'Vinculado', suggestion: null },
    { id: 'AS-2025-3415', date: '2025-10-10', account: '4135', accountName: 'Ingresos por servicios', description: 'Contrato servicios profesionales', debit: 25000000, credit: null, type: 'Asiento automático', status: 'Pendiente', suggestion: 'TRX-2025-1007 - 92% match' },
    { id: 'AS-2025-3414', date: '2025-10-10', account: '5120', accountName: 'Arrendamiento', description: 'Pago arriendo oficina central', debit: null, credit: 5500000, type: 'Asiento manual', status: 'Vinculado', suggestion: null }
]);

const accountDistribution = ref([
    { code: '1105', name: 'Bancos', description: 'Cuenta corriente', count: 542 },
    { code: '4135', name: 'Ingresos', description: 'Ingresos por servicios', count: 298 },
    { code: '2205', name: 'Proveedores', description: 'Proveedores nacionales', count: 187 }
]);

const formatCurrency = (amount) => {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
};
</script>
