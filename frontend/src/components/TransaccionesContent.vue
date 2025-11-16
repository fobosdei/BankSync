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
                    <button
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
                        @click="syncBanks"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Sincronizar
                    </button>
                    <button
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
                        @click="() => $refs.importInput.click()"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                        </svg>
                        Importar extracto
                    </button>
                    <input
                        ref="importInput"
                        type="file"
                        accept=".csv"
                        class="hidden"
                        @change="handleImportFile"
                    />
                    <button
                        class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2"
                        @click="exportTransactions"
                    >
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
                    <p class="text-2xl font-bold text-gray-900">{{ stats.total }}</p>
                    <p class="text-xs text-gray-500 mt-1">Este mes</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Ingresos</p>
                    <p class="text-2xl font-bold text-green-600">{{ formatCurrency(stats.income) }}</p>
                    <p class="text-xs text-gray-500 mt-1">{{ stats.incomeCount }} transacciones</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Egresos</p>
                    <p class="text-2xl font-bold text-red-600">{{ formatCurrency(stats.expense) }}</p>
                    <p class="text-xs text-gray-500 mt-1">{{ stats.expenseCount }} transacciones</p>
                </div>
                <div class="bg-white rounded-xl p-6 border border-gray-200">
                    <p class="text-sm text-gray-600 mb-2">Sin conciliar</p>
                    <p class="text-2xl font-bold text-orange-600">{{ stats.unreconciled }}</p>
                    <p class="text-xs text-gray-500 mt-1">
                        {{ stats.total ? ((stats.unreconciled / stats.total) * 100).toFixed(1) : 0 }}% del total
                    </p>
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
                            v-model="searchQuery"
                            type="text"
                            placeholder="Buscar transacciones..."
                            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                    </div>
                    <select
                        v-model="bankFilter"
                        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                        <option value="">Banco</option>
                        <option>Banco Nacional</option>
                        <option>Banco del País</option>
                        <option>Banco Internacional</option>
                    </select>
                    <select
                        v-model="typeFilter"
                        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                        <option value="">Tipo</option>
                        <option value="Ingreso">Ingreso</option>
                        <option value="Egreso">Egreso</option>
                    </select>
                    <select
                        v-model="statusFilter"
                        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                        <option value="">Estado</option>
                        <option value="Procesado">Procesado</option>
                        <option value="Pendiente">Pendiente</option>
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
                            <tr v-for="transaction in filteredTransactions" :key="transaction.id" class="hover:bg-gray-50">
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
                                        <button class="text-blue-600 hover:text-blue-700" @click="openEditModal(transaction)">
                                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                            </svg>
                                        </button>
                                        <button class="text-red-600 hover:text-red-700" @click="deleteTransaction(transaction.id)">
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

    <!-- Modal de edición rápida -->
    <div
        v-if="showEditModal && editableTransaction"
        class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
        @click.self="closeEditModal"
    >
        <div class="bg-white rounded-xl shadow-2xl max-w-lg w-full mx-4 p-6">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-bold text-gray-900">Editar transacción</h2>
                <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <div class="space-y-4 text-sm">
                <div>
                    <label class="block text-gray-700 mb-1">Descripción</label>
                    <input
                        v-model="editableTransaction.description"
                        type="text"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                </div>
                <div>
                    <label class="block text-gray-700 mb-1">Categoría</label>
                    <input
                        v-model="editableTransaction.category"
                        type="text"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                </div>
                <div>
                    <label class="block text-gray-700 mb-1">Estado</label>
                    <select
                        v-model="editableTransaction.status"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                        <option value="Procesado">Procesado</option>
                        <option value="Pendiente">Pendiente</option>
                    </select>
                </div>
                <div>
                    <label class="block text-gray-700 mb-1">Conciliación</label>
                    <select
                        v-model="editableTransaction.reconciliation"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                        <option value="Conciliada">Conciliada</option>
                        <option value="Pendiente">Pendiente</option>
                    </select>
                </div>
            </div>

            <div class="mt-6 flex justify-end gap-2">
                <button
                    class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm"
                    @click="closeEditModal"
                >
                    Cancelar
                </button>
                <button
                    class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm"
                    @click="saveEdit"
                >
                    Guardar cambios
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

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

