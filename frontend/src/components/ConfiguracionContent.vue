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
                        <button 
                            @click="showUserModal = true; editingUser = null;" 
                            class="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 flex items-center gap-2"
                        >
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
                                            <button @click="openEditModal(user)" class="text-blue-600 hover:text-blue-700">Editar</button>
                                            <button @click="openPasswordModal(user)" class="text-orange-600 hover:text-orange-700">Password</button>
                                            <button @click="deleteUser(user)" class="text-red-600 hover:text-red-700">Eliminar</button>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Loading State -->
                    <div v-if="loading" class="text-center py-4">
                        <p class="text-gray-600">Cargando usuarios...</p>
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
                                        {{ getUsersCountByRole(role.name) }} usuarios
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

        <!-- Modal para Crear/Editar Usuario -->
        <div v-if="showUserModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 w-full max-w-md">
                <h3 class="text-lg font-semibold mb-4">
                    {{ editingUser ? 'Editar Usuario' : 'Crear Nuevo Usuario' }}
                </h3>
                <form @submit.prevent="editingUser ? updateUser() : createUser()">
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                            <input 
                                :value="editingUser ? editingUser.email : newUser.email"
                                @input="editingUser ? (editingUser.email = $event.target.value) : (newUser.email = $event.target.value)"
                                type="email" 
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre Completo</label>
                            <input 
                                :value="editingUser ? editingUser.full_name : newUser.full_name"
                                @input="editingUser ? (editingUser.full_name = $event.target.value) : (newUser.full_name = $event.target.value)"
                                type="text" 
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Rol</label>
                            <select 
                                :value="editingUser ? editingUser.role : newUser.role"
                                @change="editingUser ? (editingUser.role = $event.target.value) : (newUser.role = $event.target.value)"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="user">Usuario</option>
                                <option value="admin">Administrador</option>
                                <option value="accountant">Contador</option>
                            </select>
                        </div>
                        <div v-if="!editingUser">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña Temporal</label>
                            <input 
                                v-model="newUser.temporary_password"
                                type="password" 
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            >
                        </div>
                    </div>
                    <div class="flex gap-3 mt-6">
                        <button type="submit" class="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700">
                            {{ editingUser ? 'Actualizar' : 'Crear' }}
                        </button>
                        <button type="button" @click="showUserModal = false" class="flex-1 bg-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-400">
                            Cancelar
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Modal para Cambiar Contraseña -->
        <div v-if="showPasswordModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 w-full max-w-md">
                <h3 class="text-lg font-semibold mb-4">
                    Cambiar Contraseña para {{ selectedUser?.name }}
                </h3>
                <form @submit.prevent="changePassword">
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Nueva Contraseña</label>
                            <input 
                                v-model="passwordData.new_password"
                                type="password" 
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            >
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Confirmar Contraseña</label>
                            <input 
                                v-model="passwordData.confirm_password"
                                type="password" 
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                required
                            >
                        </div>
                    </div>
                    <div class="flex gap-3 mt-6">
                        <button type="submit" class="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700">
                            Actualizar
                        </button>
                        <button type="button" @click="showPasswordModal = false" class="flex-1 bg-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-400">
                            Cancelar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const activeTab = ref('usuarios');
const loading = ref(false);
const showUserModal = ref(false);
const showPasswordModal = ref(false);
const selectedUser = ref(null);
const editingUser = ref(null);

const tabs = ref([
    { id: 'usuarios', name: 'Usuarios y Roles' },
    { id: 'cuentas', name: 'Cuentas Bancarias' },
    { id: 'integraciones', name: 'Integraciones' },
    { id: 'sistema', name: 'Sistema' }
]);

const users = ref([]);

const newUser = ref({
    email: '',
    full_name: '',
    role: 'user',
    temporary_password: ''
});

const passwordData = ref({
    new_password: '',
    confirm_password: ''
});

