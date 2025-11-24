<template>
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 px-4 py-12 relative overflow-hidden">
        <!-- Animated background particles -->
        <div class="absolute inset-0 overflow-hidden">
            <div class="absolute w-96 h-96 bg-blue-500/10 rounded-full blur-3xl -top-48 -left-48 animate-pulse"></div>
            <div class="absolute w-96 h-96 bg-purple-500/10 rounded-full blur-3xl -bottom-48 -right-48 animate-pulse delay-1000"></div>
        </div>

        <div class="w-full max-w-md relative z-10">
            <div class="bg-white/10 backdrop-blur-2xl rounded-3xl shadow-2xl p-10 space-y-8 border border-white/30">
                <!-- Logo con efecto hover -->
                <div class="text-center">
                    <div class="flex justify-center mb-8">
                        <div class="relative group cursor-pointer">
                            <!-- Logo -->
                            <div class="relative bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl shadow-lg overflow-hidden transition-transform group-hover:animate-shake">
                                <img src="@/assets/banksycn.png" alt="BankSync Logo" class="w-28 h-28 relative z-10" />
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Título del formulario -->
                <div class="text-center">
                    <h2 class="text-2xl font-bold text-white mb-2">Bienvenido</h2>
                    <p class="text-sm text-gray-300">Ingresa tus credenciales para continuar</p>
                </div>

                <!-- Form -->
                <form @submit.prevent="submit" class="space-y-5">
                    <div class="space-y-2">
                        <label for="emailField" class="block text-sm font-semibold text-gray-200">
                            Correo electrónico
                        </label>
                        <div class="relative group">
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <svg class="h-5 w-5 text-gray-400 group-focus-within:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                            </div>
                            <input 
                                v-model="form.username" 
                                type="email" 
                                id="emailField"
                                class="w-full pl-12 pr-4 py-3.5 bg-white/10 border-2 border-white/20 rounded-xl focus:bg-white/20 focus:border-blue-400 focus:ring-4 focus:ring-blue-400/20 outline-none transition-all text-white placeholder:text-gray-400"
                                placeholder="admin@empresa.com"
                                required
                            >
                        </div>
                    </div>

                    <div class="space-y-2">
                        <label for="passwordField" class="block text-sm font-semibold text-gray-200">
                            Contraseña
                        </label>
                        <div class="relative group">
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <svg class="h-5 w-5 text-gray-400 group-focus-within:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                </svg>
                            </div>
                            <input 
                                v-model="form.password" 
                                type="password" 
                                id="passwordField"
                                class="w-full pl-12 pr-4 py-3.5 bg-white/10 border-2 border-white/20 rounded-xl focus:bg-white/20 focus:border-blue-400 focus:ring-4 focus:ring-blue-400/20 outline-none transition-all text-white placeholder:text-gray-400"
                                placeholder="••••••••"
                                required
                            >
                        </div>
                    </div>

                    <!-- Recordar sesión y olvidaste contraseña -->
                    <div class="flex items-center justify-between text-sm pt-2">
                        <label class="flex items-center cursor-pointer group">
                            <input type="checkbox" class="w-4 h-4 text-blue-500 bg-white/10 border-white/30 rounded focus:ring-blue-500 cursor-pointer">
                            <span class="ml-2 text-gray-300 group-hover:text-white transition-colors">Recordar sesión</span>
                        </label>
                        <a href="#" class="text-blue-400 hover:text-blue-300 font-semibold hover:underline transition-all">¿Olvidaste tu contraseña?</a>
                    </div>

                    <button 
                        type="submit" 
                        class="w-full bg-white/20 hover:bg-white/30 text-white font-semibold py-4 rounded-xl transition-all duration-300 border-2 border-white/30 hover:border-white/50 backdrop-blur-sm hover:scale-[1.02] active:scale-[0.98]"
                    >
                        Iniciar sesión
                    </button>
                </form>

                <!-- Footer -->
                <div class="text-center pt-6 border-t border-white/20">
                    <p class="text-sm text-gray-300">
                        ¿No tienes cuenta? 
                        <router-link to="/register" class="font-bold text-blue-400 hover:text-purple-400 transition-colors hover:underline ml-1">
                            Regístrate aquí
                        </router-link>
                    </p>
                </div>

                <!-- Copyright -->
                <div class="text-center">
                    <p class="text-xs text-gray-400">© 2025 BankSync. Todos los derechos reservados.</p>
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