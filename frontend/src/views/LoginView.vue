<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex">
        <!-- Panel Izquierdo - Branding (oculto en móvil) -->
        <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-purple-900 via-purple-800 to-purple-900 p-12 flex-col justify-between relative overflow-hidden">
            <!-- Patrón de fondo -->
            <div class="absolute inset-0 opacity-10">
                <div class="absolute top-0 left-0 w-96 h-96 bg-purple-300 rounded-full blur-3xl"></div>
                <div class="absolute bottom-0 right-0 w-96 h-96 bg-blue-300 rounded-full blur-3xl"></div>
            </div>
            
            <div class="relative z-10">
                <!-- Logo -->
                <div class="flex items-center gap-3 mb-16">
                    <div class="w-16 h-16 bg-white rounded-2xl flex items-center justify-center shadow-lg overflow-hidden">
                        <img src="@/assets/banksycn.png" alt="BankSync" class="w-14 h-14 object-contain" />
                    </div>
                    <div>
                        <h1 class="text-2xl font-bold text-white">BankSync</h1>
                        <p class="text-xs text-purple-200">Professional Edition</p>
                    </div>
                </div>

                <!-- Mensaje principal -->
                <div class="space-y-6">
                    <h2 class="text-4xl font-bold text-white leading-tight">
                        Conciliación Bancaria
                        <br />
                        <span class="text-purple-300">Inteligente y Segura</span>
                    </h2>
                    <p class="text-lg text-purple-100 leading-relaxed max-w-md">
                        Automatiza tu proceso de conciliación con inteligencia artificial. 
                        Ahorra tiempo y elimina errores en tus operaciones financieras.
                    </p>
                </div>
            </div>

            <!-- Features -->
            <div class="relative z-10 grid grid-cols-2 gap-4 text-white">
                <div class="text-center">
                    <div class="text-3xl font-bold">-80%</div>
                    <div class="text-xs text-purple-200 mt-1">Tiempo</div>
                </div>
                <div class="text-center">
                    <svg class="w-10 h-10 mx-auto mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                    </svg>
                    <div class="text-xs text-purple-200">Seguro</div>
                </div>
            </div>
        </div>

        <!-- Panel Derecho - Formulario -->
        <div class="flex-1 flex items-center justify-center p-8">
            <div class="w-full max-w-md">
                <!-- Header -->
                <div class="mb-8">
                    <!-- Logo móvil -->
                    <div class="lg:hidden flex items-center gap-3 mb-8">
                        <div class="w-12 h-12 bg-purple-900 rounded-xl flex items-center justify-center overflow-hidden">
                            <img src="@/assets/banksycn.png" alt="BankSync" class="w-10 h-10 object-contain" />
                        </div>
                        <div>
                            <h1 class="text-xl font-bold text-gray-900">BankSync</h1>
                            <p class="text-xs text-gray-500">Professional Edition</p>
                        </div>
                    </div>

                    <h2 class="text-3xl font-bold text-gray-900 mb-2">Iniciar Sesión</h2>
                    <p class="text-gray-600">Accede a tu panel de conciliación</p>
                </div>

                <!-- Formulario -->
                <form @submit.prevent="submit" class="space-y-5">
                    <!-- Email -->
                    <div>
                        <label for="emailField" class="block text-sm font-semibold text-gray-700 mb-2">
                            Correo Electrónico
                        </label>
                        <div class="relative">
                            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            <input
                                v-model="form.username"
                                type="email"
                                id="emailField"
                                class="w-full pl-11 pr-4 py-3 bg-white border-2 border-gray-200 rounded-lg focus:border-purple-600 focus:ring-4 focus:ring-purple-100 outline-none transition-all text-gray-900 placeholder:text-gray-400"
                                placeholder="admin@empresa.com"
                                required
                            />
                        </div>
                    </div>

                    <!-- Password -->
                    <div>
                        <label for="passwordField" class="block text-sm font-semibold text-gray-700 mb-2">
                            Contraseña
                        </label>
                        <div class="relative">
                            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                            </svg>
                            <input
                                v-model="form.password"
                                :type="showPassword ? 'text' : 'password'"
                                id="passwordField"
                                class="w-full pl-11 pr-11 py-3 bg-white border-2 border-gray-200 rounded-lg focus:border-purple-600 focus:ring-4 focus:ring-purple-100 outline-none transition-all text-gray-900 placeholder:text-gray-400"
                                placeholder="••••••••"
                                required
                            />
                            <button
                                type="button"
                                @click="showPassword = !showPassword"
                                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                            >
                                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                </svg>
                                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <!-- Recordar sesión y contraseña -->
                    <div class="flex items-center justify-between text-sm pt-1">
                        <label class="flex items-center cursor-pointer group">
                            <input type="checkbox" class="w-4 h-4 text-purple-600 bg-white border-gray-300 rounded focus:ring-purple-500 cursor-pointer" />
                            <span class="ml-2 text-gray-700 group-hover:text-gray-900 transition-colors">Recordar sesión</span>
                        </label>
                        <a href="#" class="text-purple-600 hover:text-purple-700 font-medium hover:underline transition-colors">
                            ¿Olvidaste tu contraseña?
                        </a>
                    </div>

                    <!-- Botón submit -->
                    <button
                        type="submit"
                        class="w-full bg-purple-900 hover:bg-purple-800 text-white font-semibold py-3.5 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]"
                    >
                        Iniciar Sesión
                    </button>
                </form>

                <!-- Footer -->
                <div class="text-center mt-8 pt-6 border-t border-gray-200">
                    <p class="text-sm text-gray-600">
                        ¿No tienes cuenta? 
                        <router-link to="/register" class="font-semibold text-purple-600 hover:text-purple-700 transition-colors hover:underline ml-1">
                            Regístrate aquí
                        </router-link>
                    </p>
                </div>

                <!-- Copyright -->
                <div class="text-center mt-6">
                    <p class="text-xs text-gray-500">© 2025 BankSync SAS. Todos los derechos reservados.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../store/auth';

const form = ref({
    username: '',
    password: ''
});

const showPassword = ref(false);
const auth = useAuthStore();

const submit = async () => {
    localStorage.setItem('currentUser', JSON.stringify({
        username: form.value.username,
        email: form.value.username
    }));
    
    await auth.login(form.value);
}
</script>