const roles = ref([
    {
        name: 'Administrador',
        description: 'Control total del sistema',
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
        permissions: [
            'Ver conciliaciones',
            'Crear asientos ajuste',
            'Aprobar/rechazar matches',
            'Sin acceso a configuración'
        ]
    },
    {
        name: 'Usuario',
        description: 'Acceso básico al sistema',
        permissions: [
            'Ver transacciones propias',
            'Consultar reportes básicos',
            'Sin permisos de edición'
        ]
    }
]);

// Función para mapear roles de la BD al frontend
const mapRole = (role) => {
    const roleMap = {
        'user': 'Usuario',
        'admin': 'Administrador',
        'accountant': 'Contador'
    };
    return roleMap[role] || role;
};

// Función inversa para enviar al backend
const mapRoleToBackend = (role) => {
    const roleMap = {
        'Usuario': 'user',
        'Administrador': 'admin',
        'Contador': 'accountant'
    };
    return roleMap[role] || role;
};

const loadUsers = async () => {
    loading.value = true;
    try {
        const response = await fetch('http://localhost:5001/api/users');
        
        if (response.ok) {
            const usersData = await response.json();
            
            users.value = usersData.map(user => ({
                id: user.id,
                name: user.full_name || 'Sin nombre',
                email: user.email,
                role: mapRole(user.role),
                active: true,
                lastAccess: user.last_login 
                    ? new Date(user.last_login).toLocaleString('es-ES') 
                    : 'Nunca'
            }));
        } else {
            console.error('Error cargando usuarios:', response.status);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    } finally {
        loading.value = false;
    }
};

const createUser = async () => {
    try {
        const response = await fetch('http://localhost:5001/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: newUser.value.email,
                full_name: newUser.value.full_name,
                password: newUser.value.temporary_password,
                role: newUser.value.role
            })
        });

        if (response.ok) {
            await loadUsers();
            showUserModal.value = false;
            newUser.value = { email: '', full_name: '', role: 'user', temporary_password: '' };
            alert('Usuario creado exitosamente');
        } else {
            const errorData = await response.json();
            alert('Error: ' + (errorData.detail || 'No se pudo crear el usuario'));
        }
    } catch (error) {
        console.error('Error creando usuario:', error);
        alert('Error de conexión con el servidor');
    }
};

const updateUser = async () => {
    alert('Funcionalidad de edición pendiente - Necesita endpoint en backend');
    showUserModal.value = false;
};

const changePassword = async () => {
    if (passwordData.value.new_password !== passwordData.value.confirm_password) {
        alert('Las contraseñas no coinciden');
        return;
    }

    alert('Funcionalidad de cambio de contraseña pendiente - Necesita endpoint en backend');
    showPasswordModal.value = false;
};

const deleteUser = async (user) => {
    if (!confirm(`¿Estás seguro de eliminar a ${user.name}?`)) {
        return;
    }

    alert('Funcionalidad de eliminación pendiente - Necesita endpoint en backend');
};

const openPasswordModal = (user) => {
    selectedUser.value = user;
    showPasswordModal.value = true;
};

const openEditModal = (user) => {
    editingUser.value = { 
        ...user,
        role: mapRoleToBackend(user.role),
        full_name: user.name
    };
    showUserModal.value = true;
};

const getRoleClass = (role) => {
    const classes = {
        'Administrador': 'bg-purple-100 text-purple-800',
        'Contador': 'bg-blue-100 text-blue-800',
        'Usuario': 'bg-green-100 text-green-800',
        'user': 'bg-green-100 text-green-800',
        'admin': 'bg-purple-100 text-purple-800',
        'accountant': 'bg-blue-100 text-blue-800'
    };
    return classes[role] || 'bg-gray-100 text-gray-800';
};

const getUsersCountByRole = (roleName) => {
    const backendRole = mapRoleToBackend(roleName);
    return users.value.filter(user => user.role === roleName || user.role === backendRole).length;
};

// Cargar datos al montar el componente
onMounted(() => {
    loadUsers();
});
</script>