// Filtros
const searchQuery = ref('');
const bankFilter = ref('');
const typeFilter = ref('');
const statusFilter = ref('');

// Modal de edición
const showEditModal = ref(false);
const editableTransaction = ref(null);

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

const filteredTransactions = computed(() => {
    return transactions.value.filter((t) => {
        const matchesSearch =
            !searchQuery.value ||
            t.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            t.id.toLowerCase().includes(searchQuery.value.toLowerCase());
        const matchesBank = !bankFilter.value || t.bank === bankFilter.value;
        const matchesType =
            !typeFilter.value ||
            (typeFilter.value === 'Ingreso' && t.amount > 0) ||
            (typeFilter.value === 'Egreso' && t.amount < 0);
        const matchesStatus = !statusFilter.value || t.status === statusFilter.value;
        return matchesSearch && matchesBank && matchesType && matchesStatus;
    });
});

const stats = computed(() => {
    const all = transactions.value;
    const total = all.length;
    const incomeTx = all.filter((t) => t.amount > 0);
    const expenseTx = all.filter((t) => t.amount < 0);
    const unreconciled = all.filter((t) => t.reconciliation !== 'Conciliada').length;

    return {
        total,
        income: incomeTx.reduce((sum, t) => sum + t.amount, 0),
        expense: expenseTx.reduce((sum, t) => sum + Math.abs(t.amount), 0),
        incomeCount: incomeTx.length,
        expenseCount: expenseTx.length,
        unreconciled,
    };
});

const syncBanks = () => {
    alert('Sincronización simulada: aquí se llamaría al backend/bancos.');
};

const handleImportFile = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        const text = e.target.result;
        const lines = text.split(/\r?\n/).filter((l) => l.trim().length > 0);
        if (lines.length <= 1) return;

        const [header, ...rows] = lines;
        const cols = header.split(',');

        const idIdx = cols.indexOf('id');
        const dateIdx = cols.indexOf('date');
        const bankIdx = cols.indexOf('bank');
        const descIdx = cols.indexOf('description');
        const catIdx = cols.indexOf('category');
        const amountIdx = cols.indexOf('amount');

        const imported = rows.map((row, i) => {
            const parts = row.split(',');
            return {
                id: parts[idIdx] || `IMP-${i}`,
                date: parts[dateIdx] || '',
                bank: parts[bankIdx] || 'Banco Nacional',
                description: parts[descIdx] || 'Movimiento',
                category: parts[catIdx] || 'Sin categoría',
                amount: Number(parts[amountIdx] || 0),
                status: 'Pendiente',
                reconciliation: 'Pendiente',
            };
        });

        if (imported.length) {
            transactions.value = imported;
            alert(`Se importaron ${imported.length} transacciones desde el CSV.`);
        }
    };
    reader.readAsText(file, 'utf-8');

    // limpiar input para permitir volver a importar el mismo archivo
    event.target.value = '';
};

const exportTransactions = () => {
    const data = filteredTransactions.value;
    if (!data.length) {
        alert('No hay transacciones para exportar.');
        return;
    }

    const header = ['id', 'date', 'bank', 'description', 'category', 'amount', 'status', 'reconciliation'];
    const rows = data.map((t) =>
        [
            t.id,
            t.date,
            t.bank,
            t.description.replace(/,/g, ' '),
            t.category.replace(/,/g, ' '),
            t.amount,
            t.status,
            t.reconciliation,
        ].join(','),
    );
    const csv = [header.join(','), ...rows].join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'transacciones.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
};

const openEditModal = (transaction) => {
    editableTransaction.value = { ...transaction };
    showEditModal.value = true;
};

const closeEditModal = () => {
    showEditModal.value = false;
    editableTransaction.value = null;
};

const saveEdit = () => {
    if (!editableTransaction.value) return;
    const idx = transactions.value.findIndex((t) => t.id === editableTransaction.value.id);
    if (idx !== -1) {
        transactions.value[idx] = { ...editableTransaction.value };
    }
    closeEditModal();
};

const deleteTransaction = (id) => {
    if (!confirm('¿Seguro que deseas eliminar esta transacción?')) return;
    transactions.value = transactions.value.filter((t) => t.id !== id);
};
</script>
