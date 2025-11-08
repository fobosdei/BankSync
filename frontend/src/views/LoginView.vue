<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-12">
        <div class="w-full max-w-md">
            <div class="bg-white rounded-2xl shadow-lg p-8 space-y-6">
                <!-- Logo y Header -->
                <div class="text-center space-y-3">
                    <div class="flex justify-center mb-4">
                        <div class="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                            </svg>
                        </div>
                    </div>
                    <h1 class="text-2xl font-bold text-gray-900">BankSync</h1>
                    <p class="text-sm text-gray-600">Conciliación bancaria con IA</p>
                </div>

                <!-- Título del formulario -->
                <div class="pt-4">
                    <h2 class="text-lg font-semibold text-gray-900 mb-1">Iniciar sesión</h2>
                    <p class="text-sm text-gray-600">Ingresa tus credenciales para acceder al sistema</p>
                </div>

                <!-- Form -->
                <form @submit.prevent="submit" class="space-y-4">
                    <div class="space-y-2">
                        <label for="emailField" class="block text-sm font-medium text-gray-700">
                            Correo electrónico
                        </label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                            </div>
                            <input 
                                v-model="form.username" 
                                type="email" 
                                id="emailField"
                                class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition-all text-gray-900"
                                placeholder="admin@empresa.com"
                                required
                            >
                        </div>
                    </div>

                    <div class="space-y-2">
                        <label for="passwordField" class="block text-sm font-medium text-gray-700">
                            Contraseña
                        </label>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                            </div>
                            <input 
                                v-model="form.password" 
                                type="password" 
                                id="passwordField"
                                class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition-all text-gray-900"
                                placeholder="••••••••"
                                required
                            >
                        </div>
                    </div>

                    <!-- Recordar sesión y olvidaste contraseña -->
                    <div class="flex items-center justify-between text-sm">
                        <label class="flex items-center">
                            <input type="checkbox" class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
                            <span class="ml-2 text-gray-600">Recordar sesión</span>
                        </label>
                        <a href="#" class="text-blue-600 hover:text-blue-700 font-medium">¿Olvidaste tu contraseña?</a>
                    </div>

                    <button 
                        type="submit" 
                        class="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200 shadow-sm"
                    >
                        Iniciar sesión
                    </button>
                </form>

                <!-- Divider -->
                <div class="relative">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-gray-200"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="px-4 bg-white text-gray-500">O continuar con</span>
                    </div>
                </div>

                <!-- Social Login -->
                <div class="grid grid-cols-2 gap-3">
                    <button class="flex items-center justify-center gap-2 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                        <svg class="w-5 h-5" viewBox="0 0 24 24">
                            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                        </svg>
                        <span class="text-sm font-medium text-gray-700">Google</span>
                    </button>
                    <button class="flex items-center justify-center gap-2 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                        <svg class="w-5 h-5" viewBox="0 0 24 24">
                            <path fill="#00A4EF" d="M0 0h11.377v11.372H0z"/>
                            <path fill="#FFB900" d="M12.623 0H24v11.372H12.623z"/>
                            <path fill="#05A6F0" d="M0 12.628h11.377V24H0z"/>
                            <path fill="#FFBB00" d="M12.623 12.628H24V24H12.623z"/>
                        </svg>
                        <span class="text-sm font-medium text-gray-700">Microsoft</span>
                    </button>
                </div>

                <!-- Footer -->
                <div class="text-center pt-4">
                    <p class="text-sm text-gray-600">
                        ¿No tienes cuenta? 
                        <router-link to="/register" class="font-semibold text-blue-600 hover:text-blue-700 transition-colors">
                            Regístrate
                        </router-link>
                    </p>
                </div>

                <!-- Copyright -->
                <div class="text-center pt-4 border-t border-gray-100">
                    <p class="text-xs text-gray-500">© 2025 BankSync. Todos los derechos reservados.</p>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../store/auth';

const form = ref({
    username: '',
    password: ''
});

const auth = useAuthStore();

const submit = async () => {
    // Save user info to localStorage before login
    localStorage.setItem('currentUser', JSON.stringify({
        username: form.value.username,
        email: form.value.username
    }));
    
    await auth.login(form.value);
}

</script>