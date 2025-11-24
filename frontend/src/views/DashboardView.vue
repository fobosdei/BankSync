<template>
    <div class="flex h-screen">
        <!-- Sidebar with dark background -->
        <div class="relative">
            <!-- Animated Background for Sidebar -->
            <div class="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
                <!-- Animated particles -->
                <div class="absolute inset-0">
                    <div v-for="i in 20" :key="i" 
                         class="absolute w-1 h-1 bg-white/20 rounded-full"
                         :style="{
                             left: `${Math.random() * 100}%`,
                             top: `${Math.random() * 100}%`,
                             animation: `float ${5 + Math.random() * 10}s ease-in-out infinite`,
                             animationDelay: `${Math.random() * 5}s`
                         }">
                    </div>
                </div>
            </div>
            
            <!-- Sidebar Component -->
            <Sidebar :currentView="currentView" @change-view="changeView" class="relative z-10" />
        </div>

        <!-- Main Content with light background -->
        <main class="flex-1 overflow-y-auto bg-gray-50">
            <!-- Dynamic Content -->
            <component
                :is="currentComponent"
                @open-conciliation-modal="openConciliationFromDashboard"
            />
        </main>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Sidebar from '../components/Sidebar.vue';
import DashboardContent from '../components/DashboardContent.vue';
import ConciliacionesContent from '../components/ConciliacionesContent.vue';
import ReportesContent from '../components/ReportesContent.vue';
import ConfiguracionContent from '../components/ConfiguracionContent.vue';
import AyudaContent from '../components/AyudaContent.vue';

const currentView = ref('dashboard');

const components = {
    dashboard: DashboardContent,
    conciliaciones: ConciliacionesContent,
    reportes: ReportesContent,
    configuracion: ConfiguracionContent,
    ayuda: AyudaContent,
};

const currentComponent = computed(() => components[currentView.value]);

const changeView = (view) => {
    currentView.value = view;
};

const openConciliationFromDashboard = () => {
    currentView.value = 'conciliaciones';
};
</script>
