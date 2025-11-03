<template>
    <div class="flex h-screen bg-gray-50">
        <!-- Sidebar Component -->
        <Sidebar :currentView="currentView" @change-view="changeView" />

        <!-- Main Content -->
        <main class="flex-1 overflow-y-auto">
            <!-- Dynamic Content -->
            <component :is="currentComponent" />
        </main>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Sidebar from '../components/Sidebar.vue';
import DashboardContent from '../components/DashboardContent.vue';
import ConciliacionesContent from '../components/ConciliacionesContent.vue';
import TransaccionesContent from '../components/TransaccionesContent.vue';
import RegistrosContent from '../components/RegistrosContent.vue';
import ReglasIAContent from '../components/ReglasIAContent.vue';
import ReportesContent from '../components/ReportesContent.vue';
import ConfiguracionContent from '../components/ConfiguracionContent.vue';
import AyudaContent from '../components/AyudaContent.vue';

const currentView = ref('dashboard');

const components = {
    'dashboard': DashboardContent,
    'conciliaciones': ConciliacionesContent,
    'transacciones': TransaccionesContent,
    'registros': RegistrosContent,
    'reglas-ia': ReglasIAContent,
    'reportes': ReportesContent,
    'configuracion': ConfiguracionContent,
    'ayuda': AyudaContent
};

const currentComponent = computed(() => components[currentView.value]);

const changeView = (view) => {
    currentView.value = view;
};
</script>
