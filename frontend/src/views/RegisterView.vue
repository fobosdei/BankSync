<template>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex">
        <!-- Panel Izquierdo - Formulario de Registro -->
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

                    <h2 class="text-3xl font-bold text-gray-900 mb-2">Crear cuenta</h2>
                    <p class="text-gray-600">Completa el formulario para registrarte</p>
                </div>

                <!-- Form -->
                <form @submit.prevent="submit" class="space-y-5">
                    <!-- Email -->
                    <div>
                        <label for="emailField" class="block text-sm font-semibold text-gray-700 mb-2">
                            Correo electrónico
                        </label>
                        <div class="relative">
                            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            <input 
                                v-model="form.email" 
                                type="email" 
                                id="emailField"
                                class="w-full pl-11 pr-4 py-3 bg-white border-2 border-gray-200 rounded-lg focus:border-purple-600 focus:ring-4 focus:ring-purple-100 outline-none transition-all text-gray-900 placeholder:text-gray-400"
                                placeholder="tu@email.com"
                                required
                            />
                        </div>
                    </div>

                    <!-- Nombre completo -->
                    <div>
                        <label for="fullNameField" class="block text-sm font-semibold text-gray-700 mb-2">
                            Nombre completo
                        </label>
                        <div class="relative">
                            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                            <input 
                                v-model="form.full_name" 
                                type="text" 
                                id="fullNameField"
                                class="w-full pl-11 pr-4 py-3 bg-white border-2 border-gray-200 rounded-lg focus:border-purple-600 focus:ring-4 focus:ring-purple-100 outline-none transition-all text-gray-900 placeholder:text-gray-400"
                                placeholder="Tu nombre completo"
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
                                type="password" 
                                id="passwordField"
                                class="w-full pl-11 pr-4 py-3 bg-white border-2 border-gray-200 rounded-lg focus:border-purple-600 focus:ring-4 focus:ring-purple-100 outline-none transition-all text-gray-900 placeholder:text-gray-400"
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    <!-- Términos y condiciones -->
                    <div class="flex items-start pt-2">
                        <input type="checkbox" required class="w-4 h-4 mt-1 text-purple-600 bg-white border-gray-300 rounded focus:ring-purple-500 cursor-pointer" />
                        <label class="ml-3 text-sm text-gray-600">
                            Acepto los <a href="#" class="text-purple-600 hover:text-purple-700 font-semibold hover:underline">términos y condiciones</a> y la <a href="#" class="text-purple-600 hover:text-purple-700 font-semibold hover:underline">política de privacidad</a>
                        </label>
                    </div>

                    <!-- Botón submit -->
                    <button 
                        type="submit" 
                        class="w-full bg-purple-900 hover:bg-purple-800 text-white font-semibold py-3.5 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98]"
                    >
                        Crear cuenta
                    </button>
                </form>

                <!-- Footer -->
                <div class="text-center mt-8 pt-6 border-t border-gray-200">
                    <p class="text-sm text-gray-600">
                        ¿Ya tienes cuenta? 
                        <router-link to="/" class="font-semibold text-purple-600 hover:text-purple-700 transition-colors hover:underline ml-1">
                            Inicia sesión aquí
                        </router-link>
                    </p>
                </div>

                <!-- Copyright -->
                <div class="text-center mt-6">
                    <p class="text-xs text-gray-500"> 2025 BankSync SAS. Todos los derechos reservados.</p>
                </div>
            </div>
        </div>

        <!-- Panel Derecho - Branding -->
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
                        Invita a tu equipo
                        <br />
                        <span class="text-purple-300">y centraliza la conciliación</span>
                    </h2>
                    <p class="text-lg text-purple-100 leading-relaxed max-w-md">
                        Crea usuarios para tu equipo contable y controla accesos por rol. 
                        Optimiza la colaboración en tus procesos de conciliación bancaria.
                    </p>
                </div>
            </div>

            <!-- Features -->
            <div class="relative z-10 grid grid-cols-2 gap-4 text-white">
                <div class="text-center">
                    <div class="text-3xl font-bold">Multiusuario</div>
                    <div class="text-xs text-purple-200 mt-1">Roles y permisos</div>
                </div>
                <div class="text-center">
                    <svg class="w-10 h-10 mx-auto mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5V4H2v16h5m10 0v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6m10 0H7" />
                    </svg>
                    <div class="text-xs text-purple-200">Centralizado</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { registerUser } from '../store/user';

const form = ref({
    email: '',
    password: '',
    full_name: '',
    role: 'user'
});

const submit = async (e) => {
    e.preventDefault();
    console.log('Submitting form:', form.value);
    registerUser(form.value);
}

</script>