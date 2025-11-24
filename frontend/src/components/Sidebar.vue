<template>
    <aside class="w-64 bg-white/60 backdrop-blur-lg border-r border-gray-200/30 flex flex-col shadow-xl">
        <!-- Logo -->
        <div class="p-6 border-b border-gray-200/30">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                    <span class="text-white font-bold text-lg">B</span>
                </div>
                <span class="font-semibold text-gray-900">BankSync</span>
            </div>
            <div class="mt-3 text-sm text-gray-600">
                BankSync SAS.
            </div>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 p-4 space-y-1">
            <a 
                @click.prevent="$emit('change-view', 'dashboard')"
                href="#" 
                :class="currentView === 'dashboard' ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-50'"
                class="flex items-center gap-3 px-4 py-3 rounded-lg font-medium cursor-pointer transition-colors"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Dashboard
            </a>
            
            <a 
                @click.prevent="$emit('change-view', 'conciliaciones')"
                href="#"
                :class="currentView === 'conciliaciones' ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-50'"
                class="flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer transition-colors"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Conciliaciones
            </a>

            <!-- Menú simplificado: solo secciones usadas -->

            <a 
                @click.prevent="$emit('change-view', 'reportes')"
                href="#"
                :class="currentView === 'reportes' ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-50'"
                class="flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer transition-colors"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Reportes
            </a>

            <a 
                @click.prevent="$emit('change-view', 'configuracion')"
                href="#"
                :class="currentView === 'configuracion' ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-50'"
                class="flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer transition-colors"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Configuración
            </a>

            <a 
                @click.prevent="$emit('change-view', 'ayuda')"
                href="#"
                :class="currentView === 'ayuda' ? 'text-blue-600 bg-blue-50' : 'text-gray-700 hover:bg-gray-50'"
                class="flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer transition-colors"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Ayuda
            </a>
        </nav>

        <!-- User Section -->
        <div class="p-4 border-t border-gray-200/30">
            <div class="relative">
                <button 
                    @click="showUserMenu = !showUserMenu"
                    class="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-50 transition-colors"
                >
                    <div class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                        <span class="text-white font-semibold text-sm">{{ userInitials }}</span>
                    </div>
                    <div class="flex-1 text-left">
                        <p class="text-sm font-medium text-gray-900">{{ currentUser.username }}</p>
                        <p class="text-xs text-gray-600">{{ currentUser.email }}</p>
                    </div>
                    <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                </button>

                <!-- User Menu Dropdown -->
                <div 
                    v-if="showUserMenu"
                    class="absolute bottom-full left-0 right-0 mb-2 bg-white rounded-lg shadow-lg border border-gray-200 py-2"
                >
                    <button 
                        @click="handleLogout"
                        class="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2 transition-colors"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        Cerrar sesión
                    </button>
                </div>
            </div>
        </div>
    </aside>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

defineProps({
    currentView: {
        type: String,
        default: 'dashboard'
    }
});

defineEmits(['change-view']);

const showUserMenu = ref(false);
const currentUser = ref({
    username: 'Admin Usuario',
    email: 'admin@empresa.com'
});

// Get user info from localStorage on mount
onMounted(() => {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        try {
            const userData = JSON.parse(savedUser);
            currentUser.value = {
                username: userData.username || userData.email || 'Admin Usuario',
                email: userData.email || userData.username || 'admin@empresa.com'
            };
        } catch (e) {
            console.error('Error parsing user data:', e);
        }
    }
});

// Compute user initials
const userInitials = computed(() => {
    const name = currentUser.value.username;
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
});

const handleLogout = () => {
    // Clear any stored data
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('currentUser');
    
    // Redirect to login
    router.push('/');
};
</script>
