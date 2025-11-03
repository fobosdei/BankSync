<template>
    <div>
        <!-- Header -->
        <header class="bg-white border-b border-gray-200 px-8 py-6">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">Configuración</h1>
                    <p class="text-sm text-gray-600 mt-1">Administra usuarios, conexiones bancarias e integraciones</p>
                </div>
            </div>
        </header>

        <div class="p-8">
            <!-- Tabs -->
            <div class="bg-white rounded-xl border border-gray-200">
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

                <!-- Users Tab -->
                <div v-if="activeTab === 'usuarios'" class="p-6">
                    <div class="flex items-center justify-between mb-6">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-900">Gestión de Usuarios</h3>
                            <p class="text-sm text-gray-600">Administra los usuarios y sus permisos</p>
                        </div>
                        <button class="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                            </svg>
                            Agregar usuario
                        </button>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gray-50 border-b border-gray-200">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Correo electrónico</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rol</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Último acceso</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ user.name }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ user.email }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span :class="getRoleClass(user.role)" class="px-2 py-1 text-xs font-medium rounded-full">
                                            {{ user.role }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span :class="user.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'" 
                                              class="px-2 py-1 text-xs font-medium rounded-full">
                                            {{ user.active ? 'Activo' : 'Inactivo' }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ user.lastAccess }}</td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm">
                                        <div class="flex items-center gap-2">
                                            <button class="text-blue-600 hover:text-blue-700">Editar</button>
                                            <button class="text-red-600 hover:text-red-700">Desactivar</button>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Permissions Section -->
                    <div class="mt-8">
                        <h4 class="text-lg font-semibold text-gray-900 mb-4">Permisos por Rol</h4>
                        <p class="text-sm text-gray-600 mb-6">Define los niveles de acceso para cada rol</p>

                        <div class="space-y-6">
                            <div v-for="role in roles" :key="role.name" class="bg-gray-50 rounded-lg p-6">
                                <div class="flex items-center justify-between mb-4">
                                    <div>
                                        <h5 class="font-semibold text-gray-900">{{ role.name }}</h5>
                                        <p class="text-sm text-gray-600">{{ role.description }}</p>
                                    </div>
                                    <span class="px-3 py-1 bg-purple-100 text-purple-800 text-sm font-medium rounded-full">
                                        {{ role.users }} usuarios
                                    </span>
                                </div>
                                <div class="grid grid-cols-2 gap-4">
                                    <div v-for="permission in role.permissions" :key="permission" class="flex items-center gap-2">
                                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                        </svg>
                                        <span class="text-sm text-gray-700">{{ permission }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Bank Accounts Tab -->
                <div v-if="activeTab === 'cuentas'" class="p-6">
                    <p class="text-gray-600">Gestión de cuentas bancarias - En desarrollo</p>
                </div>

                <!-- Integrations Tab -->
                <div v-if="activeTab === 'integraciones'" class="p-6">
                    <p class="text-gray-600">Configuración de integraciones - En desarrollo</p>
                </div>

                <!-- System Tab -->
                <div v-if="activeTab === 'sistema'" class="p-6">
                    <p class="text-gray-600">Configuración del sistema - En desarrollo</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const activeTab = ref('usuarios');

const tabs = ref([
    { id: 'usuarios', name: 'Usuarios y Roles' },
    { id: 'cuentas', name: 'Cuentas Bancarias' },
    { id: 'integraciones', name: 'Integraciones' },
    { id: 'sistema', name: 'Sistema' }
]);

const users = ref([
    { id: 1, name: 'María González', email: 'maria.gonzalez@empresa.com', role: 'Administrador', active: true, lastAccess: '2025-10-13 14:35' },
    { id: 2, name: 'Carlos Ramírez', email: 'carlos.ramirez@empresa.com', role: 'Contador', active: true, lastAccess: '2025-10-13 14:28' },
    { id: 3, name: 'Ana Martínez', email: 'ana.martinez@empresa.com', role: 'Auditor', active: true, lastAccess: '2025-10-12 16:45' },
    { id: 4, name: 'Pedro López', email: 'pedro.lopez@empresa.com', role: 'Contador', active: false, lastAccess: '2025-10-05 09:12' }
]);

const roles = ref([
    {
        name: 'Administrador',
        description: 'Control total del sistema',
        users: 4,
        permissions: [
            'Gestión de usuarios',
            'Todas las conciliaciones',
            'Configuración del sistema',
            'Gestión de reglas de IA'
        ]
    },
    {
        name: 'Contador',
        description: 'Conciliaciones y registros',
        users: 8,
        permissions: [
            'Ver conciliaciones',
            'Crear asientos ajuste',
            'Aprobar/rechazar matches',
            'Sin acceso a configuración'
        ]
    },
    {
        name: 'Auditor',
        description: 'Solo lectura y reportes',
        users: 3,
        permissions: [
            'Ver todas las transacciones',
            'Historial de auditoría',
            'Generar reportes',
            'Sin permisos de edición'
        ]
    }
]);

const getRoleClass = (role) => {
    const classes = {
        'Administrador': 'bg-purple-100 text-purple-800',
        'Contador': 'bg-blue-100 text-blue-800',
        'Auditor': 'bg-green-100 text-green-800'
    };
    return classes[role] || 'bg-gray-100 text-gray-800';
};
</script>
